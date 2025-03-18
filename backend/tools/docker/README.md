# Commmands to run
- Build the container from root:
  - ```docker build -t flask_backend:latest -f backend/tools/docker/Dockerfile .```
- Run the container locally:
  - ```docker run -p 8000:8080 flask_backend:latest```
  - this will run the container on your host computer on port 8000



# Commands to run on linux/amd64 (e.g. Google Cloud)
- Build the container
  - ```docker buildx build -t flask_backend:latest -f backend/tools/docker/Dockerfile --platform linux/amd64 .```
  -  Running on M1 chips or ARM architecture, docker assumes you want to run this on ARM chips - this command ensures you are building it for the right platform - in this case it will be linux/amd64
 