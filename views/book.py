import json
import requests
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
from ..models.book import Book

@view_config(route_name='get_book', renderer='json', request_method='GET')
def get_book(request):
    book_id = int(request.matchdict['id'])
    book = request.dbsession.get(Book, book_id)
    if not book:
        return HTTPNotFound()
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'rating': book.rating,
        'status': book.status
    }

@view_config(route_name='create_book', renderer='json', request_method='POST')
def create_book(request):
    data = request.json_body
    book = Book(
        title=data['title'],
        author=data.get('author', ''),
        rating=data.get('rating', 0),
        status=data.get('status', 'unread')
    )
    request.dbsession.add(book)
    return {'message': 'Book created'}

@view_config(route_name='update_book', renderer='json', request_method='PUT')
def update_book(request):
    book_id = int(request.matchdict['id'])
    book = request.dbsession.get(Book, book_id)
    if not book:
        return Response(json.dumps({'error': 'Book not found'}), status=404, content_type='application/json')

    data = request.json_body
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.rating = data.get('rating', book.rating)
    book.status = data.get('status', book.status)
    return {'message': 'Book updated'}

@view_config(route_name='delete_book', renderer='json', request_method='DELETE')
def delete_book(request):
    book_id = int(request.matchdict['id'])
    book = request.dbsession.get(Book, book_id)
    if not book:
        return HTTPNotFound()
    request.dbsession.delete(book)
    return {'message': 'Book deleted'}


@view_config(route_name='search_books', renderer='json', request_method='GET')
def search_books(request):
    query = request.params.get('q', '')
    if not query:
        return {'error': 'Query cannot be empty'}

    url = f'https://openlibrary.org/search.json?q={query}'
    response = requests.get(url)
    if response.status_code != 200:
        return Response(json.dumps({'error': 'Failed to fetch from OpenLibrary'}), status=502, content_type='application/json')

    results = response.json().get('docs', [])[:10]
    books = []

    for b in results:
        title = b.get('title')
        authors = ', '.join(b.get('author_name', []))
        if title and authors:
            # Simpan ke database lokal
            book = Book(title=title, author=authors, rating=0, status='unread')
            request.dbsession.add(book)
            books.append({'title': title, 'author': authors})

    return {'message': f'{len(books)} books added', 'results': books}
