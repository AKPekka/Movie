// src/components/MovieCard.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const MovieCard = ({ movie }) => {
  const posterUrl = movie.poster_url || '/placeholder-poster.png';

  return (
    <Link
      to={`/movie/${movie.id}`}
      className="group bg-gray-900 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 hover:scale-[1.02]"
    >
      <div className="relative pb-[150%]">
        <img
          src={posterUrl}
          alt={movie.title}
          className="absolute inset-0 w-full h-full object-cover"
          loading="lazy"
          onError={(e) => {
            e.target.src = '/placeholder-poster.png';
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <div className="absolute bottom-0 left-0 right-0 p-4">
            {movie.vote_average > 0 && (
              <div className="inline-block px-2 py-1 rounded-md bg-blue-600 text-white text-xs font-bold mb-2">
                {movie.vote_average.toFixed(1)}
              </div>
            )}
            <p className="text-gray-300 text-sm line-clamp-3">{movie.overview}</p>
          </div>
        </div>
      </div>
      <div className="p-4">
        <h3 className="font-bold text-white line-clamp-1">{movie.title}</h3>
        {movie.release_date && (
          <p className="text-gray-400 text-sm mt-1">
            {new Date(movie.release_date).getFullYear()}
          </p>
        )}
      </div>
    </Link>
  );
};

export default MovieCard;
