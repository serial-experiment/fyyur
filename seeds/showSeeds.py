from flask_seeder import Seeder
from models import Show

## mock data taken from app.py
data = [
    {
        "venue_id": 1,
        "artist_id": 4,
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "artist_id": 5,
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "artist_id": 6,
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "artist_id": 6,
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "artist_id": 6,
        "start_time": "2035-04-15T20:00:00.000Z"
    }
]

class ShowSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 5
    def run(self):
        for show in data:
            show = Show(
                venue_id=show["venue_id"],
                artist_id=show["artist_id"],
                start_time=show["start_time"]
            )
            self.db.session.add(show)