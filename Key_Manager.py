# -*- coding:utf-8 -*-

#===============================================================================
# import package & module
#===============================================================================
import os
import json
#===============================================================================
#===============================================================================


#===============================================================================
# declear fundamental function
#===============================================================================
#setting defalut_value
def defalut_set():
    defalut =   {
                # key for AWS
                "access_key_id": "AKIAJ75CGAT6YYQ2AX6A",
                "secret_access_key":"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",

                # about nginx
                "ongoing_EC2_for_nginx":"",
                "ongoing_AMI_for_nginx":"",
                "stopped_EC2_for_nginx":"",
                "backup_AMI_for_nginx":"ami-0cbad1ff1711f6e1d",
                "backup_EC2_for_nginx":"i-0465fa4ef38f2064f",

                # about crontab
                "ongoing_EC2_for_crontab":"",
                "backup_AMI_for_crontab":"ami-09f15101486fb85ef",
                "backup_EC2_for_crontab":"i-052b4821f5ec94d57",

                # more infomation
                "bucket":"gachon-bigdata-lecture-201232932kang",
                "VPC_id":"sg-0d95e6146b706ae98",
                "keyname":"bigdata-lecture-ubuntu",
                "instance_type":"t2.micro",
                'SubnetId': "subnet-58aba33f",
                "regionname" : "ap-southeast-1",
                "switch_1" : False,
                "switch_2" : False,
                "switch_3" : False
                }
    with open("/home/ubuntu/myproject/source/setting.json","w") as f:
        json.dump(defalut,f)

# update value to key
def update(Key_name,value):
    with open("/home/ubuntu/myproject/source/setting.json","r") as f:
        contents = f.read()
        json_dict = json.loads(contents)
    if Key_name in json_dict.keys():
        print("It is valid key. so, I will update value.")
        json_dict[Key_name] = value
        with open("/home/ubuntu/myproject/source/setting.json","w") as f:
            json.dump(json_dict,f)
    else:
        print("It is not a valid key.")

# read 'setting_dict' for use
def read():
    with open("/home/ubuntu/myproject/source/setting.json","r") as f:
        contents = f.read()
        json_dict = json.loads(contents)
    return json_dict
#===============================================================================
#===============================================================================

#===============================================================================
# declear main_function
#===============================================================================
if __name__ == '__main__':
    defalut_set()
    # update("backup_AMI_for_nginx","ami-033f6633252fb22e5")
    # update("backup_EC2_for_nginx","i-0ba7bda5ee0e4081c")
#===============================================================================
#===============================================================================
