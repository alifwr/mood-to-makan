<script setup lang="ts">
const { toasts, removeToast } = useToast()
</script>

<template>
  <div class="fixed top-4 right-4 z-[100] flex flex-col gap-2 pointer-events-none">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="pointer-events-auto min-w-[300px] p-4 rounded-lg shadow-lg text-white transform transition-all duration-300 flex justify-between items-center"
        :class="{
          'bg-green-500': toast.type === 'success',
          'bg-red-500': toast.type === 'error',
          'bg-blue-500': toast.type === 'info',
          'bg-yellow-500': toast.type === 'warning'
        }"
      >
        <span>{{ toast.message }}</span>
        <button @click="removeToast(toast.id)" class="ml-4 text-white/80 hover:text-white">
          ✕
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
