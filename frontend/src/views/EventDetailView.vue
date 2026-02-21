<template>
  <div class="event-detail-view animate-fade-in" v-if="event">
    <div class="event-hero glass-card mb-8">
      <div class="event-hero-content">
        <div class="mb-4">
          <span class="badge badge-primary mr-2">{{ event.sport_category }}</span>
          <span v-if="event.price_tier" class="badge badge-outline">{{ event.price_tier.toUpperCase() }}</span>
        </div>
        <h1 class="page-title">{{ event.title }}</h1>
        <p class="event-location text-secondary mb-4">📍 {{ event.venue_city }} - {{ event.venue_address }}</p>
        <p class="event-date text-primary text-xl font-bold mb-6">📅 {{ formattedDate }}</p>
        
        <div class="event-stats flex gap-6 mb-8">
          <div>
            <p class="text-secondary text-sm">Price</p>
            <p class="text-xl font-bold">₹{{ event.price }}</p>
          </div>
          <div>
            <p class="text-secondary text-sm">Capacity</p>
            <p class="text-xl font-bold">{{ event.capacity }} participants</p>
          </div>
          <div v-if="event.seats_remaining !== undefined">
            <p class="text-secondary text-sm">Availability</p>
            <p class="text-xl font-bold" :class="event.seats_remaining < 10 ? 'text-error' : ''">{{ event.seats_remaining }} seats left</p>
          </div>
        </div>

        <button 
          @click="startRegistration" 
          class="btn btn-primary btn-lg"
          :disabled="isRegistering || event.seats_remaining === 0"
        >
          {{ event.seats_remaining === 0 ? 'Sold Out' : (isRegistering ? 'Processing...' : 'Register Now') }}
        </button>
      </div>
      <div class="event-hero-visual">
         <div v-if="event.sport_category === 'Football'" class="sport-icon-large">⚽</div>
        <div v-else-if="event.sport_category === 'Cricket'" class="sport-icon-large">🏏</div>
        <div v-else-if="event.sport_category === 'Basketball'" class="sport-icon-large">🏀</div>
        <div v-else-if="event.sport_category === 'Tennis'" class="sport-icon-large">🎾</div>
         <div v-else class="sport-icon-large">🏆</div>
      </div>
    </div>

    <div class="content-grid">
      <div class="main-content glass-card">
        <h2 class="text-2xl font-bold mb-4">About the Event</h2>
        <p class="whitespace-pre-wrap text-secondary">{{ event.description || 'No description provided.' }}</p>
        
        <div v-if="event.tags && event.tags.length" class="mt-8">
          <h3 class="text-lg font-bold mb-2">Tags</h3>
          <div class="flex flex-wrap gap-2">
            <span v-for="tag in event.tags" :key="tag" class="badge badge-outline">#{{ tag }}</span>
          </div>
        </div>
      </div>

      <div class="sidebar">
        <div class="glass-card similar-events" v-if="similarEvents.length">
          <h3 class="text-xl font-bold mb-4">Similar Events</h3>
          <div class="flex flex-col gap-4">
            <EventCard v-for="simEvent in similarEvents" :key="simEvent.id" :event="simEvent" />
          </div>
        </div>
      </div>
    </div>

    <!-- Payment Simulation Modal -->
    <div v-if="showPaymentModal" class="modal-backdrop">
      <div class="glass-card modal-content animate-fade-in text-center">
        <h2 class="text-2xl font-bold mb-4">Complete Payment</h2>
        <p class="mb-6 text-secondary">You are registering for <strong>{{ event.title }}</strong>. The total amount is <strong>₹{{ event.price }}</strong></p>
        
        <div v-if="paymentError" class="error-msg mb-4">{{ paymentError }}</div>

        <div class="flex gap-4 justify-center">
          <button @click="simulatePayment" class="btn btn-primary" :disabled="isProcessingPayment">
            {{ isProcessingPayment ? 'Processing...' : 'Pay via Razorpay (Simulated)' }}
          </button>
          <button @click="cancelPayment" class="btn btn-outline" :disabled="isProcessingPayment">Cancel</button>
        </div>
      </div>
    </div>
  </div>
  
  <div v-else-if="loading" class="text-center py-12">
    <p>Loading event details...</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import EventCard from '../components/EventCard.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const event = ref<any>(null);
const similarEvents = ref<any[]>([]);
const loading = ref(true);

const isRegistering = ref(false);
const showPaymentModal = ref(false);
const isProcessingPayment = ref(false);
const paymentError = ref('');
const pendingRegistrationId = ref<number | null>(null);
const pendingPaymentId = ref<number | null>(null);

