# Sample AWS AppConfig Extension: Block PII stored in configuration data

This sample contains an [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html)
[Extension](https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions.html)
which checks your AppConfig configuration profile data for PII (via Amazon
Comprehend). This can help prevent accidental disclosure of private information
to your application, which could be caused by (for example) copy and pasting
the wrong values in to your configuration data.

The Extension runs on the PRE_START_DEPLOYMENT hook, and the
content of the configuration to be deployed is passed to the
`DetectPIIEntities` API. If any entities are reported, the deployment is
blocked. For more information on the entities detected, see the [Amazon Comprehend documentation](https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html).

The Lambda function code for the extension is in `lambda/index.py`; the CDK
stack is here to build and deploy it with the correct IAM permissions, and
create an AppConfig Extension entry.

## Prerequisites

Please see the [AWS AppConfig
documentation](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html)
for details on configuring the service.

Ensure you have up-to-date Python and [AWS CDK v2](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
installed.

You will need Docker or [finch](https://github.com/runfinch/finch) installed
and running for CDK to build the Lambda function.

## Setting up

1. Clone this repo
2. In the cloned repo, create a Python virtual environment: `python -m venv .venv`
3. Activate your virtual environment: `source .venv/bin/activate`
4. Install the Python dependencies: `pip install -r requirements.txt`
5. Ensure you have suitable AWS credentials configured in your environment

## Usage

If you haven't yet bootstrapped the CDK in your environment, you will need to
run `cdk bootstrap`.

1. Deploy this CDK app: `cdk deploy`. You only need to deploy it once per AWS
   Account/Region.
2. Navigate to the AppConfig console, then choose **Extensions**
3. Choose the **PII-Comprehend** extension, then choose **Add to resource**
4. Choose the **Resource Type** to associate the Extension with
5. Choose **Create Association to Resource**

## Un-usage

1. Navigate to the AppConfig console, then choose **Extensions**
2. Choose the **PII-Comprehend** extension
3. For each entry under **Associated resources**, choose the radio button then
   choose **Remove association**, then choose **Delete**
4. Once you have removed all the Associated resources, you can `cdk destroy`
   the app

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
