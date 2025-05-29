"""Main Flask application for movie recommendations."""
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading
import json
import os

from services.tmdb_service import TMDbService
from utils.recommendation import (
    get_content_based_recommendations,
    get_hybrid_recommendations,
    get_fallback_recommendations
)
from cache import get_cache_stats, clear_cache

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize services
tmdb_service = TMDbService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'timestamp': time.time(),
        'cache': get_cache_stats()
    })

@app.route('/api/search', methods=['GET'])
def search_movies():
    """Search for movies by title."""
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        results = tmdb_service.search_movies(query, page)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/autocomplete', methods=['GET'])
def autocomplete():
    """Get movie suggestions for autocomplete."""
    query = request.args.get('query', '')

    if not query or len(query) < 2:
        return jsonify({'results': []})

    try:
        results = tmdb_service.auto_complete(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get detailed information about a movie."""
    try:
        movie = tmdb_service.get_movie_details(movie_id)
        return jsonify(movie)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/movie/<int:movie_id>', methods=['GET'])
def get_recommendations_by_movie(movie_id):
    """Get movie recommendations based on a single movie."""
    limit = request.args.get('limit', 10, type=int)

    try:
        recommendations = get_content_based_recommendations(movie_id, limit)
        return jsonify({'results': recommendations})
    except Exception as e:
        # Fallback to trending if recommendations fail
        try:
            fallback = get_fallback_recommendations()
            return jsonify({
                'results': fallback,
                'fallback': True,
                'error': str(e)
            })
        except Exception as fallback_error:
            return jsonify({'error': str(fallback_error)}), 500

@app.route('/api/recommendations/hybrid', methods=['GET'])
def get_hybrid_recommendations_endpoint():
    """Get hybrid recommendations based on multiple movies."""
    movie_ids = request.args.get('movie_ids', '')
    limit = request.args.get('limit', 10, type=int)

    if not movie_ids:
        return jsonify({'error': 'movie_ids parameter is required'}), 400

    try:
        # Parse movie IDs from comma-separated string
        movie_id_list = [int(id.strip()) for id in movie_ids.split(',') if id.strip()]

        if not movie_id_list:
            return jsonify({'error': 'No valid movie IDs provided'}), 400

        recommendations = get_hybrid_recommendations(movie_id_list, limit)
        return jsonify({'results': recommendations})
    except Exception as e:
        # Fallback to trending if recommendations fail
        try:
            fallback = get_fallback_recommendations()
            return jsonify({
                'results': fallback,
                'fallback': True,
                'error': str(e)
            })
        except Exception as fallback_error:
            return jsonify({'error': str(fallback_error)}), 500

@app.route('/api/trending', methods=['GET'])
def get_trending():
    """Get trending movies."""
    time_window = request.args.get('time_window', 'week')

    try:
        results = tmdb_service.get_trending_movies(time_window)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/cache/clear', methods=['POST'])
def clear_cache_endpoint():
    """Clear the application cache (admin endpoint)."""
    clear_cache()
    return jsonify({
        'status': 'success',
        'message': 'Cache cleared successfully',
        'cache': get_cache_stats()
    })

if __name__ == '__main__':
    # Check if TMDB API key is set
    if not os.getenv("TMDB_API_KEY"):
        print("Warning: TMDB_API_KEY is not set. Please set it in your .env file.")

    app.run(debug=True, port=5002)
