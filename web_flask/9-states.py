#!/usr/bin/python3
"""Start a Flask web application"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State

if __name__ == "__main__":
    app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """Displays an HTML page with a list of all State objects."""
    states = storage.all(State)
    return render_template("9-states.html", states=states, mode="all")


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Displays an HTML page with a list of all State id instances."""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template("9-states.html", states=state, mode="city")
    return render_template("9-states.html", states=state, mode="none")


@app.teardown_appcontext
def teardown(self):
    """Remove the current SQLAlchemy Session."""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
