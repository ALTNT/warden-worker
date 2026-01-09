import os
import boto3
from botocore.exceptions import ClientError

def verify_connection():
    # 获取环境变量
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_DEFAULT_REGION')
    s3_endpoint = os.environ.get('S3_ENDPOINT')
    
    print(f"--- Python S3 Verification Script ---")
    print(f"Access Key ID length: {len(aws_access_key_id) if aws_access_key_id else 0}")
    print(f"Secret Key length: {len(aws_secret_access_key) if aws_secret_access_key else 0}")
    print(f"Region: {aws_region}")
    print(f"Endpoint: {s3_endpoint}")

    if not aws_access_key_id:
        print("❌ Error: AWS_ACCESS_KEY_ID is missing")
        return

    if len(aws_access_key_id) < 16:
        print(f"⚠️  WARNING: Access Key ID '{aws_access_key_id}' is unusually short ({len(aws_access_key_id)} chars). Standard AWS keys are 20 chars, R2 is 32 chars.")

    try:
        # 配置 S3 客户端
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
            endpoint_url=s3_endpoint
        )
        
        print("\nAttempting to list buckets (HeadBucket or ListBuckets) to verify credentials...")
        # 尝试列出 buckets，这是最基本的权限检查
        response = s3.list_buckets()
        
        print("✅ Connection successful! Credentials are valid.")
        print("Buckets found:")
        for bucket in response.get('Buckets', []):
            print(f" - {bucket['Name']}")
            
    except ClientError as e:
        print(f"\n❌ AWS ClientError: {e}")
        print(f"Error Code: {e.response.get('Error', {}).get('Code', 'Unknown')}")
        print(f"Error Message: {e.response.get('Error', {}).get('Message', 'Unknown')}")
        
        if e.response.get('Error', {}).get('Code') == 'InvalidAccessKeyId':
            print("\n💡 Diagnosis: The S3 Service rejected the Access Key ID.")
            print("   - Please check if you copied the 'Key ID' correctly.")
            print("   - Ensure you are not using the 'Account ID' or a 'User Name'.")
            
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")

if __name__ == "__main__":
    verify_connection()