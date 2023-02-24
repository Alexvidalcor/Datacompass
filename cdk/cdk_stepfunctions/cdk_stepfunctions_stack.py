
# AWS libraries
from aws_cdk import (
    aws_stepfunctions as stepfunctions,
    aws_stepfunctions_tasks as stepfunctionsTasks,
    aws_lambda as awsLambda,
    App, Duration, Stack
)


class StepFunctionStack(Stack):
    def __init__(self, app: App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)


        # Lambda Handlers Definitions

        submitAwsLambda = awsLambda.Function(self, 'submitAwsLambda',
                                             handler='awsLambda_function.awsLambda_handler',
                                             runtime=awsLambda.Runtime.PYTHON_3_6,
                                             code=awsLambda.Code.from_asset('cdk_lambda/lambda1'))

        statusAwsLambda = awsLambda.Function(self, 'statusawsLambda',
                                             handler='awsLambda_function.awsLambda_handler',
                                             runtime=awsLambda.Runtime.PYTHON_3_6,
                                             code=awsLambda.Code.from_asset('cdk_lambda/lambda2'))


        # Step functions Definition

        submitJob = stepfunctionsTasks.LambdaInvoke(
            self, "Submit Job",
            lambda_function=submitAwsLambda,
            output_path="$.Payload",
        )

        waitJob = stepfunctions.Wait(
            self, "Wait 30 Seconds",
            time= stepfunctions.WaitTime.duration(
                Duration.seconds(30))
        )

        statusJob = stepfunctionsTasks.LambdaInvoke(
            self, "Get Status",
            lambda_function=statusAwsLambda,
            output_path="$.Payload",
        )

        failJob = stepfunctions.Fail(
            self, "Fail",
            cause='AWS Batch Job Failed',
            error='DescribeJob returned FAILED'
        )

        succeedJob = stepfunctions.Succeed(
            self, "Succeeded",
            comment='AWS Batch Job succeeded'
        )


        # Create Chain
        definition = submitJob.next(waitJob)\
            .next(statusJob)\
            .next(stepfunctions.Choice(self, 'Job Complete?')
                  .when(stepfunctions.Condition.string_equals('$.status', 'FAILED'), failJob)
                  .when(stepfunctions.Condition.string_equals('$.status', 'SUCCEEDED'), succeedJob)
                  .otherwise(waitJob))


        # Create state machine
        sm = stepfunctions.StateMachine(
            self, "StateMachine",
            definition=definition,
            timeout=Duration.minutes(5)
        )