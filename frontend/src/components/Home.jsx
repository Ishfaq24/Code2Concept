import { useState } from "react";
import { generateVideo, getPdfUrl, getVideoUrl, regeneratePdf } from "../api";
import VideoPlayer from "./VideoPlayer";
import Loader from "./Loader";
import Hero from "./Hero";

const LANGUAGE_OPTIONS = [
  { code: "en", label: "English" },
  { code: "es", label: "Spanish" },
  { code: "fr", label: "French" },
  { code: "de", label: "German" },
  { code: "it", label: "Italian" },
  { code: "pt", label: "Portuguese" },
  { code: "hi", label: "Hindi" },
];

function Home() {
  const [topic, setTopic] = useState("");
  const [language, setLanguage] = useState("en");
  const [includePdf, setIncludePdf] = useState(false);
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [pdfDownloadUrl, setPdfDownloadUrl] = useState(null);
  const [pdfStatus, setPdfStatus] = useState("idle");
  const [pdfError, setPdfError] = useState(null);
  const [videoToken, setVideoToken] = useState(null);

  const handleGenerate = async () => {
    if (!topic.trim() || loading) return;

    setLoading(true);
    setVideoUrl(null);
    setDownloadUrl(null);
    setPdfDownloadUrl(null);
    setPdfStatus(includePdf ? "idle" : "disabled");
    setPdfError(null);
    setVideoToken(null);

    try {
      const res = await generateVideo(topic.trim(), language, includePdf);
      // Only show video when backend reports a successful render
      if (res.status === "success") {
        const videoBaseUrl = getVideoUrl(res.video_token);
        setVideoToken(res.video_token);
        setDownloadUrl(videoBaseUrl);
        setPdfDownloadUrl(res.pdf_available ? getPdfUrl(res.video_token) : null);
        if (!includePdf) {
          setPdfStatus("disabled");
        } else {
          setPdfStatus(res.pdf_available ? "ready" : "unavailable");
        }
        setPdfError(res.pdf_error || null);
        const separator = videoBaseUrl.includes("?") ? "&" : "?";
        // Add cache-busting query param
        setVideoUrl(videoBaseUrl + `${separator}t=${Date.now()}`);
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

  const handleRetryPdf = async () => {
    if (!videoToken || loading || pdfStatus === "retrying") return;

    setPdfStatus("retrying");
    setPdfError(null);

    try {
      const res = await regeneratePdf(videoToken);
      if (res.status === "success" && res.pdf_available) {
        setPdfDownloadUrl(getPdfUrl(videoToken));
        setPdfStatus("ready");
      } else {
        setPdfDownloadUrl(null);
        setPdfStatus("unavailable");
        setPdfError(res.error || "PDF could not be generated yet.");
      }
    } catch (err) {
      setPdfDownloadUrl(null);
      setPdfStatus("unavailable");
      setPdfError("Could not reach backend while retrying PDF generation.");
    }
  };

  return (
    <div className="app-root">
      <Hero />

      <main className="shell">
        <section className="panel studio-panel">
          <div className="panel-header">
            <span className="panel-badge">AlgoArena • Code Together</span>
            <h2>Generate an animated explainer</h2>
            <p>
              Describe any concept and we will craft a high-quality Manim video
              to help you or your students understand it faster.
            </p>
          </div>

          <div className="input-row" role="group" aria-label="Video generation controls">
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
            <select
              className="language-select"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              disabled={loading}
              aria-label="Narration language"
            >
              {LANGUAGE_OPTIONS.map((option) => (
                <option key={option.code} value={option.code}>
                  {option.label}
                </option>
              ))}
            </select>
            <div className="pdf-control-card" aria-label="PDF study guide option">
              <label className="pdf-control-label">
                <input
                  type="checkbox"
                  checked={includePdf}
                  onChange={(e) => setIncludePdf(e.target.checked)}
                  disabled={loading}
                />
                <span>
                  Generate PDF study guide
                  <small>English PDF named after your topic</small>
                </span>
              </label>
            </div>
            <button
              className="primary-button"
              onClick={handleGenerate}
              disabled={loading || !topic.trim()}
            >
              {loading ? "Generating…" : includePdf ? "Generate Video + PDF" : "Generate Video"}
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

          <div className="output-block">
            <div className="panel-header output-header">
              <h2>Generated video</h2>
              <p>Your generated lecture and study guide will appear below automatically.</p>
            </div>

            {videoUrl ? (
              <VideoPlayer
                videoUrl={videoUrl}
                downloadUrl={downloadUrl || videoUrl}
                pdfDownloadUrl={pdfDownloadUrl}
                pdfStatus={pdfStatus}
                pdfError={pdfError}
                pdfRequested={includePdf}
                onRetryPdf={handleRetryPdf}
              />
            ) : (
              <div className="preview-placeholder">
                <div className="preview-glow" />
                <p>
                  Enter a topic and click <span>Generate Video</span> to see your
                  first animated explanation.
                </p>
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default Home;
