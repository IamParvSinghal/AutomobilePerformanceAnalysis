export function Hero() {
  return (
    <section className="hero-panel">
      <div className="hero-layout">
        <div className="hero-main">
          <h1>Estimate a car&apos;s fuel efficiency from its specs.</h1>
          <p className="hero-copy">
            Enter details like engine size, weight, year, and origin, and the app predicts how far
            the car can travel for the fuel it uses.
          </p>
        </div>
        <aside className="hero-aside" aria-label="Project summary">
          <div className="hero-chip">
            <span className="hero-chip-label">Input</span>
            <strong>Vehicle profile</strong>
            <p>Engine, weight, acceleration, year, and region.</p>
          </div>
          <div className="hero-chip">
            <span className="hero-chip-label">Output</span>
            <strong>Fuel estimate</strong>
            <p>Returns predicted efficiency in MPG or km/L.</p>
          </div>
        </aside>
      </div>
    </section>
  );
}
