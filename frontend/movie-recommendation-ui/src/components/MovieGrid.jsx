// src/components/MovieGrid.jsx
import React from 'react';
import MovieCard from './MovieCard';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

const MovieGrid = ({ movies, isLoading, error, title }) => {
  return (
    <div className="w-full">
      {title && (
        <h2 className="text-2xl font-bold text-white mb-6">{title}</h2>
      )}

      {isLoading ? (
        <div className="flex justify-center py-12">
          <LoadingSpinner />
        </div>
      ) : error ? (
        <ErrorMessage message={error} />
      ) : movies && movies.length > 0 ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
          {movies.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-400">No movies found</p>
        </div>
      )}
    </div>
  );
};

export default MovieGrid;
