#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False


while [[ $# -gt 0 ]]; do
   case "$1" in
      -firstName)
         shift
         firstName=$1
         shift
         ;;
      -lastName)
         shift
         lastName=$1
         shift
         ;;
      -email)
         shift
         email=$1
         shift
         ;;
      -region)
         shift
         region=$1
         shift
         ;;
      *)
         echo "$1 is not a recognized flag!"
         exit 1
         ;;
   esac
done

# Check if required parameters are provided
if [[ -z "$firstName" || -z "$lastName" || -z "$email" || -z "$region" ]]; then
    echo "Missing required parameters. Please provide all required parameters."
    exit 1
fi

# Check the region and run the corresponding Ansible playbook
case "$region" in
    "eu-central-1")
        sed -i 's|<replace>|$lastname,-$region|g' /home/ec2-user/eu-central-1/eu-central-1.tf
        cd /home/ec2-user/ && ansible-playbook -i hosts.ini eu-central-1.yml
        ;;
    "eu-west-1")
        sed -i 's|<replace>|$lastname,-$region|g' /home/ec2-user/eu-west-1/eu-west-1.tf
        cd /home/ec2-user/ && ansible-playbook -i hosts.ini eu-west-1.yml
        ;;
    "eu-east-1")
        sed -i 's|<replace>|$lastname -$region|g' /home/ec2-user/eu-east-1/eu-east-1.tf
        cd /home/ec2-user/ && ansible-playbook -i hosts.ini eu-east-1.yml
        ;;
    *)
        # If none of the options match, print an error message
        echo "Invalid region. Please provide one of the following options: eu-central-1, eu-west-1, eu-east-1."
        exit 1
	;;
esac
