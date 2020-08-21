# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install SCIP requirements
RUN apt-get update && apt-get install -y wget libgfortran4
RUN wget https://scip.zib.de/download.php?fname=SCIPOptSuite-7.0.1-Linux.deb -O scip.deb
RUN dpkg -i scip.deb

# Hypixel API key
ENV API_KEY = ""
# Bot Discord token
ENV DISCORD_TOKEN = ""

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "run.py"]
