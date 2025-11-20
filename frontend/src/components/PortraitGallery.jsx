import React from 'react';
import Portrait from './Portrait';
import './PortraitGallery.css';

export default function PortraitGallery({ portraits, activePortrait }) {
  return (
    <div className="portrait-gallery">
      <h2>Portraits</h2>
      <div className="portrait-grid">
        {portraits.map(portrait => (
          <Portrait
            key={portrait.id}
            name={portrait.name}
            isAwake={portrait.id === activePortrait}
            sleepImage={portrait.sleepImage}
            awakeGif={portrait.awakeGif}
          />
        ))}
      </div>
    </div>
  );
}

