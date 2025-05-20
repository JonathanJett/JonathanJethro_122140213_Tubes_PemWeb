import requests

def search_books(query):
    url = f"https://openlibrary.org/search.json?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = []
        for doc in data.get('docs', []):
            results.append({
                'title': doc.get('title'),
                'author': doc.get('author_name', ['Unknown'])[0],
            })
        return results
    return []
