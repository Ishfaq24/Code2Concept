import React from 'react';
import './VideoPlayer.css'; // Import the standard CSS file

const VideoPlayer = ({ videoUrl, posterUrl }) => {
  if (!videoUrl) return null;

  return (
    <div className="video-player-wrapper">
      <video 
        className="video-player-element"
        controls
        controlsList="nodownload noremoteplayback"
        disablePictureInPicture
        onContextMenu={(e) => e.preventDefault()}
        poster={posterUrl}
        preload="metadata"
      >
        <source src={videoUrl} type="video/mp4" />
        
        {/* Fallback for older browsers */}
        <p>Your browser does not support the video tag.</p>
      </video>
    </div>
  );
};

export default VideoPlayer;