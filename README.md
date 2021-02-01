# Kafka-Producer-Consumer

This project monitors a websites availability over the network by producing metrics on the websites and passing them through an Aiven Kafka instance into an Aiven PostgreSQL database. A Kafka producer periodically reaches out to these websites and sends the results back to a Kafka topic. A Kafka consumer reads the data from the Kafka topic and stores it into a PostgreSQL database.

The metrics collected from the websites include:
* HTTP response time
* Error code returned (200, 404, etc.)
* A phone number on the page (if one exists)
* URL of the website being checked

# Assumptions

There are a few assumptions that are made in order for the program to run correctly:
* The program assumes an Aiven Kafka instance has been created already
* The program assumes an Aiven PostgreSQL database has been created already
* The program assumes a user exists for the PostgreSQL database
* The program assumes a Kafka topic has been created in the Aiven console (NOTE: The same topic will be used for testing the producer in `tests_producer.py`)
* Docker is installed on the system this is being tested on (Docker is required for an easy setup process)

# Installation / Running

To be able to run the program we make use of Docker for an easy setup.

After cloning this repo, run the following command in order to create a Docker image:
* `docker build -t name-of-image /path/to/Dockerfile`

Once the image is finished being built, you can boot into the container and begin with the setup. To do this, run the following:
* `docker run -it name-of-image`

Once this is run, you will be greeted with an installation script. Follow the prompts to finalize the setup process.

Once you've finished with the setup you can navigate to the `aiven-kafka` folder within the container to run the actual program. All that's left to do is ensure your Aiven services are up and running and run `python3 main.py https://www.example.com website2 website3 ...`. The program will publish the inputted websites metrics to a Kafka topic and then place them into the PostgeSQL db. After it reaches out to the websites and inserts the information into the database, the program will wait 10 seconds before repeating the process. To stop the program just hit `CTRL-C`.

If at anytime after installation you would like to get back into the container to run the program, run the following commands to avoid having the go through the installation again.

First, determine the name of the docker container:
* `docker ps -a`

Once you find the name of the docker container, start the container and then attach to it:
* `docker start container-name`
* `docker attach container-name`

Then all that's left to do is direct yourself back to the `aiven-kafka` folder to run the program.

# Attributions

The following section will provide links I used that helped me create this project.
* Python Kafka and Kafka in general
  * https://towardsdatascience.com/getting-started-with-apache-kafka-in-python-604b3250aa05
  * https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka
* PostgreSQL and Python
  * https://pynative.com/psycopg2-python-postgresql-connection-pooling/
* Dockerfile creation (including install script)
  * https://www.youtube.com/watch?v=7tGcnOvRQ9o
  * https://www.youtube.com/watch?v=JgdQo0lhevU
  * https://stackoverflow.com/questions/37836764/run-command-in-docker-container-only-on-the-first-start
  * https://forums.docker.com/t/how-to-run-bash-command-after-startup/21631
  * https://serverfault.com/questions/377943/how-do-i-read-multiple-lines-from-stdin-into-a-variable
* Writing Unit Tests
  * https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug
  * https://www.youtube.com/watch?v=6tNS--WetLI
  


