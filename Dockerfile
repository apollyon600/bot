# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Setup user and directories
RUN useradd appuser
ADD . /app/
RUN mkdir /data
RUN mv /app/docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

# SCIP version
ENV SCIP_VERSION 6.0.0

# Install SCIP requirements
RUN apt-get update && apt-get install -y wget python-dev build-essential g++ zlib1g-dev bison flex libgmp-dev libreadline-dev libncurses5-dev
RUN wget https://www.scipopt.org/download/release/scipoptsuite-${SCIP_VERSION}.tgz
RUN tar zxvf scipoptsuite-${SCIP_VERSION}.tgz && \
    rm scipoptsuite-${SCIP_VERSION}.tgz && \
    cd scipoptsuite-${SCIP_VERSION} && \
    make ZIMPL=false && \
    cd scip/interfaces/ampl && \
    ./get.ASL && \
    cd solvers && \
    sh configurehere && \
    make && \
    cd .. && \
    make && \
    cd bin && \
    mv -v scipampl.linux.x86_64.gnu.opt.spx2 scip && \
    mv -v scip /app/

WORKDIR /app

# Install pip requirements
RUN python -m pip install -r requirements.txt

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN chown -R appuser /app && chown -R appuser /data
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["/docker-entrypoint.sh"]

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Hypixel API key
ENV API_KEY key

# Bot Discord token
ENV DISCORD_TOKEN token

# SCIP Timeout
ENV SCIP_TIMEOUT 10