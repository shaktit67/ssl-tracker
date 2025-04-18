Updated Instructions for docker Image generation at developer side
**********************************************************************************************************************************
1)docker login <private_docker_registry>               #login to private docker registry with username and Access token
2)docker build -t <private_docker_registry> .          #Build image from Dockerfile named ssl-tracker with tag latest
3)docker push <private_docker_registry>                #Push the image to gitlab projects docker registry

Updated Instructions for Server side setup
**********************************************************************************************************************************
Once SSL-Tracker Git repo is cloned to server follow the steps mentioned below:

1)cd ssl-tracker                                #Navigate to git repo cloned folder 
2)mv example.env .env                           #creates .env file from template provided
3)nano .env                                     #Edit and add the environment variables required (SMTP_SERVER=, SMTP_PORT=, SENDER_EMAIL=, SENDER_PASSWORD=).
4)docker login    								#login to private docker registry with username and Access token
5)docker compose up -d                          #This will start the docker container in detached mode 