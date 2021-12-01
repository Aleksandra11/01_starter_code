from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, AnyOf, URL
from enum import Enum, unique, auto

class Genres(Enum):                                                                                         #Declare an enum class Genres with names and corresponding values of the class members
    Alternative = auto()
    Blues = auto()
    Classical = auto()
    Country = auto()
    Electronic = auto()
    Folk = auto()
    Funk = auto()
    Hip_Hop = auto()
    Heavy_Metal = auto()
    Instrumental = auto()
    Jazz = auto()
    Musical_Theatre = auto()
    Pop = auto()
    Punk = auto()
    R_n_B = auto()
    Reggae = auto()
    Rock_n_Roll = auto()
    Soul = auto()
    Other = auto()

    @classmethod                                                                                                #Define a function genre_names as a method of the class Genres
    def genre_names(cls):
        choices = [(genre.name) for genre in Genres]                         #Restrict valid choices to the list of name-value pairs in Genres
        return choices

class States(Enum):                                                                                         #Declare an enum class Genres with names and corresponding values of the class members
    AL = auto()
    AK = auto()
    AZ = auto()
    AR = auto()
    CA = auto()
    CO = auto()
    CT = auto()
    DE = auto()
    DC = auto()
    FL = auto()
    GA = auto()
    HI = auto()
    ID = auto()
    IL = auto()
    IN = auto()
    IA = auto()
    KS = auto()
    KY = auto()
    LA = auto()
    ME = auto()
    MT = auto()
    NE = auto()
    NV = auto()
    NH = auto()
    NJ = auto()
    NM = auto()
    NY = auto()
    NC = auto()
    ND = auto()
    OH = auto()
    OK = auto()
    OR = auto()
    MD = auto()
    MA = auto()
    MI = auto()
    MN = auto()
    MS = auto()
    MO = auto()
    PA = auto()
    RI = auto()
    SC = auto()
    SD = auto()
    TN = auto()
    TX = auto()
    UT = auto()
    VT = auto()
    VA = auto()
    WA = auto()
    WV = auto()
    WI = auto()
    WY = auto()

    @classmethod                                                                                                #Define a function genre_names as a method of the class Genres
    def state_abbr(cls):
        choices = [(state.name) for state in States]                         #Restrict valid choices to the list of name-value pairs in Genres
        return choices

class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=States.state_abbr()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=Genres.genre_names()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_description = StringField(
        'seeking_description'
    )
    seeking_talent = BooleanField( 'seeking_talent' )

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=States.state_abbr()
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genres.genre_names()
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
     )

    website = StringField(
        'website', validators=[URL()]
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
        'seeking_description'
     )

