"""Utility functions for movie recommendations."""
from services.tmdb_service import TMDbService
from cache import cached
import random

tmdb_service = TMDbService()

@cached
def get_content_based_recommendations(movie_id, limit=10):
    """
    Get content-based movie recommendations.

    This uses TMDb's recommendation API and enhances it with additional
    filtering based on genres and keywords.
    """
    # Get movie details to extract genres and keywords
    movie_details = tmdb_service.get_movie_details(movie_id)

    # Get TMDb recommendations
    recommendations = tmdb_service.get_movie_recommendations(movie_id)

    # Extract genre ids and keyword ids from the source movie
    genre_ids = [genre['id'] for genre in movie_details.get('genres', [])]
    keyword_ids = [keyword['id'] for keyword in movie_details.get('keywords', {}).get('keywords', [])]

    # Score the recommendations based on similarity
    scored_recommendations = []

    for movie in recommendations.get('results', []):
        score = 0

        # Score based on genre overlap
        movie_genre_ids = movie.get('genre_ids', [])
        genre_overlap = set(genre_ids).intersection(set(movie_genre_ids))
        score += len(genre_overlap) * 2  # Weight genres more heavily

        # Get additional details for keywords if needed
        if keyword_ids and score > 0:
            movie_detail = tmdb_service.get_movie_details(movie['id'])
            movie_keywords = [kw['id'] for kw in movie_detail.get('keywords', {}).get('keywords', [])]
            keyword_overlap = set(keyword_ids).intersection(set(movie_keywords))
            score += len(keyword_overlap)

        # Add vote average as a factor (normalized to 0-1 range)
        if movie.get('vote_average'):
            score += movie['vote_average'] / 10

        # Add popularity as a small factor (normalized)
        if movie.get('popularity'):
            score += min(movie['popularity'] / 100, 1)

        scored_recommendations.append({
            'movie': movie,
            'score': score
        })

    # Sort by score and limit results
    scored_recommendations.sort(key=lambda x: x['score'], reverse=True)

    # Return just the movies, not the scores
    return [item['movie'] for item in scored_recommendations[:limit]]

@cached
def get_hybrid_recommendations(movie_ids, limit=10):
    """
    Get hybrid recommendations based on multiple input movies.

    This combines recommendations from multiple movies and ranks them.
    """
    if not movie_ids:
        return []

    # Get recommendations for each movie
    all_recommendations = []

    for movie_id in movie_ids:
        try:
            recommendations = get_content_based_recommendations(movie_id, limit=limit)
            all_recommendations.extend(recommendations)
        except Exception as e:
            print(f"Error getting recommendations for movie {movie_id}: {e}")

    # Remove duplicates by movie id
    unique_recommendations = {}
    for movie in all_recommendations:
        movie_id = movie['id']
        if movie_id not in unique_recommendations:
            unique_recommendations[movie_id] = {
                'movie': movie,
                'count': 1
            }
        else:
            unique_recommendations[movie_id]['count'] += 1

    # Score by frequency of occurrence and other factors
    scored_recommendations = []
    for movie_id, data in unique_recommendations.items():
        movie = data['movie']
        count = data['count']

        # Base score is the frequency of the recommendation
        score = count * 3

        # Add vote average as a factor
        if movie.get('vote_average'):
            score += movie['vote_average'] / 10

        # Add popularity as a small factor
        if movie.get('popularity'):
            score += min(movie['popularity'] / 100, 0.5)

        scored_recommendations.append({
            'movie': movie,
            'score': score
        })

    # Sort by score and limit results
    scored_recommendations.sort(key=lambda x: x['score'], reverse=True)

    # Return just the movies, not the scores
    return [item['movie'] for item in scored_recommendations[:limit]]

@cached
def get_fallback_recommendations():
    """Get trending movies as a fallback when no specific recommendations exist."""
    trending = tmdb_service.get_trending_movies()
    return trending.get('results', [])[:10]
