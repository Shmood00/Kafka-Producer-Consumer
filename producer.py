from copy import Error
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError
import requests, time, json, re

#To prevent max retries exceeded error
requests.adapters.DEFAULT_RETRIES = 5

class Producer:
    
    def __init__(self, server, security_protocol, ssl_cafile, ssl_certfile, ssl_keyfile):
        """ Intialize a producer by creating one """
        
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=server,
                security_protocol=security_protocol,
                ssl_cafile=ssl_cafile,
                ssl_certfile=ssl_certfile,
                ssl_keyfile=ssl_keyfile,
            )
        except Exception as e:
            print(f"Error creating kafka producer:\nError: {e}")
    
    
    def publish_message(self, topic, payload):
        """ Function to push website metrics to Kafka topic """

        #Convert payload to bytes
        payload_bytes = bytes(payload, encoding="utf-8")

        #Push data to topic
        try:
            self.producer.send(
                topic,
                payload_bytes
            )

            self.producer.flush()
        except KafkaTimeoutError as e:
            print(f"Error publishing data to topic:\n{e}")
            return False 

        return True
    

    def close_producer(self):
        """ Function to close producer """
        
        try:
            #Close producer
            self.producer.close()

            print("Producer closed.")
             
        except Error as e:
            print(f"Error closing producer:\n{e}")
            return False
        
        return True

    @staticmethod
    def website_data(urls):
        """
        
        Function grabs analytics from inputted URLs.
        Specifically it grabs the status code and response time when
        requests reaches out to it. If there's a phone number found
        on the page, it will grab that also.

        """
        
        #List for all payloads
        responses = []
        for url in urls:
            
            #Send request to website
            resp = requests.get(url)
            
            #Search for phone number
            phone_number = re.search("(1-)?(\()?[0-9]{3}(\))?(\s)?(-)?[0-9]{3}-[0-9]{4}", resp.text)

            if not phone_number:
                phone_number_result = "No phone number not found."
            else:
                phone_number_result = phone_number.group()

            #Create payload
            payload = json.dumps(
                {
                    "date":time.time(),
                    "url": resp.url,
                    "status":resp.status_code,
                    "response_time":resp.elapsed.total_seconds(),
                    "phone_number": phone_number_result
                }
            )

            #Add payload to list
            responses.append(payload)

        return responses
    
    
