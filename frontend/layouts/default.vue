<template>
  <div class="app-container">
    <header class="main-header glass-panel">
      <h1 class="logo">NAIVE <span class="highlight">RAG</span> APPLICATION</h1>
      <nav>
        <!-- <div class="nav-item active">CONSOLE</div> -->
      </nav>
    </header>

    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(188, 19, 254, 0.1) 0%, transparent 40%),
    radial-gradient(circle at 90% 80%, rgba(0, 243, 255, 0.1) 0%, transparent 40%);
  padding: 2rem;
}

.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  margin-bottom: 2rem;
}

.logo {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.8rem;
  margin: 0;
  letter-spacing: 3px;
}

.highlight {
  color: var(--color-primary);
}

.nav-item {
  color: var(--color-text-dim);
  font-size: 0.9rem;
  letter-spacing: 2px;
  cursor: pointer;
}

.nav-item.active {
  color: var(--color-primary);
  border-bottom: 2px solid var(--color-primary);
}
</style>
