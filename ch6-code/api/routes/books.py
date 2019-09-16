#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.books import Book, BookSchema
from api.utils.database import db
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

book_routes = Blueprint("book_routes", __name__)


@book_routes.route('/', methods=['POST'])
@jwt_required
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        book, error = book_schema.load(data)
        result = book_schema.dump(book.create()).data
        return response_with(resp.SUCCESS_201, value={"book": result})
    except Exception as e:
        print e
        return response_with(resp.INVALID_INPUT_422)


@book_routes.route('/', methods=['GET'])
def get_book_list():
    fetched = Book.query.all()
    book_schema = BookSchema(many=True, only=['author_id','title', 'year'])
    books, error = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"books": books})


@book_routes.route('/<int:id>', methods=['GET'])
def get_book_detail(id):
    fetched = Book.query.get_or_404(id)
    book_schema = BookSchema()
    books, error = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"books": books})

@book_routes.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_book_detail(id):
    data = request.get_json()
    get_book = Book.query.get_or_404(id)
    get_book.title = data['title']
    get_book.year = data['year']
    db.session.add(get_book)
    db.session.commit()
    book_schema = BookSchema()
    book, error = book_schema.dump(get_book)
    return response_with(resp.SUCCESS_200, value={"book": book})

@book_routes.route('/<int:id>', methods=['PATCH'])
@jwt_required
def modify_book_detail(id):
    data = request.get_json()
    get_book = Book.query.get_or_404(id)
    if data.get('title'):
        get_book.title = data['title']
    if data.get('year'):
        get_book.year = data['year']
    db.session.add(get_book)
    db.session.commit()
    book_schema = BookSchema()
    book, error = book_schema.dump(get_book)
    return response_with(resp.SUCCESS_200, value={"book": book})

@book_routes.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_book(id):
    get_book = Book.query.get_or_404(id)
    db.session.delete(get_book)
    db.session.commit()
    return response_with(resp.SUCCESS_204)
