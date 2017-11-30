#!flask/bin/python
from app import app
app.config['DEBUG'] = True
app.run(debug=False)