// src/main/java/com/firexis/KafkaProducerApp.java
package com.firexis;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Collection;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.stream.Collectors;

public class KafkaProducerApp {

    private final Producer<String, String> producer;    // Stores the producer
    final String outTopic;                              // Stores the topic

    // Constructor expects a Producer and String
    public KafkaProducerApp(final Producer<String, String> producer,
                            final String topic) {
        this.producer = producer;
        outTopic = topic;
    }

    // Takes a string, produces it and returns a Future
    public Future<RecordMetadata> produce(final String message) {

        final String[] parts = message.split("-");
        final String key, val;

        if (parts.length > 1) {
            key = parts[0];
            val = parts[1];
        } else {
            key = null;
            val = parts[0];
        }

        // Create a Producer Record from topic, key and val then send it
        final ProducerRecord<String, String> producerRecord = new ProducerRecord<>(outTopic, key, val);
        return producer.send(producerRecord);
    }

    // Presumably code to shutdown gracefully
    public void shutdown() {
        producer.close();
    }

    // Read properties from a file
    public static Properties loadProperties(String fileName) throws IOException {
        final Properties envProps = new Properties();
        final FileInputStream input = new FileInputStream(fileName);
        envProps.load(input);
        input.close();

        return envProps;
    }

    // Given a collection of Future RecordMetadata,
    //   print each committed message's metadata
    public void printMetadata(final Collection<Future<RecordMetadata>> metadata,
                              final String fileName) {
        System.out.println("Offsets and timestamps committed in batch from " + fileName);
        metadata.forEach(m -> {
            try {
                // Calling Future.get() will block until produce request completes
                final RecordMetadata recordMetadata = m.get();
                System.out.println("Record written to offset "
                                   + recordMetadata.offset()
                                   + " timestamp "
                                   + recordMetadata.timestamp());
            } catch (InterruptedException | ExecutionException e) {
                if (e instanceof InterruptedException) {
                    Thread.currentThread().interrupt();
                }
            }
        });
    }

    public static void main(String[] args) throws Exception {
        // Guard: Args must be provided
        if (args.length < 2) {
            throw new IllegalArgumentException(
                "This program takes two arguments:"
                + " the path to an environment configuration file and"
                + " the path to the file with records to send");
        }

        final Properties props = KafkaProducerApp.loadProperties(args[0]);
        final String topic = props.getProperty("output.topic.name");

        // Create a KafkaProducer using a properties loaded from a file
        final Producer<String, String> producer = new KafkaProducer<>(props);

        // Create an app from the KafkaProducer and topic
        final KafkaProducerApp producerApp = new KafkaProducerApp(producer, topic);

        String filePath = args[1];          // The input data file
        try {
            List<String> linesToProduce = Files.readAllLines(Paths.get(filePath));
            List<Future<RecordMetadata>> metadata = linesToProduce.stream()
                .filter(l -> !l.trim().isEmpty())
                .map(producerApp::produce)
                .collect(Collectors.toList());

            // Prints after all the records have been sent
            // This is like mini-batch, not streaming
            producerApp.printMetadata(metadata, filePath);

        } catch (IOException e) {
            System.err.printf("Error reading file %s due to %s %n", filePath, e);

        } finally {
            producerApp.shutdown();
        }
    }
}
