from producer import Producer
from consumer import Consumer
import time, configparser

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')

    #Create a new producer
    producer = Producer(
        config['DEFAULT']['host'],
        "SSL",
        config['DEFAULT']['ssl_cafile'],
        config['DEFAULT']['ssl_certfile'],
        config['DEFAULT']['ssl_keyfile'],
    )
    
    print("Producer created.")

    #Begin while loop
    while(1):
        
        payload = producer.website_data("https://www.netflix.com/")

        producer.publish_message(config['DEFAULT']['topic'], payload)


        print("Published data to topic")

        consumer = Consumer(
            config['DEFAULT']['topic'],
            'earliest',
            config['DEFAULT']['host'],
            'SSL',
            config['DEFAULT']['ssl_cafile'],
            config['DEFAULT']['ssl_certfile'],
            config['DEFAULT']['ssl_keyfile'],
        )

        print("Consumer created.")
                
        threaded_pool = consumer.db_threaded_pool(1,20,f"postgres://{config['PostgreSQL']['dbusername']}:{config['PostgreSQL']['dbpassword']}@{config['PostgreSQL']['dbhost']}:{config['PostgreSQL']['dbport']}/{config['PostgreSQL']['dbname']}?sslmode=require")

        db_conn = consumer.db_connect()  

        print("Connected to db")

        print("Inserting topic from data into db...")

        #Grab kafka topic data and add to db
        consumer.table_insert()

        print(consumer.close_consumer()+"\n")

        #Wait 5 seconds before pulling website data again
        time.sleep(5)

        