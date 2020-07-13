import os

if os.environ.get('API_KEY') is None:
    import dotenv

    dotenv.load_dotenv()

keys = os.getenv('API_KEY')

extensions = [
    # Bot commands
    'cogs.meta',
    # Combat commands
    'cogs.missing'
]

prefix = 'sbs' + ' '

dev_ids = [
    # yuerino
    148460858438057985
]

admin_ids = [
    # yuerino
    148460858438057985
]
