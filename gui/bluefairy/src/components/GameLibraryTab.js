import React, { useState } from 'react';

const GameLibraryTab = ({ loadGameFromPgn }) => {
    const [pgnInput, setPgnInput] = useState('');

    const handlePgnInputChange = (event) => {
        setPgnInput(event.target.value);
    };

    return (
        <div>
        <textarea
            value={pgnInput}
            onChange={handlePgnInputChange}
            rows="10" // Adjust the number of rows as needed
            style={{ width: '100%' }} // Adjust styling as needed
        />
        <button onClick={() => loadGameFromPgn(pgnInput)}>Load PGN</button>
            <input type="text" placeholder="Search by player" />
            <input type="text" placeholder="Search by date" />
            {/* Additional search criteria */}
        </div>
    );
};

export default GameLibraryTab;