#!/usr/bin/python3
"""Start a Flask web application"""

from flask import Flask
from flask import render_template
from models import storage
from operator import attrgetter

if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/states_list', strict_slashes=False)
    def states_list():
        """Display a HTML page with a list of all states."""
        states = storage.all("State")
        list = states.values()
        states_list = sorted(list, key=attrgetter('name'))
        return render_template('7-states_list.html', states_list=states_list)

    @app.teardown_appcontext
    def teardown_db(exception):
        """Remove SqlAlchemy Session."""
        storage.close()

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
