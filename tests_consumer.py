import unittest
from consumer import Consumer
import configparser
from psycopg2 import pool

#Read data from config file
config = configparser.ConfigParser()
config.read('config.ini')

class ConsumerTest(unittest.TestCase):

    # Create a consumer to be used in the tests
    @classmethod
    def setUpClass(cls):
        cls.consumer = Consumer(
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
    
    #Close consumer after tests
    @classmethod
    def tearDownClass(cls):
        cls.consumer.close_consumer()
    
    def test_db(self):

        #Test to make sure threaded pool and connection within the pool works properly
        #Also tests if insertion into the db table works correctly
        threaded_pool = self.consumer.db_threaded_pool(1,20,f"postgres://{config['PostgreSQL']['dbusername']}:{config['PostgreSQL']['dbpassword']}@{config['PostgreSQL']['dbhost']}:{config['PostgreSQL']['dbport']}/{config['PostgreSQL']['dbname']}?sslmode=require")
        db_connection = self.consumer.db_connect(threaded_pool)
        
        self.assertIsInstance(threaded_pool, pool.ThreadedConnectionPool)
        self.assertIsNotNone(db_connection)
        self.assertTrue(self.consumer.create_table(db_connection))
        self.assertTrue(self.consumer.table_insert())
    
        #Test to see creation of threaded pool and connection within the pool fails gracefully
        bad_threaded_pool = self.consumer.db_threaded_pool(1,20,f"postgres://{config['PostgreSQL']['dbusername']}:{config['PostgreSQL']['dbpassword']}@{config['PostgreSQL']['dbhost']}:{config['PostgreSQL']['dbport']}/FAKEDB?sslmode=require")
        bad_db_connection = self.consumer.db_connect(bad_threaded_pool)

        self.assertIsNone(bad_threaded_pool)
        self.assertIsNone(bad_db_connection)




        


if __name__ == '__main__':
    unittest.main()
