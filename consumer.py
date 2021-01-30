from kafka import KafkaConsumer
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
import psycopg2, json

class Consumer:

    def __init__(self, topic, offset_reset, client_id, group_id, server, security_protocol, ssl_cafile, ssl_certfile, ssl_keyfile):
        self.consumer = KafkaConsumer(
            topic,
            auto_offset_reset=offset_reset,
            client_id=client_id,
            group_id=group_id,
            bootstrap_servers=server,
            security_protocol=security_protocol,
            ssl_cafile=ssl_cafile,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile,
        ) 

    def db_threaded_pool(self, min,max,uri):
        """ Create new threaded pool for multiple connections.
            Using in case application in future becomes multi-threaded.
        """
        self.threaded_pool = None
        try:
            self.threaded_pool = pool.ThreadedConnectionPool(min,max,uri)
        except Exception as e:
            print("Unable to establish a connection to the database.")
    
    def db_connect(self):
        """ Create a connection within the pool """
        try:
            self.db_conn = self.threaded_pool.getconn()
        except Exception as e:
            print(f"Unable to create connection within the pool.\nError: {str(e)}")
    
    def table_insert(self):
        """
        Function reads data from topic and inserts data into PostgreSQL db
        """

        #Create cursor
        try:
            cursor = self.db_conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(f"Error creating cursor.\nError: {e}")
        
        #Create table if it doesn't exist
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS public."website-data" (date timestamp, url text, status int, response_time float);')
        except psycopg2.Error as e:
            print(f"There was an error attemtping to create the table:\n{e.pgerror}")

        ##get topic data
        for _ in range(2):
            data = self.consumer.poll(timeout_ms=1000)
            for _,msgs in data.items():
                for msg in msgs:
                    json_msg = json.loads(msg.value)

                    #Insert kafka topic data into db
                    #Assuming the table 'website-data' already exists
                    try:
                        cursor.execute('INSERT INTO "website-data" (date, url, status, response_time) VALUES (to_timestamp(%s),%s,%s, %s)', (json_msg['date'],json_msg['url'], json_msg['status'], json_msg['response_time']))
                        self.db_conn.commit()
                    except psycopg2.Error as e:
                        print(f"Error adding topic data into table.\nError: {e.pgerror}")
                    finally:

                        print("Inserted data from topic into 'website-data' table.")

        #commit offset so it's not repeated
        self.consumer.commit()
        
        #close cursor
        cursor.close()

        #release connection object back to connection pool and close
        self.threaded_pool.putconn(self.db_conn, close=True)
    
    def close_consumer(self):
        self.consumer.close()

        return "Consumer closed."

    





