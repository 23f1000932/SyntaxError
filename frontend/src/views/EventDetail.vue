<template>
  <div class="event-detail-page">
    <div class="container">
      <button @click="$router.push('/home')" class="back-link">&larr; Back to Events</button>

      <div v-if="loading" class="loading-state">Loading event details...</div>
      
      <div v-else-if="error" class="error-state">{{ error }}</div>
      
      <div v-else-if="event" class="detail-card">
        <div class="header">
          <h1>{{ event.title }}</h1>
          <span class="badge" :class="event.price_tier">{{ event.price_tier?.toUpperCase() }}</span>
        </div>

        <div class="meta-info">
          <div class="meta-item">
            <strong>Sport:</strong> {{ event.sport_category }}
          </div>
          <div class="meta-item">
            <strong>Date:</strong> {{ new Date(event.event_date).toLocaleDateString() }}
          </div>
          <div class="meta-item">
            <strong>Location:</strong> {{ event.venue_city }}
          </div>
          <div class="meta-item" v-if="event.venue_address">
            <strong>Address:</strong> {{ event.venue_address }}
          </div>
        </div>

        <div class="description">
          <h3>About this Event</h3>
          <p>{{ event.description || 'No description provided.' }}</p>
        </div>

        <div class="registration-panel">
          <div class="stats">
            <div class="stat-box">
              <span class="label">Price</span>
              <span class="value">₹{{ event.price }}</span>
            </div>
            <div class="stat-box">
              <span class="label">Seats Remaining</span>
              <span class="value">{{ event.seats_remaining }} / {{ event.capacity }}</span>
            </div>
          </div>

          <div class="action-section">
            <template v-if="!authStore.isAuthenticated">
              <p>Please <router-link to="/login">login</router-link> to register.</p>
            </template>
            <template v-else-if="authStore.isUser">
              <div v-if="registrationStatus" class="status-msg">
                You are currently: <strong>{{ registrationStatus }}</strong>
                <button v-if="registrationStatus === 'confirmed'" @click="cancelRegistration" class="btn btn-danger ml-2">Cancel Ticket</button>
              </div>
              <button 
                v-else-if="event.seats_remaining > 0"
                @click="initiateBooking" 
                class="btn btn-primary btn-lg"
                :disabled="bookingInProgress"
              >
                {{ bookingInProgress ? 'Processing...' : 'Book Ticket' }}
              </button>
              <div v-else class="sold-out">This event is sold out!</div>
            </template>
          </div>
        </div>
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
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import RazorpayCheckout from '../components/payment/RazorpayCheckout.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const event = ref<any>(null);
const loading = ref(true);
const error = ref('');
const registrationStatus = ref<string | null>(null);
const currentRegistrationId = ref<number | null>(null);

// Payment State
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
  fetchEvent(); // Refresh data
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
  padding: 2rem 0;
  background-color: #f5f5f5;
  min-height: calc(100vh - 80px);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.back-link {
  background: none;
  border: none;
  color: #00bcd4;
  cursor: pointer;
  font-size: 1rem;
  margin-bottom: 2rem;
  padding: 0;
}

.detail-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.header {
  padding: 2rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  margin: 0;
  font-size: 2rem;
  color: #333;
}

.badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: bold;
}
.badge.cheap { background: #e8f5e9; color: #2e7d32; }
.badge.mid { background: #e3f2fd; color: #1565c0; }
.badge.premium { background: #fff3e0; color: #ef6c00; }

.meta-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  padding: 2rem;
  background: #fafafa;
}

.meta-item {
  color: #555;
}

.description {
  padding: 2rem;
}

.description h3 {
  margin-bottom: 1rem;
  color: #333;
}

.registration-panel {
  padding: 2rem;
  background: #f8f9fa;
  border-top: 1px solid #eee;
}

.stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.stat-box {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  flex: 1;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.stat-box .label {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.stat-box .value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.action-section {
  text-align: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn:hover { opacity: 0.9; }

.btn-primary { background: #00bcd4; color: white; }
.btn-danger { background: #dc3545; color: white; }
.btn-lg { padding: 1rem 3rem; font-size: 1.1rem; }

.ml-2 { margin-left: 0.5rem; }

.sold-out {
  color: #dc3545;
  font-weight: bold;
  font-size: 1.2rem;
}

.status-msg {
  padding: 1rem;
  background: #d4edda;
  color: #155724;
  border-radius: 4px;
}
</style>
