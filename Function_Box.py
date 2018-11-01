# -*- coding:utf-8 -*-

#===============================================================================
# Import Package & Module
#===============================================================================
import Key_Manager as KM
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
# declear fundamental function
#===============================================================================
# Log 상태와 상세를 입력하면 추가해줌.
def Log_stamp(status, detail,path = "/home/ubuntu/myproject/log/Application.log"):
    if os.path.isfile(path) == False:
        with open(path, "w") as f:
            f.write("")
    with open(path, "a") as f:
        f.write(str(datetime.datetime.now()) + "\t" + status+ "\t" + detail+"\n")


# S3 객체와 버켓명을 넣어주면 있는 지 없는 지 확인해준다.
def S3_bucket_check(setting_dict):
    s3 = boto3.resource('s3',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])

    return True if setting_dict['bucket'] in [bucket.name for bucket in s3.buckets.all()] else False

# S3 객체와 버켓명, 지역명을 넣으면 버켓을 생성해준다.
def S3_bucket_generate(s3,Bucket_name,region_name):
    s3.create_bucket(Bucket=Bucket_name,CreateBucketConfiguration={'LocationConstraint': region_name})

# S3에서 파일을 다운로드 할 떄 활용함.
def S3_file_download(s3,Bucket_name,remote_path="./Application.log",local_path= "/home/ubuntu/myproject/log/Application.log"):
    try:
        s3.download_file(Bucket_name, remote_path,local_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

# S3에서 파일을 업로드 할 때 활용함.
def S3_file_upload(s3,Bucket_name, local_path= "/home/ubuntu/myproject/log/Application.log", remote_path="Application.log"):
    s3.upload_file(local_path, Bucket_name, remote_path)


def S3_clean(setting_dict):
    client = boto3.client('s3',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])
    resource = boto3.resource('s3',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])
    bucket_name = 'gachon-bigdata-lecture-201232932kang'
    bucket = resource.Bucket(bucket_name)

    for i in [ value.key for value in bucket.objects.all()]:
        print(i)
        response = client.delete_object(Bucket=bucket_name,Key=i)
        print(response)
        Log_stamp("FILE_DELETED",i)

# Problem3
def logfile_uploader(setting_dict):
    Log_stamp("S3_UPDATED","logfile is replaced")

    s3 = boto3.client('s3',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])

    resource = boto3.resource('s3',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])


    if S3_bucket_check(setting_dict) == False:
        S3_bucket_generate(s3,setting_dict['bucket'],setting_dict['regionname'])
        print("원격지에 Bucket이 없기에, 생성했습니다.")

    bucket = resource.Bucket('gachon-bigdata-lecture-201232932kang')
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y%m%d%H%M%S')

    if len([ value.key for value in bucket.objects.all()]) == 1:
        for file in [ value.key for value in bucket.objects.all()]:
            print("원격지에 Log파일이 저장되어 있습니다.")
            S3_file_download(s3,setting_dict['bucket'],remote_path =file ,local_path="/home/ubuntu/myproject/log/copyed.log")

            c = open("/home/ubuntu/myproject/log/Application.log", 'r')
            lines = c.readlines()

            with open("/home/ubuntu/myproject/log/copyed.log", "a") as f:
                for line in lines:
                    f.write(line)

            c.close()

            S3_clean(setting_dict)
            S3_file_upload(s3,setting_dict['bucket'],remote_path = nowDatetime+"logfile.log",local_path="/home/ubuntu/myproject/log/copyed.log")

            os.remove("/home/ubuntu/myproject/log/copyed.log")
            os.remove("/home/ubuntu/myproject/log/Application.log")

    else:
        print("원격지에 Log 파일을 업로드합니다.")
        S3_file_upload(s3,setting_dict['bucket'],remote_path = nowDatetime+"logfile.log")
        os.remove("/home/ubuntu/myproject/log/Application.log")

#===============================================================================
#===============================================================================


# 이름과 인스턴스 id가 있을 경우, ami를 만들어준다.
def AMI_generate(setting_dict,image_id,save_temp_id,AMI_name="Hong_Gil_Dong"):
    client = boto3.client('ec2',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])
    instances = client.describe_instances()
    for instance in instances["Reservations"]:
      instance_id = instance['Instances'][0]['InstanceId']

      if instance_id == image_id:
          now = datetime.datetime.now()
          nowDatetime = now.strftime('%Y%m%d%H%M%S')

          name = "Image for instance {instance_id} Created at {datetime}".format(instance_id=instance_id,datetime=nowDatetime)
          print ("creating image for instance {instance_id},Created at {datetime}".format(instance_id=instance_id,datetime=nowDatetime))
          image = client.create_image(InstanceId=instance_id,Name=AMI_name+nowDatetime)
          KM.update(save_temp_id,image['ImageId'])
          Log_stamp("AMI_CREATED",AMI_name+nowDatetime+"\t"+image['ImageId'])



def EC2_generate(setting_dict,image_id,save_temp_id):
    ec2 = boto3.resource('ec2',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])

    instances = ec2.create_instances(
        NetworkInterfaces=[{'SubnetId': setting_dict['SubnetId'], 'DeviceIndex': 0, 'Groups': [setting_dict['VPC_id']]}],
    	ImageId=image_id,
    	MinCount=1,
    	MaxCount=1,
    	KeyName=setting_dict['keyname'],
    	InstanceType=setting_dict['instance_type'])
    for instance in instances:
        print(instance.id, instance.instance_type)
        KM.update(save_temp_id,instance.id)
        Log_stamp("EC2_CREATED",instance.id)


def EC2_stop(setting_dict,instance_id):
    action = "OFF"

    ec2 = boto3.client('ec2',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])

    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
        Log_stamp("EC2_STOPPED",instance_id)
    except ClientError as e:
        print(e)

def EC2_terminate(setting_dict,instance_id):
    action = "OFF"

    ec2 = boto3.client('ec2',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])

    try:
        response = ec2.terminate_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
        Log_stamp("EC2_TERMINATED",instance_id)
    except ClientError as e:
        print(e)


def AMI_stop(setting_dict,AMI_id):
    client = boto3.client('ec2',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])


    response = client.deregister_image(DryRun=False, ImageId=AMI_id)
    Log_stamp("AMI_DEREGISTERED",AMI_id)

def GC_volumes(setting_dict):
    client = boto3.client('ec2',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])

    volumes = client.describe_volumes()

    for volume in volumes['Volumes']:
        try:
            response = client.delete_volume(VolumeId= volume['VolumeId'],DryRun=False)

        except ClientError as e:
            print(e)
    Log_stamp("GARBAGE_COLLECTED","Volumes")

def GC_snapshots(setting_dict):
    client = boto3.client('ec2',
    aws_access_key_id=setting_dict['access_key_id'],
    aws_secret_access_key=setting_dict['secret_access_key'],
    region_name= setting_dict['regionname'])
    snapshots = client.describe_snapshots(OwnerIds=['092977743884'])
    for snapshot in snapshots['Snapshots']:
        try:
            response = client.delete_snapshot(SnapshotId=snapshot['SnapshotId'],DryRun=False)
            print(snapshots['Snapshots'])
        except ClientError as e:
            print(e)

    Log_stamp("GARBAGE_COLLECTED","SNAPSHOTS")
#===============================================================================
#===============================================================================

#===============================================================================
# declear main_function
#===============================================================================
if __name__ == '__main__':
    setting_dict = KM.read()
#===============================================================================
#===============================================================================
