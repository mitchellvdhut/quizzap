# Quizzap

Created and maintained by [Mitchell](https://github.com/mitchellvdhut) and [Tijmen](https://github.com/troshujin).

## About

This app is intended to be a kahoot clone, just for fun. (And because we don't wish to pay)

## Features

 - Manage your own quizzes.
 - Start quiz sessions.
 - Have people join quiz sessions.
 - Yeah, it's just kahoot.
 - Containerized with docker.
 - Authentication.
 - Mobile support.
 - An "Anarchy" mode if you really don't like authentication :)

## Run the app

After cloning the project in your preferred way.

Currently, frontend is not included in the docker.

### Run the backend

To run locally on https, assuming you have GIT installed, use this command in a bash terminal in the root folder:

```bash
"C:\Program Files\Git\usr\bin\openssl.exe" req -x509 -newkey rsa:4096 -keyout nginx/certs/nginx.key -out nginx/certs/nginx.crt -days 365 -nodes
```

Then simply run

```cmd
docker compose up --build
```

### Run the frontend

Currently the frontend is not being run by docker, sorry.

Use these commands to boot up the frontend, assuming you have node installed.

```cmd
cd frontend

npm i

npm run 
```

### Usage

For the backend documentation, head to https://localhost/api/latest/docs.

For the quiz session testing environemnt, head to https://localhost/.

For the frontend, head to http://localhost:5173/.

For phpMyAdmin, head to http://localhost:8080/

## Technologies

### Backend

#### WebAPI

- Python
- FastAPI
- Migrations
- WebSockets
- Custom Websocket Manager
- nginx
- https
- Docker

#### Database

- MySQL
- phpMyAdmin

### Frontend

@mitchell help me out here

- NodeJS
- Vite
- Vue3
- Scss
