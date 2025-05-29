// src/pages/MoviePage.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getMovieDetails, getRecommendations } from '../services/api';
import MovieGrid from '../components/MovieGrid';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const MoviePage = () => {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingRecs, setIsLoadingRecs] = useState(true);
  const [error, setError] = useState(null);
  const [recError, setRecError] = useState(null);

  useEffect(() => {
    const fetchMovieDetails = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const data = await getMovieDetails(id);
        setMovie(data);
        document.title = `${data.title} - MovieMind`;
      } catch (err) {
        setError('Failed to load movie details');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    const fetchRecommendations = async () => {
      setIsLoadingRecs(true);
      setRecError(null);

      try {
        const data = await getRecommendations(id);
        setRecommendations(data.results || []);
      } catch (err) {
        setRecError('Failed to load recommendations');
        console.error(err);
      } finally {
        setIsLoadingRecs(false);
      }
    };

    if (id) {
      fetchMovieDetails();
      fetchRecommendations();
    }

    return () => {
      document.title = 'MovieMind';
    };
  }, [id]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <ErrorMessage message={error} />
      </div>
    );
  }

  if (!movie) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <ErrorMessage message="Movie not found" />
      </div>
    );
  }

  const backdropUrl = movie.backdrop_path
    ? `https://image.tmdb.org/t/p/original${movie.backdrop_path}`
    : null;

  return (
    <div className="min-h-screen">
      {/* Backdrop */}
      {backdropUrl && (
        <div className="relative h-96 overflow-hidden">
          <div className="absolute inset-0 bg-black opacity-50 z-10"></div>
          <img
            src={backdropUrl}
            alt={movie.title}
            className="w-full h-full object-cover"
          />
        </div>
      )}

      {/* Movie details */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className={`${backdropUrl ? '-mt-32 relative z-20' : 'pt-8'} pb-16`}>
          <div className="relative bg-black rounded-lg shadow-xl overflow-hidden">
            <div className="md:flex">
              <div className="md:flex-shrink-0">
                {movie.poster_url ? (
                  <img
                    className="h-full w-full object-cover md:w-64"
                    src={movie.poster_url}
                    alt={movie.title}
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                ) : (
                  <div className="h-96 w-full md:w-64 bg-black flex items-center justify-center">
                    <span className="text-8xl text-gray-600">🎬</span>
                  </div>
                )}
              </div>
              <div className="p-8">
                <div className="flex items-center">
                  <h1 className="text-3xl font-bold text-white">{movie.title}</h1>
                  {movie.release_date && (
                    <span className="ml-4 text-gray-400">
                      ({new Date(movie.release_date).getFullYear()})
                    </span>
                  )}
                </div>

                {movie.tagline && (
                  <p className="mt-2 text-gray-400 italic">{movie.tagline}</p>
                )}

                <div className="mt-4 flex items-center space-x-4">
                  {movie.vote_average > 0 && (
                    <div className="flex items-center">
                      <svg className="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                      </svg>
                      <span className="ml-1 text-white">
                        {movie.vote_average.toFixed(1)}
                      </span>
                    </div>
                  )}

                  {movie.runtime > 0 && (
                    <span className="text-gray-400">
                      {Math.floor(movie.runtime / 60)}h {movie.runtime % 60}m
                    </span>
                  )}
                </div>

                {movie.genres && movie.genres.length > 0 && (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {movie.genres.map(genre => (
                      <span
                        key={genre.id}
                        className="px-3 py-1 bg-gray-800 text-gray-300 text-sm rounded-full"
                      >
                        {genre.name}
                      </span>
                    ))}
                  </div>
                )}

                {movie.overview && (
                  <div className="mt-6">
                    <h3 className="text-lg font-medium text-white">Overview</h3>
                    <p className="mt-2 text-gray-300 leading-relaxed">{movie.overview}</p>
                  </div>
                )}

                {movie.credits && movie.credits.crew && (
                  <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                    {movie.credits.crew
                      .filter(person => person.job === 'Director')
                      .slice(0, 1)
                      .map(person => (
                        <div key={person.id}>
                          <h4 className="text-sm text-gray-400">Director</h4>
                          <p className="text-white">{person.name}</p>
                        </div>
                      ))}

                    {movie.production_companies && movie.production_companies.length > 0 && (
                      <div>
                        <h4 className="text-sm text-gray-400">Studio</h4>
                        <p className="text-white">{movie.production_companies[0].name}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Cast section */}
        {movie.credits && movie.credits.cast && movie.credits.cast.length > 0 && (
          <div className="mb-16">
            <h2 className="text-2xl font-bold text-white mb-6">Cast</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {movie.credits.cast.slice(0, 12).map(person => (
                <div key={person.id} className="text-center">
                  {person.profile_path ? (
                    <img
                      src={`https://image.tmdb.org/t/p/w185${person.profile_path}`}
                      alt={person.name}
                      className="w-full h-32 object-cover rounded-lg mb-2"
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                  ) : (
                    <div className="w-full h-32 bg-black rounded-lg mb-2 flex items-center justify-center">
                      <span className="text-2xl text-gray-600">👤</span>
                    </div>
                  )}
                  <h3 className="text-white text-sm font-medium">{person.name}</h3>
                  <p className="text-gray-400 text-xs">{person.character}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations section */}
        <div className="mb-16">
          <MovieGrid
            movies={recommendations}
            isLoading={isLoadingRecs}
            error={recError}
            title="Recommended Movies"
          />
        </div>
      </div>
    </div>
  );
};

export default MoviePage;
