import boto3

def lambda_handler(event, context):
    # Retrieve form data from the event
    first_name = event['queryStringParameters']['company_name']
    last_name = event['queryStringParameters']['continent']
    email = event['queryStringParameters']['company_mail']
    region = event['queryStringParameters']['region']
    
    if region == 'Europe Central':
        region = 'eu-central-1'
    elif region == 'Europe East':
        region = 'eu-east-1'
    else:
        region = 'eu-west-1'

    # Specify the SSM document name for the command execution
    document_name = "AWS-RunShellScript"

    # Construct the command with the received form data
    command = f"/home/ec2-user/automate.sh -firstName {first_name} -lastName {last_name} -email {email} -region {region}"

    # Specify the target instance ID
    instance_id = "i-08b1239d4e13aa090"

    # Create an SSM client
    ssm_client = boto3.client('ssm')

    # Send command to SSM
    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName=document_name,
        Parameters={'commands': [command]}
    )

    # Print the command execution details
    print(response)

    return {
        'statusCode': 200,
        'body': 'Command sent to SSM successfully.'
    }
