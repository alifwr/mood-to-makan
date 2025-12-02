<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: ['auth']
})

const form = ref({
  name: '',
  description: '',
  location: '',
  google_maps_url: ''
})

const isLoading = ref(false)
const router = useRouter()

const submitGem = async () => {
  isLoading.value = true
  try {
    const { error } = await useApi('/gamification/hidden-gems', {
      method: 'POST',
      body: form.value
    })

    if (error.value) throw new Error(error.value.message)

    alert('Hidden Gem submitted! Waiting for approval.')
    router.push('/client')
  } catch (e) {
    alert('Failed to submit: ' + e)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto py-12">
    <div class="text-center mb-10">
      <div class="inline-block p-3 bg-leaf-100 text-leaf-600 rounded-full text-2xl mb-4">💎</div>
      <h1 class="text-4xl font-serif font-bold text-nature-900 mb-4">Found a Hidden Gem?</h1>
      <p class="text-nature-600">Share your discovery with the community and earn badges!</p>
    </div>

    <div class="bg-white p-8 rounded-3xl shadow-lg border border-nature-100 relative overflow-hidden">
      <OrganicShape color="sand" size="lg" class="-top-20 -right-20 opacity-20" />
      
      <form @submit.prevent="submitGem" class="space-y-6 relative z-10">
        <div>
          <label class="block text-sm font-medium text-nature-700 mb-1">Place Name</label>
          <input v-model="form.name" type="text" required class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="e.g. Warung Mbah Joyo" />
        </div>

        <div>
          <label class="block text-sm font-medium text-nature-700 mb-1">Why is it special?</label>
          <textarea v-model="form.description" rows="4" required class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="Describe the food, atmosphere, or story..."></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-nature-700 mb-1">Location / Address</label>
          <input v-model="form.location" type="text" required class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="Street address or area" />
        </div>

        <div>
          <label class="block text-sm font-medium text-nature-700 mb-1">Google Maps Link (Optional)</label>
          <input v-model="form.google_maps_url" type="url" class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="https://maps.google.com/..." />
        </div>

        <div class="pt-4">
          <button type="submit" :disabled="isLoading" class="w-full py-4 bg-nature-800 text-white rounded-xl font-bold hover:bg-nature-700 shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50">
            {{ isLoading ? 'Submitting...' : 'Submit Discovery' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
