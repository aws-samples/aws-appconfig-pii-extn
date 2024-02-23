# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import base64
import json
import logging
import os

import boto3

comprehend = boto3.client("comprehend")

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))


def lambda_handler(event: dict, context):
    logger.debug(json.dumps(event))
    if (event_type := event.get("Type")) != "PreStartDeployment":
        logger.critical("Wrong event type %s for this function, ignoring", event_type)
        return
    if config_content_64 := event.get("Content"):
        config_content = base64.b64decode(config_content_64).decode("utf-8")
        logger.debug(f"decoded content: {config_content}")
        comp_response = comprehend.detect_pii_entities(Text=config_content, LanguageCode="en")
        logger.debug(json.dumps(comp_response))
        if len(comp_response["Entities"]) > 0:
            response = {
                "Error": "BadRequestError",
                "Message": "PII was detected by Amazon Comprehend",
                "Details": comp_response["Entities"]
            }
            logging.info(json.dumps(response))
            return response
    logger.info("Configuration validated")
