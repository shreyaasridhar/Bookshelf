import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_book = {
            'title': 'Anansi Boys',
            'author': 'Neil Gaiman',
            'rating': 5
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_books(self):
        self.assertEqual(self.client().get(
            '/').status_code, 200)
        res = self.client().get('/books')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))

    def test_404_pagination(self):
        res = self.client().get('/books?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)

    def test_update_book_rating(self):
        res = self.client().patch('/books/2', json={'rating': 5})
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(book.format()['rating'], 5)
        pass

# @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc.
#        Since there are four routes currently, you should have at least eight tests.
# Optional: Update the book information in setUp to make the test database your own!


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
