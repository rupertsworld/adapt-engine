import os, sys, boto3
matches = sys.argv[1:]

AWS_KEY = os.environ["ADAPT_AWS_KEY"]
AWS_BUCKET_NAME = os.environ["ADAPT_AWS_BUCKET_NAME"]
AWS_SECRET_KEY = os.environ["ADAPT_AWS_SECRET_KEY"]
AWS_ENDPOINT = os.environ["ADAPT_AWS_ENDPOINT"]
SAMPLE_PATH = os.environ["ADAPT_SAMPLE_PATH"]

session = boto3.Session()
client = session.client('s3',
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

files = client.list_objects(Bucket=AWS_BUCKET_NAME)['Contents']
for file in files:
    filename = file['Key']

    for match in matches:
        if match in filename:
            print(f"Deleting {filename}")
            client.delete_object(Bucket=AWS_BUCKET_NAME, Key=filename)