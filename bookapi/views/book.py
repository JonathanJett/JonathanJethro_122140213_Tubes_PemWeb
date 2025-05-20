from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPOk
from ..models import Book
import json

@view_config(route_name='get_books', renderer='json', request_method='GET')
def get_books(request):
    books = request.dbsession.query(Book).all()
    return [{'id': b.id, 'title': b.title, 'author': b.author, 'rating': b.rating, 'status': b.status} for b in books]

@view_config(route_name='create_book', renderer='json', request_method='POST')
def create_book(request):
    data = request.json_body
    book = Book(title=data['title'], author=data['author'], rating=data.get('rating', 0), status=data.get('status', 'unread'))
    request.dbsession.add(book)
    return {'message': 'Book created'}

@view_config(route_name='update_book', renderer='json', request_method='PUT')
def update_book(request):
    book_id = int(request.matchdict['id'])
    book = request.dbsession.query(Book).get(book_id)
    if not book:
        return Response(
    json.dumps({'error': 'Book not found'}),
    status=404,
    content_type='application/json'
)
    data = request.json_body
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.rating = data.get('rating', book.rating)
    book.status = data.get('status', book.status)
    return {'message': 'Book updated'}

@view_config(route_name='delete_book', renderer='json', request_method='DELETE')
def delete_book(request):
    book_id = int(request.matchdict['id'])
    book = request.dbsession.query(Book).get(book_id)
    if not book:
        return HTTPNotFound()
    request.dbsession.delete(book)
    return {'message': 'Book deleted'}
