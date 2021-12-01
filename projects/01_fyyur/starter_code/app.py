#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from models import *
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFError, CSRFProtect
from forms import *
import sys
from operator import attrgetter

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
  allvenues = Venue.query.order_by('id').all()
  allartists = Artist.query.order_by('id').all()
  #Sort Artists and Venues by recently created, limit to 5 listed items.
  venues = sorted(allvenues, key=lambda e:e.id, reverse=True)
  venues = venues[:5]
  artists = sorted(allartists, key=attrgetter('id'), reverse=True)
  artists = artists[:5]

  return render_template('pages/home.html', artists=artists, venues=venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  locations = set()
  venues = Venue.query.all()
  for venue in venues:
    locations.add((venue.city, venue.state))
  
  for location in locations:
    data.append({ "city": location[0], "state": location[1], "venues": []})
  
  for venue in venues:
    num_upcoming_shows = 0
    shows = Show.query.filter_by(venue_id=venue.id).all()
    now = datetime.now()
    for show in shows:
      if show.start_time > now:
        num_upcoming_shows += 1
    for i in data:
      if venue.city == i['city'] and venue.state == i['state']:
        i['venues'].append({
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": num_upcoming_shows
        })

  return render_template('pages/venues.html', areas=data, venues=venues)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = request.form.get('search_term', '')

  # case insensitive search
  results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))

  response={
    "count": results.count(),
    "data": results
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id=venue_id).all()
  current_time = datetime.now()
  upcoming_shows = []
  past_shows = []
  
  for show in shows:
    showdata = {"artist_id": show.artist.id, "artist_name": show.artist.name, "artist_image_link": show.artist.image_link, "start_time": format_datetime(str(show.start_time))}
    if show.start_time < current_time:
      past_shows.append(showdata)
    else:
      upcoming_shows.append(showdata)
  data = venue.__dict__
  data['past_shows'] = past_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows'] = upcoming_shows
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm(seeking_talent=True)
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm()
  error = False
  body = {}
  try:
    venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data, address=form.address.data,
      phone=form.phone.data, image_link=form.image_link.data, 
      facebook_link=form.facebook_link.data, genres=form.genres.data, seeking_description=form.seeking_description.data,
      website=form.website.data, seeking_talent=form.seeking_talent.data)
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue "' + request.form['name'] + '" could not be listed.')
    return render_template('forms/new_venue.html', form=form)
  else:
  # on successful db insert, flash success
    flash('Venue "' + request.form['name'] + '" was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    #return render_template('pages/home.html')
    return redirect(url_for('index'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    ven = Venue.query.filter_by(id=venue_id).one()
    db.session.delete(ven)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred.')
  else:
    flash('Venue was deleted!')
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artists = Artist.query.order_by('id').all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  # case insensitive search
  results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  response={
    "count": results.count(),
    "data": results
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist = Artist.query.get(artist_id)
  shows = Show.query.filter_by(artist_id=artist_id).all()
  current_time = datetime.now()
  upcoming_shows = []
  past_shows = []
  
  for show in shows:
    showdata = {"venue_id": show.venue.id, "venue_name": show.venue.name, "venue_image_link": show.venue.image_link, "start_time": format_datetime(str(show.start_time))}
    if show.start_time < current_time:
      past_shows.append(showdata)
    else:
      upcoming_shows.append(showdata)
  data = artist.__dict__
  data['past_shows'] = past_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows'] = upcoming_shows
  data['upcoming_shows_count'] = len(upcoming_shows)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>
  form = ArtistForm()

  artist = db.session.query(Artist).filter_by(id=artist_id).one()
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.facebook_link.data = artist.facebook_link
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.website.data = artist.website
  form.image_link.data = artist.image_link
  form.seeking_description.data = artist.seeking_description
  form.seeking_venue.data = artist.seeking_venue
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  editedItem = db.session.query(Artist).filter_by(id=artist_id).one()
  form = ArtistForm()
  error = False
  try:
    editedItem.name = form.name.data
    editedItem.city = form.city.data
    editedItem.state = form.state.data
    editedItem.phone = form.phone.data
    editedItem.genres = form.genres.data
    editedItem.website = form.website.data
    editedItem.image_link = form.image_link.data
    editedItem.facebook_link = form.facebook_link.data
    editedItem.seeking_venue = form.seeking_venue.data
    editedItem.seeking_description = form.seeking_description.data
    db.session.add(editedItem)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred.')
    return render_template('forms/edit_artist.html', form=form)
  else:
    # on successful db insert, flash success
    flash('Artist "' + request.form['name'] + '" was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>
  form = VenueForm()
  venue = db.session.query(Venue).filter_by(id=venue_id).one()
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.facebook_link.data = venue.facebook_link
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.website.data = venue.website
  form.image_link.data = venue.image_link
  form.seeking_description.data = venue.seeking_description
  form.seeking_talent.data = venue.seeking_talent
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  editedItem = db.session.query(Venue).filter_by(id=venue_id).one()
  form = VenueForm()
  error = False
  try:
    editedItem.name = form.name.data
    editedItem.city = form.city.data
    editedItem.state = form.state.data
    editedItem.address = form.address.data
    editedItem.phone = form.phone.data
    editedItem.genres = form.genres.data
    editedItem.website = form.website.data
    editedItem.image_link = form.image_link.data
    editedItem.facebook_link = form.facebook_link.data
    editedItem.seeking_talent = form.seeking_talent.data
    editedItem.seeking_description = form.seeking_description.data
    db.session.add(editedItem)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred.')
    return render_template('forms/edit_venue.html', form=form)
  else:
    # on successful db insert, flash success
    flash('Venue "' + request.form['name'] + '" was successfully updated!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm(seeking_venue=True)
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm()
  error = False
  try:
    artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data, phone=form.phone.data, image_link=form.image_link.data, 
      facebook_link=form.facebook_link.data, genres=form.genres.data, seeking_description=form.seeking_description.data,
      website=form.website.data, seeking_venue=form.seeking_venue.data)
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    return render_template('forms/new_artist.html', form=form)

  else:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = []
  shows = Show.query.order_by('id').all()
  for show in shows:
    data.append({
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm()
  error = False
  try:
    show = Show(artist_id=form.artist_id.data, venue_id=form.venue_id.data, start_time=form.start_time.data)
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    #flash(form.errors)
    flash('An error occurred. Show could not be listed.')
    return render_template('forms/new_show.html', form=form)

  else:
    # on successful db insert, flash success
    flash('Show was successfully listed!')
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

@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    return render_template('errors/csrf_error.html'), 400

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
