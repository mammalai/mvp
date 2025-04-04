# flask-mvp
A flask backend to satisfy an MVP


## Run the backend
### Install the environment
- cd into `./backend` and run `poetry install`
### Copy the .env file
- cd into `./backend` and run `cp .env.github .env` (this will copy the default environment variables for the test environment)
### Run backend development server
- cd into `./backend` and run `uvicorn backend.app:app --host 0.0.0.0 --port 8080`


## Run the frontend
### Install the environment
- cd into `./react-frontend` and run `yarn install`
### Run the front-end development server
- cd into `./react-frontend` and run `yarn start`