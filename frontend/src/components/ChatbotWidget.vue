<template>
  <div class="chatbot-widget">
    <!-- Chat Button -->
    <button 
      v-if="!isOpen" 
      class="chat-toggle-btn"
      @click="isOpen = true"
    >
      💬 Chat Support
    </button>

    <!-- Chat Window -->
    <div v-else class="chat-window">
      <div class="chat-header">
        <h4>AI Support Assistant</h4>
        <button class="close-btn" @click="isOpen = false">&times;</button>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="(msg, index) in messages" 
          :key="index"
          :class="['message', msg.role]"
        >
          <div class="msg-content">{{ msg.content }}</div>
          <div v-if="msg.escalated" class="escalation-warning">
            ⚠️ Transferred to human agent.
          </div>
        </div>
        <div v-if="loading" class="message bot loading-dots">
          Typing...
        </div>
      </div>

      <div class="chat-input-area">
        <input 
          v-model="inputMsg" 
          @keyup.enter="sendMessage"
          type="text" 
          placeholder="Ask a question..."
          :disabled="loading"
        />
        <button @click="sendMessage" :disabled="!inputMsg.trim() || loading">Send</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const isOpen = ref(false);
const loading = ref(false);
const inputMsg = ref('');
const messagesContainer = ref<HTMLElement | null>(null);

type Message = {
  role: 'user' | 'bot';
  content: string;
  escalated?: boolean;
};

const messages = ref<Message[]>([
  { role: 'bot', content: 'Hi there! I can help you with registrations, events, and payments. What do you need help with?' }
]);

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const sendMessage = async () => {
  const txt = inputMsg.value.trim();
  if (!txt) return;

  // Add User message
  messages.value.push({ role: 'user', content: txt });
  inputMsg.value = '';
  loading.value = true;
  await scrollToBottom();

  try {
    const config = authStore.token 
        ? { headers: { Authorization: `Bearer ${authStore.token}` } } 
        : {};

    const res = await axios.post(
      'http://localhost:8000/api/chatbot',
      { message: txt },
      config
    );

    messages.value.push({ 
      role: 'bot', 
      content: res.data.response,
      escalated: res.data.escalated
    });
  } catch (err) {
    messages.value.push({ 
      role: 'bot', 
      content: 'Sorry, I am having trouble connecting to the server.' 
    });
  } finally {
    loading.value = false;
    await scrollToBottom();
  }
};
</script>

<style scoped>
.chatbot-widget {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
}

.chat-toggle-btn {
  background: #00bcd4;
  color: white;
  border: none;
  padding: 1rem 1.5rem;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transition: transform 0.2s;
}

.chat-toggle-btn:hover {
  transform: translateY(-2px);
}

.chat-window {
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 25px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h4 { margin: 0; }

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: #f9f9f9;
}

.message {
  max-width: 80%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  font-size: 0.95rem;
  line-height: 1.4;
}

.message.user {
  align-self: flex-end;
  background: #00bcd4;
  color: white;
  border-bottom-right-radius: 2px;
}

.message.bot {
  align-self: flex-start;
  background: white;
  color: #333;
  border: 1px solid #eee;
  border-bottom-left-radius: 2px;
}

.escalation-warning {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #d32f2f;
  background: #ffebee;
  padding: 0.5rem;
  border-radius: 4px;
}

.chat-input-area {
  padding: 1rem;
  background: white;
  border-top: 1px solid #eee;
  display: flex;
  gap: 0.5rem;
}

.chat-input-area input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.chat-input-area input:focus {
  border-color: #00bcd4;
}

.chat-input-area button {
  background: #00bcd4;
  color: white;
  border: none;
  padding: 0 1rem;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
}

.chat-input-area button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading-dots {
  color: #888;
  font-style: italic;
}
</style>
