<template>
  <div class="event-detail-page">
    <div class="luxury-bg-mesh">
      <div class="aura-blob aura-1"></div>
      <div class="aura-blob aura-2"></div>
      <div class="aura-blob aura-3"></div>
    </div>

    <div class="container py-12">
      <button @click="$router.push('/home')" class="back-btn-corp mb-12">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
        Return to Portal
      </button>

      <div v-if="loading" class="loading-corp-full">
        <div class="pulse-loader"></div>
        <span>Synchronizing Event Intelligence...</span>
      </div>
      
      <div v-else-if="error" class="error-panel-inline">{{ error }}</div>
      
      <div v-else-if="event" class="card-premium detail-card-corp animate-corp">
        <div class="header-corp mb-12">
          <div class="header-main">
            <span class="badge-corp">{{ event.sport_category }}</span>
            <h1 class="hero-title-large mt-6">{{ event.title }}</h1>
          </div>
          <div class="tier-box-corp">
             <span class="label-muted">Access Tier</span>
             <span class="text-gradient font-900 text-3xl mt-2 block">{{ event.price_tier?.toUpperCase() }}</span>
          </div>
        </div>

        <div class="info-grid-corp mb-12">
          <div class="info-item">
            <label class="label-muted mb-3">Venue Coordinates</label>
            <p class="text-xl font-600">{{ event.venue_city }}{{ event.venue_address ? `, ${event.venue_address}` : '' }}</p>
          </div>
          <div class="info-item">
            <label class="label-muted mb-3">Temporal Window</label>
            <p class="text-xl font-600">{{ new Date(event.event_date).toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' }) }}</p>
          </div>
        </div>

        <div class="description-section mb-12">
          <label class="label-muted mb-6">Briefing</label>
          <p class="text-dim text-lg leading-relaxed max-w-4xl">{{ event.description || 'No strategic briefing provided.' }}</p>
        </div>

        <div class="registration-panel-corp pt-12 border-top-luxury">
          <div class="stats-grid-corp mb-12">
            <div class="stat-box-corp">
              <span class="label-muted mb-4 text-xs">Commitment Fee</span>
              <span class="value text-4xl font-900">₹{{ event.price }}</span>
            </div>
            <div class="stat-box-corp">
              <span class="label-muted mb-4 text-xs">Sector Availability</span>
              <span class="value text-4xl font-900">{{ event.seats_remaining }} / {{ event.capacity }}</span>
            </div>
          </div>

          <div class="action-portal-corp">
            <template v-if="!authStore.isAuthenticated">
              <div class="auth-prompt-corp text-center">
                <p class="text-dim mb-8">Authentication required for mission commitment.</p>
                <router-link to="/login" class="btn-corp btn-corp-primary px-12">Login to Access</router-link>
              </div>
            </template>
            <template v-else-if="authStore.isUser">
              <div v-if="registrationStatus" class="status-panel-corp animate-corp">
                <div class="status-info">
                   <label class="label-muted mb-2">Registration Integrity</label>
                   <p class="status-text">{{ registrationStatus.toUpperCase() }}</p>
                </div>
                <button v-if="registrationStatus === 'confirmed'" @click="cancelRegistration" class="btn-corp-link-danger">
                  Abort Registration
                </button>
              </div>
              <!-- UNIFIED REGISTRATION FORM -->
              <div v-else-if="event.seats_remaining > 0" class="registration-form mt-4 mb-8 text-left">
                <h4 class="mb-4 text-xl font-900 label-muted">Registration Details</h4>
                <div class="input-stack mb-4">
                  <label class="label-muted mb-2">Select Role</label>
                  <select v-model="regForm.role" class="input-corp w-full">
                    <option value="athlete">Athlete / Participant</option>
                    <option value="sub_vendor">Sub-Vendor / Support Provider</option>
                  </select>
                </div>
                
                <div v-if="regForm.role === 'athlete'" class="input-stack mb-4">
                  <label class="label-muted mb-2">Team / Club Name (Optional)</label>
                  <input type="text" v-model="regForm.role_details.team" class="input-corp w-full" placeholder="e.g. Thunderbolts" />
                </div>
                
                <div v-if="regForm.role === 'sub_vendor'" class="input-stack mb-4">
                  <label class="label-muted mb-2">Service Type</label>
                  <select v-model="regForm.role_details.service" class="input-corp w-full">
                    <option value="catering">Food & Catering</option>
                    <option value="medical">Medical Support</option>
                    <option value="logistics">Equipment / Logistics</option>
                  </select>
                </div>
                
                <button 
                  @click="submitRegistrationForm" 
                  class="btn-corp btn-corp-primary w-full py-6 text-lg mt-4"
                  :disabled="bookingInProgress"
                >
                  {{ bookingInProgress ? 'Processing Metadata...' : 'Book Event Ticket' }}
                </button>
              </div>
              <div v-else class="sold-out-panel">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line></svg>
                <span>Capacity Reached</span>
              </div>
            </template>
          </div>
        </div>
      </div>
      
      <div v-if="event" class="similar-events-corp mt-20 animate-corp delay-200">
        <h3 class="label-muted mb-10">Lateral Opportunities</h3>
        <RecommendationRow 
          :eventId="event.id" 
          title="" 
          :limit="4" 
        />
      </div>
    </div>

    <RazorpayCheckout 
      v-if="showCheckout"
      :is-open="showCheckout"
      :order-data="orderData"
      :event-id="String(event.id)"
      @close="showCheckout = false"
      @success="handlePaymentSuccess"
      @error="handlePaymentError"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import RazorpayCheckout from '../components/payment/RazorpayCheckout.vue';
import RecommendationRow from '../components/RecommendationRow.vue';

const route = useRoute();
const authStore = useAuthStore();

const event = ref<any>(null);
const loading = ref(true);
const error = ref('');
const registrationStatus = ref<string | null>(null);
const currentRegistrationId = ref<number | null>(null);

const bookingInProgress = ref(false);
const showCheckout = ref(false);
const orderData = ref<any>(null);

const fetchEvent = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/events/${route.params.id}`);
    event.value = res.data;
    if (authStore.isAuthenticated && authStore.isUser) {
      checkRegistrationStatus();
    }
  } catch (err: any) {
    error.value = 'Event not found.';
  } finally {
    loading.value = false;
  }
};

const checkRegistrationStatus = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/registrations/my', {
      headers: { Authorization: `Bearer ${authStore.token}` }
    });
    const reg = res.data.find((r: any) => r.event_id === event.value.id);
    if (reg) {
      registrationStatus.value = reg.status;
      currentRegistrationId.value = reg.id;
    }
  } catch (e) {
    console.error("Failed to check reg status", e);
  }
};

const regForm = ref({
  role: 'athlete',
  role_details: {
    team: '',
    service: 'catering'
  }
});

const submitRegistrationForm = async () => {
  bookingInProgress.value = true;
  try {
    await axios.post(
      'http://localhost:8000/api/registrations',
      { 
        event_id: event.value.id,
        role: regForm.value.role,
        role_details: regForm.value.role_details
      },
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    );
    
    if (event.value.price === 0) {
      alert('Registration successful! (Free Event)');
      bookingInProgress.value = false;
      fetchEvent();
      return;
    }
    
    initiateBooking();
  } catch (err: any) {
    if (err.response?.data?.message === 'Already registered') {
       if (event.value.price > 0) {
          initiateBooking();
       } else {
         alert('You are already registered!');
         bookingInProgress.value = false;
       }
    } else {
      alert(err.response?.data?.message || 'Failed to submit registration');
      bookingInProgress.value = false;
    }
  }
};

const initiateBooking = async () => {
  bookingInProgress.value = true;
  try {
    const res = await axios.post(
      'http://localhost:8000/api/payments/create-order',
      { event_id: event.value.id },
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    );
    orderData.value = res.data;
    showCheckout.value = true;
  } catch (err: any) {
    alert(err.response?.data?.message || 'Failed to initiate booking');
  } finally {
    bookingInProgress.value = false;
  }
};

const handlePaymentSuccess = () => {
  showCheckout.value = false;
  alert('Payment successful! Your ticket is confirmed.');
  fetchEvent();
};

const handlePaymentError = (msg: string) => {
  showCheckout.value = false;
  alert(msg);
};

const cancelRegistration = async () => {
  if (!confirm('Are you sure you want to cancel this ticket?')) return;
  try {
    await axios.put(
      `http://localhost:8000/api/registrations/${currentRegistrationId.value}/cancel`,
      {},
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    );
    alert('Ticket cancelled.');
    fetchEvent();
  } catch (err: any) {
    alert('Failed to cancel: ' + err.response?.data?.message);
  }
};

