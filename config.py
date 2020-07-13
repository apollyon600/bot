import os

if os.environ.get('API_KEY') is None:
    import dotenv

    dotenv.load_dotenv()

keys = os.getenv('API_KEY')

extensions = [
    'cogs.missing',
    'cogs.meta'
]

prefix = 'sbs' + ' '

admin_ids = [
    148460858438057985
]
