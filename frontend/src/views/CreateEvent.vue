<template>
  <div class="create-event-page">
    <div class="form-container">
      <h1>Create New Event</h1>
      <form @submit.prevent="handleSubmit" class="event-form">
        <div class="form-group">
          <label>Title</label>
          <input v-model="form.title" type="text" required />
        </div>
        
        <div class="form-group">
          <label>Description</label>
          <textarea v-model="form.description" rows="4"></textarea>
        </div>
        
        <div class="form-group">
          <label>Date and Time</label>
          <input v-model="form.date" type="datetime-local" required />
        </div>
        
        <div class="form-group">
          <label>Location</label>
          <input v-model="form.location" type="text" required />
        </div>
        
        <div class="form-group">
          <label>Category</label>
          <select v-model="form.category" required>
            <option value="Football">Football</option>
            <option value="Basketball">Basketball</option>
            <option value="Tennis">Tennis</option>
            <option value="Cricket">Cricket</option>
            <option value="Swimming">Swimming</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="form-group">
          <label>Max Participants</label>
          <input v-model="form.max_participants" type="number" min="1" required />
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>
        
        <div class="actions">
          <button type="button" class="btn btn-secondary" @click="router.push('/organizer')">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Event' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useEventsStore } from '@/stores/events';

const router = useRouter();
const eventsStore = useEventsStore();

const loading = ref(false);
const error = ref('');

const form = ref({
  title: '',
  description: '',
  date: '',
  location: '',
  category: 'Football',
  max_participants: 100
});

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    // Convert local datetime to ISO format
    const isoDate = new Date(form.value.date).toISOString();
    
    await eventsStore.createEvent({
      ...form.value,
      date: isoDate
    });
    
    router.push('/organizer');
  } catch (err: any) {
    error.value = eventsStore.error || 'Failed to create event';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.create-event-page {
  padding: 2rem;
  display: flex;
  justify-content: center;
}

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 600px;
}

h1 {
  color: #333;
  margin-bottom: 1.5rem;
  text-align: center;
}

.event-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 500;
  color: #555;
}

input, textarea, select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.error-message {
  color: #dc3545;
  background: #f8d7da;
  padding: 0.75rem;
  border-radius: 4px;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}
</style>
