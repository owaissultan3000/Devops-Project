from constructs import Construct
from aws_cdk import (
    Stack,
    pipelines as pipelines,
    SecretValue as SecretValue,
    aws_codepipeline_actions as aws_codepipeline_actions
    
)
import aws_cdk as cdk
from sprint3.sprint3_pipeline_stage import ibrahimMustafaPipelineStage

class WorkshopPipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        # our repo from where the aws pipeline will get the stored code
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipelineSource.html
        git_repo = pipelines.CodePipelineSource.git_hub("ibrahimmustafa2022skipq/Orion_Python", "main",
        authentication = SecretValue.secrets_manager("pipeline_github-token_ibrahim"),
        trigger = aws_codepipeline_actions.GitHubTrigger("POLL")
        )
        
        # what we are going to do with the code shellstep is the functions/commands that are going to run in the environmet
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ShellStep.html
        #commands=["cd ibrahimMustafa/sprint3/", "pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"],
        shellsynth=pipelines.ShellStep("Synth",
        input=git_repo,
        commands=["cd ibrahimMustafa/sprint3/", "pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"],
        primary_output_directory  = "ibrahimMustafa/sprint3/cdk.out"
            )
         
        # tests to perform on beta stage in pre condition   
        shellPreTest=pipelines.ShellStep("preTest",
        input=git_repo,
        commands=["cd ibrahimMustafa/sprint3/", "pip install -r requirements.txt", "pip install pytest", "pytest"],
        
            )

        # Pipeline code will go here
        ibrahimMustafa_Pipeline = pipelines.CodePipeline(self, "ibrahimMustafa_Pipeline",
            self_mutation=True,
            synth=shellsynth,
            )
        
        
        # creating stages in aws pipeline
        # beta testing stage 
        beta_stage = ibrahimMustafaPipelineStage(self ,"beta")
        
        # creating stages in aws pipeline
        # production stage 
        production_stage = ibrahimMustafaPipelineStage(self ,"production")
        
        # adding beta testing stage to pipeline 
        # pre condition of shellPreTest
        ibrahimMustafa_Pipeline.add_stage(beta_stage, pre=[shellPreTest] )
        
        # adding production stage to pipeline 
        # post condition of manual approval step
        ibrahimMustafa_Pipeline.add_stage(production_stage,  post=[pipelines.ManualApprovalStep("PromoteToProd")] )