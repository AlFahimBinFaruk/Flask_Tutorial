### Basic
* Here i have created a basic CRUD application Flask using
  - SQLAlchemy
  - SQLITE db.
1. to create a db after first time running the server

```bash
from server import server,db
server.app_context().push()
db.create_all()
```

2. genarete req.txt
```bash
pip3 freeze > requirements.txt
```