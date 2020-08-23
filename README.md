# skyblock-simplified
Multi-purpose bot for hypixel skyblock

# REQUIREMENTS

Python 3.8+

MongoDB

SCIP Solver binary with AMPL interface (https://www.scipopt.org/index.php#download) in same folder as bot

# DOCKER DEPLOYMENT
`git clone https://github.com/Skyblock-Simplified/bot`

Edit the Dockerfile and add your API key, Discord token, MongoDB URI to it.

`docker-compose up`

# NORMAL DEPLOYMENT
```git clone https://github.com/Skyblock-Simplified/bot
cd bot
pip install -r requirements.txt
cp .env_default .env
```

Add your API key, Discord token, MongoDB URI to the .env file. 

Your bot should now be able to run. Launch it with `run.bat` or `run.sh`.

# TODO
Add deployment script to setup MongoDB collections/aggeration/validation stuff.