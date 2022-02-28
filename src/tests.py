from utils import AWSOperations, AWSNotifications

aws = AWSNotifications()

message = "This is a message with some detail: a. This is detail 1  b. This is detail 2"

aws.generate_json_event('load.py', 'Start', message)