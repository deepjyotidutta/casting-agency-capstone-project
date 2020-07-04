import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from model.models import setup_db, Actor, MovieCast, Movie
from model.models import db_drop_create_initialize

''' SETUP AUTH TOKENS '''
bearer_tokens = {
    "EXECUTIVE_PRODUCER": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1fWV9hQURNTTR6c1lsWlRMWEJLRSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ici13Z3Blby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMjZjM2JhYmEwMzAwMDE5Y2UwYjRkIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MzgwMDgxNSwiZXhwIjoxNTkzODg3MjE1LCJhenAiOiJOSWQxQjdlOEhFMmEyZk1YekI2ZTg5Z0F4VzdIOTlZUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.E7Oz2vsnRzzbCS_UbXKqjJHj3PJS3DDEQzVQHVVEE4Z6RTXH9KvRkR0Oxie9IDHvIQ1tONfuuyy_H_J0GzOicgPqr6G2ptqp2MVAcF59qsUVFpARwyVrw4ev-zJp1_YlnOrXT4YUp_z_z9YQAILVBTy2XBkemYoZUiGIt568bsgkGcUY4MlEjFDqX0OgmhqElEeuL5kUnQpMjomlprVTHexV-NNsEHp1HnHySkz3SNmiTITIDIzKcElyICI-opWNA2AIYocVhgPgtOttFOpkGpomet93ko21IfSYVtPvXgNt6ZJnDGs0XvjSDYE_6tfOVvM9wvOoXzmVg_Kk5iNWMg",
    "CASTING_ASSISTANT": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1fWV9hQURNTTR6c1lsWlRMWEJLRSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ici13Z3Blby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMjZjZDk3Nzk3YzEwMDEzNzAxYjNjIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MzgwMDQ5NCwiZXhwIjoxNTkzODg2ODk0LCJhenAiOiJOSWQxQjdlOEhFMmEyZk1YekI2ZTg5Z0F4VzdIOTlZUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIl19.moUQBzW4Rsc7e2wmoMipeKXgAd8gNmeo0TKeKQJXbnhhFtwPtYc_nsWYlhrEos4PnZPkqJQeyvPeiY-Z1QVXZv0JAYl9HkywJziZOIMQBiS-fsDgBORHLcfPxmKj4qIHFggdKFIJeM_D0p5Vp-E_o6DioixYdjcB1uStwjp_ZdXDRq8wapK7AhiBvAGn5wM3fjCxZ56ANzB3ACuv8VMOzJJ5PT5oKqRnUew09IHVKWe5EqoolgY15ugQLLb9GUuo5hfbkppN4DXuGjjN1H8hT9WGObIBxFy6Cq_lmm6dgDLm_Cx2dkz22hUqA3efmU_BeKClzBJqDuNdELRw-1qGYw",
    "CASTING_DIRECTOR": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1fWV9hQURNTTR6c1lsWlRMWEJLRSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ici13Z3Blby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTI3MjkzNDE2MDUwMDE5ZGQ1MWY1IiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MzgwMDYzMiwiZXhwIjoxNTkzODg3MDMyLCJhenAiOiJOSWQxQjdlOEhFMmEyZk1YekI2ZTg5Z0F4VzdIOTlZUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.HUiDDhBSxGOwqrKG_YXGVnkGcn8BlsgtLSgjQyz9QspYJCL4Cm3FxX_U3knfs32DfaCdRRpwSqzQHRqTu93r72-LCrIlL-of9DIaRVXJJq4YFQ4yQbfvHiWQ0w7tf27CUZ9pCbkhXlC4k2VhFsdlM0PvNAzEiPSOEAVLoCMZ_4ySL2SmFZ5nqDaAcpVCZx7CZtlzlyAUsCuX9wOXf30mDCZexugua8VXmlzhrN0m7eTNeiyhsveMbXcYsRB_U-e0YxNPE2rqOXV_uDfj40X2FjI5oIOiKd1OpMl7GjBrI3oEHlCy_uX0BFvOQWUSCV8lXVqn_r1UXjHR5mV_qra_vQ"
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

    # --------------------------------------------------------------------#
    # Tests for /actors POST WITH AUTH
    # --------------------------------------------------------------------#

    def test_post_actor(self):
        """Test POST new actor."""
        res = self.client().post('/actors', json=json_create_actor,
                                 headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    # --------------------------------------------------------------------#
    # Tests for /actors POST WITH NO AUTH FOR 401
    # --------------------------------------------------------------------#

    def test_401_post_actor(self):
        """Test POST new actor."""
        res = self.client().post('/actors', json=json_create_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    # --------------------------------------------------------------------#
    # Tests for /actors POST WITH BAD INPUT FOR 422
    # --------------------------------------------------------------------#

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
    # --------------------------------------------------------------------#
    # Tests for /actors GET WITH AUTH
    # --------------------------------------------------------------------#

    def test_get_actors(self):
        res = self.client().get('/actors', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
    # --------------------------------------------------------------------#
    # Tests for /actors GET NO AUTH HEADERS FOR 401
    # --------------------------------------------------------------------#

    def test_401_get_actors_error(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Missing Authorization header.")
    # --------------------------------------------------------------------#
    # Tests for /actors GET WITH AUTH HEADERS FOR 404
    # --------------------------------------------------------------------#

    def test_404_get_actors_pagination_error(self):
        res = self.client().get('/actors?page=123',
                                headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")
    # --------------------------------------------------------------------#
    # Tests for /actors PATCH WITH AUTH HEADERS
    # --------------------------------------------------------------------#

    def test_patch_actors(self):
        json_create_actor = {
            'name': 'TEST ABC',
            'age': 30,
            'gender': 'Male'
        }
        res = self.client().patch(
            '/actors/1',
            json=json_create_actor,
            headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    # --------------------------------------------------------------------#
    # Tests for /actors PATCH WITH AUTH HEADERS FOR 404
    # --------------------------------------------------------------------#

    def test_404_patch_actors_error(self):
        json_create_actor = {
            'name': 'TEST ABC',
            'age': 30,
            'gender': 'Male'
        }
        res = self.client().patch(
            '/actors/123',
            json=json_create_actor,
            headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    # --------------------------------------------------------------------#
    # Tests for /actors DELETE WITH AUTH HEADERS
    # --------------------------------------------------------------------#

    def test_delete_actors(self):
        res = self.client().delete('/actors/1', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    # --------------------------------------------------------------------#
    # Tests for /actors DELETE WITH AUTH HEADERS FOR 404
    # --------------------------------------------------------------------#

    def test_404_delete_actors_error(self):
        res = self.client().delete('/actors/123', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    # --------------------------------------------------------------------#
    # Tests for /movies POST WITH AUTH
    # --------------------------------------------------------------------#

    def test_post_movie(self):
        """Test POST new actor."""
        res = self.client().post('/movies', json=json_create_movie,
                                 headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    # --------------------------------------------------------------------#
    # Tests for /movies POST WITH AUTH FOR 422
    # --------------------------------------------------------------------#

    def test_422_post_movie_error(self):
        """Test POST new movie."""
        json_create_movie = {
            'release_date': '12/12/2020'
        }
        res = self.client().post('/movies', json=json_create_movie,
                                 headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    # --------------------------------------------------------------------#
    # Tests for /movies GET WITH AUTH HEADERS
    # --------------------------------------------------------------------#

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))
    # --------------------------------------------------------------------#
    # Tests for /movies GET WITH AUTH FOR 404
    # --------------------------------------------------------------------#

    def test_404_get_movie_error(self):
        res = self.client().get(
            '/movies?page=123', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    # --------------------------------------------------------------------#
    # Tests for /movies GET NO AUTH HEADERS FOR 401
    # --------------------------------------------------------------------#

    def test_401_get_movies_error(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Missing Authorization header.")
    # --------------------------------------------------------------------#
    # Tests for /movies PATCH WITH AUTH HEADERS
    # --------------------------------------------------------------------#

    def test_patch_movies(self):
        json_patch_movie = {
            'title': 'The lost world',
            'release_date': '12/12/2020'
        }
        res = self.client().patch(
            '/movies/1',
            json=json_patch_movie,
            headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    # --------------------------------------------------------------------#
    # Tests for /movies PATCH WITH AUTH HEADERS FOR 404
    # --------------------------------------------------------------------#

    def test_404_patch_movies_error(self):
        json_patch_movie = {
            'title': 'The lost world',
            'release_date': '12/12/2020'
        }
        res = self.client().patch(
            '/movies/123',
            json=json_patch_movie,
            headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    # --------------------------------------------------------------------#
    # Tests for /movies DELETE WITH AUTH HEADERS
    # --------------------------------------------------------------------#

    def test_delete_movies(self):
        res = self.client().delete('/movies/1', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    # --------------------------------------------------------------------#
    # Tests for /movies DELETE WITH AUTH HEADERS FOR 404
    # --------------------------------------------------------------------#

    def test_404_delete_movies_error(self):
        res = self.client().delete('/movies/123', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    ''' RBAC TEST CASES '''
    # --------------------------------------------------------------------#
    # Tests for CASTING_ASSISTANT Role
    # --------------------------------------------------------------------#

    def test_get_actors_as_assistant(self):
        res = self.client().get('/actors', headers=assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_403_post_actors_as_assistant_error(self):
        res = self.client().post(
            '/actors',
            json=json_create_actor,
            headers=assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    # --------------------------------------------------------------------#
    # Tests for CASTING_DIRECTOR Role
    # --------------------------------------------------------------------#

    def test_post_actors_as_director(self):
        res = self.client().post(
            '/actors',
            json=json_create_actor,
            headers=director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_403_post_movies_as_director(self):
        res = self.client().post(
            '/movies',
            json=json_create_movie,
            headers=director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    # --------------------------------------------------------------------#
    # Tests for EXECUTIVE_PRODUCER Role
    # --------------------------------------------------------------------#

    def test_get_actors_as_producer(self):
        res = self.client().get('/actors', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_movies_as_producer(self):
        res = self.client().post(
            '/movies',
            json=json_create_movie,
            headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
