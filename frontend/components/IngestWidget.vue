<template>
  <div class="ingest-widget glass-panel">
    <div class="header">
      <h3 class="neon-text-sec">DATA INGESTION</h3>
    </div>
    
    <div 
      class="drop-zone"
      @dragover.prevent="dragOver"
      @dragleave.prevent="dragLeave"
      @drop.prevent="handleDrop"
      :class="{ 'active': isDragging }"
    >
      <div v-if="selectedFiles.length === 0" class="placeholder" @click="triggerFileInput">
        <div class="icon">⭳</div>
        <p>DROP DATA PACKET HERE</p>
        <span class="sub">or click to browse</span>
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileSelect" 
          class="hidden-input"
          multiple
        />
      </div>

      <div v-else class="file-preview">
        <div class="file-info">
          <span class="file-name">{{ selectedFiles.length === 1 ? selectedFiles[0].name : `${selectedFiles.length} files selected` }}</span>
          <span class="file-size">{{ formatInfo(selectedFiles) }}</span>
        </div>
        <button @click="clearFile" class="remove-btn">×</button>
      </div>
    </div>

    <div class="collection-input">
      <label>TARGET DATASET:</label>
      <input 
        v-model="collectionName" 
        type="text" 
        placeholder="default"
        class="neon-input-sm"
        disabled
      />
    </div>

    <div class="actions">
      <div v-if="status" :class="['status-msg', statusType]">
        {{ status }}
      </div>
      <button 
        @click="uploadFile" 
        class="ingest-btn"
        :disabled="selectedFiles.length === 0 || uploading"
      >
        {{ uploading ? 'UPLOADING...' : 'INITIATE UPLOAD' }}
      </button>
    </div>
    
    <div v-if="uploading" class="progress-bar-container">
      <div class="progress-bar"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const { ingest } = useRagApi();

const isDragging = ref(false);
const selectedFiles = ref([]);
const collectionName = ref('default');
const fileInput = ref(null);
const uploading = ref(false);
const status = ref('');
const statusType = ref('info');

const dragOver = () => { isDragging.value = true; };
const dragLeave = () => { isDragging.value = false; };

const handleDrop = (e) => {
  isDragging.value = false;
  const files = Array.from(e.dataTransfer.files);
  if (files.length) selectedFiles.value = files;
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileSelect = (e) => {
  const files = Array.from(e.target.files);
  if (files.length) selectedFiles.value = files;
};

const clearFile = () => {
  selectedFiles.value = [];
  status.value = '';
  if (fileInput.value) fileInput.value.value = '';
};

const uploadFile = async () => {
  if (!selectedFiles.value.length) return;

  uploading.value = true;
  status.value = 'Transmitting data...';
  statusType.value = 'info';

  try {
    await ingest(selectedFiles.value, collectionName.value);
    status.value = 'Upload Complete. Resources Indexed.';
    statusType.value = 'success';
    setTimeout(clearFile, 3000);
  } catch (err) {
    status.value = 'Upload Failed. Network Error.';
    statusType.value = 'error';
  } finally {
    uploading.value = false;
  }
};

const formatInfo = (files) => {
  if (files.length === 1) {
    const bytes = files[0].size;
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
  return `${files.length} items`;
};

const formatSize = (bytes) => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};
</script>

<style scoped>
.ingest-widget {
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.header h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  letter-spacing: 2px;
}

.neon-text-sec {
  color: var(--color-secondary);
  text-shadow: 0 0 5px var(--color-secondary);
}

.drop-zone {
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
  background: rgba(0,0,0,0.2);
}

.drop-zone:hover, .drop-zone.active {
  border-color: var(--color-secondary);
  background: rgba(188, 19, 254, 0.05);
  box-shadow: 0 0 15px rgba(188, 19, 254, 0.1);
}

.placeholder {
  pointer-events: auto;
}

/* Make Drop Zone clickable by covering with input or click handler */
.hidden-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.icon {
  font-size: 2rem;
  color: var(--color-secondary);
  margin-bottom: 0.5rem;
}

.sub {
  display: block;
  font-size: 0.8rem;
  color: var(--color-text-dim);
  margin-top: 0.5rem;
}

.file-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255,255,255,0.05);
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.remove-btn {
  background: none;
  border: none;
  color: #ff4444;
  font-size: 1.5rem;
  cursor: pointer;
}

.ingest-btn {
  width: 100%;
  margin-top: 1rem;
  background: transparent;
  border: 1px solid var(--color-secondary);
  color: var(--color-secondary);
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.ingest-btn:hover:not(:disabled) {
  background: var(--color-secondary);
  color: #fff;
  box-shadow: 0 0 15px var(--color-secondary);
}

.ingest-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.status-msg {
  margin-top: 1rem;
  font-size: 0.9rem;
  text-align: center;
}
.status-msg.success { color: #00ff88; }
.status-msg.error { color: #ff4444; }

.progress-bar-container {
  height: 4px;
  background: rgba(255,255,255,0.1);
  margin-top: 1rem;
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: var(--color-secondary);
  width: 50%; /* Animated in real app */
  animation: progress-indeterminate 1s infinite linear;
}

@keyframes progress-indeterminate {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(200%); }
}

.collection-input {
  margin-top: 1.5rem;
}

.collection-input label {
  display: block;
  font-size: 0.8rem;
  color: var(--color-text-dim);
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}

.neon-input-sm {
  width: 100%;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 0.6rem;
  border-radius: 6px;
  font-family: inherit;
  outline: none;
  transition: all 0.3s;
  box-sizing: border-box; /* Fix width overflow */
}

.neon-input-sm:focus {
  border-color: var(--color-secondary);
  box-shadow: 0 0 10px rgba(188, 19, 254, 0.2);
}
</style>
