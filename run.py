#!venv/bin/python
from app import app
#disable debug for production!!
app.run(host="0.0.0.0:8000")
