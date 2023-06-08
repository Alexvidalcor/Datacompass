# AWS libraries
from aws_cdk import (
    App,
    Environment,
    Tags
)


# Custom importation
from modules.cdk_support import *


# Stacks importation
from cdk_s3.cdk_s3_stack import S3stack
from cdk_secretmanager.cdk_secretmanager_stack import SecretManagerStack
from cdk_stepfunctions.cdk_stepfunctions_stack import StepFunctionsLayer


# Set AWS environment
awsEnv = Environment(account=awsAccount, region=awsRegion)


# Execute stacks
app = App()
S3Layer = S3stack(app, f"{appName}-{envDeploy}--s3-stack-{timestamp}", env=awsEnv)
SecretManagerLayer = SecretManagerStack(app, f"{appName}-{envDeploy}--secretmanager-stack-{timestamp}", env=awsEnv)
StepFunctionsLayer = StepFunctionsStack(app, f"{appName}-{envDeploy}--stepfunctions-stack-{timestamp}", env=awsEnv)


# Add tags
Tags.of(S3Layer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(S3Layer).add("Name", awsTagName + "-" + envDeploy + "-s3")

Tags.of(SecretManagerLayer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(SecretManagerLayer).add("Name", awsTagName + "-" + envDeploy + "-secretmanager")

Tags.of(StepFunctionsLayer).add("Group", awsTagName + "-" + envDeploy)
Tags.of(StepFunctionsLayer).add("Name", awsTagName + "-" + envDeploy + "-stepfunctions")


# Execute deploy
app.synth()