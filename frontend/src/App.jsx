import { useState } from "react";
import { generateVideo, getVideoUrl } from "./api";
import VideoPlayer from "./components/VideoPlayer";
import Loader from "./components/Loader";

function App() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);

  const handleGenerate = async () => {
    if (!topic.trim() || loading) return;

    setLoading(true);
    setVideoUrl(null);

    try {
      const res = await generateVideo(topic.trim());
      // Only show video when backend reports a successful render
      if (res.status === "success") {
        // Use /video endpoint and add a cache-busting query param
        setVideoUrl(getVideoUrl() + `?t=${Date.now()}`);
      } else {
        const detail = res.error_details || res.error || res.message || "Unknown error";
        alert("Video generation failed: " + detail);
      }
    } catch (err) {
      alert("Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-root">
      <header className="hero">
        <div className="hero-pill">
          <span className="hero-pill-icon">⚡</span>
          <span>Real-time learning collaboration</span>
        </div>

        <h1 className="hero-title">
          <span className="hero-title-accent">Learn Faster,</span>
          <br />
          Understand Better
        </h1>

        <p className="hero-subtitle">
          Turn any topic into a cinematic explanation. Generate animated video
          lectures and AI-crafted notes aligned with your syllabus.
        </p>

        <div className="hero-tags">
          <span className="tag tag-active">AI Notes Generator</span>
          <span className="tag">Animated Video Lectures</span>
          <span className="tag">Personalized Study Paths</span>
        </div>

        <div className="hero-metrics">
          <div className="metric">
            <div className="metric-value">10K+</div>
            <div className="metric-label">Active Users</div>
          </div>
          <div className="metric">
            <div className="metric-value">50K+</div>
            <div className="metric-label">Sessions</div>
          </div>
          <div className="metric">
            <div className="metric-value">99.9%</div>
            <div className="metric-label">Uptime</div>
          </div>
        </div>
      </header>

      <main className="shell">
        <section className="panel input-panel">
          <div className="panel-header">
            <span className="panel-badge">AlgoArena • Code Together</span>
            <h2>Generate an animated explainer</h2>
            <p>
              Describe any concept and we will craft a high-quality Manim video
              to help you or your students understand it faster.
            </p>
          </div>

          <div className="input-row">
            <input
              className="topic-input"
              type="text"
              placeholder="e.g. Binary Search, Basic Arm Anatomy"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleGenerate();
              }}
            />
            <button
              className="primary-button"
              onClick={handleGenerate}
              disabled={loading || !topic.trim()}
            >
              {loading ? "Generating…" : "Generate Video"}
            </button>
          </div>

          {loading && (
            <div className="status-row">
              <Loader />
              <span className="status-text">
                Rendering with Manim • This may take a minute
              </span>
            </div>
          )}
        </section>

        <section className="panel preview-panel">
          <div className="panel-header">
            <h2>Live preview</h2>
            <p>Your generated lecture will appear here automatically.</p>
          </div>

          {videoUrl ? (
            <VideoPlayer videoUrl={videoUrl} />
          ) : (
            <div className="preview-placeholder">
              <div className="preview-glow" />
              <p>
                Enter a topic and click <span>Generate Video</span> to see your
                first animated explanation.
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;