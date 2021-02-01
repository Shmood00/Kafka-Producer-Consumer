import unittest
from producer import Producer
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class ProducerTest(unittest.TestCase):

    #Create a producer to be used in the tests
    @classmethod
    def setUpClass(cls):
        cls.producer = Producer(
            config['DEFAULT']['host'],
            "SSL",
            config['DEFAULT']['ssl_cafile'],
            config['DEFAULT']['ssl_certfile'],
            config['DEFAULT']['ssl_keyfile'],
        )

    #Close producer after tests
    @classmethod
    def tearDownClass(cls):
        cls.producer.close_producer()

    # Check to see if producer gets created successfully
    def test_make_producer(self):
        self.assertIsNotNone(self.producer)
        

    # Check to see if data is published to topic correctly
    #NOTE: This tests assumes the topic 'test-topic' exists
    def test_publish_message(self):
        self.assertTrue(self.producer.publish_message(
            "test-topic", "test payload"))
        
        self.assertFalse(self.producer.publish_message("fake-topic", "test payload"))
    

if __name__ == '__main__':
    unittest.main()
