import { useEffect, useRef, useState } from "react";
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
  const [isLanguageOpen, setIsLanguageOpen] = useState(false);
  const [includePdf, setIncludePdf] = useState(false);
  const [loading, setLoading] = useState(false);
  const [pdfRequested, setPdfRequested] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [pdfDownloadUrl, setPdfDownloadUrl] = useState(null);
  const [pdfStatus, setPdfStatus] = useState("idle");
  const [pdfError, setPdfError] = useState(null);
  const [videoToken, setVideoToken] = useState(null);
  const languagePickerRef = useRef(null);

  const selectedLanguage =
    LANGUAGE_OPTIONS.find((option) => option.code === language) || LANGUAGE_OPTIONS[0];

  useEffect(() => {
    const onDocumentMouseDown = (event) => {
      if (!languagePickerRef.current?.contains(event.target)) {
        setIsLanguageOpen(false);
      }
    };

    document.addEventListener("mousedown", onDocumentMouseDown);
    return () => {
      document.removeEventListener("mousedown", onDocumentMouseDown);
    };
  }, []);

  useEffect(() => {
    if (loading) {
      setIsLanguageOpen(false);
    }
  }, [loading]);

  const handleGenerate = async (generatePdf = false) => {
    if (!topic.trim() || loading) return;

    setLoading(true);
    setPdfRequested(generatePdf);
    setVideoUrl(null);
    setDownloadUrl(null);
    setPdfDownloadUrl(null);
    setPdfStatus(generatePdf ? "idle" : "disabled");
    setPdfError(null);
    setVideoToken(null);

    try {
      const res = await generateVideo(topic.trim(), language, generatePdf);
      // Only show video when backend reports a successful render
      if (res.status === "success") {
        const videoBaseUrl = getVideoUrl(res.video_token);
        setVideoToken(res.video_token);
        setDownloadUrl(videoBaseUrl);
        setPdfDownloadUrl(res.pdf_available ? getPdfUrl(res.video_token) : null);
        if (!generatePdf) {
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
    } catch {
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
    } catch {
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

          <div className="generation-grid">
            <section className="generation-card">
              <div className="generation-card-header">
                <span className="generation-card-kicker">Video</span>
                <h3>Generate the animated explainer</h3>
                <p>Use this section when you only want the video output.</p>
              </div>

              <div className="input-row input-row-video" role="group" aria-label="Video generation controls">
                <input
                  className="topic-input"
                  type="text"
                  placeholder="e.g. Binary Search, Basic Arm Anatomy"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") handleGenerate(includePdf);
                  }}
                />
                <div className="language-picker" ref={languagePickerRef}>
                  <button
                    type="button"
                    className={`language-picker-trigger ${isLanguageOpen ? "open" : ""}`}
                    onClick={() => setIsLanguageOpen((prev) => !prev)}
                    disabled={loading}
                    aria-haspopup="listbox"
                    aria-expanded={isLanguageOpen}
                    aria-label="Narration language selector"
                  >
                    <span className="language-picker-label">Language</span>
                    <span className="language-picker-value">{selectedLanguage.label}</span>
                  </button>

                  {isLanguageOpen && (
                    <ul className="language-picker-menu" role="listbox" aria-label="Narration language options">
                      {LANGUAGE_OPTIONS.map((option) => (
                        <li key={option.code} role="option" aria-selected={option.code === language}>
                          <button
                            type="button"
                            className={`language-picker-option ${option.code === language ? "active" : ""}`}
                            onClick={() => {
                              setLanguage(option.code);
                              setIsLanguageOpen(false);
                            }}
                          >
                            {option.label}
                          </button>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
                <button
                  className="primary-button"
                  onClick={() => handleGenerate(includePdf)}
                  disabled={loading || !topic.trim()}
                >
                  {loading ? "Generating…" : includePdf ? "Generate Video + PDF" : "Generate Video"}
                </button>
              </div>
            </section>

            <section className="generation-card generation-card-pdf">
              <div className="generation-card-header">
                <span className="generation-card-kicker generation-card-kicker-pdf">PDF Export</span>
                <h3>Build a polished study guide</h3>
                <p>
                  Create a topic-named English PDF with a structured handout for revision,
                  teaching, or sharing.
                </p>
              </div>

              <div className="pdf-control-card">
                <div className="pdf-control-copy">
                  <p className="pdf-control-title">What the PDF includes</p>
                  <ul className="pdf-feature-list">
                    <li>English-only revision guide</li>
                    <li>Overview, core concepts, and a worked example</li>
                    <li>Common misconceptions and practice questions</li>
                  </ul>
                </div>

                <label className="pdf-optin-toggle" aria-label="Include PDF with generation">
                  <input
                    type="checkbox"
                    checked={includePdf}
                    onChange={(e) => setIncludePdf(e.target.checked)}
                    disabled={loading}
                  />
                  <span>
                    Include PDF in next generation request
                    <small>No second request. Video and PDF are generated together.</small>
                  </span>
                </label>
              </div>
            </section>
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

          <div className="output-block pdf-output-block">
            <div className="panel-header output-header">
              <h2>PDF study guide</h2>
              <p>
                {pdfRequested
                  ? "Your English PDF guide is generated below when available."
                  : "Enable PDF in the PDF Export section above, then click Generate Video once."}
              </p>
            </div>

            {pdfRequested ? (
              <div className="pdf-result-card">
                {pdfDownloadUrl ? (
                  <>
                    <div className="pdf-ready-banner">
                      <span className="pdf-ready-label">PDF ready</span>
                      <p>Your study guide is available to download now.</p>
                    </div>
                    <a className="pdf-download-button" href={pdfDownloadUrl} download>
                      Download PDF Study Guide
                    </a>
                  </>
                ) : (
                  <div className="pdf-result-empty">
                    <p>
                      {pdfStatus === "retrying"
                        ? "Retrying PDF generation..."
                        : pdfStatus === "unavailable"
                          ? "PDF guide is not available yet. You can retry generation below."
                          : "PDF guide will appear here after generation."}
                    </p>
                    {pdfStatus === "unavailable" && (
                      <button
                        type="button"
                        className="secondary-button"
                        onClick={handleRetryPdf}
                        disabled={!videoToken || loading}
                      >
                        Retry PDF Generation
                      </button>
                    )}
                  </div>
                )}
                {pdfError && <p className="video-pdf-error">PDF note: {pdfError}</p>}
              </div>
            ) : (
              <div className="preview-placeholder pdf-preview-placeholder">
                <div className="preview-glow" />
                <p>
                  The PDF export lives in its own panel so the workflow stays clean and the
                  guide is generated only when you actually need it.
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
