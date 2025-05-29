# MovieMind - Movie Recommendation App

A full-stack movie recommendation application that helps users discover new movies based on their preferences using content-based and hybrid recommendation algorithms.

## Features

- **Smart Search**: Intelligent movie search with auto-complete suggestions
- **Content-Based Recommendations**: Get movie suggestions based on genres, actors, directors, and themes
- **Hybrid Recommendations**: Combine multiple movies you love for more accurate recommendations
- **Trending Movies**: Stay up-to-date with the latest trending films
- **Detailed Movie Information**: View comprehensive movie details including cast, crew, and ratings
- **Responsive Design**: Optimized for desktop and mobile devices

## Architecture

### Frontend
- **React 18** with functional components and hooks
- **React Router** for client-side routing
- **Tailwind CSS** for styling and responsive design
- **Modern UI/UX** with dark theme and smooth animations

### Backend
- **Flask** REST API with CORS support
- **TMDb API** integration for movie data
- **Caching system** for improved performance
- **Content-based recommendation engine**
- **Hybrid recommendation algorithms**

## Quick Start

### Prerequisites
- Node.js 14+ and npm
- Python 3.8+
- TMDb API key (free from https://www.themoviedb.org/settings/api)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd movie-recommendation-app
   ```

2. **Backend Setup**
   ```bash
   cd backend
   
   # Install Python dependencies
   pip install -r requirements.txt
   
   # The API key is already configured in h.env, but you can update it if needed
   # TMDB_API_KEY=your_api_key_here
   
   # Start the Flask development server
   python app.py
   ```
   The backend will run on `http://localhost:5002`

3. **Frontend Setup**
   ```bash
   cd frontend/movie-recommendation-ui
   
   # Install Node.js dependencies
   npm install
   
   # Start the React development server
   npm start
   ```
   The frontend will run on `http://localhost:3000`

### Running the Application

1. **Start the Backend**: In the `backend` directory, run `python app.py`
2. **Start the Frontend**: In the `frontend/movie-recommendation-ui` directory, run `npm start`
3. **Open your browser**: Navigate to `http://localhost:3000`

## API Endpoints

### Movie Search & Discovery
- `GET /api/search?query={query}&page={page}` - Search movies by title
- `GET /api/autocomplete?query={query}` - Get autocomplete suggestions
- `GET /api/trending?time_window={week|day}` - Get trending movies

### Movie Details & Recommendations
- `GET /api/movie/{movie_id}` - Get detailed movie information
- `GET /api/recommendations/movie/{movie_id}?limit={limit}` - Get content-based recommendations
- `GET /api/recommendations/hybrid?movie_ids={id1,id2,id3}&limit={limit}` - Get hybrid recommendations

### System
- `GET /api/health` - Health check and cache statistics
- `POST /api/admin/cache/clear` - Clear application cache

## Project Structure

```
movie-recommendation-app/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── h.env                  # Environment variables
│   ├── requirements.txt       # Python dependencies
│   ├── services/
│   │   └── tmdb_service.py    # TMDb API integration
│   ├── utils/
│   │   └── recommendation.py  # Recommendation algorithms
│   └── cache/
│       └── __init__.py        # Caching implementation
└── frontend/
    └── movie-recommendation-ui/
        ├── public/
        │   └── index.html     # HTML template
        ├── src/
        │   ├── components/    # React components
        │   ├── pages/         # React pages/routes
        │   ├── services/      # API service layer
        │   ├── App.js         # Main React component
        │   ├── index.js       # React entry point
        │   └── index.css      # Global styles
        ├── package.json       # Node.js dependencies
        ├── tailwind.config.js # Tailwind CSS configuration
        └── postcss.config.js  # PostCSS configuration
```

## Key Components

### Backend Components
- **TMDb Service**: Handles all interactions with The Movie Database API
- **Recommendation Engine**: Implements content-based and hybrid algorithms
- **Caching System**: TTL-based caching for improved performance
- **Flask API**: RESTful endpoints for frontend communication

### Frontend Components
- **AutocompleteSearch**: Smart search with real-time suggestions
- **MovieCard**: Reusable movie display component
- **MovieGrid**: Grid layout for movie collections
- **MoviePage**: Detailed movie view with recommendations
- **Navbar**: Navigation with responsive design

## Recommendation Algorithms

### Content-Based Filtering
- Analyzes movie genres, keywords, and metadata
- Scores recommendations based on similarity metrics
- Considers vote averages and popularity factors

### Hybrid Recommendations
- Combines multiple movie preferences
- Weights recommendations by frequency and relevance
- Provides diverse and accurate suggestions

## Technologies Used

### Frontend
- React 18
- React Router 6
- Tailwind CSS 3
- Modern JavaScript (ES6+)

### Backend
- Flask 2.3
- Python 3.8+
- Requests library
- Cachetools
- Python-dotenv

### External APIs
- The Movie Database (TMDb) API v3

## Performance Features

- **Caching**: Intelligent caching of API responses
- **Rate Limiting**: Respectful API usage with built-in rate limiting
- **Lazy Loading**: Optimized image loading
- **Responsive Design**: Mobile-first approach
- **Error Handling**: Graceful error handling throughout the application

## Future Enhancements

- User authentication and personalized recommendations
- Watchlist and favorites functionality
- Advanced filtering options
- Social features (ratings, reviews)
- Machine learning-based collaborative filtering
- Integration with streaming services

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License. 
