<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  layout: 'default',
  middleware: ['auth']
})

const authStore = useAuthStore()
const { data: badges } = await useApi<any[]>('/gamification/my-badges')
const { data: hiddenGems } = await useApi<any[]>('/gamification/hidden-gems')

// Filter my gems
const myGems = computed(() => hiddenGems.value?.filter(g => g.user_id === authStore.user?.id) || [])
</script>

<template>
  <div class="py-12">
    <!-- Profile Header -->
    <div class="bg-white rounded-3xl shadow-sm border border-nature-100 p-8 mb-8 flex flex-col md:flex-row items-center md:items-start gap-8">
      <div class="relative">
        <img :src="authStore.user?.image_url || 'https://via.placeholder.com/150'" class="w-32 h-32 rounded-full object-cover border-4 border-white shadow-lg" />
        <button class="absolute bottom-0 right-0 bg-nature-800 text-white p-2 rounded-full hover:bg-nature-700 shadow-md">
          📷
        </button>
      </div>
      <div class="flex-1 text-center md:text-left">
        <h1 class="text-3xl font-serif font-bold text-nature-900 mb-2">{{ authStore.user?.full_name }}</h1>
        <p class="text-nature-600 mb-4">{{ authStore.user?.email }}</p>
        <div class="flex flex-wrap justify-center md:justify-start gap-2">
          <span class="px-3 py-1 bg-leaf-100 text-leaf-700 rounded-full text-sm font-medium">Food Explorer</span>
          <span class="px-3 py-1 bg-sand-100 text-sand-700 rounded-full text-sm font-medium">Level 1</span>
        </div>
      </div>
      <div class="flex flex-col gap-3">
        <NuxtLink to="/client/hidden-gems/new" class="px-6 py-3 bg-nature-800 text-white rounded-xl font-medium hover:bg-nature-700 shadow-lg transition-transform hover:-translate-y-0.5">
          💎 Submit Hidden Gem
        </NuxtLink>
        <button @click="authStore.logout()" class="px-6 py-3 border border-nature-200 text-nature-600 rounded-xl font-medium hover:bg-nature-50">
          Sign Out
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <!-- Badges Section -->
      <div class="md:col-span-2">
        <h2 class="text-2xl font-serif font-bold text-nature-900 mb-6">Earned Badges</h2>
        <div v-if="!badges || badges.length === 0" class="bg-white p-8 rounded-2xl border border-nature-100 text-center text-nature-500">
          <div class="text-4xl mb-2">🏆</div>
          <p>No badges yet. Start exploring and reviewing to earn them!</p>
        </div>
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <div v-for="badge in badges" :key="badge.id" class="bg-white p-4 rounded-xl border border-nature-100 flex flex-col items-center text-center">
            <img :src="badge.icon_url" class="w-16 h-16 mb-2" />
            <h3 class="font-bold text-nature-800">{{ badge.name }}</h3>
            <p class="text-xs text-nature-500">{{ badge.description }}</p>
          </div>
        </div>

        <h2 class="text-2xl font-serif font-bold text-nature-900 mb-6 mt-12">My Hidden Gem Submissions</h2>
        <div class="space-y-4">
          <div v-for="gem in myGems" :key="gem.id" class="bg-white p-4 rounded-xl border border-nature-100 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-nature-900">{{ gem.name }}</h3>
              <p class="text-sm text-nature-600">{{ gem.location }}</p>
            </div>
            <span 
              class="px-3 py-1 rounded-full text-xs font-bold uppercase"
              :class="{
                'bg-yellow-100 text-yellow-700': gem.status === 'pending',
                'bg-green-100 text-green-700': gem.status === 'approved',
                'bg-red-100 text-red-700': gem.status === 'rejected'
              }"
            >
              {{ gem.status }}
            </span>
          </div>
        </div>
      </div>

      <!-- Preferences / Stats -->
      <div>
        <h2 class="text-2xl font-serif font-bold text-nature-900 mb-6">Taste Profile</h2>
        <div class="bg-white p-6 rounded-2xl border border-nature-100">
          <div class="space-y-4">
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-nature-600">Spicy</span>
                <span class="font-bold text-nature-800">8/10</span>
              </div>
              <div class="h-2 bg-nature-100 rounded-full overflow-hidden">
                <div class="h-full bg-red-400 w-[80%]"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-nature-600">Sweet</span>
                <span class="font-bold text-nature-800">4/10</span>
              </div>
              <div class="h-2 bg-nature-100 rounded-full overflow-hidden">
                <div class="h-full bg-pink-400 w-[40%]"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-nature-600">Salty</span>
                <span class="font-bold text-nature-800">6/10</span>
              </div>
              <div class="h-2 bg-nature-100 rounded-full overflow-hidden">
                <div class="h-full bg-blue-400 w-[60%]"></div>
              </div>
            </div>
          </div>
          <button class="w-full mt-6 py-2 border border-nature-200 rounded-lg text-sm font-medium hover:bg-nature-50">
            Update Preferences
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
