import boto3
import logging
import json

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    #define the connection
    ec2 = boto3.resource('ec2')

    # Get and parse SNS message
    message = event["Records"][0]["Sns"]["Message"]
    parsed_message = json.loads(message) 
    
    # Get instance id from message, this give us unicode value:
    id = parsed_message["Trigger"]["Dimensions"][0]["value"] 
    # Convert it to the list
    list_id = [id]
    
    instance = ec2.Instance(id=str(list_id))
    
    # Create filter for instance tags
    filters  = {u'Value': 'YES', u'Key': 'Can_be_terminated'}
    
    if filters in instance.tags:
        ec2.instances.filter(InstanceIds=list_id).stop()
    else:
        print "tags don't match, stopping aborted"

