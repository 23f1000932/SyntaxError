<template>
  <div class="checkout-modal" v-if="isOpen">
    <div class="checkout-content">
      <div class="header">
        <h3>Complete Payment</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="order-details">
        <p><strong>Order ID:</strong> {{ orderData.order_id }}</p>
        <p><strong>Amount:</strong> ₹{{ (orderData.amount / 100).toFixed(2) }}</p>
      </div>

      <div class="mock-bank">
        <h4>Razorpay Test Environment</h4>
        <p class="info-text">You are in test mode. Click below to simulate a successful payment.</p>
        
        <button 
          class="btn btn-success" 
          @click="simulateSuccess"
          :disabled="processing"
        >
          {{ processing ? 'Processing...' : 'Simulate Success' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const props = defineProps<{
  isOpen: boolean;
  orderData: {
    order_id: string;
    amount: number;
    key_id: string;
  };
  eventId: string;
}>();

const emit = defineEmits(['close', 'success', 'error']);
const authStore = useAuthStore();
const processing = ref(false);

const simulateSuccess = async () => {
  processing.value = true;
  try {
    // Simulate Razorpay returning a success payload
    const mockPayload = {
      razorpay_order_id: props.orderData.order_id,
      razorpay_payment_id: `pay_${Math.random().toString(36).substr(2, 9)}`,
      razorpay_signature: "test_signature" // Our backend handles this gracefully
    };

    // Send verification request to our backend
    const response = await axios.post(
      'http://localhost:8000/api/payments/verify', 
      mockPayload,
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    );

    emit('success', response.data);
  } catch (err: any) {
    emit('error', err.response?.data?.message || 'Payment verification failed');
  } finally {
    processing.value = false;
  }
};
</script>

<style scoped>
.checkout-modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.checkout-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.order-details {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.mock-bank {
  text-align: center;
  padding: 1.5rem;
  border: 1px dashed #00bcd4;
  border-radius: 4px;
}

.info-text {
  color: #666;
  font-size: 0.9rem;
  margin: 1rem 0;
}

.btn {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>
