// src/components/AutocompleteSearch.jsx
import React, { useState, useEffect, useRef } from 'react';
import { getAutocompleteSuggestions } from '../services/api';
import { useNavigate } from 'react-router-dom';

const AutocompleteSearch = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const searchRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (query.length < 2) {
        setSuggestions([]);
        return;
      }

      setIsLoading(true);
      try {
        const data = await getAutocompleteSuggestions(query);
        setSuggestions(data.results || []);
      } catch (error) {
        console.error('Error fetching suggestions:', error);
      } finally {
        setIsLoading(false);
      }
    };

    const debounceTimeout = setTimeout(fetchSuggestions, 300);
    return () => clearTimeout(debounceTimeout);
  }, [query]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query)}`);
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (movieId) => {
    navigate(`/movie/${movieId}`);
    setShowSuggestions(false);
    setQuery('');
  };

  return (
    <div className="relative w-full max-w-xl search-container" ref={searchRef}>
      <form onSubmit={handleSearch} className="w-full">
        <div className="relative">
          <input
            type="text"
            className="w-full py-3 px-4 pr-12 rounded-full bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent relative z-10"
            placeholder="Search for movies..."
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setShowSuggestions(true);
            }}
            onFocus={() => setShowSuggestions(true)}
          />
          <button
            type="submit"
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white z-20"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </div>
      </form>

      {showSuggestions && (query.length >= 2) && (
        <div className="absolute w-full mt-1 bg-gray-900 border border-gray-700 rounded-md shadow-lg max-h-96 overflow-y-auto search-suggestions">
          {isLoading ? (
            <div className="p-4 text-center text-gray-400">Loading suggestions...</div>
          ) : suggestions.length > 0 ? (
            <ul>
              {suggestions.map((movie) => (
                <li
                  key={movie.id}
                  className="px-4 py-3 hover:bg-gray-800 cursor-pointer flex items-center gap-3 border-b border-gray-800"
                  onClick={() => handleSuggestionClick(movie.id)}
                >
                  {movie.poster_url ? (
                    <img
                      src={movie.poster_url}
                      alt={movie.title}
                      className="w-10 h-15 rounded-sm object-cover"
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                  ) : (
                    <div className="w-10 h-15 bg-gray-700 rounded-sm flex items-center justify-center">
                      <span className="text-xs text-gray-400">🎬</span>
                    </div>
                  )}
                  <div>
                    <div className="text-white font-medium">{movie.title}</div>
                    {movie.year && (
                      <div className="text-xs text-gray-400">
                        {movie.year}
                      </div>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <div className="p-4 text-center text-gray-400">No results found</div>
          )}
        </div>
      )}
    </div>
  );
};

export default AutocompleteSearch;
