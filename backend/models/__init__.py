import os

from dotenv import load_dotenv
load_dotenv()

if os.environ.get("DB_TYPE") == "mongodb":
    print("Using MongoDB")
    from .mongodb.user import User
    from .mongodb.role import Role
elif os.environ.get("DB_TYPE") == "sqlalchemy":
    print("Using SQLAlchemy")
    from .sqlalchemy.user import User
    from .sqlalchemy.role import Role
else:
    raise Exception("DB_TYPE not set in configuration.")

# from .sqlalchemy.token import TokenBlocklist
