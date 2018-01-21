from pathlib import Path

root_dir = Path('.').parent
SECRET = Path(root_dir, 'client_secret.json')

SCOPE = ['https://spreadsheets.google.com/feeds']
