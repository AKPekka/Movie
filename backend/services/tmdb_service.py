"""Service for interacting with the TMDb API."""
import requests
from urllib.parse import quote
import time
from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL
from cache import cached

class TMDbService:
    """Service class for TMDb API operations."""

    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.base_url = TMDB_BASE_URL
        self.image_base_url = TMDB_IMAGE_BASE_URL
        self.request_count = 0
        self.last_request_time = 0

    def _make_request(self, endpoint, params=None):
        """Make a rate-limited request to the TMDb API."""
        # Basic rate limiting (40 requests per 10 seconds)
        current_time = time.time()
        if current_time - self.last_request_time < 0.25:  # Limit to ~4 requests per second
            time.sleep(0.25 - (current_time - self.last_request_time))

        if params is None:
            params = {}

        params['api_key'] = self.api_key

        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        self.last_request_time = time.time()

        if response.status_code == 200:
            return response.json()
        else:
            error_message = f"Error {response.status_code}: {response.text}"
            raise Exception(error_message)

    @cached
    def search_movies(self, query, page=1):
        """Search for movies matching a query."""
        endpoint = "search/movie"
        params = {
            'query': query,
            'page': page,
            'include_adult': 'false'
        }

        results = self._make_request(endpoint, params)

        # Enhance movie data with poster paths
        for movie in results.get('results', []):
            if movie.get('poster_path'):
                movie['poster_url'] = f"{self.image_base_url}{movie['poster_path']}"
            else:
                movie['poster_url'] = None

        return results

    @cached
    def get_movie_details(self, movie_id):
        """Get detailed information about a movie."""
        endpoint = f"movie/{movie_id}"
        params = {
            'append_to_response': 'credits,videos,keywords'
        }

        movie = self._make_request(endpoint, params)

        # Add full poster URL
        if movie.get('poster_path'):
            movie['poster_url'] = f"{self.image_base_url}{movie['poster_path']}"
        else:
            movie['poster_url'] = None

        return movie

    @cached
    def get_movie_recommendations(self, movie_id, page=1):
        """Get movie recommendations based on a movie."""
        endpoint = f"movie/{movie_id}/recommendations"
        params = {
            'page': page
        }

        results = self._make_request(endpoint, params)

        # Enhance movie data with poster paths
        for movie in results.get('results', []):
            if movie.get('poster_path'):
                movie['poster_url'] = f"{self.image_base_url}{movie['poster_path']}"
            else:
                movie['poster_url'] = None

        return results

    @cached
    def get_trending_movies(self, time_window='week'):
        """Get trending movies for the day or week."""
        if time_window not in ['day', 'week']:
            time_window = 'week'

        endpoint = f"trending/movie/{time_window}"

        results = self._make_request(endpoint)

        # Enhance movie data with poster paths
        for movie in results.get('results', []):
            if movie.get('poster_path'):
                movie['poster_url'] = f"{self.image_base_url}{movie['poster_path']}"
            else:
                movie['poster_url'] = None

        return results

    @cached
    def auto_complete(self, query):
        """Get movie suggestions for auto-complete."""
        if not query or len(query) < 2:
            return {'results': []}

        results = self.search_movies(query)

        # Limit results and simplify data for autocomplete
        simple_results = []
        for movie in results.get('results', [])[:10]:  # Limit to 10 results for autocomplete
            simple_results.append({
                'id': movie.get('id'),
                'title': movie.get('title'),
                'year': movie.get('release_date', '')[:4] if movie.get('release_date') else '',
                'poster_url': movie.get('poster_url')
            })

        return {'results': simple_results}
