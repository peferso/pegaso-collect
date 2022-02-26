import logging
import time
import os
import json

class AWSOperations():

    def __init__(self):
        logging.basicConfig(
            format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
            level=logging.INFO)

    def get_database_public_ip(self):
        time_start = time.time()
        logging.info('Start')
        instance_info = self.retrieve_aws_ec2_info()
        if instance_info['insSt'] != 'running':
            logging.info('The database instance was not found running: ' + instance_info['insSt'])
            ACTION = 'UNKNOWN'
            while ACTION != 'START':
                ACTION = input("# ------------------------------------------------------------------------- #" +
                               "\n#\tThe database was found in state: \"" + instance_info['insSt'] + "\"" +
                               "\n#\tIf you want to start it, enter START." +
                               "\n#\tIf the database instance does not exists deploy it, and then enter START." +
                               "\n#\tEnter EXIT to exit this program." +
                               "\n# ------------------------------------------------------------------------- #\n")
                if ACTION == 'EXIT':
                    exit()
                elif ACTION == 'START':
                    self.start_database_ec2_if_stopped()
                    instance_info = self.retrieve_aws_ec2_info()
        logging.info('Found ip: ' + instance_info['pubIp'])
        time_end = time.time()
        logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')
        return instance_info['pubIp']

    def retrieve_aws_ec2_info(self):
        time_start = time.time()
        logging.info('Start')
        found = False
        tag_key = 'Name'
        tag_value = 'dev-0-database_ec2'
        while not found:
            output = os.popen(
            'aws ec2 --region eu-west-3 \
                     --profile ec2Manager \
            describe-instances \
                     --query "Reservations[].Instances[].{insId: InstanceId, pubIp: PublicIpAddress, insSt: State.Name, name: Tags[?Key == \'' + tag_key + '\'].Value | [0]} | []"')
            ec2_info = output.read()
            ec2_info = ec2_info.replace('\n', '').replace(' ', '').replace('[', '').replace(']', '').replace('},{', '}},{{').split('},{')
            logging.info('Found ' + str(len(ec2_info)) + ' instances')
            ii = 1
            for d in ec2_info:
                ec2_info_dict = json.loads(d)
                logging.info('Discovered instance ' + str(ii) + ':' + str(ec2_info_dict))
                if ec2_info_dict[tag_key.lower()] == tag_value:
                    #logging.info('The database instance was found: \n' + json.dumps(ec2_info_dict, indent=2))
                    logging.info('The database instance was found: ' + ec2_info_dict['insId'])
                    found = True
                    break
                else:
                    found = False
                ii += 1
            if not found:
                logging.error('The database instance was not found! \nEnsure that it is tagged somewhere as \'name=dev-0-database_ec2\'')
                ACTION = 'UNKNOWN'
                while ACTION != 'START' or ACTION != 'EXIT':
                    ACTION = input("# ------------------------------------------------------------------------- #\n" +
                                   "#\tThe database was not found " +
                                   "\n#\tIts name is not tagged properly or it is destroyed)." +
                                   "\n#\tThis program looks for an EC2 instance with tag:" +
                                   "\n#\t\t\"" + tag_key + "\": \"" + tag_value + "\"" +
                                   "\n#\tManually deploy it or modify the corresponding tag and then enter CONTINUE." +
                                   "\n#\tEnter EXIT to exit this program." +
                                   "\n# ------------------------------------------------------------------------- #\n"
                                   )
                    if ACTION == 'EXIT':
                        exit()
                    elif ACTION == 'CONTINUE':
                        self.start_database_ec2_if_stopped()
        time_end = time.time()
        logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')
        return ec2_info_dict

    def start_database_ec2_if_stopped(self):
        time_start = time.time()
        logging.info('Start')
        ec2_info = self.retrieve_aws_ec2_info()
        if ec2_info['insSt'].lower() == 'stopped':
            logging.info('Starting database instance: ' + ec2_info['insId'])
            aws_command = 'aws ec2 --profile ec2Manager \
                            start-instances --instance-ids ' + str(ec2_info['insId'])
            output = os.popen(aws_command).read()
            # TODO: add error control by processing output_info
            while ec2_info['insSt'].lower() != 'running':
                time.sleep(30)
                ec2_info = self.retrieve_aws_ec2_info()
                logging.info('Checking current database state: ' + ec2_info['insSt'])
        else:
            logging.info('Current database state: ' + ec2_info['insSt'] + ' is different from \'stopped\'. Not starting')
        time_end = time.time()
        logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')

    def stop_database_ec2_if_running(self):
        time_start = time.time()
        logging.info('Start')
        ec2_info = self.retrieve_aws_ec2_info()
        if ec2_info['insSt'].lower() == 'running':
            logging.info('Stopping database instance: ' + ec2_info['insId'])
            aws_command = 'aws ec2 --profile ec2Manager \
                            stop-instances --instance-ids ' + str(ec2_info['insId'])
            output = os.popen(aws_command)
            output_info = output.read()
            # TODO: add error control by processing output_info
            while ec2_info['insSt'].lower() != 'stopped':
                time.sleep(30)
                ec2_info = self.retrieve_aws_ec2_info()
                logging.info('Checking current database state: ' + ec2_info['insSt'])
        else:
            logging.info('Current database state: ' + ec2_info['insSt'] + ' is different from \'running\'. Not stopping')

        time_end = time.time()
        logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')
