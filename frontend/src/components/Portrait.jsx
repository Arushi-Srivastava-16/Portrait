import React from 'react';
import './Portrait.css';

export default function Portrait({ name, isAwake, sleepImage, awakeGif }) {
  return (
    <div className={`portrait ${isAwake ? 'awake' : 'sleeping'}`}>
      <div className="portrait-frame">
        {isAwake && awakeGif ? (
          <img 
            src={awakeGif} 
            alt={`${name} awake`}
            className="portrait-image"
            onError={(e) => {
              // Fallback to sleep image if awake gif doesn't exist
              e.target.src = sleepImage || '/portraits/default-sleep.png';
            }}
          />
        ) : (
          <img 
            src={sleepImage || '/portraits/default-sleep.png'} 
            alt={`${name} sleeping`}
            className="portrait-image"
          />
        )}
      </div>
      <p className="portrait-name">{name}</p>
      {isAwake && <div className="speaking-indicator">💬</div>}
    </div>
  );
}

