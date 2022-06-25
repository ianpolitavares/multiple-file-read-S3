from asyncio import events
import json
import boto3

s3_client = boto3.client('s3')
s3 = boto3.resource('s3')


def lambda_handler(event, context):
    
    # declaração das variaveis
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    object_name = event["Records"][0]["s3"]["object"]["key"]
    my_file_to_upload = "/tmp/my_file_to_upload.json"

    bucket_s3 = s3.Bucket(bucket)
    my_data = []


    for object_summary in bucket_s3.objects.filter(Prefix=object_name):
        file_content = object_summary.get()['Body'].read().decode('utf-8')
        if file_content != '':
            json_content = json.loads(file_content)
            my_data.append(json_content)
        
        else:
            json_content = ''
        print(json_content)
        # print(object_summary.key)

    with open(my_file_to_upload, 'a') as f:
        json.dump(my_data, f)

    try:
        object_path = "destino/object_name_concat.json"
        s3_client.upload_file(my_file_to_upload, bucket, object_path)
        
    except Exception as e:
        raise e
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello Lambda!')
    }
