<template>
  <div class="card-premium event-corp-card animate-corp">
    <div class="card-glow"></div>
    <div class="event-header-corp">
      <div class="category-pill-corp">
        <svg v-if="event.sport_category === 'Football'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z"></path><path d="M12 12l8.5-5"></path><path d="M12 12l-8.5-5"></path><path d="M12 12V2.5"></path><path d="M12 12l6 8.5"></path><path d="M12 12l-6 8.5"></path></svg>
        <svg v-else-if="event.sport_category === 'Cricket'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20"></path><path d="M8 2v20"></path><path d="M16 2v20"></path><path d="M4 6h16"></path><path d="M4 18h16"></path></svg>
        <span>{{ event.sport_category }}</span>
      </div>
      <div class="tier-indicator">
        <span v-for="i in 3" :key="i" :class="{ active: i <= getPriceTier(event.price_tier) }"></span>
      </div>
    </div>

    <div class="event-body-corp">
      <h3 class="event-title-corp">{{ event.title }}</h3>
      <div class="event-meta-corp">
        <div class="meta-item-corp">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
          <span>{{ event.venue_city }}</span>
        </div>
        <div class="meta-item-corp">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
          <span>{{ formattedDate }}</span>
        </div>
      </div>
    </div>

    <div class="event-footer-corp">
      <div class="price-box-corp">
        <span class="label-corp">Investment</span>
        <span class="value-corp">₹{{ event.price }}</span>
      </div>
      <router-link :to="`/events/${event.id}`" class="btn-corp-link">
        Details
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  event: Object as () => any
});

const formattedDate = computed(() => {
  if (!props.event.event_date) return 'TBD';
  const date = new Date(props.event.event_date);
  return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
});

const getPriceTier = (tier: string) => {
  if (tier === 'cheap') return 1;
  if (tier === 'mid') return 2;
  if (tier === 'premium') return 3;
  return 1;
};
</script>

<style scoped>
.event-corp-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 280px;
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  padding-top: 100%;
  background: radial-gradient(circle at center, var(--brand-glow), transparent 70%);
  opacity: 0;
  transition: opacity 0.5s var(--ease);
  pointer-events: none;
  transform: translateY(-50%) translateX(20%);
}

.event-corp-card:hover .card-glow {
  opacity: 1;
}

.event-header-corp {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.category-pill-corp {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-dim);
}

.tier-indicator {
  display: flex;
  gap: 4px;
}

.tier-indicator span {
  width: 12px;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.tier-indicator span.active {
  background: var(--brand-primary);
  box-shadow: 0 0 8px var(--brand-primary);
}

.event-title-corp {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: white;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.event-meta-corp {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.meta-item-corp {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-dim);
  font-size: 0.9rem;
  font-weight: 500;
}

.event-footer-corp {
  margin-top: 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.price-box-corp {
  display: flex;
  flex-direction: column;
}

.label-corp {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: var(--brand-primary);
  font-weight: 800;
  letter-spacing: 0.1em;
  margin-bottom: 0.2rem;
}

.value-corp {
  font-size: 1.6rem;
  font-weight: 900;
  color: white;
  letter-spacing: -0.03em;
}

.btn-corp-link {
  color: var(--brand-primary);
  text-decoration: none;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  transition: all 0.3s;
  background: rgba(0, 240, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: var(--radius-pill);
}

.btn-corp-link:hover {
  background: var(--brand-primary);
  color: black;
  gap: 0.75rem;
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
}
</style>
