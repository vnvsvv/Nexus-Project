import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.models import db
from src.api.app import app
from src.utils.helpers import Logger

logger = Logger.setup()

def init_db():
    with app.app_context():
        db.create_all()
        logger.info("Database initialized!")

if __name__ == "__main__":
    init_db()
