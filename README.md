
# Run service with docker 
1. Clone the Repo and Navigate under root directory

# Env file for local testing
Create `.envs` folder in root directory and configure the environment variable .envs


# Run the following commands to build and up the docker containers in detach mode run only command
1. make build
# Another way to install it locally
```
python -m venv projectenv
source projectenv/bin/activate  
cd JobPortal/
pip install -r requirements/local.txt
python3 manage.py runserver 0.0.0.0
```

# Run fastapi swagger on browser
 - http://0.0.0.0:8000/docs