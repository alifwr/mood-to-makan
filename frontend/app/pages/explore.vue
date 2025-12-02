<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const query = ref('')
const searchResults = ref<any[]>([])
const isSearching = ref(false)

// Initial fetch of all stores
const { data: allStores } = await useApi<any[]>('/stores/')

const handleSearch = async () => {
  if (!query.value) {
    searchResults.value = []
    return
  }

  isSearching.value = true
  try {
    const { data } = await useApi<any[]>('/ai/search', {
      method: 'POST',
      query: { query: query.value }
    })
    searchResults.value = data.value || []
  } catch (e) {
    console.error(e)
  } finally {
    isSearching.value = false
  }
}

const displayStores = computed(() => {
  return searchResults.value.length > 0 ? searchResults.value : (allStores.value || [])
})
</script>

<template>
  <div class="py-12">
    <!-- AI Search Header -->
    <div class="text-center max-w-3xl mx-auto mb-16">
      <h1 class="text-4xl md:text-5xl font-serif font-bold text-nature-900 mb-6">
        Lagi <span class="text-leaf-600 italic">mood</span> makan apa?
      </h1>
      <div class="relative">
        <input 
          v-model="query" 
          @keyup.enter="handleSearch"
          type="text" 
          class="w-full px-8 py-5 rounded-full border-2 border-nature-200 focus:border-leaf-500 focus:ring-4 focus:ring-leaf-100 outline-none text-lg shadow-lg transition-all"
          placeholder="Coba 'mie pedas tempat nyaman' atau 'martabak manis deket sini'..." 
        />
        <button 
          @click="handleSearch"
          class="absolute right-3 top-3 bg-nature-800 text-white p-3 rounded-full hover:bg-nature-700 transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        </button>
      </div>
      <div class="mt-4 flex justify-center gap-2 text-sm text-nature-500">
        <span>Coba ini:</span>
        <button @click="query='Nasi Padang Asli'; handleSearch()" class="hover:text-leaf-600 underline">Nasi Padang Asli</button>
        <button @click="query='Tempat ngopi santuy'; handleSearch()" class="hover:text-leaf-600 underline">Kopi Santuy</button>
        <button @click="query='Jajanan murah meriah'; handleSearch()" class="hover:text-leaf-600 underline">Jajanan Murah</button>
      </div>
    </div>

    <!-- Results -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="store in displayStores" :key="store.id" class="group">
        <NuxtLink :to="`/stores/${store.id}`" class="block bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 border border-nature-100 h-full flex flex-col">
          <div class="h-64 overflow-hidden relative">
            <img :src="store.image_url || 'https://via.placeholder.com/600x400'" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
            <div class="absolute top-4 left-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider text-nature-800">
              {{ store.category }}
            </div>
            <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-6 pt-12">
              <h3 class="text-white text-xl font-bold font-serif">{{ store.name }}</h3>
            </div>
          </div>
          <div class="p-6 flex-1 flex flex-col justify-between">
            <div>
              <p class="text-nature-600 line-clamp-2 mb-4">{{ store.description }}</p>
              <div class="flex items-center gap-4 text-sm text-nature-500 mb-4">
                <span class="flex items-center gap-1">📍 {{ store.address }}</span>
              </div>
            </div>
            <div class="flex items-center justify-between pt-4 border-t border-nature-100">
              <span class="font-bold text-leaf-600">{{ store.price_range }}</span>
              <span class="text-sm font-medium text-nature-400 group-hover:text-nature-800 transition-colors">Lihat Detail →</span>
            </div>
          </div>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
