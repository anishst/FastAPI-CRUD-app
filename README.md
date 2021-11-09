# FastAPI REST App

## Versions
- **app** folder contains simple FastAPI using sqlite
- **app_mongo** folder contains simple FastAPI using mongodb
- **app_postgress** folder contains simple FastAPI using postgress

## Run Locally - Linux
- create virtual env: ```python3 -m venv venv```
- activate: ```source venv/bin/activate```
- install required dependencies: ```pip install -r requirements.txt```
- run app from command line: ``` uvicorn app.main:app --reload --host=0.0.0.0```

## Run with Docker Compose

simple app:
1. create dockerfile and docker compose
2. build: ```docker-compose build```
3. run container: ```docker-compose up -d```

## Mongo app:
1. run container using specific docker compose file: ```docker-compose -f docker-compose_mongo.yml up```

## REST Endpoint Docs
- [Swagger UI](http://192.168.1.25:8000/docs)
- [Redocs UI](http://192.168.1.25:8000/redoc)

## Test Mongo App using Curl
- launch app: ```uvicorn app_mongo.main:app --reload --host=0.0.0.0```
- get all: ```curl -X GET http://192.168.1.25:8000/blog```
- get by id: ```curl -X GET http://192.168.1.25:8000/blog/1```
- add a new post : ```curl -d '{"id": 2, "title": "Adding with Curl", "author": "Anish Sebastian", "content": "I was added via curl post!", "created_at": "2021-03-01T18:17:45.194020", "published_at": "2021-03-01T18:17:58.887Z", "published": true}' -H "Content-Type: application/json" -X POST http://192.168.1.25:8000/blog```
- update post : ```curl -d '{"id": 1, "title": "Adding with Curl updated", "author": "Anish Sebastian", "content": "I was added via curl post!", "created_at": "2021-03-01T18:17:45.194020", "published_at": "2021-03-01T18:17:58.887Z", "published": true}' -H "Content-Type: application/json" -X PUT http://192.168.1.25:8000/blog```
- delete ```curl -X DELETE http://192.168.1.25:8000/blog/1```


## Postgress app:
1. run container using specific docker compose file: ```docker-compose -f docker-compose_mongo.yml up```
- [Video](https://www.youtube.com/watch?v=ToXOb-lpipM&t=17011s)
    - [Git Repo](https://github.com/Sanjeev-Thiyagarajan/fastapi-course)
    
## Resources
- FastAPI Main Docs:
    - [FastAPI Github](https://github.com/tiangolo/fastapi)
    - [SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [uvicorn](https://www.uvicorn.org/)
- [MongoDB Python Drivers](https://docs.mongodb.com/drivers/python/)
- [Motor: Asynchronous Python driver for MongoDB](https://motor.readthedocs.io/en/stable/)
  - https://motor.readthedocs.io/en/stable/tutorial-asyncio.html#creating-a-client
- Articles
  - [Python REST APIs with FastAPI, CRUD application](https://dev.to/xarala221/python-rest-apis-with-fastapi-crud-application-9kc)
  - [Getting Started with MongoDB and FastAPI](https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/)
  - [Dockerizing FastAPI with Postgres, Uvicorn, and Traefik](https://testdriven.io/blog/fastapi-docker-traefik/)