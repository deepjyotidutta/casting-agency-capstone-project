import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from model.models import setup_db, Actor, MovieCast, Movie,db_drop_create_initialize

bearer_tokens = {
    "EXECUTIVE_PRODUCER": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1fWV9hQURNTTR6c1lsWlRMWEJLRSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ici13Z3Blby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMjZjM2JhYmEwMzAwMDE5Y2UwYjRkIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MzcwNzM3NSwiZXhwIjoxNTkzNzkzNzc1LCJhenAiOiJOSWQxQjdlOEhFMmEyZk1YekI2ZTg5Z0F4VzdIOTlZUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.H-LfYi-ZJZDLB_kddgxSApBJkGiXSNg5UB1TCaTj3k4q29J98oM5I_tZ-z-eu08UHGSjRf2ke64IF0YvchZ4VrW-o8QD17hEocdhDvS2KQU0fIewWJhQS6MacvBgW8Zdf4TPERj7gTuDNnjOADcued95NSDx60WWuO17r9kXAajEezDb-c-00oosA4cGhzCdtI74pSLHqqoerhIuiOrNUHG1ubjUsbMQ3seOlkUQuf8AV16YNMF67Idhp9iuMM2dQE1PzngfR94aqAIIK3RwSmLjt-l0-P0HnBOUK_ZDritmgr271hUHpFayRzAVaaJmJPkOoVb_c5A7TkT__0cC_w"
}
database_path = os.environ.get('DATABASE_URL_TEST')
if not database_path:
    database_name = "casting_agency_test"
    database_path = "postgres://{}/{}".format(
        'postgres:pass@localhost:5432', database_name)

auth_token_producer = os.environ.get('EXECUTIVE_PRODUCER')
if not auth_token_producer:
    producer_auth_header = {
        'Authorization': bearer_tokens['EXECUTIVE_PRODUCER']
    }
print(auth_token_producer)


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        db_drop_create_initialize()
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_post_actor(self):
        """Test POST new actor."""
        json_create_actor = {
            'name': 'TEST ABC',
            'age': 25,
            'gender': 'Female'
        }
        res = self.client().post('/actors', json=json_create_actor,
                                 headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_movie(self):
        """Test POST new actor."""
        json_create_movie = {
            'title': 'Jurassic Park',
            'release_date': '12/12/2020'
        }
        res = self.client().post('/movies', json=json_create_movie,
                                 headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors(self):
        res = self.client().get('/actors', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_401_get_actors_error(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Missing Authorization header.")

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_401_get_movies_error(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Missing Authorization header.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
