import os

if os.environ.get('API_KEY') is None:
    import dotenv

    dotenv.load_dotenv()

keys = os.getenv('API_KEY')
SCIP_TIMELIMIT = os.getenv('SCIP_TIMELIMIT', 4)

extensions = [
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

prefix = [
    'Exp' + ' ',
    'exp' + ' ',
]

# to use high level commands
owner_ids = [
    148460858438057985,  # yuerino
]

# to get error DM from bot
dev_ids = [
    148460858438057985,  # yuerino
]

# to bypass cooldown
admin_ids = [
    148460858438057985,  # yuerino
]
