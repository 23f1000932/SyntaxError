<template>
  <div class="landing-page">
    <section class="hero-v3">
      <div class="container text-center animate-corp">
        <span class="badge-corp">Professional Sports Platform</span>
        <h1 class="hero-main-title delay-100">
          Sports Event <br/> <span class="text-gradient">Management.</span>
        </h1>
        <p class="hero-description delay-200">
          The easy way to organize, manage, and discover sports tournaments. Scale your events and automate your operations with our professional platform.
        </p>
        <div class="hero-actions delay-300">
          <router-link to="/register" class="btn-corp btn-corp-primary">
            Join Now
          </router-link>
          <router-link to="/login" class="btn-corp btn-corp-outline">
            Login
          </router-link>
        </div>
      </div>
    </section>

    <section class="section-spacer">
      <div class="container">
        <div class="section-header text-center animate-corp">
          <h2 class="section-title-large">Key Features</h2>
          <p class="section-subtitle">A powerful set of tools for managing your sports events.</p>
        </div>

        <div class="capabilities-grid mt-20">
          <div class="card-premium cap-card animate-corp delay-100">
            <div class="cap-icon-box">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--brand-primary)" stroke-width="1.5"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
            </div>
            <h3>Event Management</h3>
            <p>Easily manage every part of your event from a simple dashboard.</p>
          </div>
          
          <div class="card-premium cap-card animate-corp delay-200">
            <div class="cap-icon-box">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--brand-secondary)" stroke-width="1.5"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
            </div>
            <h3>Live Insights</h3>
            <p>Access accurate data on registrations and sales to help you grow your business.</p>
          </div>

          <div class="card-premium cap-card animate-corp delay-300">
            <div class="cap-icon-box">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--brand-accent)" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
            </div>
            <h3>Secure System</h3>
            <p>Your data is protected with professional security and automated tools.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section-spacer">
      <div class="container">
        <div class="portal-grid">
          <div class="card-premium portal-card-v2 animate-corp">
            <div class="portal-header">
              <span class="badge-corp">Users</span>
              <h3>For Participants</h3>
            </div>
            <p>Find your favorite sporting events, book tickets, and manage your registrations with ease.</p>
            <router-link to="/login" class="btn-corp btn-corp-primary w-full mt-10">Get Started &rarr;</router-link>
          </div>
          
          <div class="card-premium portal-card-v2 animate-corp delay-100">
            <div class="portal-header">
              <span class="badge-corp">Vendors</span>
              <h3>For Event Vendors</h3>
            </div>
            <p>Create and manage events, track sales, and grow your audience through our platform.</p>
            <router-link to="/login" class="btn-corp btn-corp-outline w-full mt-10">Vendor Dashboard &rarr;</router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.landing-page {
  background: transparent;
}

.hero-main-title {
  margin: 1rem 0 1.5rem;
}

.capabilities-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.cap-card {
  padding: 2rem;
}

.cap-card h3 {
  margin: 1.25rem 0 0.75rem;
  font-size: 1.1rem;
  letter-spacing: -0.02em;
}

.cap-card p {
  color: var(--text-dim);
  font-size: 0.9rem;
  line-height: 1.5;
}

.cap-icon-box {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
}

.portal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.portal-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.portal-card-v2 {
  padding: 2rem;
}

.portal-card-v2 h3 {
  font-size: 1.25rem;
  margin: 0;
  line-height: 1.2;
}

.portal-card-v2 p {
  color: var(--text-dim);
  font-size: 0.9rem;
  line-height: 1.5;
}

.mt-20 { margin-top: 3rem; }

@media (max-width: 1024px) {
  .capabilities-grid, .portal-grid {
    grid-template-columns: 1fr;
  }
}
</style>
