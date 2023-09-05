from app import *
from models import *
from datetime import datetime
from flask_seeder import Seeder

## mock data taken from app.py
data = [{
    "name": "The Musical Hop",
    "genres": '{"Jazz", "Reggae", "Swing", "Classical", "Folk"}',
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://www.themusicalhop.com/media/musician.jpg",
}, {
    "name": "Park Square Live Music & Coffee",
    "genres": '{"Rock n Roll", "Jazz", "Classical", "Folk"}',
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "seeking_description": None,
    "image_link": "https://www.parksquarelivemusicandcoffee.com/media/musician.jpg",
}]

class VenueSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.db = db
        
    def run(self):
        for venue_data in data:
            venue = Venue(
                name=venue_data["name"],
                genres=venue_data["genres"],
                address=venue_data["address"],
                city=venue_data["city"],
                state=venue_data["state"],
                phone=venue_data["phone"],
                website=venue_data["website"],
                facebook_link=venue_data["facebook_link"],
                seeking_talent=venue_data["seeking_talent"],
                seeking_description=venue_data["seeking_description"],
                image_link=venue_data["image_link"],
            )
            self.db.session.add(venue)
        self.db.session.commit() 

