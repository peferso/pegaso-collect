from utils import AWSOperations, AWSNotifications
import os

aws = AWSNotifications()

message = "This is a message with some detail: a. This is detail 1  b. This is detail 2"
"""
aws.generate_json_event('load.py', 'Start', message)

awsO = AWSOperations()

ec2_info_dict = awsO.retrieve_aws_ec2_info()

nq_s = 123120
nq_f_o = 3131
nq_f_pk = 123

aws.generate_json_event('test.py', 'End', 'The data load has finished. The database final state is ' + str(ec2_info_dict['insSt']) + '.' +
                          'A total of ' + str(nq_s + nq_f_o + nq_f_pk) + ' were executed, ' +
                          str(nq_s) + ' were OK, ' + str(nq_f_pk) + ' failed due to primary key, ' + str(nq_f_o) + ' for other reasons. ' +
                          ' The queries can be tracked by batch date(s): ' +
                          str(os.listdir('../')).replace('[', '').replace(']', '').replace('\'', '').replace('\"', '') )
"""
SCRIPT = 'extract.py'

dw_s_t = os.popen('df -kh . | awk -F " " \'{print $4}\' | tail -1').read()
dw_s_t_pc = os.popen('df -kh . | awk -F " " \'{print $5}\' | tail -1').read()

aws.generate_json_event(SCRIPT, 'Start', 'The size available in the filesystem is ' + str(dw_s_t).replace('\n', '') +
                        ', ' + str(dw_s_t_pc).replace('\n', '') + ' used.')