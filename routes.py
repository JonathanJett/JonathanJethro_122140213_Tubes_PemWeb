def includeme(config):
    config.add_route('get_book', '/api/books/{id}')
    config.add_route('create_book', '/api/books')
    config.add_route('update_book', '/api/books/{id}')
    config.add_route('delete_book', '/api/books/{id}')
    config.add_route('search_books', '/api/search')  
    config.add_route('home', '/')
