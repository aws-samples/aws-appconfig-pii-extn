# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from typing import cast
from aws_cdk import (
    aws_appconfig_alpha as appconfig,
    aws_lambda_python_alpha as aws_python,
    aws_lambda,
    aws_iam as iam,
    Stack,
)
from constructs import Construct


class AppconfigPiiExtnStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function = aws_python.PythonFunction(
            self,
            "pii_check_fn",
            index="index.py",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="lambda_handler",
            entry="lambda",
            bundling=aws_python.BundlingOptions(
                asset_excludes=[".venv", ".mypy_cache", ".ruff_cache"]
            ),
            description="AppConfig Extension to check for PII in configuration data with Amazon Comprehend",
        )
        function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["comprehend:DetectPiiEntities"],
                resources=["*"],
            )
        )
        appconfig_svc_role = iam.Role(
            self,
            "appconfig_role",
            assumed_by=cast(
                iam.IPrincipal, iam.ServicePrincipal("appconfig.amazonaws.com")
            ),
        )
        function.grant_invoke(appconfig_svc_role)

        appconfig.Extension(
            self,
            "pii_exten",
            actions=[
                appconfig.Action(
                    action_points=[appconfig.ActionPoint.PRE_START_DEPLOYMENT],
                    description="Check configuration data for PII",
                    event_destination=appconfig.LambdaDestination(
                        cast(aws_lambda.IFunction, function)
                    ),
                )
            ],
            extension_name="PII-Comprehend",
            description="Checks for PII in configuration data with Amazon Comprehend before deployment",
        )
