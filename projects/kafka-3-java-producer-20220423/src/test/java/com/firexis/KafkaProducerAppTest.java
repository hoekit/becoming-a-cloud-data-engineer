// src/test/java/com/firexis/KafkaProducerAppTest.java`
// - Tests for KafkaProducerApp
// - Use Mock Producer - https://kafka.apache.org/25/javadoc/org/apache/kafka/clients/producer/MockProducer.html
package com.firexis;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;
import java.util.stream.Collectors;
// use org.apache.kafka.clients.producer.KafkaProducer;     // in DEV/PROD
import org.apache.kafka.clients.producer.MockProducer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.streams.KeyValue;
import org.junit.Test;

public class KafkaProducerAppTest {

    private final static String TEST_CONFIG_FILE = "configuration/test.properties";

    @Test
    public void testProduce() throws IOException {
        final StringSerializer stringSerializer = new StringSerializer();
        // A real producer takes in Properties
        //   final Producer<String, String> producer = new KafkaProducer<>(props);
        // A mock producer takes in the serializers
        final MockProducer<String, String> mockProducer = new MockProducer<>(true, stringSerializer, stringSerializer);
        // Reuse the loadProperties method in KafkaProducerApp
        final Properties props = KafkaProducerApp.loadProperties(TEST_CONFIG_FILE);
        final String topic = props.getProperty("output.topic.name");
        // Create the app with a mock producer
        final KafkaProducerApp producerApp = new KafkaProducerApp(mockProducer, topic);
        // Create a list test input strings
        final List<String> records = Arrays.asList("perl-camel","snake-python","coffee-java","C");

        // Produce each record using the mock producer
        records.forEach(producerApp::produce);
        // and produce the actual results
        final List<KeyValue<String, String>> actualList = mockProducer
            .history()                      // List<ProducerRecord<K,V>>

            .stream()                       // Stream<ProducerRecord<K,V>>
                                            //   convert a collection to
                                            //   a sequential stream

            .map(this::toKeyValue)          // Stream<KeyValue<K,V>>
                                            //   method defined below

            .collect(Collectors.toList());  // List<KeyValue<K,v>>
                                            //   accumulate stream
                                            //   elements into a List

        // Declare the expected results
        final List<KeyValue<String, String>> expectedList = Arrays.asList(
            KeyValue.pair("perl","camel"),
            KeyValue.pair("snake","python"),
            KeyValue.pair("coffee","java"),
            KeyValue.pair(null,"C"));

        // Compare actual and expected
        assertThat(actualList, equalTo(expectedList));
        producerApp.shutdown();
    }

    private KeyValue<String, String> toKeyValue(final ProducerRecord<String, String> producerRecord) {
        return KeyValue.pair(producerRecord.key(), producerRecord.value());
    }
}
