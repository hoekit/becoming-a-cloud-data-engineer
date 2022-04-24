# Kafka Java Producer


----
### Kafka Java Producer

__ Scope

- Create a Java Producer for Kafka
    - Source data is a text file

- Create tests for the Java Producer
..

__ 1. The docker-compose.yml file:

```
---
version: '2'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:6.2.1
    hostname: zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  broker:
    image: confluentinc/cp-kafka:6.2.1
    hostname: broker
    container_name: broker
    depends_on:
      - zookeeper
    ports:
      - "29092:29092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_TOOLS_LOG4J_LOGLEVEL: ERROR

  schema-registry:
    image: confluentinc/cp-schema-registry:6.2.1
    hostname: schema-registry
    container_name: schema-registry
    depends_on:
      - broker
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: 'broker:9092'
      SCHEMA_REGISTRY_LOG4J_ROOT_LOGLEVEL: WARN
```
..

__ 2. Create a topic

- Open a shell in the broker service:

    docker-compose exec broker bash

- Create a topic:

    kafka-topics --create --topic output-topic \
        --bootstrap-server broker:9092 \
        --replication-factor 1 \
        --partitions 1
..
__ Step Notes

- Messed up the creation and needed to delete the topic

- So go into the broker service

    docker-compose exec broker bash

- Go to where the server.properties file for Kafka is found:

    cd /etc/kafka

- Add the property at the end cos vim doesn't work in the docker image:

    cat >> server.properties
    delete.topic.enable=true
    # Press Ctrl-D to end

    cat server.properties       # Check that the line was added

- Remove the topic:

    kafka-topics --delete --topic output-topic --bootstrap-server broker:9092

- Manually delete Apache Kafka topics, 2018
    - https://contactsunny.medium.com/manually-delete-apache-kafka-topics-424c7e016ff3
    - Commands are outdated but one can guess the correct ones
..

__ 3. Create a `gradle.build` file for the project

- See: build.gradle

- Create the Gradle wrapper _after_ creating the build.gradle file
    - `gradle wrapper`

- Create a .gitignore file
..

__ 4. Setup Configuration used

- `mkdir configuration`
    - Create directory for configuration data

- Create file: configuration/dev.properties
    - This is the properties for development

..

__ 5. Create the KafkaProducer application

- Create directory
    - `mkdir -p src/main/java/com/firexis`

- Edit the file
    - `vim src/main/java/com/firexis/KafkaProducerApp.java`

- Build the shadowJar
    - `./gradlew shadowJar`

..

__ 6. Run the app

- Create a test input file: input.txt

- Run the jar:
    - `java -jar build/libs/kafka-producer-application-standalone-0.0.1.jar configuration/dev.properties input.txt`

- Check by consuming
    - `docker-compose exec broker bash`
        - Run a shell on the broker
    ```
        docker exec -it broker kafka-console-consumer --topic output-topic \
            --bootstrap-server broker:9092 \
            --from-beginning \
            --property print.key=true \
            -property key.separator=" : "
    ```
..

__ 7. Create tests

- Create a configuration file for test: `configuration/test.properties`

- Create the test application
    - `mkdir -p src/test/java/com/firexis`
        - Create the folder for the tests
    - `vim src/test/java/com/firexis/KafkaProducerAppTest.java`

- Run the test
    - `./gradlew test`

- Check results
    - `build/reports/tests/test/index.html`
..

__ Notes

- This project introduces the notion of Schema Registry

- Schema Registry
    - Motivation:
        - The schema of topics change and needs to be managed
        - Eliminates runtime failures from unmaaged schema changes
    - Is:
        - a server process external to Kafka brokers
    - Does:
        - maintain a database of schemas
        - database is store in an internal Kafka topic
        - cached in Schema Registry for low latency
    - HA deployment:
        - available
    - Works by:
        - Producers send message to REST endpoint
    - Performance:
        - Producers caches the REST endpoint results
    - Supported Formats:
        - JSON, Avro, Protobuf
    - Summary:
        - Does type checking and prevents Producers from sending
          incompatible messages
        - Also prevents Consumers from ingesting incompatible messages

- See Also: Schema Evolution with Kafka Schema Registry
    - https://www.youtube.com/watch?v=Qqg948wE2Gk

- The docker-compose.yml file (version 2) in this project does not have
  the below environment variables found in the
  `kafka-2-docker-compose-20220422` project (version 3):
    - KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
    - KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1

- Summary:
    - This project does not have Kafka transactions enabled.

- See: Hands-Free Kafka Replication, 2015
    - https://www.confluent.io/blog/hands-free-kafka-replication-a-lesson-in-operational-simplicity/
    - ISR: in-sync replica

- See: https://stackoverflow.com/questions/56888050
    - `Transaction state` is an internal topic created when Kafka is
      configured to use transactions
    - KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: The minimum in-sync replica
      for the internal topic 'transaction.state'
    - - KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: The replication
        factor for the internal topic 'transaction.state'

= See: https://www.confluent.io/blog/transactions-apache-kafka/
    - Transactions in Apache Kafka, 2017
..

__ Next Steps

- Create multiple brokers
    - Then increase partitions and replications

- Create more than one producer

- Use public key instead of plaintext

- Create an email connector
    - https://www.confluent.io/hub/jcustenborder/kafka-connect-email
    - https://github.com/jcustenborder/kafka-connect-email
    - https://github.com/wardziniak/kafka-connect-email

- Create a consumer group

- Study this article on the various settings:
    - https://blog.softwaremill.com/help-kafka-ate-my-data-ae2e5d3e6576

- Schema Evolution, 2020, 59:39 mins
    - https://www.youtube.com/watch?v=Qqg948wE2Gk

- More Confluent Tutorials
    - https://developer.confluent.io/tutorials/#learn-the-basics

- Confluent Kafka Courses
    - https://developer.confluent.io/learn-kafka/?ajs_aid=e4ba1fec-4466-4846-bf47-8e34146f1797

- Unrelated: Fix Lenovo Bug
    - https://duckduckgo.com/?t=ffab&q=lenovo+uefi+vulnerabilities&ia=web
    - https://support.lenovo.com/us/en/product_security/ps500040-uefi-edk2-capsule-update-vulnerabilities
..

__ Links

- Apache Kafka 101: Schema Registry
    - https://www.youtube.com/watch?v=_x9RacHDQY0

- How to build your first Apache KafkaProducer application
    - https://developer.confluent.io/tutorials/creating-first-apache-kafka-producer-application/kafka.html

- Kafka Mock Producer
    - https://kafka.apache.org/25/javadoc/org/apache/kafka/clients/producer/MockProducer.html
..
