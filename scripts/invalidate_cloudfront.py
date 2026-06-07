import boto3
import time
import argparse
from botocore.exceptions import ClientError

def invalidate_cloudfront(distribution_id, paths=["/*"]):
    """
    Creates an invalidation batch for a CloudFront distribution.
    """
    cf_client = boto3.client('cloudfront')
    
    # Caller reference needs to be unique for each invalidation request
    caller_reference = str(time.time())
    
    print(f"[*] Starting CloudFront invalidation for Distribution ID: {distribution_id}")
    print(f"    -> Paths to invalidate: {paths}")
    
    try:
        response = cf_client.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(paths),
                    'Items': paths
                },
                'CallerReference': caller_reference
            }
        )
        
        invalidation_id = response['Invalidation']['Id']
        status = response['Invalidation']['Status']
        
        print(f"[SUCCESS] Invalidation batch created successfully!")
        print(f"[INFO] Invalidation ID: {invalidation_id}")
        print(f"[INFO] Status: {status}")
        
        return invalidation_id
        
    except ClientError as e:
        print(f"[ERROR] Could not create invalidation: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate CloudFront Cache Invalidation")
    parser.add_argument("--distribution-id", required=True, help="The ID of the CloudFront Distribution")
    parser.add_argument("--paths", nargs='+', default=["/*"], help="Paths to invalidate (default: /*)")
    
    args = parser.parse_args()
    invalidate_cloudfront(args.distribution_id, args.paths)
