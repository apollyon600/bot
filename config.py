import os

if os.environ.get('DISCORD_TOKEN') is None:
    import dotenv

    dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('API_KEY')
SCIP_TIMELIMIT = os.getenv('SCIP_TIMELIMIT', 4)
DATABASE_URI = os.getenv('DATABASE_URI')
MAINTAINER_IDS = os.getenv('MAINTAINER_IDS')

COG_EXTENSIONS = [
    # Event/Error handler
    'cogs.event_handler',
    'cogs.error_handler',
    # Staff commands
    'cogs.staff',
    # Bot commands
    'cogs.meta',
    # Damage commands
    'cogs.damage_calculator',
    'cogs.optimize_gear',
    'cogs.view_missing',
    # Auction commands
    'cogs.auction_price',
    # Spy commands
    'cogs.view_guild',
    'cogs.view_player',
    # Skyblock general
    'cogs.verify_system',
    'cogs.reputation_system',
    'cogs.skyblock_events',
]

BOT_PREFIXES = [
    'Exp' + ' ',
    'exp' + ' ',
]
