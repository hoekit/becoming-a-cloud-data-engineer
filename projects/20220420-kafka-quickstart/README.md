# Kafka Quick Start


----
### Kafka Quick Start
__ Get Kafka

wget https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz
tar -xzvf kafka_2.13-3.1.0.tgz
rm kafka_2.13-3.1.0.tgz
cd kafka_2.13-3.1.0
..
__ Start ZooKeeper service

# Note: Soon, ZooKeeper will no longer be required by Apache Kafka
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
bin/zookeeper-server-start.sh config/zookeeper.properties &
..
__   Issues

Got an error while starting zookeeper:

    20220420-kafka-quickstart/kafka_2.13-3.1.0/bin/kafka-run-class.sh:
        line 342:
            /usr/lib/jvm/java-8-openjdk-amd64/bin/java:
                No such file or directory

Cause:

    # JAVA_HOME incorrectly setup on my laptop
    #
    echo $JAVA_HOME
    # /usr/lib/jvm/java-8-openjdk-amd64

    # Actual JAVA location
    #
    type java
    # java is /usr/bin/java
    #
    ls -al /usr/bin/java
    # /usr/bin/java -> /etc/alternatives/java
    #
    ls -l /etc/alternatives/java
    # /etc/alternatives/java -> /usr/lib/jvm/java-11-openjdk-amd64/bin/java

Solution:

    # Set JAVA_HOME to correct value
    #
    export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
..
__ Start Kafka Brokers

# Start the Kafka broker service
bin/kafka-server-start.sh config/server.properties &
..
__ Create topic

bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
..
__ Show topic details

bin/kafka-topics.sh --describe --topic quickstart-events --bootstrap-server localhost:9092
..
__ Write events to topic from STDIN

bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092
# This is my first event
# This is my second event
Ctrl-D to stop
..
__ Read events from topic to STDOUT

# Run the following in a separate terminal
bin/kafka-console-consumer.sh \
    --topic quickstart-events \
    --from-beginning \
    --bootstrap-server localhost:9092
..
__ Terminate and cleanup

1. Stop producer and consumer clients with Ctrl-C

2. Stop the kafka broker with Ctrl-C

3. Stop ZooKeeper server with Ctrl-C

4. Remove logs
    - rm -rf /tmp/kafka-logs /tmp/zookeeper
..
__ Links

- Apache Kafka Quickstart
    - https://kafka.apache.org/quickstart
..

