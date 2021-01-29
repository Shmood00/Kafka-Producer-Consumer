from kafka import KafkaProducer
import requests, time, json

class Producer:
    
    def __init__(self, server, security_protocol, ssl_cafile, ssl_certfile, ssl_keyfile):
        """ Intialize a producer by creating one """

        self.producer = KafkaProducer(
            bootstrap_servers=server,
            security_protocol=security_protocol,
            ssl_cafile=ssl_cafile,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile,
        )
    

    def publish_message(self, topic, payload):

        #Convert payload to bytes
        payload_bytes = bytes(payload, encoding="utf-8")

        #Push data to topic
        self.producer.send(
            topic,
            payload_bytes
        )
        
        
        self.producer.flush()
    

    def close_producer(self):
        self.producer.close()

        return "Producer closed."

    @staticmethod
    def website_data(url):

        resp = requests.get(url)

        payload = json.dumps(
            {
                "date":time.time(),
                "url": resp.url,
                "status":resp.status_code,
                "response_time":resp.elapsed.total_seconds()
                
            }
        )

        return payload
    
    