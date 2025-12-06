<script setup lang="ts">
definePageMeta({
  layout: 'umkm',
  middleware: ['auth']
})

const { data: reviews, pending: reviewsPending } = await useApi<any[]>('/reviews/umkm/me')
const { data: stores } = await useApi<any[]>('/stores/')

// Map store IDs to names
const storeMap = computed(() => {
  const map: Record<number, string> = {}
  if (stores.value) {
    stores.value.forEach(s => {
      map[s.id] = s.name
    })
  }
  return map
})

// Calculate stats
const totalReviews = computed(() => reviews.value?.length || 0)
const averageRating = computed(() => {
  if (!reviews.value || reviews.value.length === 0) return 0
  const sum = reviews.value.reduce((acc, r) => acc + r.rating, 0)
  return (sum / reviews.value.length).toFixed(1)
})

// Helper to format date
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('id-ID', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<template>
  <div>
    <h1 class="text-3xl font-serif font-bold text-nature-900 mb-8">Ulasan Pelanggan</h1>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-nature-100">
        <div class="text-nature-500 text-sm mb-1">Total Ulasan</div>
        <div class="text-3xl font-bold text-nature-800">{{ totalReviews }}</div>
      </div>
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-nature-100">
        <div class="text-nature-500 text-sm mb-1">Rata-rata Rating</div>
        <div class="text-3xl font-bold text-nature-800 flex items-center gap-2">
          {{ averageRating }} <span class="text-yellow-400 text-2xl">★</span>
        </div>
      </div>
    </div>

    <!-- Reviews List -->
    <div class="bg-white rounded-2xl shadow-sm border border-nature-100 p-6">
      <h2 class="text-xl font-bold text-nature-800 mb-6">Daftar Ulasan</h2>

      <div v-if="reviewsPending" class="text-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-nature-600 mx-auto"></div>
      </div>

      <div v-else-if="totalReviews === 0" class="text-center py-12 text-nature-500">
        Belum ada ulasan yang masuk.
      </div>

      <div v-else class="space-y-6">
        <div v-for="review in reviews" :key="review.id" class="border-b border-nature-100 pb-6 last:border-0 last:pb-0">
          <div class="flex justify-between items-start mb-2">
            <div class="flex items-center gap-2">
              <div class="flex text-yellow-400">
                <span v-for="i in 5" :key="i">
                  {{ i <= Math.round(review.rating) ? '★' : '☆' }}
                </span>
              </div>
              <span class="font-bold text-nature-800">{{ review.rating }}</span>
            </div>
            <span class="text-sm text-nature-400">{{ formatDate(review.created_at) }}</span>
          </div>
          
          <p class="text-nature-700 mb-3">{{ review.comment }}</p>
          
          <div class="flex gap-2 text-xs">
             <span v-if="review.store_id && storeMap[review.store_id]" class="bg-nature-100 text-nature-600 px-2 py-1 rounded">
               Toko: {{ storeMap[review.store_id] }}
             </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
