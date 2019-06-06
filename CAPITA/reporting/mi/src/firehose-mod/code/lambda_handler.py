import boto3
import cfnresponse


def handler(event, context):
    print(f"event: {str(event)}")
    print(f"boto3 version = {boto3.__version__}")
    print(f"boto3 region = {boto3.session.Session().region_name}")

    '''Pass in parameters in ResourceProperties under Custom Resource'''
    rp = event.get("ResourceProperties", {})
    firehose = rp.get("FirehoseName")

    # Prefix and error prefix
    prefix = rp.get("Prefix")
    err_prefix = rp.get("ErrorPrefix")

    # Data transformation
    transformation_db = rp.get("TransformationDb")
    transformation_table = rp.get("TransformationTable")
    transformation_role = rp.get("TransformationRole")

    # Preprocessor configuration
    preProcessorArn = rp.get("PreProcessorArn")

    client = boto3.client('firehose')
    account_id = boto3.client('sts').get_caller_identity().get('Account')

    try:
        # Look up existing firehose resource
        response = client.describe_delivery_stream(DeliveryStreamName=firehose)
        versionId = response.get("DeliveryStreamDescription", {}) \
                            .get("VersionId")

        destinationId = response.get("DeliveryStreamDescription", {})\
                                .get("Destinations")[0]\
                                .get("DestinationId")

        update = {}

        print(f"Firehose: {firehose}")
        print(f"VersionId: {versionId}")
        print(f"DestinationId: {destinationId}")

        if prefix:
            print(f"Setting prefix to: {prefix}")
            update['Prefix'] = prefix

        if err_prefix:
            print(f"Setting error prefix to: {err_prefix}")
            update['ErrorOutputPrefix'] = err_prefix

        if transformation_db and transformation_table and transformation_role:
            print(f"Adding Transformation to firehose")
            print(f"Setting transformation glue db to: {transformation_db}")
            print(f"Setting transformation glue table to: "
                  f"{transformation_table}")
            print(f"Setting transformation role arn to: {transformation_role}")

            transformation_role = f"arn:aws:iam::{account_id}:role/{transformation_role}"
            update['DataFormatConversionConfiguration'] = {
                'SchemaConfiguration': {
                    'RoleARN': transformation_role,
                    'DatabaseName': transformation_db,
                    'TableName': transformation_table,
                    'Region': boto3.session.Session().region_name
                },
                'InputFormatConfiguration': {
                    'Deserializer': {
                        'OpenXJsonSerDe': {}
                    }
                },
                'OutputFormatConfiguration': {
                    'Serializer': {
                        'ParquetSerDe': {
                            'Compression': 'SNAPPY',
                            'EnableDictionaryCompression': True
                        }
                    }
                }
            }

        if preProcessorArn:
            print(f"Adding preprocessor: {preProcessorArn}")
            update['ProcessingConfiguration'] = {
                'Enabled': True,
                'Processors': [{
                        'Type': 'Lambda',
                        'Parameters': [{
                                'ParameterName': 'LambdaArn',
                                'ParameterValue': preProcessorArn
                            }]
                        }]
            }

        if update:
            response = client.update_destination(
                DeliveryStreamName=firehose,
                CurrentDeliveryStreamVersionId=versionId,
                DestinationId=destinationId,
                ExtendedS3DestinationUpdate=update
            )
            print(response)
    except Exception as e:
        print(e)

    if not event.get("debug"):
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
