<script setup lang="ts">
definePageMeta({
  layout: 'umkm',
  middleware: ['auth']
})
</script>

<template>
  <div>
    <h1 class="text-3xl font-serif font-bold text-nature-900 mb-8">Ulasan Pelanggan</h1>
    <div class="bg-white p-12 rounded-2xl shadow-sm border border-nature-100 text-center">
      <div class="text-6xl mb-4">⭐</div>
      <h2 class="text-xl font-bold text-nature-800 mb-2">Kata Mereka</h2>
      <p class="text-nature-600">Fitur ulasan akan segera hadir. Pantau terus ya!</p>
    </div>
  </div>
</template>
