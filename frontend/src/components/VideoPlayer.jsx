import React from 'react';
import './VideoPlayer.css'; // Import the standard CSS file

const VideoPlayer = ({ videoUrl, downloadUrl, pdfDownloadUrl, pdfStatus, pdfError, onRetryPdf, posterUrl }) => {
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
        {pdfDownloadUrl && (
          <a
            className="video-download-button video-download-button-secondary"
            href={pdfDownloadUrl}
            download="study-guide.pdf"
          >
            Download PDF Guide
          </a>
        )}
        {!pdfDownloadUrl && (
          <>
            {pdfStatus === "unavailable" && onRetryPdf ? (
              <button
                type="button"
                className="video-download-button video-download-button-secondary"
                onClick={onRetryPdf}
              >
                Retry PDF Guide
              </button>
            ) : (
              <span
                className="video-download-button video-download-button-disabled"
                title="Generating PDF guide..."
              >
                {pdfStatus === "retrying" ? "Retrying PDF Guide" : "Preparing PDF Guide"}
              </span>
            )}
          </>
        )}
      </div>
      {pdfError && <p className="video-pdf-error">PDF note: {pdfError}</p>}
    </div>
  );
};

export default VideoPlayer;