onMounted(() => {
  fetchEvent();
});
</script>

<style scoped>
.event-detail-page {
  background-color: var(--bg-site);
  min-height: 100vh;
  position: relative;
}

.back-btn-corp {
  background: none;
  border: none;
  color: var(--text-dim);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s var(--ease-luxury);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.8rem;
}

.back-btn-corp:hover {
  color: white;
  transform: translateX(-8px);
}

.detail-card-corp {
  padding: 2.5rem;
}

.hero-title-large {
  font-size: 2.5rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  line-height: 1.05;
}

.info-grid-corp {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.stats-grid-corp {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.border-top-luxury {
  border-top: 1px solid var(--border-subtle);
}

.registration-panel-corp {
  background: rgba(10, 10, 15, 0.4);
  border-radius: var(--radius-lg);
  padding: 3rem;
  border: 1px solid var(--border-subtle);
  box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
  margin-top: 2rem;
}

.status-panel-corp {
  background: rgba(0, 240, 255, 0.05);
  border: 1px solid rgba(0, 240, 255, 0.2);
  padding: 2.5rem;
  border-radius: var(--radius-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 0 30px rgba(0, 240, 255, 0.05);
}

.status-text {
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--brand-primary);
  margin-top: 0.5rem;
  letter-spacing: 0.05em;
}

.btn-corp-link-danger {
  color: #ff5555;
  background: none;
  border: none;
  font-weight: 800;
  cursor: pointer;
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  transition: var(--transition-fast);
}

.btn-corp-link-danger:hover {
  filter: brightness(1.2);
  text-decoration: underline;
}

.sold-out-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: var(--text-dim);
  font-weight: 900;
  text-transform: uppercase;
  padding: 2.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-md);
  font-size: 1.2rem;
  letter-spacing: 0.2em;
}

.loading-corp-full {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 80px 0;
  color: var(--text-dim);
}

.text-xl { font-size: 1.1rem; }
.text-3xl { font-size: 1.5rem; }
.text-4xl { font-size: 1.75rem; }
.font-600 { font-weight: 600; }
.font-900 { font-weight: 900; }

@media (max-width: 1024px) {
  .detail-card-corp { padding: 1.5rem; }
  .hero-title-large { font-size: 2rem; }
  .info-grid-corp, .stats-grid-corp { grid-template-columns: 1fr; gap: 1.5rem; }
}
</style>
