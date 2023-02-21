# import AWS libraries
import boto3

# let's use Amazon S3
s3 = boto3.resource("s3")

# print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

# download files
s3.download_file(
    Bucket="kaggle1-datasets",
    Key="train.csv",
    Filename="data/dataset_21-02-23.csv"
)

# upload files
s3.upload_file(
    Bucket="kaggle1-datasets",
    Key="new_file.csv",
    Filename="data/downloaded_from_s3.csv"
)
