// src/pages/Search.jsx
import React, { useState, useEffect } from 'react';
import { useSearchParams, useLocation } from 'react-router-dom';
import MovieGrid from '../components/MovieGrid';
import { searchMovies, getTrendingMovies } from '../services/api';

const Search = () => {
  const [searchParams] = useSearchParams();
  const location = useLocation();
  const query = searchParams.get('q') || '';
  const searchType = searchParams.get('type') || 'movie';
  const isTrendingPage = location.pathname === '/trending';

  const [movies, setMovies] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  useEffect(() => {
    const fetchMovies = async () => {
      setIsLoading(true);
      setError(null);

      try {
        let data;
        if (isTrendingPage) {
          data = await getTrendingMovies();
        } else if (query) {
          data = await searchMovies(query, page, searchType);
        } else {
          setMovies([]);
          setIsLoading(false);
          return;
        }
        
        setMovies(data.results || []);
        setTotalPages(data.total_pages || 0);
      } catch (err) {
        setError(isTrendingPage ? 'Failed to load trending movies' : 'Failed to search movies');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMovies();
  }, [query, page, isTrendingPage, searchType]);

  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1);
      window.scrollTo(0, 0);
    }
  };

  const handlePrevPage = () => {
    if (page > 1) {
      setPage(page - 1);
      window.scrollTo(0, 0);
    }
  };

  const getPageTitle = () => {
    if (isTrendingPage) return 'Trending Movies';
    if (query) {
      if (searchType === 'person') return `Movies featuring "${query}"`;
      return `Search results for "${query}"`;
    }
    return 'Search movies';
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold text-white mb-8">
        {getPageTitle()}
      </h1>

      <MovieGrid
        movies={movies}
        isLoading={isLoading}
        error={error}
      />

      {totalPages > 1 && !isTrendingPage && searchType !== 'person' && (
        <div className="flex items-center justify-center space-x-4 mt-12">
          <button
            onClick={handlePrevPage}
            disabled={page === 1}
            className={`px-4 py-2 rounded-md ${
              page === 1
                ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            Previous
          </button>
          <span className="text-gray-400">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={handleNextPage}
            disabled={page === totalPages}
            className={`px-4 py-2 rounded-md ${
              page === totalPages
                ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default Search;
