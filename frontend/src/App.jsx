import React, { useState } from 'react';
import CameraFeed from './components/CameraFeed';
import PortraitGallery from './components/PortraitGallery';
import ConversationLog from './components/ConversationLog';
import axios from 'axios';
import './App.css';

const PORTRAITS = [
  { id: 'fat_lady', name: 'Fat Lady', sleepImage: '/portraits/fat-lady-sleep.png', awakeGif: '/portraits/fat-lady-awake.gif' },
  { id: 'sir_cadogan', name: 'Sir Cadogan', sleepImage: '/portraits/sir-cadogan-sleep.png', awakeGif: '/portraits/sir-cadogan-awake.gif' },
  { id: 'headmaster', name: 'Headmaster Dippet', sleepImage: '/portraits/headmaster-sleep.png', awakeGif: '/portraits/headmaster-awake.gif' },
  { id: 'mermaid', name: 'The Mermaid', sleepImage: '/portraits/mermaid-sleep.png', awakeGif: '/portraits/mermaid-awake.gif' },
  { id: 'ambrose', name: 'Ambrose Swot', sleepImage: '/portraits/ambrose-sleep.png', awakeGif: '/portraits/ambrose-awake.gif' },
];

export default function App() {
  const [conversation, setConversation] = useState([]);
  const [activePortrait, setActivePortrait] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  async function handleObjectDetected(detection) {
    if (isProcessing) return; // Prevent multiple simultaneous conversations
    
    const object = detection.objects[0];
    if (!object) return;
    
    setIsProcessing(true);
    
    try {
      // Trigger conversation
      const response = await axios.post('http://localhost:8000/api/chat', {
        detected_object: object,
        visitor_name: 'Guest'
      });
      
      const turns = response.data.turns;
      
      // Play conversation turn by turn
      for (const turn of turns) {
        setActivePortrait(turn.portrait);
        setConversation(prev => [...prev, turn]);
        
        // Play TTS audio
        await playAudio(turn.text, turn.voice);
        
        await sleep(1000); // Pause between turns
      }
      
      setActivePortrait(null);
    } catch (error) {
      console.error('Error generating conversation:', error);
    } finally {
      setIsProcessing(false);
    }
  }

  async function playAudio(text, voiceParams) {
    try {
      const response = await axios.post('http://localhost:8000/api/speak', {
        text,
        voice: voiceParams
      }, { responseType: 'blob' });
      
      const audio = new Audio(URL.createObjectURL(response.data));
      await new Promise((resolve, reject) => {
        audio.onended = resolve;
        audio.onerror = reject;
        audio.play();
      });
    } catch (error) {
      console.error('Error playing audio:', error);
    }
  }

  return (
    <div className="app">
      <h1>🪄 Magical Portraits</h1>
      
      <div className="main-layout">
        <div className="camera-section">
          <CameraFeed onObjectDetected={handleObjectDetected} />
        </div>
        
        <div className="portraits-section">
          <PortraitGallery 
            portraits={PORTRAITS} 
            activePortrait={activePortrait} 
          />
        </div>
      </div>
      
      <ConversationLog conversation={conversation} />
    </div>
  );
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

