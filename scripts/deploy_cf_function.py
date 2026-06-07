import boto3
from botocore.exceptions import ClientError

def deploy_cf_function(distribution_id):
    client = boto3.client('cloudfront')
    function_name = 'SecurityHeaders'
    
    # Read function code
    with open('scripts/security_headers.js', 'r') as f:
        function_code = f.read()
        
    try:
        print(f"[*] Creating CloudFront Function: {function_name}...")
        response = client.create_function(
            Name=function_name,
            FunctionConfig={'Comment': 'Inject HTTP Security Headers', 'Runtime': 'cloudfront-js-1.0'},
            FunctionCode=function_code.encode('utf-8')
        )
        etag = response['ETag']
        print("[SUCCESS] Function created.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'FunctionAlreadyExists':
            print("[*] Function already exists. Updating...")
            desc = client.describe_function(Name=function_name)
            etag = desc['ETag']
            response = client.update_function(
                Name=function_name,
                IfMatch=etag,
                FunctionConfig={'Comment': 'Inject HTTP Security Headers', 'Runtime': 'cloudfront-js-1.0'},
                FunctionCode=function_code.encode('utf-8')
            )
            etag = response['ETag']
        else:
            print(f"[ERROR] {e}")
            return
            
    # Publish function
    print("[*] Publishing function to LIVE stage...")
    publish_response = client.publish_function(Name=function_name, IfMatch=etag)
    function_arn = publish_response['FunctionSummary']['FunctionMetadata']['FunctionARN']
    
    # Get distribution config
    print(f"[*] Fetching config for distribution {distribution_id}...")
    dist_config_response = client.get_distribution_config(Id=distribution_id)
    dist_config = dist_config_response['DistributionConfig']
    dist_etag = dist_config_response['ETag']
    
    # Update DefaultCacheBehavior
    associations = dist_config['DefaultCacheBehavior'].get('FunctionAssociations', {'Quantity': 0, 'Items': []})
    
    already_associated = False
    for item in associations.get('Items', []):
        if item['EventType'] == 'viewer-response' and item['FunctionARN'] == function_arn:
            already_associated = True
            
    if not already_associated:
        items = [item for item in associations.get('Items', []) if item['EventType'] != 'viewer-response']
        items.append({
            'EventType': 'viewer-response',
            'FunctionARN': function_arn
        })
        associations['Items'] = items
        associations['Quantity'] = len(items)
        dist_config['DefaultCacheBehavior']['FunctionAssociations'] = associations
        
        print("[*] Attaching function to CloudFront Distribution...")
        try:
            client.update_distribution(
                DistributionConfig=dist_config,
                Id=distribution_id,
                IfMatch=dist_etag
            )
            print("[SUCCESS] Distribution updated! Security Headers will be injected globally in ~3 minutes.")
        except ClientError as e:
            print(f"[ERROR] Failed to update distribution: {e}")
    else:
        print("[SUCCESS] Function is already attached to the distribution.")

if __name__ == '__main__':
    # Using the CloudFront Distribution ID from our architecture
    deploy_cf_function('E7V0VCJZAXIHT')
