# FSND: Capstone Casting Agency Project

## Content

1. [Motivation](#motivation)
2. [Start Project locally](#start-locally)
3. [API Documentation](#api)
4. [Authentification](#authentification)

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
3.1 Create new Auth0 project which will genrate ClientId. And setup callback URLs like -
    http://localhost:5000/, https://casting-agency-deepjyotidutta.herokuapp.com/
3.2 Create new Auh0 API. And setup a new API Audience. Enable RBAC and 'Add Permissions in the Access Token'
3.3 Create Roles 
```
    a. Casting Assistant - Add permissions get:actor , get:movie
    b. Casting Director - Add permissions delete:actor , get:actor , get:movie , patch:actor , patch:movie , post:actor
    c. Executive Producer - Add permisisions delete:actor , delete:movie, get:actor, get:movie, patch:actor, patch:movie, post:actor, post:movie
```
* FOR UDACITY REVIEW PLEASE USE THE TOKENS ALREADY SETUP IN THE ATTACHED POSTMAP EXPORT

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



### Authentification

Please see Authent

### Available Endpoints

## API Documentation

GET "/actors"
    Fetches a list of Actors
    Request Parameters: None
    Requires permission: get:actor
    Response Body: 
        actors: List of actors
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/actors
# Reponse Example
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
GET "/movies"
    Fetches a list of Movies
    Request Parameters: None
    Requires permission: get:movie
    Response Body: 
        actors: List of movies
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/movies
# Reponse Example
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
POST "/actors"
    Adds a new Actor
    Request Parameters: Actor object
    ```
        {
            "name": "Kajol",
            "age": "30",
            "gender":"Female"
        }
    ```
    Requires permission: post:actor
    Response Body: 
        actors: List of movies
        success: Boolean
    Heroku Endpoint - https://casting-agency-deepjyotidutta.herokuapp.com/movies
# Reponse Example
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
GET "/questions?page=1"
    Fetches the questions based on the page number
    Request Parameters: page: Page number
    Response Body:
      questions: List of questions
      categories: Dictionary of Category ID <-> Category Type
      total_questions: Total number of questions
      currentPage : page number
```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentPage": 1,
  "current_category": "None",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "success": true,
  "total_questions": 18
}
```
DELETE "/questions/int:question_id"
    Deletes a question
    Request Parameters: question_id: Question ID to be deleted
    Response Body:
      deleted: Deleted Question ID
```bash
{
  "question_deleted": 15,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "success": true,
  "total_questions": 17
}
```
POST "/questions"
    Adds a questions to the DB
    Request Body:
      question: Question
      answer: Answer
      category: Category ID
      difficulty: Difficulty Level
    Response Body:
      question_added: Question obect that is created
      total_questions: Total Number of questions
      questions: List of all questions
```bash
{
  "total_questions": 20,
  "question_added": {
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  }
}
```
POST "/search"
    Fetches questions based on the search term
    Request Body:
      searchTerm: Search term
    Response Body:
      questions: List of questions found in search
      total_questions: Total number of questions
```bash
{
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  }],
  "total_questions": 1
}
```
GET "/categories/int:category_id/questions"
    Fetches questions from the requested category
    Request Parameters: category_id: Category ID for questions
    Response Body:
      questions: List of category questions
      total_questions: Total number of questions
      current_category: Current category ID
```bash
{
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  }],
  "total_questions": 1,
  "current_category": 1
}
```

# <a name="authentification"></a>
## Authentification

All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to config Auth0 accordingly

### Auth0 for locally use
#### Create an App & API

1. Login to https://manage.auth0.com/ 
2. Click on Applications Tab
3. Create Application
4. Give it a name like `Music` and select "Regular Web Application"
5. Go to Settings and find `domain`. Copy & paste it into config.py => auth0_config['AUTH0_DOMAIN'] (i.e. replace `"example-matthew.eu.auth0.com"`)
6. Click on API Tab 
7. Create a new API:
   1. Name: `Music`
   2. Identifier `Music`
   3. Keep Algorithm as it is
8. Go to Settings and find `Identifier`. Copy & paste it into config.py => auth0_config['API_AUDIENCE'] (i.e. replace `"Example"`)

#### Create Roles & Permissions

1. Before creating `Roles & Permissions`, you need to `Enable RBAC` in your API (API => Click on your API Name => Settings = Enable RBAC => Save)
2. Also, check the button `Add Permissions in the Access Token`.
2. First, create a new Role under `Users and Roles` => `Roles` => `Create Roles`
3. Give it a descriptive name like `Casting Assistant`.
4. Go back to the API Tab and find your newly created API. Click on Permissions.
5. Create & assign all needed permissions accordingly 
6. After you created all permissions this app needs, go back to `Users and Roles` => `Roles` and select the role you recently created.
6. Under `Permissions`, assign all permissions you want this role to have. 

# <a name="authentification-bearer"></a>
### Auth0 to use existing API
If you want to access the real, temporary API, bearer tokens for all 3 roles are included in the `config.py` file.

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (view:actors): Can see all actors
  - GET /movies (view:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (create:actors): Can create new Actors
  - PATCH /actors (edit:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (edit:movies): Can edit existing Movies
3. Exectutive Dircector (everything from Casting Director plus)
  - POST /movies (create:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Motives from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).

For example: (Bearer token for `Executive Director`)
```js
{
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik16azVRVUk0TXpSR04wSXhOVU13TkRrME16QXdNMFpHTmtFMU1VWXdPRUpCTmpnMFJrVTBSZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWF0dGhldy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0N2VmYzc2N2YxYmEwZWJiNDIwMTYzIiwiYXVkIjoiTXVzaWMiLCJpYXQiOjE1ODE4NjI0NjksImV4cCI6MTU4MTg2OTY2OSwiYXpwIjoiVGh2aG9mdmtkRTQwYlEzTkMzSzdKdFdSSzdSMzFOZDciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.iScamWOFNx9pjiVZhsvPzDoRi6EraZaxWg-WMj80HNW_-dchkOymnKA7OOhPQ8svLc9-wViLlCT-ySnupZ-209cIBVHSA_slncSP-lzEM6NKbBmDEETTQ1oxv2jTH-JL72eLhyAWUsmSIZDmEab1hln1yWEN7mUnn0nZJfxCRCs89h5EGJzXS2v8PbAjq9Mu7wFsrioEMx_PGWzSM0r5WIrKBvpXRy0Jm-vssZl4M1akDHIL5Shcfp_Bfnarc2OLOMvdQVHVDEWhrbFSnfCENLDxkcmB18VnOedJAuY_C88YRUfY2wQAOPux8RVuqIb5KxTg4YP7kiDcBUKXEnhL9A"
}
```