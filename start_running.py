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

backup_EC2_for_crontab = raw_input("input your crontab_EC2_id")
KM.update("backup_EC2_for_crontab",backup_EC2_for_crontab)
KM.update("ongoing_EC2_for_crontab",backup_EC2_for_crontab)

backup_EC2_for_nginx = raw_input("input your nginx_EC2_id")
KM.update("backup_EC2_for_nginx",backup_EC2_for_nginx)
KM.update("ongoing_EC2_for_nginx",backup_EC2_for_nginx)

access_key_id = raw_input("input your access_key_id")
KM.update("access_key_id",access_key_id)

secret_access_key = raw_input("input your secret_access_key_id")
KM.update("secret_access_key",secret_access_key)

bucket = raw_input("input your bucket name")
KM.update("bucket",bucket)

VPC_id = raw_input("input your VPC_id")
KM.update("VPC_id",VPC_id)

keyname = raw_input("input your keyname")
KM.update("keyname",keyname)

SubnetId = raw_input("input your SubnetId")
KM.update("SubnetId",SubnetId)

regionname = raw_input("input your regionname")
KM.update("regionname",regionname)
KM.update("switch_1",True)
