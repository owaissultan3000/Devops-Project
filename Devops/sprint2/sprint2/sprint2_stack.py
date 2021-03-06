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
    
    # aws_sqs as sqs,
)
from constructs import Construct 
from resources.constants import * # To Access Global Variables In My Constant File

class Sprint2Stack(Stack):

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
            sources=[s3deploy_.Source.asset("./resource")],
            destination_bucket=ibrahimMustafaS3_bucket,  
            retain_on_delete=False     #It means when we will destroy cdk data will not be retained in S3
            )    
        
        #SNS Topic is logical access point that acts a communication channel.
        #apply removal policy to completely delete sns
        #Add Email Subscription to get notified through email
        
        ibrahimMustafaTopic = sns.Topic(self, "ibrahimMustafaSNSTOPIC")  
        ibrahimMustafaTopic.apply_removal_policy(RemovalPolicy.DESTROY)
        ibrahimMustafaTopic.add_subscription(subscriptions.EmailSubscription("ibrahim.mustafa.skipq@gmail.com"))
        
        
        
        # Calling Lambda Role Function To Access CloudWatch And BasicLambdaExecutionRole
        
        lambda_role=self.create_lambda_role()
        
        
        #Calling Lambda Function and passing arguments by name,resource,handler,role
        
        WHLamda_Function=self.createWHLambda("WhLambda","./resources","WHLamda.lambda_handler",lambda_role)
        
        #Giving access to lambda function to read and write in S3
        
        ibrahimMustafaS3_bucket.grant_read_write(WHLamda_Function)
    
    
        # Destroying Lambda Function
        
        WHLamda_Function.apply_removal_policy(RemovalPolicy.DESTROY)
    
    
        # initializing Events For Lambda To Invoke Lambda After Every Minute
        
        lambdaSchedule=events_.Schedule.rate(Duration.minutes(1))
    
        
        # initializing Targets To Get Destination Of Lambda
        
        lamdaTarget=targets_.LambdaFunction(handler=WHLamda_Function)
    
    
    
        # Defining Rule For lambda Function To Invoke Periodically
        
        rule=events_.Rule(self,"ibrahimMustafaWHLambdaRule",
        description="Creating a rule to invoke my lambda function periodically",
        enabled=True,
        schedule=lambdaSchedule,
        targets=[lamdaTarget],
        )
        
        
        # Using Loop To Trigger Alarm For Three Urls !!!
        
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
                    
            availability_alarm.add_alarm_action(cw_actions.SnsAction(ibrahimMustafaTopic))
            
            
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
            latency_alarm.add_alarm_action(cw_actions.SnsAction(ibrahimMustafaTopic))    
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