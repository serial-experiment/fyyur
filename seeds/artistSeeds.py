from flask_seeder import Seeder
from models import Artist

## mock data taken from app.py
data = [{
    "id": 4,
    "name": "Guns N Petals",
    "genres": ['Rock n Roll'],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
}, {
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ['Jazz'],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "website": None,
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "seeking_description": None,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
}, {
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ['Jazz', 'Classical'],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "website": None,
    "facebook_link": None,
    "seeking_venue": False,
    "seeking_description": None,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
}
]

class ArtistSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1
    def run(self):
        for artist in data:
            artist = Artist(
                id=artist["id"],
                name=artist["name"],
                genres=artist["genres"],
                city=artist["city"],
                state=artist["state"],
                phone=artist["phone"],
                website=artist["website"],
                facebook_link=artist["facebook_link"],
                seeking_venue=artist["seeking_venue"],
                seeking_description=artist["seeking_description"],
                image_link=artist["image_link"]
            )
            self.db.session.add(artist)