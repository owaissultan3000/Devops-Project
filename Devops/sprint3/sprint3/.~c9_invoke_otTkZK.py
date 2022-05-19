from constructs import Construct
from aws_cdk import (
    Stack,
    pipelines as pipelines,
    SecretValue as SecretValue,
    aws_codepipeline_actions as aws_codepipeline_actions
    
)
import aws_cdk as cdk
from sprint3_pipeline_stage import ibrahimMustafaPipelineStage

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
        shellsynth=pipelines.ShellStep("Synth",
        input=git_repo,
        commands=["cd ibrahimMustafa/sprint3/", "pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"],
        primary_output_directory  = "ibrahimMustafa/sprint3/cdk.out"
        )

        # Pipeline code will go here
        modern_pipeline = pipelines.CodePipeline(self, "ibrahimMustafa_Pipeline",
            self_mutation=True,
            synth=shellsynth,
        )
        
        beta_stage = 
        
        production_stage = 