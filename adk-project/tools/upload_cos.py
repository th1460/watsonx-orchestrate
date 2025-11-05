import ibm_boto3
from ibm_botocore.client import Config

BUCKET = "cloud-object-storage-cos-static-web-hosting-hz7"


def upload_cos(page: bytes, creds: dict) -> str:

    cos = ibm_boto3.client("s3",
                           aws_access_key_id=creds.get("S3_ACCESS_KEY_ID_WRITE"),
                           aws_secret_access_key=creds.get("S3_SECRET_ACCESS_KEY_WRITE"),
                           config=Config(signature_version="s3v4"),
                           endpoint_url="https://s3.us-east.cloud-object-storage.appdomain.cloud"
                           )
    cos.put_object(
        Bucket=BUCKET,
        Key="index.html",
        Body=page,
        ContentType="text/html"
    )

    return "https://" + BUCKET + ".s3.us-east.cloud-object-storage.appdomain.cloud/index.html"
