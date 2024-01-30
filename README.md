# Cardazim
Cardazim Arazim project.

## Installation
1. Install the requirements using

`pip install -r requirements.txt`

2. Run the mongo image using the following commands

[If your docker service isn't running you'll need to start it first using the following command]

[Assuming you're running systemd as your init system, otherwise, using your init system's commands]

[Of course use sudo as needed]

`systemctl start docker`

`docker pull mongo:latest`

`docker run -d -p 27017:27017 --name mongodb mongo`

3. Start the api using uvicorn, from the root directory of the project:

`uvicorn backend.api.api:app --reload`

4. Start the frontend using streamlit:

`streamlit run gui/home.py`

## Notes
The API docs is available at `http://localhost:8000/docs` once the api is up and running

The frontend is available at `http://localhost:8501` once the frontend is up and running,
it should appear automatically in your browser, but if it doesn't, simply open the url that
appears in your terminal. Or you can just click [here](http://localhost:8501)

## Authors

Me