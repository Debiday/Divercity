"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
import json
import os
import flickrapi

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = os.environ["FLASK_KEY"]
app.jinja_env.undefined = StrictUndefined

# <------------FLICKR API------------>

api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]

flickr = flickrapi.FlickrAPI(api_key, api_secret,format='json')
photos = flickr.photos.search(user_id='73509078@N00', per_page='10')
sets = flickr.photosets.getList(user_id='73509078@N00')

# parsed = json.loads(raw_json.decode('utf-8'))

SIZES = ["url_o", "url_k", "url_h", "url_l", "url_c"]  # in order of preference


# <---------------------------------->

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('test2.html')


@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)


@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
    else:
        crud.create_user(email, password)
        flash('Account created! Please log in.')

    return redirect('/')


@app.route('/users/<user_id>')
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
