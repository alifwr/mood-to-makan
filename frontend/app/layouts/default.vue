<template>
  <div class="min-h-screen relative overflow-hidden bg-nature-50 text-nature-900 font-sans selection:bg-leaf-400 selection:text-white">
    <!-- Background Decorations -->
    <OrganicShape color="leaf" size="xl" class="-top-20 -left-20 opacity-30" />
    <OrganicShape color="clay" size="lg" class="top-40 right-0 opacity-20 delay-1000" />
    <OrganicShape color="sand" size="xl" class="bottom-0 left-1/3 opacity-20 delay-2000" />

    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 px-6 py-4 transition-all duration-300" :class="{ 'bg-white/80 backdrop-blur-md shadow-sm': isScrolled }">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <NuxtLink to="/" class="text-2xl font-serif font-bold tracking-tighter text-nature-800">
          Mood2Makan
        </NuxtLink>
        
        <div class="hidden md:flex items-center space-x-8">
          <NuxtLink to="/" class="text-sm font-medium hover:text-leaf-600 transition-colors">Beranda</NuxtLink>
          <NuxtLink to="/about" class="text-sm font-medium hover:text-leaf-600 transition-colors">Tentang Kita</NuxtLink>
          <NuxtLink to="/explore" class="text-sm font-medium hover:text-leaf-600 transition-colors">Cekidot</NuxtLink>
        </div>

        <div class="flex items-center space-x-4">
          <NuxtLink to="/auth/login/client" class="text-sm font-medium px-4 py-2 rounded-full hover:bg-nature-100 transition-colors">
            Masuk Sini
          </NuxtLink>
          <NuxtLink to="/auth/login/umkm" class="text-sm font-medium px-4 py-2 bg-nature-800 text-nature-50 rounded-full hover:bg-nature-700 transition-colors shadow-lg hover:shadow-xl">
            Login Juragan
          </NuxtLink>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="pt-24 pb-12 px-6 min-h-[calc(100vh-80px)]">
      <div class="max-w-7xl mx-auto">
        <slot />
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-nature-100 py-12 px-6 mt-12">
      <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        <div class="col-span-1 md:col-span-2">
          <h3 class="text-2xl font-serif font-bold mb-4 text-nature-800">Mood2Makan</h3>
          <p class="text-nature-600 max-w-sm">
            Temukan spot makan tersembunyi dan rasa otentik. Hubungkan pecinta kuliner dengan juragan lokal.
          </p>
        </div>
        <div>
          <h4 class="font-bold mb-4 text-nature-800">Platform</h4>
          <ul class="space-y-2 text-sm text-nature-600">
            <li><NuxtLink to="/explore" class="hover:text-leaf-600">Cekidot</NuxtLink></li>
            <li><NuxtLink to="/about" class="hover:text-leaf-600">Tentang Kita</NuxtLink></li>
            <li><NuxtLink to="/auth/login/umkm" class="hover:text-leaf-600">Buat Juragan</NuxtLink></li>
          </ul>
        </div>
        <div>
          <h4 class="font-bold mb-4 text-nature-800">Legal</h4>
          <ul class="space-y-2 text-sm text-nature-600">
            <li><a href="#" class="hover:text-leaf-600">Kebijakan Privasi</a></li>
            <li><a href="#" class="hover:text-leaf-600">Syarat & Ketentuan</a></li>
          </ul>
        </div>
      </div>
      <div class="max-w-7xl mx-auto mt-12 pt-8 border-t border-nature-200 text-center text-sm text-nature-500">
        © {{ new Date().getFullYear() }} Mood2Makan. All rights reserved.
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const isScrolled = ref(false)

onMounted(() => {
  window.addEventListener('scroll', () => {
    isScrolled.value = window.scrollY > 20
  })
})
</script>
