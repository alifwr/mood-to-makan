<script setup lang="ts">
definePageMeta({
  layout: 'umkm',
  middleware: ['auth']
})

const { data: stores } = await useApi<any[]>('/stores/')
const authStore = useAuthStore()
const myStores = computed(() => stores.value?.filter(s => s.owner_id === authStore.user?.id) || [])
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-serif font-bold text-nature-900">Toko Gue</h1>
      <NuxtLink to="/umkm/stores/create" class="px-4 py-2 bg-leaf-600 text-white rounded-lg font-medium hover:bg-leaf-500 transition-colors">
        + Buka Toko Baru
      </NuxtLink>
    </div>

    <div v-if="myStores.length === 0" class="text-center py-20 bg-white rounded-2xl border border-nature-100">
      <div class="text-6xl mb-4">🏪</div>
      <h3 class="text-xl font-bold text-nature-800 mb-2">Belum Ada Toko</h3>
      <p class="text-nature-600 mb-6">Mulai langkahmu dengan buka toko pertama.</p>
      <NuxtLink to="/umkm/stores/create" class="px-6 py-3 bg-nature-800 text-white rounded-xl font-medium hover:bg-nature-700">
        Buka Toko
      </NuxtLink>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="store in myStores" :key="store.id" class="bg-white border border-nature-200 rounded-xl overflow-hidden hover:shadow-lg transition-all group">
        <div class="h-48 overflow-hidden relative">
          <img :src="store.image_url || 'https://via.placeholder.com/400x200?text=No+Image'" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
          <div class="absolute top-2 right-2 bg-white/90 px-2 py-1 rounded text-xs font-bold uppercase tracking-wider text-nature-800">
            {{ store.category }}
          </div>
        </div>
        <div class="p-5">
          <h3 class="font-bold text-xl mb-2 text-nature-900">{{ store.name }}</h3>
          <p class="text-sm text-nature-600 line-clamp-2 mb-4">{{ store.description }}</p>
          <div class="flex items-center justify-between pt-4 border-t border-nature-100">
            <span class="text-sm font-medium text-nature-500">{{ store.price_range }}</span>
            <NuxtLink :to="`/umkm/stores/${store.id}`" class="text-leaf-600 font-medium hover:text-leaf-700">
              Atur →
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
