from constructs import Construct
from aws_cdk import (
    Stage
)
from sprint3.sprint3_stack import Sprint3Stack
# from .cdk_workshop_stack import CdkWorkshopStack

class ibrahimMustafaPipelineStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.stage = Sprint3Stack(self, 'ibrahimMustafaStack')