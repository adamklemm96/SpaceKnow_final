from pathlib import Path
from datetime import datetime

def create_directory(directory = '.', time=datetime.now()):
    timestamp = time.strftime('%Y_%m_%d')
    path = Path(f'{directory}/output/{timestamp}')
    path.mkdir(parents=True)

    return path