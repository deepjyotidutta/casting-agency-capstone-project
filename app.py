import sys
from flask import Flask, request, abort, jsonify
from model.models import setup_db, Actor, MovieCast, Movie, db
from flask_cors import CORS
from flask_migrate import Migrate
from auth.auth import AuthError, requires_auth
import os

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)

    ITEMS_PER_PAGE = 10
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    API_AUDIENCE = os.environ.get('API_AUDIENCE')
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CALLBACK_URL = os.environ.get('AUTH0_CALLBACK_URL')

    def paginate(request, item_list):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        formatted_list = [item.format() for item in item_list]
        return formatted_list[start:end]

    @app.route('/')
    def home():
        return "Hello World"

    @app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        """ Helper method for generating JWT URL """
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{AUTH0_CLIENT_ID}&redirect_uri=' \
            f'{AUTH0_CALLBACK_URL}'
        return jsonify({
            'url': url
        })

    @app.route('/actors')
    @requires_auth('get:actor')
    def get_actors(jwt):
        """ Service to fetch all actors """
        print("LOG START /actors")
        actors = Actor.query.all()
        # 404 if no drinks found
        if len(actors) == 0:
            return jsonify({
                'success': False,
                'actors': None
            }), 404
        paginated_actors = paginate(request, actors)
        if not len(paginated_actors):
            abort(404)
        return jsonify({
            'success': True,
            'actors':  paginated_actors
        }), 200


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def create_actors(jwt):
        """ Service to add an actor """
        success = False
        try:
            name = request.json.get('name', None)
            age = request.json.get('age', None)
            gender = request.json.get('gender', None)
            print(name)
            if not (name and age and gender):
                return abort(
                    422)
            actor_instance = Actor(name, age, gender)
            actor_instance.insert()
            success = True
            actor_list = Actor.query.all()
            paginated_actor_list = paginate(
                request, actor_list)
            return jsonify({
                'success': True,
                'actors': paginated_actor_list,
                'total_actors': len(actor_list),
                'actor_added': actor_instance.format()
            })
        except BaseException:
            return abort(422)

    @app.route('/movies')
    @requires_auth('get:movie')
    def get_movies(jwt):
        """ Service to get all movies """
        print("LOG START /movies")
        movies = Movie.query.all()
        # 404 if no drinks found
        if len(movies) == 0:
            return jsonify({
                'success': False,
                'movies': None
            }), 404
        paginated_movies = paginate(request, movies)
        if not len(paginated_movies):
          abort(404)
        return jsonify({
            'success': True,
            'movies':  paginated_movies
        }), 200


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def create_movies(jwt):
        """ Service to add a movie """         
        success = False
        try:
            title = request.json.get('title', None)
            release_date = request.json.get('release_date', None)
            print(title)
            if not (title and release_date):
                return abort(
                    422)
            movie_instance = Movie(title, release_date)
            movie_instance.insert()
            success = True
            movie_list = Movie.query.all()
            paginated_movie_list = paginate(
                request, movie_list)
            return jsonify({
                'success': True,
                'movies': paginated_movie_list,
                'total_movies': len(movie_list),
                'movie_added': movie_instance.format()
            })
        except BaseException:
            print(sys.exc_info())
            return abort(422)

    @app.route('/movieCast', methods=['POST'])
    @requires_auth('post:movie')
    def create_movieCast(jwt):
        """ Service to add a moviecast """               
        error = False
        movie_id = request.json.get('movie_id', None)
        actor_id = request.json.get('actor_id', None)
        role = request.json.get('role', None)
        if not (movie_id and actor_id):
            return abort(
                422)
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            return abort(422)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            return abort(422)
        if (actor and movie):
            movieCast = MovieCast(movie_id, actor_id, role)
            movieCast.insert()
            success = True
            movieCast_list = MovieCast.query.all()
            paginated_movieCast_list = paginate(
                request, movieCast_list)
            return jsonify({
                'success': True,
                'movie_cast': paginated_movieCast_list,
                'total_movie_cast': len(movieCast_list),
                'movie_cast_added': movieCast.format()
            })
        else:
            return abort(422)

    def formatMovieCast(movieCast):
        return {
            'movie_title': movieCast.movie_title,
            'actor_name': movieCast.actor_name,
            'role': movieCast.role}

    @app.route('/movieCast')
    @requires_auth('get:actor')
    def get_all_movie_cast(jwt):
        # displays list of movies with cast
        try:
            movie_cast = db.session.query(MovieCast).join(Movie).join(Actor).add_columns(Movie.title.label('movie_title')).add_columns(
                Actor.name.label('actor_name')).add_columns(MovieCast.role.label('role')).order_by(Movie.title).all()
            if len(movie_cast) == 0:
                return jsonify({
                    'success': False,
                    'movies': None
                }), 404
            return jsonify({
                'success': True,
                'movie_cast':  [formatMovieCast(item) for item in movie_cast]
            }), 200
        except BaseException:
            print(sys.exc_info())
            return abort(500)

    @app.route('/movieCast/movie/<int:movie_id>')
    @requires_auth('get:movie')
    def get_movie_cast_by_movieid(jwt, movie_id):
        # displays list of movies with cast
        if movie_id is not None:
            try:
                movie_cast = db.session.query(MovieCast).join(Movie).join(Actor).add_columns(Movie.title.label('movie_title')).add_columns(
                    Actor.name.label('actor_name')).add_columns(MovieCast.role.label('role')).filter(Movie.id == movie_id).order_by(Movie.title).all()
                if len(movie_cast) == 0:
                    return jsonify({
                        'success': False,
                        'movies': None
                    }), 404
                return jsonify({
                    'success': True,
                    'movie_cast':  [formatMovieCast(item) for item in movie_cast]
                }), 200
            except BaseException:
                print(sys.exc_info())
                return abort(500)
        else:
            return abort(422)

    @app.route('/movieCast/actor/<int:actor_id>')
    @requires_auth('get:actor')
    def get_movie_cast_by_actorid(jwt, actor_id):
        # displays list of movies with cast
        if actor_id is not None:
            try:
                movie_cast = db.session.query(MovieCast).join(Movie).join(Actor).add_columns(Movie.title.label('movie_title')).add_columns(
                    Actor.name.label('actor_name')).add_columns(MovieCast.role.label('role')).filter(Actor.id == actor_id).order_by(Movie.title).all()
                if len(movie_cast) == 0:
                    return jsonify({
                        'success': False,
                        'movies': None
                    }), 404
                return jsonify({
                    'success': True,
                    'movie_cast':  [formatMovieCast(item) for item in movie_cast]
                }), 200
            except BaseException:
                print(sys.exc_info())
                return abort(500)
        else:
            return abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(jwt, id):
        """ Service to delete a movie """               
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if not movie:
            abort(404)
        try:
            movie.delete()
        except BaseException:
            print(sys.exc_info())
            abort(500)
        return jsonify({'success': True, 'delete': id}), 200

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(jwt, id):
        """ Service to delete an actor """               
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if not actor:
            abort(404)
        try:
            actor.delete()
        except BaseException:
            print(sys.exc_info())
            abort(500)
        return jsonify({'success': True, 'delete': id}), 200

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(jwt, id):
        """ Service to Update a movie """               
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if not movie:
            abort(404)
        req = request.get_json()
        try:
            input_release_date = req.get('release_date')
            input_title = req.get('title')
            if input_release_date is not None:
                movie.release_date = input_release_date
            if input_title is not None:
                movie.title = input_title
            movie.update()
        except BaseException:
            print(sys.exc_info())
            abort(500)
        return jsonify({'success': True, 'movies': movie.format()}), 200

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(jwt, id):
        """ Service to update an actor """     
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if not actor:
            abort(404)
        req = request.get_json()
        try:
            input_name = req.get('name')
            input_gender = req.get('gender')
            input_age = req.get('age')

            if input_name is not None:
                actor.name = input_name
            if input_gender is not None:
                actor.gender = input_gender
            if input_age is not None:
                actor.age = input_age
            actor.update()
        except BaseException:
            print(sys.exc_info())
            abort(500)
        return jsonify({'success': True, 'actors': actor.format()}), 200

    # Error Handling
    '''
  Example error handling for unprocessable entity
  '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error.'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(
            Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    return app
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
app = create_app()
# Default port:
