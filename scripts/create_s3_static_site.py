import os
import mimetypes
import boto3
from botocore.exceptions import ClientError
import json
import argparse

def create_static_site(bucket_name, region, website_folder):
    """
    Automates the creation and deployment of an S3 static website.
    """
    s3_client = boto3.client('s3', region_name=region)
    s3_resource = boto3.resource('s3', region_name=region)

    print(f"[*] Starting deployment for bucket: {bucket_name}")

    # 1. Create Bucket
    try:
        print("[1/5] Creating bucket...")
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print("    -> Bucket created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print("    -> Bucket already exists and is owned by you.")
        else:
            print(f"    -> Error creating bucket: {e}")
            return False

    # 2. Disable Block Public Access
    try:
        print("[2/5] Disabling 'Block Public Access'...")
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        print("    -> Public access blocks removed.")
    except ClientError as e:
        print(f"    -> Error removing public access blocks: {e}")
        return False

    # 3. Add Bucket Policy for Public Read
    try:
        print("[3/5] Applying public read bucket policy...")
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        print("    -> Bucket policy applied.")
    except ClientError as e:
        print(f"    -> Error applying bucket policy: {e}")
        return False

    # 4. Enable Static Website Hosting
    try:
        print("[4/5] Enabling static website hosting...")
        website_configuration = {
            'ErrorDocument': {'Key': 'index.html'},
            'IndexDocument': {'Suffix': 'index.html'},
        }
        s3_client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration=website_configuration
        )
        print("    -> Website hosting enabled.")
    except ClientError as e:
        print(f"    -> Error enabling website hosting: {e}")
        return False

    # 5. Upload Files
    try:
        print(f"[5/5] Uploading files from '{website_folder}'...")
        if not os.path.exists(website_folder):
            print(f"    -> Error: Folder '{website_folder}' does not exist.")
            return False

        for root, dirs, files in os.walk(website_folder):
            for file in files:
                local_path = os.path.join(root, file)
                # Ensure correct forward slash routing for S3 object keys
                s3_key = os.path.relpath(local_path, website_folder).replace('\\', '/')
                
                # Guess the content type (MIME type)
                content_type, _ = mimetypes.guess_type(local_path)
                if content_type is None:
                    content_type = 'binary/octet-stream'

                print(f"      - Uploading {s3_key} ({content_type})...")
                s3_client.upload_file(
                    local_path, 
                    bucket_name, 
                    s3_key,
                    ExtraArgs={'ContentType': content_type}
                )
        print("    -> All files uploaded successfully.")
    except ClientError as e:
        print(f"    -> Error uploading files: {e}")
        return False

    # Success
    endpoint = f"http://{bucket_name}.s3-website.{region}.amazonaws.com"
    print("\n[SUCCESS] Deployment Complete!")
    print(f"[INFO] Website Endpoint: {endpoint}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate S3 Static Website Creation")
    parser.add_argument("--bucket", required=True, help="Globally unique S3 bucket name")
    parser.add_argument("--region", default="ap-south-1", help="AWS region (e.g. us-east-1)")
    parser.add_argument("--folder", default="website", help="Local folder containing website files")
    
    args = parser.parse_args()
    create_static_site(args.bucket, args.region, args.folder)
