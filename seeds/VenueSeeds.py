from flask_seeder import Seeder
from models import Venue

## mock data taken from app.py
data = [{
    "id": 1,
    "name": "The Musical Hop",
    "genres": ['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],
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
    "id": 2,
    "name": "Park Square Live Music & Coffee",
    "genres": ['Rock n Roll', 'Jazz', 'Classical', 'Folk'],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "seeking_description": None,
    "image_link": "https://www.parksquarelivemusicandcoffee.com/media/musician.jpg",
}, {
    "id": 3,
    "name": "The Dueling Pianos Bar",
    "genres": ['Classical', 'R&B', 'Hip-Hop'],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "seeking_description": None,
    "image_link": "https://www.theduelingpianos.com/media/musician.jpg",
}, {
    "id": 4,
    "name": "The Blue Note",
    "genres": ['Jazz', 'Blues', 'Classical', 'Folk'],
    "address": "131 W 3rd St",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.bluenote.com",
    "facebook_link": "https://www.facebook.com/bluenote",
    "seeking_talent": False,
    "seeking_description": None,
    "image_link": "https://www.bluenote.com/media/musician.jpg",
}
]

class VenueSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1
    def run(self):
        for venue_data in data:
            venue = Venue(
                id=venue_data["id"],
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