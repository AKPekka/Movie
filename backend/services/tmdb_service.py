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

    @cached
    def get_movie_watch_providers(self, movie_id):
        """Get watch provider information for a movie."""
        endpoint = f"movie/{movie_id}/watch/providers"
        # The API returns results for all regions by default.
        # We are primarily interested in US providers, which the frontend will filter.
        return self._make_request(endpoint)

    @cached
    def search_person_movies(self, query, page=1):
        """Search for movies by a person (actor/director)."""
        # Step 1: Search for the person
        person_search_endpoint = "search/person"
        person_params = {
            'query': query,
            'page': page # Use page for person search as well, though we primarily want the first result
        }
        person_search_results = self._make_request(person_search_endpoint, person_params)

        if not person_search_results or not person_search_results.get('results'):
            return {'results': [], 'page': 1, 'total_pages': 0, 'total_results': 0} # TMDb like structure

        # Assuming the first result is the correct person
        person = person_search_results['results'][0]
        person_id = person['id']

        # Step 2: Get movie credits for that person
        movie_credits_endpoint = f"person/{person_id}/movie_credits"
        # The movie_credits endpoint for a person doesn't support pagination directly in the API call for combined credits.
        # It returns all cast and crew roles. We will return this as a single "page".
        movie_credits = self._make_request(movie_credits_endpoint)

        # Combine cast and crew, and ensure unique movies (a person can be cast and crew in the same movie)
        all_roles = movie_credits.get('cast', []) + movie_credits.get('crew', []) 
        movies_map = {}
        for role in all_roles:
            # We need a consistent movie structure, similar to search_movies results
            if role.get('id') not in movies_map:
                movies_map[role['id']] = {
                    'id': role.get('id'),
                    'title': role.get('title') or role.get('name'), # Some might use 'name' for TV shows
                    'poster_path': role.get('poster_path'),
                    'release_date': role.get('release_date') or role.get('first_air_date'),
                    'overview': role.get('overview'),
                    'vote_average': role.get('vote_average'),
                    'popularity': role.get('popularity'),
                    # Add poster_url like in search_movies
                    'poster_url': f"{self.image_base_url}{role['poster_path']}" if role.get('poster_path') else None,
                    'job': role.get('job', None), # For crew
                    'character': role.get('character', None) # For cast
                }
        
        # Sort by popularity (descending) as a default sort order for person's movies
        # The API returns cast and crew roles; they don't have a top-level 'popularity' like movies in a general search.
        # We'll sort by the movie's own popularity field.
        sorted_movies = sorted(list(movies_map.values()), key=lambda x: x.get('popularity', 0), reverse=True)

        # Mimic the structure of search_movies response for consistency
        return {
            'results': sorted_movies,
            'page': 1, # Person credits are not paginated in the same way
            'total_pages': 1,
            'total_results': len(sorted_movies)
        }
