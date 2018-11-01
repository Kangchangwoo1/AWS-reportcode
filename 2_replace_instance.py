# -*- coding:utf-8 -*-

#===============================================================================
# Import Package & Module
#===============================================================================
import Key_Manager as KM
import Function_Box as FB
import boto3
import botocore
import datetime
import json
from time import sleep
from botocore.exceptions import ClientError
import os
#===============================================================================
#===============================================================================

#===============================================================================
# main function
#===============================================================================
if __name__ == '__main__':
    setting_dict = KM.read()
    if setting_dict['switch_2'] == True:
        old_EC2 = setting_dict['ongoing_EC2_for_nginx']

        client = boto3.client('ec2',
        aws_access_key_id=setting_dict['access_key_id'],
        aws_secret_access_key=setting_dict['secret_access_key'],
        region_name= setting_dict['regionname'])
        ec2 = boto3.resource('ec2',
        aws_access_key_id=setting_dict['access_key_id'],
        aws_secret_access_key=setting_dict['secret_access_key'],
        region_name= setting_dict['regionname'])

        # wait for running (EC2)
        instancestate = ""
        while instancestate != "running":
            try:
                response = client.describe_instance_status(InstanceIds= [old_EC2])
                print("'this_EC2' is "+ response['InstanceStatuses'][0]['InstanceState']['Name'])
                instancestate = response['InstanceStatuses'][0]['InstanceState']['Name']
                if instancestate != "running":
                    sleep(25)
            except Exception as E:
                continue

        # wait for running (AMI)
        available = ""
        while available != "available":
            try:
                image = ec2.Image(setting_dict['ongoing_AMI_for_nginx'])
                print("'this_AMI' is "+ image.state)
                available = image.state
                if available != 'available':
                    sleep(25)
            except Exception as E:
                continue

        # replace & stop Old_EC2
        KM.update('stopped_EC2_for_nginx',old_EC2)
        FB.EC2_stop(setting_dict,old_EC2)

        # generate new_EC2
        FB.EC2_generate(setting_dict,setting_dict['ongoing_AMI_for_nginx'],"ongoing_EC2_for_nginx")
        KM.update("switch_3",True)
    else:
        print("switch off")
#===============================================================================
#===============================================================================
