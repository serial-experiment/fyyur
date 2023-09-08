#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *
from flask_seeder import FlaskSeeder
#from seeders import VenueSeeder

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# Initialize seeder
seeder = FlaskSeeder()
seeder.init_app(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  try:
    # get all venues
    venues = Venue.query.all()
    data = []
    # get all areas
    areas = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()
    # for each area get venues
    for a in areas:
      venues = Venue.query.filter(Venue.city == a.city, Venue.state == a.state).all()
      venues_data = []
      # for each venue get upcoming shows
      for v in venues:
        upcoming_shows = Show.query.filter(Show.venue_id == v.id, Show.start_time > datetime.now()).all()
        venues_data.append({
          "id": v.id,
          "name": v.name,
          "num_upcoming_shows": len(upcoming_shows)
        })
      data.append({
        "city": a.city,
        "state": a.state,
        "venues": venues_data
      })
  except:
    print(sys.exc_info())
    flash("An error occurred. Venues could not be listed.")
  finally:
    db.session.close()

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  try:
    # get search term
    search_term = request.form.get('search_term', '')
    # search for venues with search term
    venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
    data = []
    # for each venue get upcoming shows
    for v in venues:
      upcoming_shows = Show.query.filter(Show.venue_id == v.id, Show.start_time > datetime.now()).all()
      data.append({
        "id": v.id,
        "name": v.name,
        "num_upcoming_shows": len(upcoming_shows)
      })
    response = {
      "count": len(venues),
      "data": data
    }
  except:
    print(sys.exc_info())
    flash("An error occurred. Venues could not be listed.")
  finally:
    db.session.close()

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  # return data from sql query for venue with id = venue_id
  try:
    v = Venue.query.get(venue_id)
    data = {
      "id": v.id,
      "name": v.name,
      "genres": v.genres,
      "address": v.address,
      "city": v.city,
      "state": v.state,
      "phone": v.phone,
      "website": v.website,
      "facebook_link": v.facebook_link,
      "seeking_talent": v.seeking_talent,
      "seeking_description": v.seeking_description,
      "image_link": v.image_link,
    }

    # get past shows
    ps = Show.query.filter(Show.venue_id == venue_id, Show.start_time < datetime.now()).all()
    past_shows = []
    for p in ps:
      past_shows.append({
        "artist_id": p.artist_id,
        "artist_name": p.artist.name,
        "artist_image_link": p.artist.image_link,
        "start_time": p.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })
    data["past_shows"] = past_shows

    # get upcoming shows
    us = Show.query.filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).all()
    upcoming_shows = []
    for u in us:
      upcoming_shows.append({
        "artist_id": u.artist_id,
        "artist_name": u.artist.name,
        "artist_image_link": u.artist.image_link,
        "start_time": u.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })
    data["upcoming_shows"] = upcoming_shows

    # get past shows count
    data["past_shows_count"] = len(past_shows)

    # get upcoming shows count
    data["upcoming_shows_count"] = len(upcoming_shows)
    
  except:
    print(sys.exc_info())
    flash("An error occurred. Venue could not be listed.")
  finally:  
    db.session.close()

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    # get form data
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    image_link = request.form.get('image_link')
    website = request.form.get('website')
    seeking_talent = True if request.form.get('seeking_talent') == 'y' else False
    seeking_description = request.form.get('seeking_description')

    # create venue object
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
    # add venue to db
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    print(sys.exc_info())
    flash("An error occurred. Could not add Venue.")
  finally:
      db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    # get venue by id
    venue = Venue.query.get(venue_id)
    # delete venue
    db.session.delete(venue)
    db.session.commit()
    # on successful db delete, flash success
    flash('Venue ' + venue.name + ' was successfully deleted!')
  except:
    print(sys.exc_info())
    flash("An error occurred. Could not delete Venue.")
  finally:
    db.session.close()

  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  try:
    # get all artists
    artists = Artist.query.all()
    data = []
    # for each artist get upcoming shows
    for a in artists:
      upcoming_shows = Show.query.filter(Show.artist_id == a.id, Show.start_time > datetime.now()).all()
      data.append({
        "id": a.id,
        "name": a.name,
        "num_upcoming_shows": len(upcoming_shows)
      })
  except:
    print(sys.exc_info())
    flash("An error occurred. Artists could not be listed.")
  finally:
    db.session.close()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  try:
    # get search term
    search_term = request.form.get('search_term', '')
    # search for artists with search term
    artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
    data = []
    # for each artist get upcoming shows
    for a in artists:
      upcoming_shows = Show.query.filter(Show.artist_id == a.id, Show.start_time > datetime.now()).all()
      data.append({
        "id": a.id,
        "name": a.name,
        "num_upcoming_shows": len(upcoming_shows)
      })
    response = {
      "count": len(artists),
      "data": data
    }
  except:
    print(sys.exc_info())
    flash("An error occurred. Artists could not be listed.")
  finally:
    db.session.close()

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  try:
    # get artist by id
    a = Artist.query.get(artist_id)
    data = {
      "id": a.id,
      "name": a.name,
      "genres": a.genres,
      "city": a.city,
      "state": a.state,
      "phone": a.phone,
      "website": a.website,
      "facebook_link": a.facebook_link,
      "seeking_venue": a.seeking_venue,
      "seeking_description": a.seeking_description,
      "image_link": a.image_link,
    }

    # get past shows
    ps = Show.query.filter(Show.artist_id == artist_id, Show.start_time < datetime.now()).all()
    past_shows = []
    for p in ps:
      past_shows.append({
        "venue_id": p.venue_id,
        "venue_name": p.venue.name,
        "venue_image_link": p.venue.image_link,
        "start_time": p.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })
    data["past_shows"] = past_shows

    # get upcoming shows
    us = Show.query.filter(Show.artist_id == artist_id, Show.start_time > datetime.now()).all()
    upcoming_shows = []
    for u in us:
      upcoming_shows.append({
        "venue_id": u.venue_id,
        "venue_name": u.venue.name,
        "venue_image_link": u.venue.image_link,
        "start_time": u.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })
    data["upcoming_shows"] = upcoming_shows

    # get past shows count
    data["past_shows_count"] = len(past_shows)

    # get upcoming shows count
    data["upcoming_shows_count"] = len(upcoming_shows)
  except:
    print(sys.exc_info())
    flash("An error occurred. Artist could not be listed.")
  finally:
    db.session.close()

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  try:
    # get artist by id
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
  except:
    print(sys.exc_info())
    flash("An error occurred. Artist could not be listed.")
  finally:
    db.session.close()

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    # get artist by id
    artist = Artist.query.get(artist_id)
    # get form data
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form.get('facebook_link')
    artist.image_link = request.form.get('image_link')
    artist.website = request.form.get('website')
    artist.seeking_venue = True if request.form.get('seeking_venue') == 'y' else False
    artist.seeking_description = request.form.get('seeking_description')
    # update artist
    db.session.commit()
    # on successful db update, flash success
    flash('Artist ' + artist.name + ' was successfully updated!')
  except:
    print(sys.exc_info())
    flash("An error occurred. Artist could not be updated.")
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  try:
    # get venue by id
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
  except:
    print(sys.exc_info())
    flash("An error occurred. Venue could not be listed.")
  finally:
    db.session.close()

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  try:
    # get venue by id
    venue = Venue.query.get(venue_id)
    # get form data
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form.get('facebook_link')
    venue.image_link = request.form.get('image_link')
    venue.website = request.form.get('website')
    venue.seeking_talent = True if request.form.get('seeking_talent') == 'y' else False
    venue.seeking_description = request.form.get('seeking_description')
    # update venue
    db.session.commit()
    # on successful db update, flash success
    flash('Venue ' + venue.name + ' was successfully updated!')
  except:
    print(sys.exc_info())
    flash("An error occurred. Venue could not be updated.")
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    # get form data
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    image_link = request.form.get('image_link')
    website = request.form.get('website_link')
    seeking_venue = True if request.form.get('seeking_venue') == 'y' else False
    seeking_description = request.form.get('seeking_description')

    # create artist object
    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
    # add artist to db
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    print(sys.exc_info())
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  try:
    # get all shows
    shows = Show.query.all()
    data = []
    # for each show get venue and artist
    for s in shows:
      venue = Venue.query.get(s.venue_id)
      artist = Artist.query.get(s.artist_id)
      data.append({
        "venue_id": s.venue_id,
        "venue_name": venue.name,
        "artist_id": s.artist_id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": s.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })
  except:
    print(sys.exc_info())
    flash("An error occurred. Shows could not be listed.")
  finally:
    db.session.close()

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    # get form data
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')

    # create show object
    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    # add show to db
    db.session.add(show)
    db.session.commit()
    flash('Added show for Artist: ' + artist_id + ' in Venue: ' + venue_id + ' at ' + start_time)
  except:
    print(sys.exc_info())
    flash('Failed to add show for Artist: ' + artist_id + ' in Venue: ' + venue_id + ' at ' + start_time)
  finally:
    db.session.close()

  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
