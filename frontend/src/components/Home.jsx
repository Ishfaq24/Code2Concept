import { useState } from "react";
import { generateVideo, getVideoUrl } from "../api";
import VideoPlayer from "./VideoPlayer";
import Loader from "./Loader";
import Hero from "./Hero";

function Home() {
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
      <Hero />

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

export default Home;
