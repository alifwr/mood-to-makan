<template>
  <div class="min-h-screen bg-nature-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-nature-800 text-nature-50 flex-shrink-0 hidden md:flex flex-col">
      <div class="p-6">
        <NuxtLink to="/" class="text-2xl font-serif font-bold tracking-tighter">Mood2Makan</NuxtLink>
        <div class="text-xs text-nature-400 mt-1 uppercase tracking-widest">Partner Portal</div>
      </div>

      <nav class="flex-1 px-4 space-y-2">
        <NuxtLink to="/umkm" class="flex items-center px-4 py-3 rounded-xl hover:bg-nature-700 transition-colors" active-class="bg-nature-700 text-white">
          <span class="mr-3">📊</span> Dashboard
        </NuxtLink>
        <NuxtLink to="/umkm/stores" class="flex items-center px-4 py-3 rounded-xl hover:bg-nature-700 transition-colors" active-class="bg-nature-700 text-white">
          <span class="mr-3">🏪</span> My Stores
        </NuxtLink>
        <NuxtLink to="/umkm/products" class="flex items-center px-4 py-3 rounded-xl hover:bg-nature-700 transition-colors" active-class="bg-nature-700 text-white">
          <span class="mr-3">📦</span> Products
        </NuxtLink>
        <NuxtLink to="/umkm/reviews" class="flex items-center px-4 py-3 rounded-xl hover:bg-nature-700 transition-colors" active-class="bg-nature-700 text-white">
          <span class="mr-3">⭐</span> Reviews
        </NuxtLink>
      </nav>

      <div class="p-4 border-t border-nature-700">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 rounded-full bg-leaf-500 flex items-center justify-center text-lg font-bold">
            {{ userInitials }}
          </div>
          <div class="ml-3">
            <div class="text-sm font-medium">{{ authStore.user?.full_name }}</div>
            <div class="text-xs text-nature-400">Partner</div>
          </div>
        </div>
        <button @click="authStore.logout()" class="w-full py-2 px-4 bg-nature-900 rounded-lg text-sm hover:bg-black transition-colors">
          Sign Out
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto">
      <div class="p-8">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

const userInitials = computed(() => {
  const name = authStore.user?.full_name || ''
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})
</script>
