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
    if setting_dict['switch_1'] == True:
        switch_for_stop_AMI = False
        client = boto3.client('ec2',
        aws_access_key_id=setting_dict['access_key_id'],
        aws_secret_access_key=setting_dict['secret_access_key'],
        region_name= setting_dict['regionname'])

        if setting_dict['stopped_EC2_for_nginx'] != "":
            print("terminate EC2")
            FB.EC2_terminate(setting_dict,setting_dict['stopped_EC2_for_nginx'])
            FB.GC_volumes(setting_dict)
            KM.update('stopped_EC2_for_nginx',"")

        # wait for running (EC2)
        instancestate = ""
        while instancestate != "running":
            try:
                response = client.describe_instance_status(InstanceIds= [setting_dict['ongoing_EC2_for_nginx']])
                print("'this_EC2' is "+ response['InstanceStatuses'][0]['InstanceState']['Name'])
                instancestate = response['InstanceStatuses'][0]['InstanceState']['Name']
                if instancestate != "running":
                    sleep(25)
            except Exception as E:
                continue

        # backup old_AMI
        if setting_dict["ongoing_AMI_for_nginx"] != '':
            old_AMI = setting_dict["ongoing_AMI_for_nginx"]
            switch_for_stop_AMI = True

        # generate new_AMI
        FB.AMI_generate(setting_dict,setting_dict['ongoing_EC2_for_nginx'],"ongoing_AMI_for_nginx")

        # stop old_AMI
        if switch_for_stop_AMI == True:
            FB.AMI_stop(setting_dict,old_AMI)
            print(old_AMI)

        # garvage collect for snapshots
        FB.GC_snapshots(setting_dict)
        KM.update("switch_2",True)
    else:
        print("switch off")
#===============================================================================
#===============================================================================
