import React, { useRef, useEffect, useState, useCallback } from 'react';
import axios from 'axios';

export default function CameraFeed({ onObjectDetected }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [error, setError] = useState(null);

  const startCamera = useCallback(async () => {
    try {
      console.log('🎥 Requesting camera access...');
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 640 }, 
          height: { ideal: 480 },
          facingMode: 'user'
        } 
      });
      console.log('✅ Camera access granted');
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        // Wait for video to be ready
        await new Promise((resolve) => {
          if (videoRef.current) {
            videoRef.current.onloadedmetadata = () => {
              console.log('✅ Video ready, dimensions:', videoRef.current?.videoWidth, 'x', videoRef.current?.videoHeight);
              resolve();
            };
          }
        });
      }
      setError(null);
    } catch (err) {
      console.error('❌ Error accessing camera:', err);
      setError('Unable to access camera. Please check permissions.');
    }
  }, []);

  useEffect(() => {
    startCamera();
    // Store ref value for cleanup
    const videoElement = videoRef.current;
    return () => {
      // Cleanup: stop camera stream
      if (videoElement && videoElement.srcObject) {
        const stream = videoElement.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, [startCamera]);

  const startDetectionLoop = useCallback(() => {
    console.log('🔄 Starting detection loop...');
    setIsDetecting(true);
    
    const interval = setInterval(async () => {
      if (!videoRef.current || !canvasRef.current) {
        console.log('⚠️ Video or canvas not ready');
        return;
      }
      
      // Check if video is actually playing and has dimensions
      const video = videoRef.current;
      if (video.readyState < 2 || video.videoWidth === 0 || video.videoHeight === 0) {
        console.log('⚠️ Video not ready yet, waiting...', {
          readyState: video.readyState,
          width: video.videoWidth,
          height: video.videoHeight
        });
        return;
      }
      
      try {
        // Capture frame from video - use actual video dimensions
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        console.log(`📸 Captured frame: ${canvas.width}x${canvas.height}`);
        
        // Convert to blob and send to backend
        canvas.toBlob(async (blob) => {
          if (!blob) {
            console.error('❌ Failed to create blob from canvas');
            return;
          }
          
          console.log(`📤 Sending frame to backend (${blob.size} bytes)`);
          
          const formData = new FormData();
          formData.append('file', blob, 'frame.jpg');
          
          try {
            // Don't set Content-Type manually - let axios set it with boundary
            const response = await axios.post(
              'http://localhost:8000/api/detect',
              formData,
              {
                headers: {
                  // Let axios set Content-Type automatically with boundary
                },
                timeout: 10000, // 10 second timeout
              }
            );
            
            console.log('📥 Detection response:', response.data);
            
            if (response.data.objects && response.data.objects.length > 0) {
              console.log('✅ Objects detected:', response.data.objects);
              onObjectDetected(response.data);
            } else {
              console.log('ℹ️ No objects detected in this frame');
            }
          } catch (error) {
            if (error.response) {
              console.error('❌ Detection error (response):', error.response.status, error.response.data);
            } else if (error.request) {
              console.error('❌ Detection error (no response):', error.message);
            } else {
              console.error('❌ Detection error:', error.message);
            }
          }
        }, 'image/jpeg', 0.8);
      } catch (err) {
        console.error('❌ Error in detection loop:', err);
      }
    }, 5000); // Detect every 5 seconds (reduced frequency to avoid spam)

    return interval;
  }, [onObjectDetected]);

  useEffect(() => {
    if (!error && videoRef.current && canvasRef.current) {
      const interval = startDetectionLoop();
      return () => {
        if (interval) {
          clearInterval(interval);
        }
      };
    }
  }, [error, startDetectionLoop]);

  return (
    <div className="camera-feed">
      {error ? (
        <div className="camera-error">
          <p>{error}</p>
          <button onClick={startCamera}>Retry Camera</button>
        </div>
      ) : (
        <>
          <video 
            ref={videoRef} 
            autoPlay 
            playsInline
            style={{ width: '100%', borderRadius: '8px' }}
          />
          <canvas 
            ref={canvasRef} 
            width={640} 
            height={480} 
            style={{ display: 'none' }}
          />
          {isDetecting && <p className="detection-status">🔍 Detecting objects...</p>}
        </>
      )}
    </div>
  );
}

