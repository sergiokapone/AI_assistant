# LLM AI Assistant 📝

The goal of the project is to create a web service that uses the LLM with learning opportunities based on PDF documents uploaded by the user. The application allows you to analyze uploaded PDF documents and answer questions related to the text of the document in a chat mode.


## Setup

1. Clone this repository `git clone https://github.com/sergiokapone/AI_assistant.git`
2. Move to the directory `cd AI_assistant`
3. Create a `.env` (next to `README.md` and `docker-compose.yaml`) a
4. Build docker images `docker compose build`
5. Create docker containers `docker compose up -d`
6. Go to [http://localhost:8000/docs](http://localhost:8000/docs) to see if the FastAPI server is running.
7. Go to [http://localhost:8001](http://localhost:8001/) to interact with the application through the client.