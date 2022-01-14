import os
import re
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from sqlalchemy.sql.operators import endswith_op

from models import setup_db, Contact

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars
    @app.route("/books")
    def get_books():
        books = Book.query.order_by(Book.id).all()
        total_books = len(books)
        if not books:
            abort(404)
        page = int(request.args.get("page", 1))
        start = (page - 1) * BOOKS_PER_SHELF
        end = start + BOOKS_PER_SHELF   # start + BOOKS_PER_SHELF
        books = [book.format() for book in books]

        return jsonify({
            "success": True,
            "books": books[start:end],
            "total_books": total_books
        })

    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
    @app.route("/books/<int:book_id>", methods=["PATCH","GET"])
    def update_book(book_id):
        body = request.get_json()
        book = Book.query.get(book_id)
        if book is None:
            abort(404)
        if request.method == "PATCH":
            if "rating" in body:
                book.rating = int(body["rating"])
            book.update()
            return jsonify({
                "success": True,
                "book": book.format()
            })
        else:
            return jsonify({
                "success": True,
                "book": book.format()
            })
    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'

    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.
    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if book is None:
            abort(404)
        book.delete()
        return jsonify({
            "success": True,
            "deleted": book_id
        })
    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.
    @app.route("/books", methods=["POST"])
    def create_book():
        body = request.get_json()
        if body is None:
            abort(400)
        if "title" not in body or "author" not in body or "rating" not in body:
            abort(400)
        book = Book(title=body["title"], author=body["author"], rating=body["rating"])
        book.insert()
        return jsonify({
            "success": True,
            "created": book.id,
            "books": [book.format()],
            "total_books": Book.query.count()
        })

    @app.route('/books/search', methods=['POST'])
    def search_books():
        body = request.get_json()
        if body is None:
            abort(400)
        if "searchTerm" not in body:
            abort(400)
        search_term = body["searchTerm"]
        books = Book.query.filter(Book.title.ilike(f'%{search_term}%')).all()
        books = [book.format() for book in books]
        return jsonify({
            "success": True,
            "books": books,
            "total_books": len(books)
        })
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app
