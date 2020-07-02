import os
from sbs import Bot

if not os.environ.get('DISCORD_TOKEN'):
    import dotenv
    dotenv.load_dotenv()

client = Bot()
client.run(os.getenv('DISCORD_TOKEN'))
