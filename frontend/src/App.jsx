import React, { useState, useRef } from 'react';
import CameraFeed from './components/CameraFeed';
import PortraitGallery from './components/PortraitGallery';
import ConversationLog from './components/ConversationLog';
import axios from 'axios';
import './App.css';

const PORTRAITS = [
  { id: 'fat_lady', name: 'Fat Lady', sleepImage: '/portraits/fat_lady-sleep.png', awakeGif: '/portraits/fat_lady-awake.png' },
  { id: 'sir_cadogan', name: 'Sir Cadogan', sleepImage: '/portraits/sir_cadogan-sleep.png', awakeGif: '/portraits/sir_cadogan-awake.png' },
  { id: 'headmaster', name: 'Headmaster Dippet', sleepImage: '/portraits/headmaster-sleep.png', awakeGif: '/portraits/headmaster-awake.png' },
  { id: 'mermaid', name: 'The Mermaid', sleepImage: '/portraits/mermaid-sleep.png', awakeGif: '/portraits/mermaid-awake.png' },
  { id: 'ambrose', name: 'Ambrose Swot', sleepImage: '/portraits/ambrose-sleep.png', awakeGif: '/portraits/ambrose-awake.png' },
];

export default function App() {
  const [conversation, setConversation] = useState([]);
  const [activePortrait, setActivePortrait] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const currentAudioRef = useRef(null);
  const lastObjectRef = useRef(null);
  const lastDetectionTimeRef = useRef(0);

  async function handleObjectDetected(detection) {
    if (isProcessing) {
      console.log('Already processing, skipping detection');
      return; // Prevent multiple simultaneous conversations
    }
    
    const object = detection.objects[0];
    if (!object) return;
    
    // Cooldown: Don't trigger same object within 30 seconds
    const now = Date.now();
    const timeSinceLastDetection = now - lastDetectionTimeRef.current;
    
    if (lastObjectRef.current === object && timeSinceLastDetection < 30000) {
      console.log(`Same object "${object}" detected too soon (${Math.round(timeSinceLastDetection/1000)}s ago). Waiting...`);
      return;
    }
    
    lastObjectRef.current = object;
    lastDetectionTimeRef.current = now;
    
    setIsProcessing(true);
    console.log('Starting conversation for:', object);
    
    try {
      // Trigger conversation
      const response = await axios.post('http://localhost:8000/api/chat', {
        detected_object: object,
        visitor_name: 'Guest'
      });
      
      const turns = response.data.turns;
      console.log(`Got ${turns.length} conversation turns`);
      
      // Play conversation turn by turn sequentially
      for (let i = 0; i < turns.length; i++) {
        const turn = turns[i];
        console.log(`Playing turn ${i + 1}/${turns.length}: ${turn.portrait}`);
        
        setActivePortrait(turn.portrait);
        setConversation(prev => [...prev, turn]);
        
        // Play TTS audio and wait for it to complete
        await playAudio(turn.text, turn.voice);
        
        // Longer pause between turns to ensure separation
        await sleep(800);
      }
      
      setActivePortrait(null);
      console.log('✅ Conversation complete. Cooldown started for 30 seconds.');
      
      // Add a short pause after conversation ends before allowing new detections
      await sleep(2000);
    } catch (error) {
      console.error('Error generating conversation:', error);
    } finally {
      setIsProcessing(false);
    }
  }

  async function playAudio(text, voiceParams) {
    return new Promise(async (resolveMain, rejectMain) => {
      try {
        // Stop any currently playing audio
        if (currentAudioRef.current) {
          console.log('Stopping previous audio');
          currentAudioRef.current.pause();
          currentAudioRef.current.currentTime = 0;
          currentAudioRef.current = null;
          await sleep(100); // Small delay to ensure cleanup
        }
        
        console.log('Fetching audio for:', text.substring(0, 50) + '...');
        const response = await axios.post('http://localhost:8000/api/speak', {
          text,
          voice: voiceParams
        }, { responseType: 'blob' });
        
        const audioUrl = URL.createObjectURL(response.data);
        const audio = new Audio(audioUrl);
        currentAudioRef.current = audio;
        
        // Set up event handlers before playing
        audio.onended = () => {
          console.log('✅ Audio playback completed');
          URL.revokeObjectURL(audioUrl);
          currentAudioRef.current = null;
          resolveMain();
        };
        
        audio.onerror = (e) => {
          console.error('❌ Audio playback error:', e);
          URL.revokeObjectURL(audioUrl);
          currentAudioRef.current = null;
          resolveMain(); // Resolve anyway to continue
        };
        
        audio.onloadeddata = () => {
          console.log(`🎵 Audio loaded: ${audio.duration.toFixed(1)}s`);
        };
        
        // Start playback
        console.log('▶️ Starting audio playback...');
        await audio.play();
        
      } catch (error) {
        console.error('Error in playAudio:', error);
        if (currentAudioRef.current) {
          currentAudioRef.current = null;
        }
        resolveMain(); // Resolve anyway to continue
      }
    });
  }

  return (
    <div className="app">
      <h1>🖼️ The Wall of Whispering Frames</h1>
      
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

