# FastAPI REST App with MongoDB

## Run Locally - Linux
- create virtual env: ```python3 -m venv venv```
- activate: ```source venv/bin/activate```
- install required dependencies: ```pip install -r requirements.txt```
- run app from command line: ``` uvicorn main:app --reload --host=0.0.0.0```

## Test using Curl
- get all: ```curl -X GET http://192.168.1.25:8000/blog```
- get by id: ```curl -X GET http://192.168.1.25:8000/blog/1```
- add a new post : ```curl -d '{"id": 2, "title": "Adding with Curl", "author": "Ousseynou DIOP", "content": "I was added via curl post!", "created_at": "2021-03-01T18:17:45.194020", "published_at": "2021-03-01T18:17:58.887Z", "published": true}' -H "Content-Type: application/json" -X POST http://192.168.1.25:8000/blog```
- update post : ```curl -d '{"id": 1, "title": "Adding with Curl updated", "author": "Ousseynou DIOP", "content": "I was added via curl post!", "created_at": "2021-03-01T18:17:45.194020", "published_at": "2021-03-01T18:17:58.887Z", "published": true}' -H "Content-Type: application/json" -X PUT http://192.168.1.25:8000/blog```
- delete ```curl -X DELETE http://192.168.1.25:8000/blog/1```
## Resources
- FastAPI Main Docs:
    - [FastAPI Github](https://github.com/tiangolo/fastapi)
    - [SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [uvicorn](https://www.uvicorn.org/)
- Articles
  - [Python REST APIs with FastAPI, CRUD application](https://dev.to/xarala221/python-rest-apis-with-fastapi-crud-application-9kc)