import boto3
from botocore.exceptions import ClientError

def create_billing_alarm(threshold_usd=1.0):
    """
    Creates a CloudWatch Billing Alarm in us-east-1.
    Note: Billing metrics are only available in the us-east-1 region.
    """
    try:
        # Billing alarms MUST be in us-east-1
        cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        
        print(f"[*] Creating CloudWatch Billing Alarm for ${threshold_usd}...")
        
        cloudwatch.put_metric_alarm(
            AlarmName=f'AWS-Billing-Alarm-{threshold_usd}USD',
            AlarmDescription=f'Alarm when AWS charges exceed ${threshold_usd}',
            ActionsEnabled=False, # Set to True if you attach an SNS topic later
            MetricName='EstimatedCharges',
            Namespace='AWS/Billing',
            Statistic='Maximum',
            Dimensions=[
                {
                    'Name': 'Currency',
                    'Value': 'USD'
                },
            ],
            Period=21600, # 6 hours
            EvaluationPeriods=1,
            Threshold=threshold_usd,
            ComparisonOperator='GreaterThanThreshold',
            TreatMissingData='missing'
        )
        
        print("[SUCCESS] Billing Alarm created successfully in us-east-1!")
        print("[INFO] You can view it in the AWS Console under CloudWatch -> Alarms.")
        
    except ClientError as e:
        print(f"[ERROR] Could not create Billing Alarm. Ensure you have enabled Billing Alerts in the AWS Billing Console.")
        print(e)

if __name__ == "__main__":
    create_billing_alarm(1.0)
