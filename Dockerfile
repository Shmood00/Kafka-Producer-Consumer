#Grab ubuntu:18.04 image
FROM ubuntu:18.04

#Create folder to put certs in
RUN mkdir aiven-kafka && mkdir /aiven-kafka/certs/

#Move required files to image
COPY producer.py /aiven-kafka/producer.py
COPY consumer.py /aiven-kafka/consumer.py
COPY tests_producer.py /aiven-kafka/tests_producer.py
COPY tests_consumer.py /aiven-kafka/tests_consumer.py
COPY main.py /aiven-kafka/main.py
COPY install.sh /aiven-kafka/install.sh

#Update / install required packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3-pip && \
    pip3 install kafka-python requests && \
    pip3 install psycopg2-binary

#Make install script executable
RUN chmod +x /aiven-kafka/install.sh

#Run install script on first boot
ENTRYPOINT "./aiven-kafka/install.sh" && /bin/bash