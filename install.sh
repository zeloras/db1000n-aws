#!/bin/bash

if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi


aws configure set aws_access_key_id $AWS_ACCESS_KEY
aws configure set aws_secret_access_key $AWS_SECRET_KEY
aws configure set default.region $AWS_REGION
python3 pscripts/generate_keypair.py
chmod 400 ec2-keypair.pem
python3 pscripts/create_instances.py $AWS_INSTANCE_ID $AWS_INSTANCE_COUNT $AWS_REGION
python3 pscripts/instances_init.py $AWS_ACCESS_KEY $AWS_SECRET_KEY $AWS_REGION
