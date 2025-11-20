import React from 'react';
import Portrait from './Portrait';
import './PortraitGallery.css';

export default function PortraitGallery({ portraits, activePortrait }) {
  // Separate Fat Lady from others
  const fatLady = portraits.find(p => p.id === 'fat_lady');
  const otherPortraits = portraits.filter(p => p.id !== 'fat_lady');
  
  return (
    <div className="portrait-gallery">
      <h2>The Whispering Frames</h2>
      <div className="portrait-grid">
        {/* Fat Lady - tall portrait on the left */}
        {fatLady && (
          <div className="fat-lady-portrait">
            <Portrait
              key={fatLady.id}
              name={fatLady.name}
              isAwake={fatLady.id === activePortrait}
              sleepImage={fatLady.sleepImage}
              awakeGif={fatLady.awakeGif}
            />
          </div>
        )}
        
        {/* Square grid for the other 4 portraits */}
        <div className="square-portraits">
          {otherPortraits.map(portrait => (
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
    </div>
  );
}

