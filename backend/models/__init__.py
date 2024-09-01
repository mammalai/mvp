import os

from dotenv import load_dotenv
load_dotenv()

if os.environ.get("DB_TYPE") == "mongodb":
    print("Using MongoDB")
    from .mongodb.user import User
else:
    print("Using SQLAlchemy")
    from .sqlalchemy.user import User