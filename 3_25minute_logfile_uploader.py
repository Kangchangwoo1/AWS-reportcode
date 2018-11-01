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
# this main function upload to 's3 bucket'
#===============================================================================
if __name__ == '__main__':
    setting_dict = KM.read()
    if setting_dict['switch_3'] == True:
        FB.logfile_uploader(setting_dict)
    else:
        print("switch off")
#===============================================================================
#===============================================================================
