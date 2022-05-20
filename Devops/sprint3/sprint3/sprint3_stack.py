from aws_cdk import (
    # Duration,
    aws_lambda as lambda_,# For Using Lambda Service
    Stack,
    RemovalPolicy,# To Remove Lambda S3 SNS Completly
    aws_events as events_,#To Schedule My Lambda Function To Invoke After Each Minute
    Duration,#To get Date And Time
    aws_cloudwatch as cloudwatch_,#To Monitor My Lambda Function
    aws_events_targets as targets_,
    aws_iam,# To Get Access Of Cloud Watch
    aws_s3 as s3,# To make S3 Bucket
    aws_s3_deployment as s3deploy_,# To Deploy S3 Bucket
    aws_sns as sns,# To Enable Simple Notification Service
    aws_sns_subscriptions as subscriptions,# To Enable Email Subscription SNS
    aws_cloudwatch_actions as cw_actions,# To Perform Alarm Action On Cloud Watch
    aws_codedeploy as codedeploy_,
    
    # aws_sqs as sqs,
)
from constructs import Construct 
from resources.constants import * # To Access Global Variables In My Constant File

class Sprint3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        #S3 is a cloud object storage service
        #Bucket is a container for objects store in Amazon S3
        #Creating s3 Bucket
        #Paramter:
        #auto_delete_objects means if it will be false our s3 can't be deleted
        #removal policy to destroy s3 with cdk destroy
        #block public access means no access to anyone else
        
        ibrahimMustafaS3_bucket = s3.Bucket(
            self,
            "ibrahimMustafaS3Bucket",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
            )
            
        # Deploying S3 Bucket    
        
        s3deploy_.BucketDeployment(
            self, 
            "IBRAHIMMUSTAFABUCKET",
            sources=[s3deploy_.Source.asset("./resources")],
            destination_bucket=ibrahimMustafaS3_bucket,  
            retain_on_delete=False     #It means when we will destroy cdk data will not be retained in S3
            )    
        
        #SNS Topic is logical access point that acts a communication channel.
        #apply removal policy to completely delete sns
        #Add Email Subscription to get notified through email
        
        ibrahimMustafatopic = sns.Topic(self, "ibrahimMustafaSNSTOPIC")  
        ibrahimMustafatopic.apply_removal_policy(RemovalPolicy.DESTROY)
        ibrahimMustafatopic.add_subscription(subscriptions.EmailSubscription("owaissultan958@gmail.com"))
        
        
        
        # Calling Lambda Role Function To Access CloudWatch And BasicLambdaExecutionRole
        
        lambda_role=self.create_lambda_role()
        
        
        #Calling Lambda Function and passing arguments by name,resource,handler,role
        
        WhLambda_Function=self.createWHLambda("WhLambda","./resources","WhLambda.lambda_handler",lambda_role)
        
        #Giving access to lambda function to read and write in S3
        
        ibrahimMustafaS3_bucket.grant_read_write(WhLambda_Function)
    
    
        # Destroying Lambda Function
        
        WhLambda_Function.apply_removal_policy(RemovalPolicy.DESTROY)
    
    
        # initializing Events For Lambda To Invoke Lambda After Every Minute
        
        lambdaSchedule=events_.Schedule.rate(Duration.minutes(1))
    
        
        # initializing Targets To Get Destination Of Lambda
        
        lamdaTarget=targets_.LambdaFunction(handler=WhLambda_Function)
    
    
    
        # Defining Rule For lambda Function To Invoke Periodically
        #some changes occured
        
        rule=events_.Rule(self,"ibrahimMustafaWHLambdaRule",
        description="Creating a rule to invoke my lambda function periodically",
        enabled=True,
        schedule=lambdaSchedule,
        targets=[lamdaTarget],
        )
        
        
        # Using Loop To Trigger Alarm For Three Urls !!!
        
        
        # get matrics of lambda function 
        # dimensions={"FunctionName":WhLambda_Function.function_name}
        
        # lambda_Duration_metric=cloudwatch_.Metric(
        #     metric_name="Duration",
        #     namespace="AWS/Lambda",
        #     dimensions_map=dimensions,
        #         )
        
        
        # lambda_Errors_metric=cloudwatch_.Metric(
        #     metric_name="Errors",
        #     namespace="AWS/Lambda",
        #     dimensions_map=dimensions,
        #         )
        
        # creating alarms on lambda duration using WhLambda_Function.metric_duration()
        lambda_Duration_alarm=cloudwatch_.Alarm(self,
                id="Alarm On lambda Duration",
                evaluation_periods=1,
                metric=WhLambda_Function.metric_duration(),#gets lambda duration metric
                threshold=2.5,
                comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                datapoints_to_alarm=1,
                    )
        
        # creating alarms on lambda Errors using WhLambda_Function.metric_errors()
        lambda_Errors_alarm=cloudwatch_.Alarm(self,
                id="Alarm On lambda Errors",
                evaluation_periods=1,
                metric=WhLambda_Function.metric_errors(),# get lambda error metric
                threshold=1.0,
                comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                datapoints_to_alarm=1,
                    )
        
        #creating lambda version alias
        version = WhLambda_Function.current_version
        version1_alias = lambda_.Alias(self, "alias",
            alias_name="prod",
            version=version
        )
        
        
        # creating a deployment group 
        # adding alarms of lambda duration and errors
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/README.html
        deployment_group = codedeploy_.LambdaDeploymentGroup(self, "ibrahimMustafaBlueGreenDeployment",
            alias=version1_alias,
            deployment_config=codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_10_MINUTES,
            alarms = [lambda_Errors_alarm, lambda_Duration_alarm]
        )
        
        
        for i in url_To_Monitor:
            
        # Creating metric for availability alarmm
            
            dimensions={"URL":i}
            availability_metric=cloudwatch_.Metric(
                metric_name=url_Monitor_METRIC_AVAILABILITY,
                color="#ff2233",
                namespace=url_Monitor_NameSpace,
                dimensions_map=dimensions,
                label="Availability Metric",
                period=Duration.minutes(1)
                    )
                 
                 
        # Creating alarm for availability         
            
            availability_alarm=cloudwatch_.Alarm(self,
                id="Alarm On Availability"+i,
                evaluation_periods=1,
                metric=availability_metric,
                threshold=availability_threshold,
                comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                datapoints_to_alarm=1,
                    )
                    
            availability_alarm.add_alarm_action(cw_actions.SnsAction(ibrahimMustafatopic))
            
            
            # Creating metric latency alarmm
            
            latency_metric=cloudwatch_.Metric(
                metric_name=url_Monitor_METRIC_LATENCY,
                color="#ffdd33",
                namespace=url_Monitor_NameSpace,
                dimensions_map=dimensions,
                label="Latency Metric",
                period=Duration.minutes(1)
                     )
                 
                 
                 
        # Creating alarm for latency metrics
            latency_alarm=cloudwatch_.Alarm(self,
                id="Alarm On Latency"+i,
                evaluation_periods=1,
                metric=latency_metric,
                threshold=latency_threshold,
                comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                datapoints_to_alarm=1,
                    )        
            latency_alarm.add_alarm_action(cw_actions.SnsAction(ibrahimMustafatopic))    
            
            
            
        # defining lambda function
    def createWHLambda(self,id,asset,handler,role):
        return lambda_.Function(
        self,
        id= id,
        code=lambda_.Code.from_asset(asset),
        handler=handler,
        runtime=lambda_.Runtime.PYTHON_3_6,
        role=role,
        timeout=Duration.seconds(60) #By Deafult Lambda Function Excution Time Is 3 Seconds And It Can Be Extended upto 900 seconds
        )
        
        # defining lambda role to access cloudwatch 
    def create_lambda_role(self):
        lambdaRole=aws_iam.Role(self,"LambdaRole",
        assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
        managed_policies=[  
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")
            
            ])
            
        return lambdaRole