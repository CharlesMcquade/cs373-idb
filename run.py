#!py3env/bin/python3
from app import app
#disable debug for production!!
app.run(host='0.0.0.0', port='8000')
