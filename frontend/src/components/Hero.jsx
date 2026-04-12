function Hero() {
  return (
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
  );
}

export default Hero;
