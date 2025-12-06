<script setup lang="ts">
definePageMeta({
  layout: 'umkm',
  middleware: ['auth']
})
</script>

<template>
  <div>
    <h1 class="text-3xl font-serif font-bold text-nature-900 mb-8">Produk Kamu</h1>
    <div class="bg-white p-12 rounded-2xl shadow-sm border border-nature-100 text-center">
      <div class="text-6xl mb-4">📦</div>
      <h2 class="text-xl font-bold text-nature-800 mb-2">Kelola Menu di Sini</h2>
      <p class="text-nature-600 mb-6">Fitur ini akan segera hadir. Kamu bisa kelola menu lewat halaman Toko.</p>
      <NuxtLink to="/umkm/stores" class="px-6 py-3 bg-leaf-600 text-white rounded-xl font-medium hover:bg-leaf-500">
        Ke Halaman Toko
      </NuxtLink>
    </div>
  </div>
</template>
