def includeme(config):
    config.add_route('get_books', '/api/books')            # GET semua buku
    config.add_route('get_book', '/api/books/{id}')        # GET detail 1 buku
    config.add_route('create_book', '/api/books')          # POST buku baru
    config.add_route('update_book', '/api/books/{id}')     # PUT update buku
    config.add_route('delete_book', '/api/books/{id}')     # DELETE buku
    config.add_route('home', '/')                     # GET home