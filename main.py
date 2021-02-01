from producer import Producer
from consumer import Consumer
import time, configparser, sys

def main():
    # List of websites to get metrics for, inputted through commandline arguments
    websites = sys.argv[1:]

    # Read information from config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Create a new producer
    producer = Producer(
        config['DEFAULT']['host'],
        "SSL",
        config['DEFAULT']['ssl_cafile'],
        config['DEFAULT']['ssl_certfile'],
        config['DEFAULT']['ssl_keyfile'],
    )

    print("Producer created.")

    # Retreive analytics from websites
    payloads = producer.website_data(websites)

    # Sending website analytics to Kafka topic, create consumer and publish to PostgreSQL db
    for site in payloads:

        # Send analytics to kafka topic
        producer.publish_message(config['DEFAULT']['topic'], site)

        print("Published data to topic")

        # Create consumer
        consumer = Consumer(
            config['DEFAULT']['topic'],
            'earliest',
            config['DEFAULT']['client_id'],
            config['DEFAULT']['group_id'],
            config['DEFAULT']['host'],
            'SSL',
            config['DEFAULT']['ssl_cafile'],
            config['DEFAULT']['ssl_certfile'],
            config['DEFAULT']['ssl_keyfile'],
        )

        print("Consumer created.")

        # Create new threaded pool
        threaded_pool = consumer.db_threaded_pool(1, 20, f"postgres://{config['PostgreSQL']['dbusername']}:{config['PostgreSQL']['dbpassword']}@{config['PostgreSQL']['dbhost']}:{config['PostgreSQL']['dbport']}/{config['PostgreSQL']['dbname']}?sslmode=require")

        # Connect to db
        db_conn = consumer.db_connect(threaded_pool)

        print("Connected to db")

        # Create table in db (if not already created)
        consumer.create_table(db_conn)

        print("Inserting data from topic into db...")

        # Grab data from topic and add to db
        consumer.table_insert()

        # Close consumer
        if consumer.close_consumer():
            print("Consumer closed.\n")


if __name__ == '__main__':

    # Continually loop and wait 10 seconds between getting new website analytics
    while (1):
        main()
        time.sleep(10)
