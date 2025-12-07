<template>
  <div class="split-view">
    <div class="side-panel">
      <IngestWidget />
      
      <div class="info-card glass-panel">
        <h4>SYSTEM STATUS</h4>
        <div class="stat-row">
          <span>Backend</span>
          <span class="active-txt">CONNECTED</span>
        </div>
        <div class="stat-row">
          <span>Latency</span>
          <span>12ms</span>
        </div>
      </div>
    </div>
    
    <div class="main-panel">
      <ChatWidget />
    </div>
  </div>
</template>

<style scoped>
.split-view {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

@media (max-width: 900px) {
  .split-view {
    grid-template-columns: 1fr;
  }
}

.info-card {
  padding: 1.5rem;
}

.info-card h4 {
  margin: 0 0 1rem 0;
  color: var(--color-text-dim);
  font-size: 0.8rem;
  letter-spacing: 1px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.active-txt {
  color: #00ff88;
  text-shadow: 0 0 5px #00ff88;
}
</style>
