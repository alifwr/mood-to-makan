<script setup lang="ts">
definePageMeta({
  layout: 'umkm',
  middleware: ['auth'] // We need to create this middleware
})

const { data: stores } = await useApi<any[]>('/stores/')
// Filter stores for current user (client-side filtering as per plan)
const authStore = useAuthStore()
const myStores = computed(() => stores.value?.filter(s => s.owner_id === authStore.user?.id) || [])
</script>

<template>
  <div>
    <h1 class="text-3xl font-serif font-bold text-nature-900 mb-8">Ringkasan Toko</h1>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-nature-100">
        <div class="text-nature-500 text-sm mb-1">Total Toko</div>
        <div class="text-3xl font-bold text-nature-800">{{ myStores.length }}</div>
      </div>
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-nature-100">
        <div class="text-nature-500 text-sm mb-1">Total Produk</div>
        <div class="text-3xl font-bold text-nature-800">-</div>
      </div>
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-nature-100">
        <div class="text-nature-500 text-sm mb-1">Total Ulasan</div>
        <div class="text-3xl font-bold text-nature-800">-</div>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-sm border border-nature-100 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-nature-800">Toko Kamu</h2>
        <NuxtLink to="/umkm/stores/create" class="px-4 py-2 bg-leaf-600 text-white rounded-lg text-sm font-medium hover:bg-leaf-500 transition-colors">
          + Tambah Toko Baru
        </NuxtLink>
      </div>

      <div v-if="myStores.length === 0" class="text-center py-12 text-nature-500">
        Belum ada toko nih, bikin dulu gih.
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="store in myStores" :key="store.id" class="border border-nature-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
          <img :src="store.image_url || 'https://via.placeholder.com/400x200?text=No+Image'" class="w-full h-48 object-cover" />
          <div class="p-4">
            <h3 class="font-bold text-lg mb-1">{{ store.name }}</h3>
            <p class="text-sm text-nature-600 line-clamp-2 mb-4">{{ store.description }}</p>
            <NuxtLink :to="`/umkm/stores/${store.id}`" class="text-leaf-600 font-medium text-sm hover:underline">
              Atur Toko →
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
