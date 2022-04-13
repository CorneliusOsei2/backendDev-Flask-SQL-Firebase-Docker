Name: CORNELIUS BOATENG
NetID: cob32

Challenges Attempted (Tier I/II/III):
Working Endpoint: GET /api/courses/
Your Docker Hub Repository Link: https://hub.docker.com/repository/docker/cornelius2/cmsx

Questions:
Explain the concept of containerization in your own words.
---
Compressing the source code and other dependencies into a production environment like Docker
and setting the production environment up for running and deployment. 
---

What is the difference between a Docker image and a Docker container?
---
Docker container is a live instance of a Docker image which is a template of 
the actual application and contains the code, libraries and other dependencies
of the application.
---

What is the command to list all Docker images?
---
docker images
---

What is the command to list all Docker containers?
---
docker ps
---

What is a Docker tag and what is it used for?
---
Tags are customizable identifiers of images. They make it easier to identify and
reference images corresponding to specific applications.
---

What is Docker Hub and what is it used for?
---
An online platform for keeping Docker images and sharing them with others. Also supports
other requests as pull.
---

What is Docker compose used for?
---
To manage an application with multiple containers.
---

What is the difference between the RUN and CMD commands?
---
RUN executes shell commands: what comes after the run is a command as typed in the terminal.
CMD runs the server when a container is created from the image.
---