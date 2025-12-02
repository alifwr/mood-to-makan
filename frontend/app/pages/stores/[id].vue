<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const route = useRoute()
const storeId = route.params.id

const { data: store } = await useApi<any>(`/stores/${storeId}`)
const { data: products } = await useApi<any[]>(`/products/?store_id=${storeId}`)
const { data: reviews, refresh: refreshReviews } = await useApi<any[]>(`/reviews/?store_id=${storeId}`)

const authStore = useAuthStore()
const newReview = ref({
  rating: 5,
  comment: ''
})
const isSubmittingReview = ref(false)

const submitReview = async () => {
  if (!authStore.isAuthenticated) {
    alert('Please login to review')
    return
  }

  isSubmittingReview.value = true
  try {
    const { error } = await useApi('/reviews/', {
      method: 'POST',
      body: {
        ...newReview.value,
        store_id: parseInt(storeId as string)
      }
    })

    if (error.value) throw new Error(error.value.message)

    await refreshReviews()
    newReview.value = { rating: 5, comment: '' }
  } catch (e) {
    alert('Failed to submit review: ' + e)
  } finally {
    isSubmittingReview.value = false
  }
}
</script>

<template>
  <div v-if="store" class="pb-20">
    <!-- Hero Banner -->
    <div class="relative h-[50vh] min-h-[400px] rounded-3xl overflow-hidden mb-12">
      <img :src="store.image_url || 'https://via.placeholder.com/1200x600'" class="w-full h-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-nature-900/80 via-nature-900/20 to-transparent"></div>
      <div class="absolute bottom-0 left-0 right-0 p-8 md:p-12 text-white">
        <div class="max-w-4xl mx-auto">
          <div class="flex items-center gap-4 mb-4">
            <span class="px-3 py-1 bg-leaf-500 rounded-full text-xs font-bold uppercase tracking-wider">{{ store.category }}</span>
            <span class="text-white/80">{{ store.price_range }}</span>
          </div>
          <h1 class="text-5xl md:text-6xl font-serif font-bold mb-4">{{ store.name }}</h1>
          <p class="text-xl text-white/90 max-w-2xl">{{ store.description }}</p>
          <div class="mt-6 flex items-center gap-2 text-white/80">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            {{ store.address }}
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-6">
      <!-- Menu Section -->
      <section class="mb-16">
        <h2 class="text-3xl font-serif font-bold text-nature-900 mb-8 flex items-center gap-3">
          <span class="text-4xl">📜</span> Menu
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="product in products" :key="product.id" class="bg-white p-4 rounded-2xl border border-nature-100 flex gap-4 hover:shadow-md transition-shadow">
            <img :src="product.image_url || 'https://via.placeholder.com/150'" class="w-24 h-24 rounded-xl object-cover bg-nature-100" />
            <div class="flex-1">
              <div class="flex justify-between items-start mb-1">
                <h3 class="font-bold text-lg text-nature-900">{{ product.name }}</h3>
                <span class="font-bold text-leaf-600">Rp {{ product.price.toLocaleString() }}</span>
              </div>
              <p class="text-sm text-nature-600 line-clamp-2">{{ product.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Reviews Section -->
      <section>
        <h2 class="text-3xl font-serif font-bold text-nature-900 mb-8 flex items-center gap-3">
          <span class="text-4xl">💬</span> Reviews
        </h2>

        <!-- Add Review -->
        <div class="bg-nature-50 p-6 rounded-2xl border border-nature-100 mb-8">
          <h3 class="font-bold text-lg mb-4">Write a Review</h3>
          <form @submit.prevent="submitReview" class="space-y-4">
            <div class="flex items-center gap-4">
              <label class="text-sm font-medium">Rating:</label>
              <div class="flex gap-2">
                <button type="button" v-for="i in 5" :key="i" @click="newReview.rating = i" class="text-2xl focus:outline-none transition-transform hover:scale-110">
                  {{ i <= newReview.rating ? '⭐' : '☆' }}
                </button>
              </div>
            </div>
            <textarea v-model="newReview.comment" rows="3" class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none bg-white" placeholder="Share your experience..."></textarea>
            <div class="flex justify-end">
              <button type="submit" :disabled="isSubmittingReview" class="px-6 py-2 bg-nature-800 text-white rounded-lg font-medium hover:bg-nature-700 disabled:opacity-50">
                Post Review
              </button>
            </div>
          </form>
        </div>

        <!-- Review List -->
        <div class="space-y-6">
          <div v-for="review in reviews" :key="review.id" class="bg-white p-6 rounded-2xl border border-nature-100">
            <div class="flex justify-between items-start mb-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-nature-200 flex items-center justify-center font-bold text-nature-600">
                  {{ review.user_id }} <!-- Should fetch user name if possible, or backend should populate -->
                </div>
                <div>
                  <div class="font-bold text-nature-900">User #{{ review.user_id }}</div>
                  <div class="text-xs text-nature-500">Verified Customer</div>
                </div>
              </div>
              <div class="flex text-yellow-400 text-sm">
                <span v-for="i in 5" :key="i">{{ i <= review.rating ? '⭐' : '☆' }}</span>
              </div>
            </div>
            <p class="text-nature-700">{{ review.comment }}</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
