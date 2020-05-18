import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

# TODO: Define the create_app method and complete initial set up of the application
# TODO: Enable CORS and set response headers
# TODO: Define an app route to retrieve all books
# TODO: Define pagination behavior on the get request

# TODO: Define an endpoint to delete a book based on id. If it doesn't exist, abort.
# TODO: Define a PATCH endpoint that updates a book's rating.
# Abort if the book doesn't exist or the update fails
# TODO: Define a POST endpoint to handle creating a new book instance.
# Abort if creation is unsuccessful

# TODO: Write error handlers for all abort status codes utilized in the endpoints
# They should return the code, a message, and success value.

# TODO: AFTER writing the corresponding tests, write an endpoint or update a previous endpoint
# that handles a search arg in the body of the request and return paginated results.


def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    books = [book.format() for book in selection]

    return books[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/books')
    def retrieve_books():
        selection = Book.query.order_by(Book.id).all()
        current_books = paginate_books(request, selection)

        if len(current_books) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'books': current_books,
            'total_books': len(Book.query.all())
        })

    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):

        body = request.get_json()

        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)

            if 'rating' in body:
                book.rating = int(body.get('rating'))

            book.update()

            return jsonify({
                'success': True,
                'id': book.id
            })

        except:
            abort(400)

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            print(book)
            if book is None:
                abort(404)

            book.delete()
            selection = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, selection)

            return jsonify({
                'success': True,
                'deleted': book_id,
                'books': current_books,
                'total_books': len(Book.query.all())
            })

        except:
            abort(422)

    @app.route('/books', methods=['POST'])
    def create_book():
        body = request.get_json()
        print(body)
        try:
            if 'search' in body:
                selection = Book.query.order_by(Book.id).filter(
                    Book.title.ilike('%{}%'.format(body['search'])))
                current_books = paginate_books(request, selection)
                return jsonify({
                    'success': True,
                    'books': current_books,
                    'total_books': len(selection.all())
                })
            else:
                book = Book(title=body['title'],
                            author=body['author'], rating=body['rating'])
                book.insert()

                formatted_books = paginate_books(
                    request, Book.query.order_by(Book.id).all())

                return jsonify({
                    'success': True,
                    'created': book.id,
                    'books': formatted_books,
                    'total_books': len(Book.query.all())
                })
        except:
            abort(422)

    # @TODO: Create a new endpoint or update a previous endpoint to handle searching for a team in the title
    # the body argument is called 'search' coming from the frontend.
    # If you use a different argument, make sure to update it in the frontend code.
    # The endpoint will need to return success value, a list of books for the search and the number of books with the search term
    # Response body keys: 'success', 'books' and 'total_books'
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
