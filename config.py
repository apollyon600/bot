import os

if os.environ.get('API_KEY') is None:
    import dotenv

    dotenv.load_dotenv()

API_KEYS = os.getenv('API_KEY')
SCIP_TIMELIMIT = os.getenv('SCIP_TIMELIMIT', 4)

COG_EXTENSIONS = [
    # Event/Error handler
    'cogs.event_handler',
    'cogs.error_handler',
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
    'Exp' + ' ',
    'exp' + ' ',
]

# to use high level commands
OWNER_IDS = [
    148460858438057985,  # yuerino
]

# to get error DM from bot
DEV_IDS = [
    148460858438057985,  # yuerino
]

# to bypass cooldown
ADMIN_IDS = [
    148460858438057985,  # yuerino
]
