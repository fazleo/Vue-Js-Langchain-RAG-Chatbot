<template>
  <div class="chat-widget glass-panel">
    <div class="chat-header">
      <h2 class="neon-text">CHAT WITH BOT</h2>
      <div class="status-dot"></div>
      <div class="header-controls">
         <input 
          v-model="collectionName" 
          type="text" 
          placeholder="Collection" 
          class="neon-input-xs"
          title="Target Collection"
          disabled
        />
      </div>
    </div>
    
    <div class="chat-messages" ref="messagesRef">
      <div 
        v-for="(msg, index) in messages" 
        :key="index"
        :class="['message', msg.role === 'user' ? 'user' : 'ai']"
      >
        <div class="message-content">
          <div v-if="msg.role === 'ai'" v-html="renderMarkdown(msg.content)"></div>
          <div v-else>{{ msg.content }}</div>

          <div v-if="msg.sources && msg.sources.length" class="sources-list">
            <small class="sources-label">DATA STREAMS:</small>
            <div v-for="(source, sIdx) in msg.sources" :key="sIdx" class="source-item">
              > {{ source }}
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="loading" class="message ai loading">
        <span class="typing-cursor">_</span>
      </div>
    </div>

    <div class="chat-input-area">
      <input 
        v-model="inputMessage" 
        @keyup.enter="sendMessage"
        type="text" 
        placeholder="Enter command query..."
        :disabled="loading"
        class="neon-input"
      />
      <button @click="sendMessage" :disabled="!inputMessage || loading" class="send-btn">
        SEND
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt({ html: true, linkify: true, typographer: true });
const { chat } = useRagApi();

const messages = ref([
  { role: 'ai', content: 'System Online. Ready for queries.' }
]);
const inputMessage = ref('');
const collectionName = ref('default');
const loading = ref(false);
const messagesRef = ref(null);

const renderMarkdown = (text) => {
  return md.render(text || '');
};

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return;

  const userText = inputMessage.value;
  messages.value.push({ role: 'user', content: userText });
  inputMessage.value = '';
  loading.value = true;
  
  await scrollToBottom();

  try {
    const response = await chat(userText, collectionName.value);
    // Assuming response format, adjust as needed e.g. response.answer or response.text
    // If backend returns plain string:
    // messages.value.push({ role: 'ai', content: response });
    // If object:
    const aiText = typeof response === 'string' ? response : (response?.answer || response?.message || JSON.stringify(response));
    const sources = response?.sources || [];
    messages.value.push({ role: 'ai', content: aiText, sources });
  } catch (err) {
    messages.value.push({ role: 'ai', content: 'Incompetent Network. Connection Severed.' });
  } finally {
    loading.value = false;
    await scrollToBottom();
  }
};

const scrollToBottom = async () => {
  await nextTick();
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
  }
};
</script>

<style scoped>
.chat-widget {
  display: flex;
  flex-direction: column;
  height: 600px;
  width: 100%;
  overflow: hidden;
}

.chat-header {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.status-dot {
  width: 10px;
  height: 10px;
  background-color: var(--color-primary);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--color-primary);
  box-shadow: 0 0 10px var(--color-primary);
  animation: pulse-glow 2s infinite;
}

.header-controls {
  margin-left: auto;
  margin-right: 1rem;
}

.neon-input-xs {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--color-primary);
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  width: 120px;
  outline: none;
  text-align: right;
}

.neon-input-xs:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 5px var(--color-primary-dim);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  max-width: 80%;
  padding: 0.8rem 1.2rem;
  border-radius: 12px;
  line-height: 1.5;
  font-size: 0.95rem;
}

.message.user {
  align-self: flex-end;
  background: rgba(0, 243, 255, 0.1);
  border: 1px solid var(--color-primary);
  color: #fff;
  border-bottom-right-radius: 2px;
}

.message.ai {
  align-self: flex-start;
  background: rgba(188, 19, 254, 0.1);
  border: 1px solid var(--color-secondary);
  color: #fff;
  border-bottom-left-radius: 2px;
}

/* Markdown Styles */
:deep(.message-content p) {
  margin: 0 0 0.5rem 0;
}

:deep(.message-content p:last-child) {
  margin-bottom: 0;
}

:deep(.message-content code) {
  background: rgba(0, 0, 0, 0.3);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
  color: #ff79c6; /* Dracula pinkish for high contrast */
}

:deep(.message-content pre) {
  background: rgba(0, 0, 0, 0.4);
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 0.5rem 0;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.message-content pre code) {
  background: transparent;
  padding: 0;
  color: inherit;
}

:deep(.message-content ul), :deep(.message-content ol) {
  padding-left: 1.5rem;
  margin: 0.5rem 0;
}

:deep(.message-content li) {
  margin-bottom: 0.2rem;
}

:deep(.message-content h1), :deep(.message-content h2), :deep(.message-content h3) {
  margin: 1rem 0 0.5rem 0;
  font-weight: 600;
  color: var(--color-primary);
}

:deep(.message-content a) {
  color: var(--color-primary);
  text-decoration: underline;
}

.sources-list {
  margin-top: 0.8rem;
  padding-top: 0.8rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.8rem;
}

.sources-label {
  display: block;
  color: var(--color-primary-dim);
  margin-bottom: 0.4rem;
  font-weight: bold;
}

.source-item {
  color: var(--color-text-dim);
  font-family: monospace;
}

.chat-input-area {
  padding: 1rem;
  display: flex;
  gap: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.2);
}

.neon-input {
  flex: 1;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 0.8rem;
  border-radius: 8px;
  font-family: inherit;
  outline: none;
  transition: all 0.3s;
}

.neon-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 243, 255, 0.2);
}

.send-btn {
  background: var(--color-primary);
  color: #000;
  border: none;
  padding: 0 1.5rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(1);
}

.typing-cursor {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
</style>
