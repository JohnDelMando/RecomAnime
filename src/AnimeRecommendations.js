import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './AnimeRecommendations.css';

const AnimeRecommendations = () => {
  const [genre, setGenre] = useState('');
  const [animeList, setAnimeList] = useState([]);
  const [top100Anime, setTop100Anime] = useState([]);

  // Fetch anime recommendations based on genre
  const fetchAnime = () => {
    axios.get('http://localhost:5000/api/get_genreAnime', {
      params: { genre: genre }
    })
    .then(response => {
      setAnimeList(response.data);
    })
    .catch(error => {
      console.error('Error fetching anime data!', error);
    });
  };

  // Fetch the top 100 anime
  useEffect(() => {
    axios.get('http://localhost:5000/api/get_yearlyAnime', {
      params: { year: new Date().getFullYear() } // Fetch the current year's top anime
    })
    .then(response => {
      setTop100Anime(response.data);
    })
    .catch(error => {
      console.error('Error fetching top 100 anime!', error);
    });
  }, []);

  return (
    <div>
      <h1>Anime Recommendations</h1>
      <input 
        type="text" 
        placeholder="Enter genre" 
        value={genre}
        onChange={(e) => setGenre(e.target.value)}
      />
      <button onClick={fetchAnime}>Get Recommendations</button>
      
      <div className="anime-list">
        {animeList.map(anime => (
          <div key={anime.id} className="anime-item">
            <h3>{anime.title.romaji}</h3>
            <img src={anime.coverImage.large} alt={anime.title.romaji} />
            <p>{anime.description || 'No description available'}</p>
          </div>
        ))}
      </div>

      <h2>Top 100 Anime</h2>
      <div className="top-100-anime-list">
        {top100Anime.map(anime => (
          <div key={anime.id} className="anime-item">
            <h3>{anime.title.romaji}</h3>
            <img src={anime.coverImage.large} alt={anime.title.romaji} />
            <p>{anime.description || 'No description available'}</p>
            {/* Conditional rendering to ensure anime.genres is defined */}
            {anime.genres && <p><strong>Genres:</strong> {anime.genres.join(', ')}</p>}
            {/* Conditional rendering to ensure anime.tags is defined */}
            {anime.tags && <p><strong>Tags:</strong> {anime.tags.map(tag => tag.name).join(', ')}</p>}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AnimeRecommendations;