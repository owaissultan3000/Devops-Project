import boto3 
# Made CloudWatchPutMetric Class To Show Lambda Function In CloudWatch Service By Amazon
class CloudWatchPutMetric:
    def __init__(self):
        self.client=boto3.client('cloudwatch') #Need To Ask
        
        
    # Defined Put Metric Function To Take Parameter From User To Monitor Results In Cloud Watch
    def put_metric_data(self,nameSpace,metricName,dimesnions,value):
        response = self.client.put_metric_data(     #Need To Ask
            Namespace=nameSpace,
            MetricData=[
                {
                    'MetricName': metricName,
                    'Dimensions': dimesnions,
                        'Value': value,
                },
                ]
                )