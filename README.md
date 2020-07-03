# FSND: Capstone Casting Agency Project

## Content

1. [Motivation](#motivation)
2. [Local Project Setup](#start-locally)
3. [API Documentation](#api)
4. [Authentification](#authentification)
5. [Heroku Setup](#heroku)
6. [POSTMAN Setup](#postman)

<a name="motivation"></a>
## Motivations

This project is part of the `Udacity-Full-Stack-Nanodegree` Program.
Topics covered in this project :

1. Database modeling using `postgres` & `sqlalchemy` (see `model/models.py`)
2. API to perform CRUD Operations on database using `Flask` (see `app.py`)
3. Automated testing using `Unittest` (see `test_app`)
4. Authorization & Role based Authentification using `Auth0` (see `auth/auth.py`)
5. Deployment on `Heroku`

<a name="start-locally"></a>
## Local Setup

Install the latest version of [Python 3](https://www.python.org/downloads/)
and [postgres](https://www.postgresql.org/download/) .

Install/Update Python package manager PIP
py -m pip install --upgrade pip

Install virtualenv
py -m pip install --user virtualenv

To start and run the local development server,

1. Initialize and activate a virtualenv env:
  ```bash
  $ py -m venv env
  $ source env/scripts/activate
  ```

2. Install the dependencies:
```bash
$ pip install -r requirements.txt
```

3. Setup Auth0
#### 3.1 Create new Auth0 project which will generate a ClientId. And setup callback URLs like -
    http://localhost:5000/, https://casting-agency-deepjyotidutta.herokuapp.com/
#### 3.2 Create new Auh0 API. And setup a new API Audience. Enable RBAC and 'Add Permissions in the Access Token'
#### 3.3 Create Roles and Permissions
```
    a. Casting Assistant - Add permissions get:actor , get:movie
    b. Casting Director - Add permissions delete:actor , get:actor , get:movie , patch:actor , patch:movie , post:actor
    c. Executive Producer - Add permisisions delete:actor , delete:movie, get:actor, get:movie, patch:actor, patch:movie, post:actor, post:movie
```
#### FOR UDACITY REVIEW : KINDLY USE THE TOKENS ALREADY SETUP IN THE ATTACHED POSTMAP EXPORT

5. Run the development server:
  ```bash 
  $ FLASK_APP=app.py FLASK_DEBUG=true flask run
  ```

6. Execute test cases, run
```bash 
$ py test_app.py
```
## API Documentation
<a name="api"></a>

Base URL - https://casting-agency-deepjyotidutta.herokuapp.com/

### GET "/actors"
    Fetches a list of Actors
    Request Parameters: None
    Requires permission: get:actor
    Response Body: 
        actors: List of actors
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/actors
### Reponse Example
  ```bash
 {
  "actors": [
    {
      "age": 50,
      "gender": "Male",
      "id": 2,
      "name": "Shahrukh Khan"
    },
    {
      "age": 30,
      "gender": "Male",
      "id": 6,
      "name": "Vicky Kaushal"
    }
  ],
  "success": true
}
```
### GET "/movies"
    Fetches a list of Movies
    Request Parameters: None
    Requires permission: get:movie
    Response Body: 
        actors: List of movies
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/movies
### Reponse Example
  ```bash
{
  "movies": [
    {
      "id": 1,
      "release_date": "31/12/2020",
      "title": "John Wick 4"
    },
    {
      "id": 2,
      "release_date": "12/12/2020",
      "title": "Jurassic Park"
    },
    {
      "id": 4,
      "release_date": "12/12/2020",
      "title": "Jurassic Park 3"
    }
  ],
  "success": true
}

  ```
### POST "/actors"
    Adds a new Actor
    Request Body: Actor object
    ```
        {
            "name": "Kajol",
            "age": "30",
            "gender":"Female"
        }
    ```
    Requires permission: post:actor
    Response Body: 
        actors: List of actors
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/actors
### Reponse Example
  ```bash
{
  "actor_added": {
    "age": 30,
    "gender": "Female",
    "id": 2,
    "name": "Kajol"
  },
  "actors": [
    {
      "age": 45,
      "gender": "Male",
      "id": 1,
      "name": "Hrithik Roshan"
    },
    {
      "age": 30,
      "gender": "Female",
      "id": 2,
      "name": "Kajol"
    }
  ],
  "success": true,
  "total_actors": 2
}
  ```

### POST "/movies"
    Adds a new Movie
    Request Body: Movie object
    ```
    {
        "title": "Jurassic Park 3",
        "release_date": "12/12/2020"
    }
    ```
    Requires permission: post:movie
    Response Body: 
        actors: List of movies
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/movies
### Reponse Example
  ```bash
{
  "movie_added": {
    "id": 4,
    "release_date": "12/12/2020",
    "title": "Jurassic Park 3"
  },
  "movies": [
    {
      "id": 1,
      "release_date": "31/12/2020",
      "title": "John Wick 4"
    }
  ],
  "success": true,
  "total_movies": 4
}
  ```
### DELETE "/actors/{{id}}"
    Delete an  Actor
    Request Parameters: Id
    Requires permission: delete:actor
    Response Body: 
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/actors/2
### Reponse Example
  ```bash
    {
    "delete": 3,
    "success": true
    }
  ```
### DELETE "/movies/{{id}}"
    Delete a  Movie
    Request Parameters: Id
    Requires permission: delete:movie
    Response Body: 
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/movies/3
### Reponse Example
  ```bash
    {
    "delete": 3,
    "success": true
    }
  ```
### PATCH "/actors/{{id}}"
    UPDATE an  Actor
    Request Parameters: Id
    Request Body: Actor Object
    {
        "age": 40,
        "gender": "Male",
        "name": "Hrithik Roshan"
    }
    Requires permission: patch:actor
    Response Body: 
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/actors/1
### Reponse Example
  ```bash
    {
    "actors": {
        "age": 40,
        "gender": "Male",
        "id": 1,
        "name": "Hrithik Roshan"
    },
    "success": true
    }
  ```
### PATCH "/movies/{{id}}"
    UPDATE an  Movie
    Request Parameters: Id
    Request Body: Movie Object
    {
        "title": "John Wick 4",
        "release_date": "31/12/2020"
    }
    Requires permission: patch:movie
    Response Body: 
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/movies/1
### Reponse Example
  ```bash
    {
    "movies": {
        "id": 1,
        "release_date": "31/12/2020",
        "title": "John Wick 4"
    },
    "success": true
    }
  ```
# <a name="authentification"></a>
## Authentification

All API Endpoints are decorated with Auth0 permissions. Refer to steps provided in Local Setup section for Auth0 Setup details.

### Role Mapping
Role Summary :
```
    Casting Assistant
        Can view actors and movies
    Casting Director
        All permissions a Casting Assistant has and…
        Add or delete an actor from the database
        Modify actors or movies
    Executive Producer
        All permissions a Casting Director has and…
        Add or delete a movie from the database
```
```
a. Role Casting Assistant - Permissions get:actor , get:movie
b. Role Casting Director - Permissions delete:actor , get:actor , get:movie , patch:actor , patch:movie , post:actor
c. Role Executive Producer - Permissions delete:actor , delete:movie, get:actor, get:movie, patch:actor, patch:movie, post:actor, post:movie
```
### UDACITY REVIEW - Please find below some valid tokens for each role at the time of Submission
```
{
    "EXECUTIVE_PRODUCER": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1fWV9hQURNTTR6c1lsWlRMWEJLRSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ici13Z3Blby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMjZjM2JhYmEwMzAwMDE5Y2UwYjRkIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MzgwMDgxNSwiZXhwIjoxNTkzODg3MjE1LCJhenAiOiJOSWQxQjdlOEhFMmEyZk1YekI2ZTg5Z0F4VzdIOTlZUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.E7Oz2vsnRzzbCS_UbXKqjJHj3PJS3DDEQzVQHVVEE4Z6RTXH9KvRkR0Oxie9IDHvIQ1tONfuuyy_H_J0GzOicgPqr6G2ptqp2MVAcF59qsUVFpARwyVrw4ev-zJp1_YlnOrXT4YUp_z_z9YQAILVBTy2XBkemYoZUiGIt568bsgkGcUY4MlEjFDqX0OgmhqElEeuL5kUnQpMjomlprVTHexV-NNsEHp1HnHySkz3SNmiTITIDIzKcElyICI-opWNA2AIYocVhgPgtOttFOpkGpomet93ko21IfSYVtPvXgNt6ZJnDGs0XvjSDYE_6tfOVvM9wvOoXzmVg_Kk5iNWMg",
    "CASTING_ASSISTANT": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1fWV9hQURNTTR6c1lsWlRMWEJLRSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ici13Z3Blby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmMjZjZDk3Nzk3YzEwMDEzNzAxYjNjIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MzgwMDQ5NCwiZXhwIjoxNTkzODg2ODk0LCJhenAiOiJOSWQxQjdlOEhFMmEyZk1YekI2ZTg5Z0F4VzdIOTlZUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIl19.moUQBzW4Rsc7e2wmoMipeKXgAd8gNmeo0TKeKQJXbnhhFtwPtYc_nsWYlhrEos4PnZPkqJQeyvPeiY-Z1QVXZv0JAYl9HkywJziZOIMQBiS-fsDgBORHLcfPxmKj4qIHFggdKFIJeM_D0p5Vp-E_o6DioixYdjcB1uStwjp_ZdXDRq8wapK7AhiBvAGn5wM3fjCxZ56ANzB3ACuv8VMOzJJ5PT5oKqRnUew09IHVKWe5EqoolgY15ugQLLb9GUuo5hfbkppN4DXuGjjN1H8hT9WGObIBxFy6Cq_lmm6dgDLm_Cx2dkz22hUqA3efmU_BeKClzBJqDuNdELRw-1qGYw",
    "CASTING_DIRECTOR": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1fWV9hQURNTTR6c1lsWlRMWEJLRSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ici13Z3Blby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTI3MjkzNDE2MDUwMDE5ZGQ1MWY1IiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTU5MzgwMDYzMiwiZXhwIjoxNTkzODg3MDMyLCJhenAiOiJOSWQxQjdlOEhFMmEyZk1YekI2ZTg5Z0F4VzdIOTlZUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.HUiDDhBSxGOwqrKG_YXGVnkGcn8BlsgtLSgjQyz9QspYJCL4Cm3FxX_U3knfs32DfaCdRRpwSqzQHRqTu93r72-LCrIlL-of9DIaRVXJJq4YFQ4yQbfvHiWQ0w7tf27CUZ9pCbkhXlC4k2VhFsdlM0PvNAzEiPSOEAVLoCMZ_4ySL2SmFZ5nqDaAcpVCZx7CZtlzlyAUsCuX9wOXf30mDCZexugua8VXmlzhrN0m7eTNeiyhsveMbXcYsRB_U-e0YxNPE2rqOXV_uDfj40X2FjI5oIOiKd1OpMl7GjBrI3oEHlCy_uX0BFvOQWUSCV8lXVqn_r1UXjHR5mV_qra_vQ"
}
```

<a name="heroku"></a>
## Heroku Setup
1. Create Heroku account
2. Download and install Heroku CLI in your local.
3. Create/Update requirements.txt file to be used by Heroku to install dependencies
4. Set up environment variables in Heroku
5. The project will be served using Gunicorn http server. Install Gunicorn and configure Gunicorn in the Heroku config file named Procfile[Already set up for this project with value ```web: gunicorn app:app``` ]
6. To manage and setup DB in Heroku add the configurations in manage.py [Refer to project manage.py file]
7. Create the new app with name like 'casting-agency-deepjyotidutta' in Heroku using CLI like ``` heroku create casting-agency-deepjyotidutta ``` 
8. Add git remote for Heroku to local repository  ``` git remote add heroku https://git.heroku.com/casting-agency-deepjyotidutta.git ```
9. Add postgresql addon for the database ``` heroku addons:create heroku-postgresql:hobby-dev --app casting-agency-deepjyotidutta ```
10. Check to ensure that Heroku config is good. ``` heroku config --app casting-agency-deepjyotidutta ```
11. GIT push project to Heroku ``` git push heroku master ```
12. Run Heroku DB migrations ``` heroku run python manage.py db upgrade --app casting-agency-deepjyotidutta ```
13. The app should be live now. Test the endpoints from POSTMAN
14. Heroku Logs can be checked using https://dashboard.heroku.com/apps/casting-agency-deepjyotidutta/logs OR Heroku CLI

<a name="postman"></a>
## POSTMAN Setup

Please check the Postman export file. Import it in your local. It has 2 Folders for testing the Heroku hosted App and localhost hosted app. Each folder again has list of APIs for each Auth Role