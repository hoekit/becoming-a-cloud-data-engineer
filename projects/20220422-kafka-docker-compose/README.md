# Kafka Docker Compose


----
### Kafka Docker Compose
__ Scope

- Create a Kafka cluster in Docker:
- Create a topic manually
- Produce a few events
- Consume a few events
- Tear down
..

__ Project Folders/Files Structure

- $PROJECT
    - docker-compose.yaml
..

__ Steps

1. Create the docker-compose.yaml file with two containers
    - zookeeper
    - kafka

2. Create a topic manually:
    ```
    docker exec -it kafka kafka-topics --create \
        --topic kafker-events \
        --bootstrap-server localhost:9092
    ```
    - `kafka` is the name of the kafka service
    - `kafka-topics` is the executable similar to `bin/kafka-topics.sh`
      in the `20220420-kafka-quickstart` project

3. Start producing events
    ```
    docker exec -it kafka kafka-console-producer \
        --topic kafker-events \
        --bootstrap-server localhost:9092
    ```
    - Then enter a few messages terminated by newlines
    - Enter Ctrl-D to end the session

4. Consume events
    ```
    docker exec -it kafka kafka-console-consumer --from-beginning \
        --topic kafker-events \
        --bootstrap-server localhost:9092
    ```
    - Expect the produced messages to be displayed
    - Enter Ctrl-C to end the session

5. Stop kafka and zookeeper
    - `docker-compose stop`
    - This will cause all data in kafka container to be deleted
..

__ Next Steps

How do we create a kafka container where the messages are retained?

- Check where Confluent/Kafka stored the logs:
    ```
    kafka-log-dirs --describe \
        --topic-list $TOPIC \
        --bootstrap-server localhost:9092
    ```
    - Stored in `/var/lib/kafka/data` for each broker

- Declare volumes for the kafka service:
    - See: https://stackoverflow.com/questions/69898673
    - See: https://tecadmin.net/docker-compose-persistent-mysql-data/
        - This does not work

- The current docker-compose.yaml file works:
    ```
    volumes:
      kafka-data:
        driver: local
        driver_opts:
          o: bind
          type: none
          device: /home/hoekit/tmp/kafka_data
    ```

- Viewing docker volumes:
    - docker volume ls
        - lists all volumes
    - docker volume rm `docker volume ls -q`
        - remove all volumes
    - docker rm `docker ps -aq`
        - remove all containers
    - docker volume inspect $VOLUME
        - See volume details
..

__ Cleanup

- Remove containers
    - docker rm `docker ps -aq`

- Remove volumes
    - docker volume rm `docker volume ls -q`

- Remove mapped folder
    - sudo rm -r /home/hoekit/tmp/kafka_data
..

__ Links

- Processing Kafka Sources and Sinks with Apache Flink in Python
    - https://thecodinginterface.com/blog/kafka-source-sink-with-apache-flink-table-api/
    - https://www.youtube.com/watch?v=bG2U7c5rYBo

- Kafka Event Streaming Applications
    - https://github.com/confluentinc/cp-demo
    - The docker-compose.yml file:
        - https://github.com/confluentinc/cp-demo/blob/7.1.0-post/docker-compose.yml
    - The environment values:
        - https://github.com/confluentinc/cp-demo/blob/7.1.0-post/env_files/config.env
..
