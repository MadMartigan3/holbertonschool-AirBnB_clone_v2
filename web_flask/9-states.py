#!/usr/bin/python3
"""Start a Flask web application"""

from flask import Flask
from flask import render_template
from models import storage
from operator import attrgetter

if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/states', strict_slashes=False)
    def states_id(id):
        """Display a HTML page with states id"""
        for state in storage.all("State").values():
            if state.id == id:
                return render_template('9-states.html', states=state)
            return render_template('9-states.html', states=None, mode="none")

    @app.route('/cities_by_states', strict_slashes=False)
    def cities_by_states():
        """Display a HTML page with a list of all cities by states."""
        states = storage.all("State")
        list = states.values()
        states_list = sorted(list, key=attrgetter('name'))
        return render_template('8-cities_by_states.html',
                               states_list=states_list)

    @app.route('/states_list', strict_slashes=False)
    def states_list():
        """Display a HTML page with a list of all states."""
        states = storage.all("State")
        list = states.values()
        states_list = sorted(list, key=attrgetter('name'))
        return render_template('7-states_list.html', states_list=states_list)

    @app.teardown_appcontext
    def teardown_db(self):
        """Remove SqlAlchemy Session."""
        storage.close()

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
