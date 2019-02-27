import boto3
import cfnresponse


def handler(event, context):
    print(f"event: {str(event)}")
    print(f"boto3 version = {boto3.__version__}")
    rp = event.get("ResourceProperties", {})
    firehose = rp.get("FirehoseName")
    clientId = rp.get("ClientId")
    dbName = rp.get("DbName")
    tableName = rp.get("TableName")
    roleArn = rp.get("RoleArn")
    preProcessorArn = rp.get("PreProcessorArn")

    client = boto3.client('firehose')

    try:
        response = client.describe_delivery_stream(DeliveryStreamName=firehose)
        versionId = response.get("DeliveryStreamDescription", {}) \
                            .get("VersionId")

        destinationId = response.get("DeliveryStreamDescription", {})\
                                .get("Destinations")[0]\
                                .get("DestinationId")

        prefix = 'agent_interval/clientname=' + clientId + \
                 '/rowdate=!{timestamp:yyyy-MM-dd}/'

        err_prefix = 'errors/agent_interval/!{firehose:error-output-type}/clientname=' + \
                     clientId + '/rowdate=!{timestamp:yyyy-MM-dd}/'

        print(f"firehose: ${firehose}")
        print(f"versionId: ${versionId}")
        print(f"destinationId: ${destinationId}")
        print(f"Setting prefix to: {prefix}")
        print(f"Setting err prefix to: {err_prefix}")
        print(f"Setting role arn to: {roleArn}")
        print(f"Setting preProcessorArn to: {preProcessorArn}")

        response = client.update_destination(
            DeliveryStreamName=firehose,
            CurrentDeliveryStreamVersionId=versionId,
            DestinationId=destinationId,
            ExtendedS3DestinationUpdate={
                'Prefix': prefix,
                'ErrorOutputPrefix': err_prefix,
                'DataFormatConversionConfiguration': {
                    'SchemaConfiguration': {
                        'RoleARN': roleArn,
                        'DatabaseName': dbName,
                        'TableName': tableName
                    },
                    'InputFormatConfiguration': {
                        'Deserializer': {
                            'OpenXJsonSerDe': {}
                        }
                    },
                    'OutputFormatConfiguration': {
                        'Serializer': {
                            'ParquetSerDe': {
                                'EnableDictionaryCompression': True
                            }
                        }
                    }
                },
                'ProcessingConfiguration': {
                    'Enabled': True,
                    'Processors': [{
                            'Type': 'Lambda',
                            'Parameters': [{
                                    'ParameterName': 'LambdaArn',
                                    'ParameterValue': preProcessorArn
                                }]
                            }
                    ]
                }
            }
        )
        print(response)
    except Exception as e:
        print(e)

    if not event.get("debug"):
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
