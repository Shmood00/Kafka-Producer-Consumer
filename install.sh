#!/bin/bash

CONTAINER_ALREADY_STARTED="/aiven-kafka/config.ini"

if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED

    echo "This script sets up your 'config.ini' file needed to run the applicaiton."
    echo ""
    echo "**********************************************************************************"
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
    echo "***********************************************************************************"
    echo ""
    echo "All of your credentials have been moved to '/aiven-kafka/certs/"
    read -p "Enter in your kafka service URI: " host
    read -p "Enter in your kafka topic: " topic

    echo "*********************************************************************************"
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
    echo "Creating your 'config.ini' file."
    echo ""

    echo -e "[DEFAULT]\nhost=$host\ntopic=$topic\nssl_cafile=/aiven-kafka/certs/ca.pem\nssl_certfile=/aiven-kafka/certs/client.cert\nssl_keyfile=/aiven-kafka/certs/client.key\n\n[PostgreSQL]\ndbusername=$dbusername\ndbpassword=$dbpassword\ndbhost=$dbhost\ndbport=$dbport\ndbname=$dbname" >> $CONTAINER_ALREADY_STARTED
    echo ""
    echo "Your 'config.ini' file has been created and moved to the location: /home/$CONTAINER_ALREADY_STARTED"
    echo ""
    
else
    echo "Already done."
fi
