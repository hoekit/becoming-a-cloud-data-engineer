FROM openjdk:8-jre-alpine
WORKDIR /
COPY build/libs/kafka-producer-application-standalone-0.0.1.jar /app.jar
COPY configuration/prod.properties /config.properties
COPY input.txt /input.txt
CMD [ "java", "-jar", "/app.jar", "/config.properties", "/input.txt"]
