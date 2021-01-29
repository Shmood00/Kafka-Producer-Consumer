#!/bin/bash

#This script runs on the first bootup of the docker container.
#It collects all information required in order for the underlying
#Python program to run correctly. This script aims to automate as
#much of the setup process as possible.

#Variable to config location
CONTAINER_ALREADY_STARTED="/aiven-kafka/config.ini"

#Check if config file already exists
#This is used so once a user initially sets up their container,
#they don't need to go through this process whenever they
#want to access their container. Using the 'docker start'
#and 'docker attach' commands, a user will boot right into
#bash shell.
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED

    echo "This script sets up your 'config.ini' file needed to run the applicaiton."
    echo ""
    echo "**********************************************************************************"
    echo ""
    echo "We will now store the 2 certifications and 1 key required for this program to properly run."
    echo "Please paste below your Access Key (Press enter then CTRL-D once pasted):"
    access_key=$(</dev/stdin)

    echo ""
    echo "Please paste below your Access Certificate (Press enter then CTRL-D once pasted):"
    access_cert=$(</dev/stdin)
    
    echo ""
    echo "Please paste below your CA Certificate (Press enter then CTRL-D once pasted):"
    ca_cert=$(</dev/stdin)

    echo "$access_key" >> /aiven-kafka/certs/client.key
    echo "$access_cert" >> /aiven-kafka/certs/client.cert
    echo "$ca_cert" >> /aiven-kafka/certs/ca.pem
    echo ""
    echo "***********************************************************************************"
    echo ""
    echo "All of your credentials have been moved to '/aiven-kafka/certs/"
    echo ""
    echo "***********************************************************************************"
    echo ""
    read -p "Enter in your kafka service URI: " host
    read -p "Enter in your kafka topic: " topic
    echo ""
    echo "*********************************************************************************"
    echo ""
    echo "Now to capture your PostgreSQL information."
    echo ""

    read -p "Enter your PostgreSQL username: " dbusername
    read -s -p "Enter in your PostgreSQL password: " dbpassword
    echo ""
    read -p "Enter your PostgreSQL hostname: " dbhost
    read -p "Enter your PostgreSQL port: " dbport
    read -p "Enter in your PostgreSQL database name: " dbname

    echo ""
    echo "**********************************************************************************"
    echo ""
    echo "Creating your 'config.ini' file."
    echo ""

    echo -e "[DEFAULT]\nhost=$host\ntopic=$topic\nssl_cafile=/aiven-kafka/certs/ca.pem\nssl_certfile=/aiven-kafka/certs/client.cert\nssl_keyfile=/aiven-kafka/certs/client.key\n\n[PostgreSQL]\ndbusername=$dbusername\ndbpassword=$dbpassword\ndbhost=$dbhost\ndbport=$dbport\ndbname=$dbname" >> $CONTAINER_ALREADY_STARTED
    echo ""
    echo "Your 'config.ini' file has been created and moved to the location: $CONTAINER_ALREADY_STARTED"
    echo "Please navigate to the /aiven-kafka/ folder to run the program."
    echo ""
    
else
    echo "Config file already created."
fi
