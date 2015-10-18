#!py3env/bin/python3
from app import app
#disable debug for production!!
app.run(debug=True)
