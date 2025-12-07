<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: ['auth']
})

const route = useRoute()
const router = useRouter()
const query = route.query.q as string

const { data: searchResponse, pending, error } = await useApi<any>('/ai/search-foods', {
  params: {
    query: query,
    limit: 10
  }
})
</script>

<template>
  <div class="py-12 px-6 max-w-7xl mx-auto">
    <div class="mb-8">
      <button @click="router.back()" class="mb-4 text-nature-600 hover:text-nature-900 flex items-center gap-2 transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        Kembali
      </button>
      <h1 class="text-3xl font-serif font-bold text-nature-900">
        Hasil pencarian untuk "<span class="text-leaf-600">{{ query }}</span>"
      </h1>
      <p v-if="searchResponse" class="text-nature-600 mt-2">
        Ditemukan {{ searchResponse.total_results }} menu yang cocok dengan mood kamu.
      </p>
    </div>

    <div v-if="pending" class="flex justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-leaf-600"></div>
    </div>

    <div v-else-if="error" class="text-center py-12 text-red-600 bg-red-50 rounded-2xl">
      <p class="font-bold">Terjadi kesalahan saat mencari.</p>
      <p class="text-sm mt-1">{{ error }}</p>
    </div>

    <div v-else-if="!searchResponse?.foods?.length" class="text-center py-20 bg-nature-50 rounded-3xl">
      <div class="text-4xl mb-4">🤔</div>
      <h3 class="text-xl font-bold text-nature-800 mb-2">Belum ada menu yang pas nih</h3>
      <p class="text-nature-600">Coba cari dengan kata kunci mood yang lain ya.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <NuxtLink 
        v-for="food in searchResponse.foods" 
        :key="food.id"
        :to="`/foods/${food.id}`"
        class="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 border border-nature-100 group flex flex-col"
      >
        <div class="h-56 overflow-hidden relative bg-nature-100">
          <img :src="food.image_url || 'https://via.placeholder.com/400x300?text=No+Image'" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
          <div class="absolute top-3 left-3 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider text-nature-800 shadow-sm">
            {{ food.category }}
          </div>
        </div>
        <div class="p-5 flex-1 flex flex-col">
          <div class="flex justify-between items-start mb-2">
            <h3 class="font-bold text-lg text-nature-900 line-clamp-1 group-hover:text-leaf-600 transition-colors">{{ food.name }}</h3>
            <span class="text-leaf-600 font-bold text-sm whitespace-nowrap ml-2">Rp {{ food.price.toLocaleString() }}</span>
          </div>
          
          <p class="text-sm text-nature-600 line-clamp-2 mb-4 flex-1">{{ food.description }}</p>
          
          <div class="space-y-3">
            <!-- Mood Tags -->
            <div v-if="food.mood_tags?.length" class="flex flex-wrap gap-1.5">
              <span v-for="mood in food.mood_tags.slice(0, 3)" :key="mood" class="px-2 py-0.5 bg-purple-50 text-purple-600 rounded-md text-xs font-medium border border-purple-100">
                ✨ {{ mood }}
              </span>
            </div>
            
            <!-- Taste Profile -->
            <div v-if="food.taste_profile?.length" class="flex flex-wrap gap-1.5">
              <span v-for="taste in food.taste_profile.slice(0, 3)" :key="taste" class="px-2 py-0.5 bg-orange-50 text-orange-600 rounded-md text-xs font-medium border border-orange-100">
                👅 {{ taste }}
              </span>
            </div>
          </div>
        </div>
      </NuxtLink>
    </div>
  </div>
</template>
