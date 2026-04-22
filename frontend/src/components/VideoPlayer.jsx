import React from 'react';
import './VideoPlayer.css'; // Import the standard CSS file

const VideoPlayer = ({ videoUrl, downloadUrl, posterUrl }) => {
  if (!videoUrl) return null;

  return (
    <div className="video-player-wrapper">
      <video
        className="video-player-element"
        controls
        disablePictureInPicture
        poster={posterUrl}
        preload="metadata"
      >
        <source src={videoUrl} type="video/mp4" />

        {/* Fallback for older browsers */}
        <p>Your browser does not support the video tag.</p>
      </video>

      <div className="video-download-row">
        <a
          className="video-download-button"
          href={downloadUrl || videoUrl}
          download="generated-video.mp4"
        >
          Download Video
        </a>
      </div>
    </div>
  );
};

export default VideoPlayer;