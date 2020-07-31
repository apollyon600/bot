import os

if os.environ.get('DISCORD_TOKEN') is None:
    import dotenv

    dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('API_KEY')
SCIP_TIMELIMIT = os.getenv('SCIP_TIMELIMIT', 4)

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
    'cogs.auction_price'
]

BOT_PREFIXES = [
    'Sbs' + ' ',
    'sbs' + ' ',
]

# to use high level commands
OWNER_IDS = [
    148460858438057985,  # yuerino
    181152738086748160,  # plutie
]

# to get error DM from bot
DEV_IDS = [
    148460858438057985,  # yuerino
    181152738086748160,  # plutie
]

# to bypass cooldown
ADMIN_IDS = [
    148460858438057985,  # yuerino
    181152738086748160,  # plutie
    288896160385597440,  # grm
]
