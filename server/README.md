# Server

This is a server-side part that uses FastAPI.

To start the server locally, go to the `/server/` folder and run the command

```shell
poetry run uvicorn src.main:app --host 0.0.0.0.0 --port 8000 --reload
```

Then go to [http://localhost:8000/docs](http://localhost:8000/docs) to see if the FastAPI server is running.
