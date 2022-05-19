import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint3.sprint3_stack import Sprint3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint3/sprint3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })


# checking if S3 bucket(1) is available
def test_S3_Bucket_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::S3::Bucket",1)
    
    
def test_Lambda_Function_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is('AWS::Lambda::Function', 3)