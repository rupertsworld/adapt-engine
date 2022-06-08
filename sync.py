import os, boto3

AWS_KEY = os.environ["ADAPT_AWS_KEY"]
AWS_BUCKET_NAME = os.environ["ADAPT_AWS_BUCKET_NAME"]
AWS_SECRET_KEY = os.environ["ADAPT_AWS_SECRET_KEY"]
AWS_ENDPOINT = os.environ["ADAPT_AWS_ENDPOINT"]
SAMPLE_PATH = os.environ["ADAPT_SAMPLE_PATH"]
if "ADAPT_PRESAMPLE_PATH" in os.environ:
    PRESAMPLE_PATH = os.environ["ADAPT_PRESAMPLE_PATH"]
else:
    PRESAMPLE_PATH = None

session = boto3.Session()
client = session.client('s3',
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

if PRESAMPLE_PATH:
    for dirname in os.listdir(f'{PRESAMPLE_PATH}/'):
        for filename in os.listdir(f"{PRESAMPLE_PATH}/{dirname}"):
            if ('.wav' in filename):
                print(f"Compressing {dirname}/{filename}")
                new_filename = f"{filename[:-4]}.aac"
                os.system(f"ffmpeg -i {PRESAMPLE_PATH}/{dirname}/{filename} -c:a aac -b:a 256k {PRESAMPLE_PATH}/{dirname}/{new_filename}")
                os.remove(f"{PRESAMPLE_PATH}/{dirname}/{filename}")
                filename = new_filename

                print(f"Uploading {dirname}/{filename}")
                client.upload_file(f"{PRESAMPLE_PATH}/{dirname}/{filename}", AWS_BUCKET_NAME, f"{dirname}-{filename}")

            print(f"Converting {dirname}/{filename} to wav")
            if not os.path.exists(f'{SAMPLE_PATH}/{dirname}'):
                os.makedirs(f'{SAMPLE_PATH}/{dirname}')
            
            new_filename = f"{filename[:-4]}.wav"
            os.system(f"ffmpeg -i {PRESAMPLE_PATH}/{dirname}/{filename} -ac 2 -ar 44100 -acodec pcm_s16le {SAMPLE_PATH}/{dirname}/{new_filename}")
            os.remove(f"{PRESAMPLE_PATH}/{dirname}/{filename}")

print("Preparing downloads")
files = []
paginator = client.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=AWS_BUCKET_NAME)

for page in pages:
    for obj in page['Contents']:
        files.append(obj['Key'])

for filename in files:
    print(f"Checking sample {filename}...")
    folder = filename.split('-')[0]
    dest_filename = '-'.join(filename.split('-')[1:])

    if os.path.exists(f"{SAMPLE_PATH}/{folder}/{dest_filename[:-4]}.wav"):
        print("Already downloaded.")
        continue

    if not os.path.exists(f'{SAMPLE_PATH}/{folder}'):
        os.makedirs(f'{SAMPLE_PATH}/{folder}')
    
    if not os.path.exists(f'{SAMPLE_PATH}/{folder}/{dest_filename}'):
        print(f"Downloading sample {filename}")
        client.download_file(AWS_BUCKET_NAME, filename, f"{SAMPLE_PATH}/{folder}/{dest_filename}")

    print(f"Decompressing {folder}/{dest_filename}")
    new_filename = f"{dest_filename[:-4]}.wav"
    os.system(f"ffmpeg -i {SAMPLE_PATH}/{folder}/{dest_filename} -ac 2 -ar 44100 -acodec pcm_s16le {SAMPLE_PATH}/{folder}/{new_filename} >> /dev/null")
    os.remove(f"{SAMPLE_PATH}/{folder}/{dest_filename}")