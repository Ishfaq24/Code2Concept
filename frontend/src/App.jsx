import { useState } from "react";
import { generateVideo, getVideoUrl } from "./api";
import VideoPlayer from "./components/VideoPlayer";
import Loader from "./components/Loader";

function App() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);

  const handleGenerate = async () => {
    if (!topic) return;

    setLoading(true);
    setVideoUrl(null);

    try {
      const res = await generateVideo(topic);

      if (res.message) {
        setVideoUrl(getVideoUrl() + `?t=${Date.now()}`); // prevent caching
      } else {
        alert("Error: " + res.error);
      }
    } catch (err) {
      alert("Failed to connect to backend");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      <h1>🎬 AI Video Generator</h1>

      <input
        type="text"
        placeholder="Enter topic (e.g. Binary Search)"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        style={{ padding: "10px", width: "300px" }}
      />

      <br /><br />

      <button onClick={handleGenerate} style={{ padding: "10px 20px" }}>
        Generate Video
      </button>

      <br /><br />

      {loading && <Loader />}
      {videoUrl && <VideoPlayer videoUrl={videoUrl} />}
    </div>
  );
}

export default App;