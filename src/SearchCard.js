import React, { useState } from 'react';
import './SearchCard.css';

const SearchCard = () => {
    // bool for handleSearch, set to false by default
    const [showData, setShowData] = useState(false);

    // handles the search bar's position
    const handleSearch = () => {
        setShowData(true);
    };

    // temporary data - will change
    const data = [
        "Naruto", "Attack on Titan", "One Piece",
        "My Hero Academia", "Fullmetal Alchemist",
        "Death Note", "Sword Art Online", "Demon Slayer",
        "Tokyo Ghoul", "Hunter x Hunter", "Bleach", "Dragon Ball Z"
    ];

    // html return
    return (
        <div className={`search-container ${showData ? 'data-shown' : ''}`}>
            <div className="search-bar">
                <input type="text" placeholder="What are you looking for?" />
                <button onClick={handleSearch}>ENTER</button>
            </div>
            {showData && (
                <div className="data-container">
                    {data.map((item, index) => (
                        <div key={index} className="data-item">{item}</div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SearchCard;