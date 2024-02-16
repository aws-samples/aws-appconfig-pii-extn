#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import aws_cdk as cdk

from appconfig_pii_extn.appconfig_pii_extn_stack import AppconfigPiiExtnStack

app = cdk.App()
AppconfigPiiExtnStack(app, "AppconfigPiiExtnStack")

app.synth()