const formattedDate = computed(() => {
  if (!event.value?.event_date) return '';
  return new Date(event.value.event_date).toLocaleString('en-US', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });
});

const loadEvent = async () => {
  loading.value = true;
  try {
    const id = route.params.id;
    const [eventRes, similarRes] = await Promise.all([
      api.get(`/events/${id}`),
      api.get(`/events/${id}/similar`).catch(() => ({ data: [] }))
    ]);
    event.value = eventRes.data.event || eventRes.data;
    similarEvents.value = similarRes.data || [];
  } catch (err) {
    console.error(err);
    router.push('/events');
  } finally {
    loading.value = false;
  }
};

const startRegistration = async () => {
  if (!authStore.token) {
    router.push('/login');
    return;
  }

  isRegistering.value = true;
  try {
    // 1. Create Registration
    const regRes = await api.post('/registrations', { event_id: event.value.id });
    pendingRegistrationId.value = regRes.data.registration.id;
    
    // 2. Initiate Payment if price > 0
    if (event.value.price > 0) {
      const payRes = await api.post('/payments', {
        registration_id: pendingRegistrationId.value,
        amount: event.value.price,
        payment_method: 'razorpay'
      });
      pendingPaymentId.value = payRes.data.payment.id;
      
      // Open modal to simulate Razorpay
      showPaymentModal.value = true;
    } else {
      // Free event, registration complete
      alert('Successfully registered for the free event!');
      router.push('/profile');
    }
  } catch (err: any) {
    alert(err.response?.data?.message || 'Failed to start registration');
  } finally {
    isRegistering.value = false;
  }
};

const simulatePayment = async () => {
  isProcessingPayment.value = true;
  paymentError.value = '';
  
  try {
    // Simulate Razorpay Webhook Verification
    await api.post(`/payments/verify/${pendingPaymentId.value}`, {
      razorpay_payment_id: `pay_mock_${Date.now()}`,
      razorpay_order_id: `order_mock_${pendingPaymentId.value}`,
      razorpay_signature: 'mock_signature'
    });
    
    alert('Payment successful! Registration confirmed.');
    showPaymentModal.value = false;
    router.push('/profile');
  } catch (err: any) {
    paymentError.value = err.response?.data?.message || 'Payment verification failed.';
  } finally {
    isProcessingPayment.value = false;
  }
};

const cancelPayment = () => {
  showPaymentModal.value = false;
  paymentError.value = '';
  // Optionally clean up pending registration/payment via API
};

onMounted(() => {
  loadEvent();
});
</script>

<style scoped>
.mb-8 { margin-bottom: 2rem; }
.mb-6 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mt-8 { margin-top: 2rem; }
.mr-2 { margin-right: 0.5rem; }
.py-12 { padding-top: 3rem; padding-bottom: 3rem; }
.text-center { text-align: center; }

.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.gap-6 { gap: 1.5rem; }
.gap-4 { gap: 1rem; }
.gap-2 { gap: 0.5rem; }
.justify-center { justify-content: center; }

.text-secondary { color: var(--text-secondary); }
.text-primary { color: var(--accent-primary); }
.text-error { color: var(--error); }
.text-sm { font-size: 0.875rem; }
.text-lg { font-size: 1.125rem; }
.text-xl { font-size: 1.25rem; }
.text-2xl { font-size: 1.5rem; }
.font-bold { font-weight: 700; }
.whitespace-pre-wrap { white-space: pre-wrap; }

.event-hero {
  display: flex;
  flex-direction: column-reverse;
  padding: 0;
  overflow: hidden;
}

@media (min-width: 768px) {
  .event-hero {
    flex-direction: row;
  }
}

.event-hero-content {
  padding: 3rem;
  flex: 1;
}

.event-hero-visual {
  flex: 1;
  background: linear-gradient(135deg, var(--bg-tertiary), #2a2a35);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.sport-icon-large {
  font-size: 8rem;
  opacity: 0.5;
}

.btn-lg {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 1024px) {
  .content-grid {
    grid-template-columns: 2fr 1fr;
  }
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(10, 10, 15, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 500px;
  border: 1px solid var(--accent-primary);
  box-shadow: 0 0 40px rgba(0, 229, 255, 0.2);
}

.error-msg {
  color: var(--error);
  font-size: 0.9rem;
  background: rgba(255, 23, 68, 0.1);
  padding: 0.75rem;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(255, 23, 68, 0.2);
}
</style>
