#Grab ubuntu:18.04 image
FROM ubuntu:18.04

#Move required files to image
RUN mkdir aiven-kafka && mkdir /aiven-kafka/certs/
COPY producer.py /aiven-kafka/producer.py
COPY consumer.py /aiven-kafka/consumer.py
COPY main.py /aiven-kafka/main.py
COPY install.sh /aiven-kafka/install.sh

#Update / install required packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3-pip && \
    pip3 install kafka-python requests && \
    pip3 install psycopg2-binary

RUN chmod +x /aiven-kafka/install.sh
ENTRYPOINT "./aiven-kafka/install.sh" && /bin/bash