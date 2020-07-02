import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from model.models import setup_db, Actor, MovieCast, Movie, db_drop_create_initialize

''' SETUP AUTH TOKENS '''
bearer_tokens = {
    "EXECUTIVE_PRODUCER": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1fWV9hQURNTTR6c1lsWlRMWEJLRSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ici13Z3Blby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMjZjM2JhYmEwMzAwMDE5Y2UwYjRkIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MzcwNzM3NSwiZXhwIjoxNTkzNzkzNzc1LCJhenAiOiJOSWQxQjdlOEhFMmEyZk1YekI2ZTg5Z0F4VzdIOTlZUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.H-LfYi-ZJZDLB_kddgxSApBJkGiXSNg5UB1TCaTj3k4q29J98oM5I_tZ-z-eu08UHGSjRf2ke64IF0YvchZ4VrW-o8QD17hEocdhDvS2KQU0fIewWJhQS6MacvBgW8Zdf4TPERj7gTuDNnjOADcued95NSDx60WWuO17r9kXAajEezDb-c-00oosA4cGhzCdtI74pSLHqqoerhIuiOrNUHG1ubjUsbMQ3seOlkUQuf8AV16YNMF67Idhp9iuMM2dQE1PzngfR94aqAIIK3RwSmLjt-l0-P0HnBOUK_ZDritmgr271hUHpFayRzAVaaJmJPkOoVb_c5A7TkT__0cC_w",
    "CASTING_ASSISTANT": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1fWV9hQURNTTR6c1lsWlRMWEJLRSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ici13Z3Blby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMjZjZDk3Nzk3YzEwMDEzNzAxYjNjIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MzcwNTk1NSwiZXhwIjoxNTkzNzkyMzU1LCJhenAiOiJOSWQxQjdlOEhFMmEyZk1YekI2ZTg5Z0F4VzdIOTlZUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIl19.mpCE1lTkYiM3bmKM3kL44_B1C-Pz3SbKaDiseuu_xskyFS0lGnC5GfFTApTKUK8cUavmhPpEjZbGDvMGZGBQf6MEdegoT6-FVrhL8Z2PcLlva7FTYTm_NIxAkoifndiPwZ_FYBWJO4Cow-_1NlPtdvHGCQUb-lkoJxdGycxHVP6moXt2VX18KtLuSMJ0NQ-_oYm88fWJFgkaJe13ybLMlwdH56Cs9Utx-agoZ6Hnk3Lv_RZwURsqJtzkpJYc3h-aiWbrJylip9sISE-BLUIp5EnUR55qpAehMqGmuCrXyZjVhH8v94f06DkE3sMotwwLO5krhXPwxBmMvc13BUywZA",
    "CASTING_DIRECTOR": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1fWV9hQURNTTR6c1lsWlRMWEJLRSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ici13Z3Blby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTI3MjkzNDE2MDUwMDE5ZGQ1MWY1IiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MzcxMTk1NCwiZXhwIjoxNTkzNzk4MzU0LCJhenAiOiJOSWQxQjdlOEhFMmEyZk1YekI2ZTg5Z0F4VzdIOTlZUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.FQSNBXYIq9iAnbq3etKHBWMTLz0Kq5qTjieAKKCa0HDvUT14OGeet9b6Js0kSpBYwNjPxhSAcH_JLEkL-EvScZjHgoXQlAM1r73l-CSphNsdyks0tQa7i718lFwXd6pAGo4BHJv2IMump1R2FS6LOX0802tVvCZt7-pf9QfX418UMkVjGzKaH-vYjuWyD8q80-arfygrcMWTAiL0HhywlA7L5ukCKw40cXh30QZNHG58p6BcjUGuRSAfhP5RubZIviNZaIrUMHyHhJ5NVgb-SdqbhBtRQ0IpnFb066dsJ5xQfazkBat-IHHXReh5tfcDdY-47Brc0btTjcBOf6k5Mg"
}
auth_token_producer = os.environ.get('EXECUTIVE_PRODUCER')
if not auth_token_producer:
    producer_auth_header = {
        'Authorization': bearer_tokens['EXECUTIVE_PRODUCER']
    }
else:
    producer_auth_header = {
        'Authorization': os.environ.get('EXECUTIVE_PRODUCER')
    }

auth_token_director = os.environ.get('CASTING_DIRECTOR')
if not auth_token_director:
    director_auth_header = {
        'Authorization': bearer_tokens['CASTING_DIRECTOR']
    }
