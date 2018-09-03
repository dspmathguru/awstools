import sys
import os
import argparse

import boto3
from botocore.exceptions import ClientError


class EC2Instance:
  def __init__(self, ec2Name):
    self.ec2 = boto3.client('ec2')
    self.inst = self.findInst(ec2Name)
    if self.inst == None:
      print("ERROR: can not find instance with name: ", ec2Name)

  def findInst(self, ec2Name):
    resp = self.ec2.describe_instances()
    for reserve in resp['Reservations']:
      for inst in reserve['Instances']:
        for tag in inst['Tags']:
          if tag['Key'] == 'Name' and tag['Value'] == ec2Name:
            return inst

    return None

  def isStopped(self):
    return self.inst != None and self.inst['State']['Name'] == 'stopped'

  def isRunning(self):
    return self.inst != None and self.inst['State']['Name'] == 'running'

  def instId(self):
    if self.inst == None:
      return 'None'
    else:
      return self.inst['InstanceId']

  def start(self):
    if self.inst == None and not self.isStopped():
      print("ERROR: can not start instance")
      return

    try:
      self.ec2.start_instances(InstanceIds=[self.instId()], DryRun=False)
    except ClientError as e:
      print(e)

  def stop(self):
    if self.inst == None and not self.isRunning():
      print("ERROR: can not stop instance")
      return

    try:
      self.ec2.stop_instances(InstanceIds=[self.instId()], DryRun=False)
    except ClientError as e:
      print(e)

def main():
  parser = argparse.ArgumentParser(description='Startup EC2 instance')
  parser.add_argument('ec2Names', metavar='ec2Names', type=str, nargs='+',
                      help="names of ec2 instances to start")
  parser.add_argument('--start', action='store_true', 
                      help='Start ec2 with this tag Name',
                      default=False)
  parser.add_argument('--stop', action='store_true',
                      help='Stop ec2 with this tag Name',
                      default=False)
  args = parser.parse_args()

  if args.start and args.stop:
    print("ERROR: please pick one of start or stop")

  for ec2Name in args.ec2Names:
    ec2 = EC2Instance(ec2Name)
    if args.start:
      ec2.start()

    if args.stop:
      ec2.stop()

