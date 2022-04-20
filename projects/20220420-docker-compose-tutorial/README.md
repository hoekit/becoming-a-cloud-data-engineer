# Docker Compose Tutorial


----
### Docker Compose Tutorial
__ Folders and files structure

- $PROJECT
    - product/
        - api.py
        - requirements.txt
        - Dockerfile
    - website/
    - docker-compose.yaml
..
__ Docker build/run just the product/api.py service

Build a docker image:

    docker build -t product-api:0.1 .

Run image and port map:

    docker run -p 5001:80 --name product-service product-api:0.1
..
__ Clean Up

Remove docker containers:

    docker rm product-service

Remove docker image:

    docker rmi product-api:0.1
..
__ Docker Compose

Run the docker compose file:

    docker-compose up


Start docker-compose in background:

    docker-compose up -d


Stop docker-compose services in the background:

    docker-compose stop
..
__ Clean Up

Remove containers:

    docker ps -a
    docker rm 202204020-docker-compose-tutorial_website_1
    docker rm 202204020-docker-compose-tutorial_product-service_1

Remove images:

    docker images
    docker rmi $(docker images -aq)     # Removes all images
..

__ Docker Compose Notes

- Either filename works:
    - docker-compose.yaml
    - docker-compose.yml

- Creates a private network for all containers
    - All containers can listen to port 80
        - Each container is differentiated by the service name

- Mounting volumes in docker-compose
    - makes the container see live changes in the mounted directory

- The `depends_on` property of `services` is pretty neat
..
__ Python Notes

- Include a `requirements.txt` file
    - Used by python-onbuild docker images to automatically install
      requirements from the `requirements.txt` file
    - python-onbuild expects the code in `/usr/src/app`
..

__ Links

- Docker Compose in 12 Minutes
    - https://www.youtube.com/watch?v=Qw9zlE3t8Ko

- Learn Docker in 12 Minutes, 2016
    - https://www.youtube.com/watch?v=YFl2mCHdv24
..

