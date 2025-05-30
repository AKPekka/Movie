// src/services/api.js
const API_BASE_URL =
  process.env.REACT_APP_API_BASE || 'http://localhost:5002/api';

export const searchMovies = async (query, page = 1) => {
  const response = await fetch(`${API_BASE_URL}/search?query=${encodeURIComponent(query)}&page=${page}`);
  if (!response.ok) throw new Error('Failed to search movies');
  return response.json();
};

export const getAutocompleteSuggestions = async (query) => {
  if (!query || query.length < 2) return { results: [] };

  const response = await fetch(`${API_BASE_URL}/autocomplete?query=${encodeURIComponent(query)}`);
  if (!response.ok) throw new Error('Failed to get suggestions');
  return response.json();
};

export const getMovieDetails = async (movieId) => {
  const response = await fetch(`${API_BASE_URL}/movie/${movieId}`);
  if (!response.ok) throw new Error('Failed to fetch movie details');
  return response.json();
};

export const getRecommendations = async (movieId, limit = 10) => {
  const response = await fetch(`${API_BASE_URL}/recommendations/movie/${movieId}?limit=${limit}`);
  if (!response.ok) throw new Error('Failed to get recommendations');
  return response.json();
};

export const getHybridRecommendations = async (movieIds, limit = 10) => {
  const movieIdsParam = Array.isArray(movieIds) ? movieIds.join(',') : movieIds;
  const response = await fetch(`${API_BASE_URL}/recommendations/hybrid?movie_ids=${movieIdsParam}&limit=${limit}`);
  if (!response.ok) throw new Error('Failed to get hybrid recommendations');
  return response.json();
};

export const getTrendingMovies = async (timeWindow = 'week') => {
  const response = await fetch(`${API_BASE_URL}/trending?time_window=${timeWindow}`);
  if (!response.ok) throw new Error('Failed to get trending movies');
  return response.json();
};
