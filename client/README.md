# Client

This is a client-side.

This is a server-side part that uses FastAPI.

To start the server locally, go to the `/client/` folder and run the command 

```shell
poetry run streamlit run --server.port 8001 --server.enableCORS false src/About.py
```

Then go to [http://localhost:8000/docs](http://localhost:8001) to see if the FastAPI server is running.
