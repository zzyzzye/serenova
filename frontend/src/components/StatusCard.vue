<template>
  <section class="panel status-card">
    <div class="status-row">
      <span class="status-label">后端状态</span>
      <span :class="['status-badge', statusClass]">{{ statusText }}</span>
    </div>
    <dl v-if="healthData" class="status-grid">
      <div>
        <dt>服务名</dt>
        <dd>{{ healthData.service }}</dd>
      </div>
      <div>
        <dt>版本</dt>
        <dd>{{ healthData.version }}</dd>
      </div>
    </dl>
    <p v-if="message" class="status-message">{{ message }}</p>
  </section>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  healthData: {
    type: Object,
    default: null,
  },
  errorMessage: {
    type: String,
    default: "",
  },
});

const statusText = computed(() => {
  if (props.loading) return "检测中";
  if (props.errorMessage) return "不可用";
  if (props.healthData) return "正常";
  return "未检测";
});

const statusClass = computed(() => {
  if (props.loading) return "is-loading";
  if (props.errorMessage) return "is-error";
  if (props.healthData) return "is-ok";
  return "is-idle";
});

const message = computed(() => {
  if (props.errorMessage) return props.errorMessage;
  if (props.loading) return "正在请求后端健康检查接口。";
  if (props.healthData) return "前后端联通正常，可以在此基础上继续开发业务。";
  return "";
});
</script>

<style scoped>
.status-card {
  padding: 24px;
}

.status-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.status-label {
  font-size: 18px;
  font-weight: 600;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 14px;
}

.is-ok {
  color: #166534;
  background: #dcfce7;
}

.is-error {
  color: #991b1b;
  background: #fee2e2;
}

.is-loading {
  color: #92400e;
  background: #fef3c7;
}

.is-idle {
  color: #374151;
  background: #e5e7eb;
}

.status-grid {
  margin: 20px 0 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

dt {
  color: #6b7280;
  font-size: 13px;
}

dd {
  margin: 6px 0 0;
  font-size: 16px;
  font-weight: 600;
}

.status-message {
  margin: 20px 0 0;
  color: #4b5563;
}
</style>