else:
    director_auth_header = {
        'Authorization': os.environ.get('CASTING_DIRECTOR')
    }

auth_token_assistant = os.environ.get('CASTING_ASSISTANT')
if not auth_token_assistant:
    assistant_auth_header = {
        'Authorization': bearer_tokens['CASTING_ASSISTANT']
    }
else:
    assistant_auth_header = {
        'Authorization': os.environ.get('CASTING_ASSISTANT')
    }

json_create_actor = {
    'name': 'TEST ABC',
    'age': 25,
    'gender': 'Female'
}
json_create_movie = {
    'title': 'Jurassic Park',
    'release_date': '12/12/2020'
}
''' SETUP TEST DB CONNECTION STRING '''
database_path = os.environ.get('DATABASE_URL_TEST')
if not database_path:
    database_name = "casting_agency_test"
    database_path = "postgres://{}/{}".format(
        'postgres:pass@localhost:5432', database_name)


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

    #----------------------------------------------------------------------------#
    # Tests for /actors POST WITH AUTH
    #----------------------------------------------------------------------------#

    def test_post_actor(self):
        """Test POST new actor."""
        res = self.client().post('/actors', json=json_create_actor,
                                 headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    #----------------------------------------------------------------------------#
    # Tests for /actors POST WITH NO AUTH FOR 401
    #----------------------------------------------------------------------------#

    def test_401_post_actor(self):
        """Test POST new actor."""
        res = self.client().post('/actors', json=json_create_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    #----------------------------------------------------------------------------#
    # Tests for /actors POST WITH BAD INPUT FOR 422
    #----------------------------------------------------------------------------#

    def test_422_post_actor(self):
        """Test POST new actor."""
        json_create_actor_bad = {
            'name': 'TEST ABC',
            'age': 25
        }
        res = self.client().post('/actors', json=json_create_actor_bad,
                                 headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    #----------------------------------------------------------------------------#
    # Tests for /actors GET WITH AUTH
    #----------------------------------------------------------------------------#

    def test_get_actors(self):
        res = self.client().get('/actors', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
    #----------------------------------------------------------------------------#
    # Tests for /actors GET NO AUTH HEADERS FOR 401
    #----------------------------------------------------------------------------#

    def test_401_get_actors_error(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Missing Authorization header.")
    #----------------------------------------------------------------------------#
    # Tests for /actors GET WITH AUTH HEADERS FOR 404
    #----------------------------------------------------------------------------#

    def test_404_get_actors_pagination_error(self):
        res = self.client().get('/actors?page=123', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")
    #----------------------------------------------------------------------------#
    # Tests for /actors PATCH WITH AUTH HEADERS 
    #----------------------------------------------------------------------------#

    def test_patch_actors(self):
        json_create_actor = {
            'name': 'TEST ABC',
            'age': 30,
            'gender': 'Male'
        }
        res = self.client().patch('/actors/1',json=json_create_actor, headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    #----------------------------------------------------------------------------#
    # Tests for /actors PATCH WITH AUTH HEADERS FOR 404
    #----------------------------------------------------------------------------#

    def test_404_patch_actors_error(self):
        json_create_actor = {
            'name': 'TEST ABC',
            'age': 30,
            'gender': 'Male'
        }
        res = self.client().patch('/actors/123',json=json_create_actor, headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    #----------------------------------------------------------------------------#
    # Tests for /actors DELETE WITH AUTH HEADERS 
    #----------------------------------------------------------------------------#

    def test_delete_actors(self):
        res = self.client().delete('/actors/1',headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    #----------------------------------------------------------------------------#
    # Tests for /actors DELETE WITH AUTH HEADERS FOR 404
    #----------------------------------------------------------------------------#

    def test_404_delete_actors_error(self):
        res = self.client().delete('/actors/123', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    #----------------------------------------------------------------------------#
    # Tests for /movies POST WITH AUTH
    #----------------------------------------------------------------------------#

    def test_post_movie(self):
        """Test POST new actor."""
        res = self.client().post('/movies', json=json_create_movie,
                                 headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #----------------------------------------------------------------------------#
    # Tests for /movies GET WITH AUTH HEADERS
    #----------------------------------------------------------------------------#

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))
    #----------------------------------------------------------------------------#
    # Tests for /movies GET NO AUTH HEADERS FOR 401
    #----------------------------------------------------------------------------#

    def test_401_get_movies_error(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Missing Authorization header.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
