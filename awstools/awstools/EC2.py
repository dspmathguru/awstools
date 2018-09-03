import boto3
from botocore.exceptions import ClientError

class EC2:
  def __init__(self):
    self.ec2 = boto3.client('ec2')
    resp = self.ec2.describe_instances()

    self.insts = []
    for res in resp['Reservations']:
      inst = {}
      for i in res['Instances']:
        inst['InstanceId'] = i['InstanceId']
        inst['KeyName'] = i['KeyName']
        inst['State'] = i['State']['Name']
        for tag in i['Tags']:
          if tag['Key'] == 'Name':
            inst['Name'] = tag['Value']
          if 'PublicIpAddress' in i:
            inst['PublicIpAddress'] = i['PublicIpAddress']
      self.insts.append(inst)

  def __str__(self):
    str = ''
    for inst in self.insts:
      str = str + inst['InstanceId']
      str = str + ' ' + inst['KeyName'] + ' ' + inst['State']
      if 'Name' in inst:
        str = str + ' ' + inst['Name']
      if 'PublicIpAddress' in inst:
        str = str + ' ' + inst['PublicIpAddress']
      str = str + '\n'
    
    return str[:-1]

def main():
  ec2 = EC2()
  print(ec2)

  
