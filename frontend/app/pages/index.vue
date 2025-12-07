<template>
  <div>
    <!-- Hero Section -->
    <section class="relative min-h-[80vh] flex items-center justify-center overflow-hidden">
      <OrganicShape color="leaf" size="xl" class="top-20 -left-20 opacity-30" />
      <OrganicShape color="clay" size="xl" class="bottom-20 -right-20 opacity-30 delay-1000" />
      
      <div class="text-center z-10 max-w-4xl mx-auto px-6">
        <h1 class="text-6xl md:text-8xl font-serif font-bold mb-6 text-nature-900 leading-tight animate-fade-in-up">
          Mood Kamu, <br />
          <span class="text-leaf-600 italic">Rekomendasi Kami</span>
        </h1>
        <p class="text-xl md:text-2xl text-nature-600 mb-10 max-w-2xl mx-auto animate-fade-in-up delay-200">
          Platform penghubung UMKM kuliner dengan seleramu. Cari makan pake bahasa sehari-hari, AI kami yang carikan.
        </p>
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in-up delay-300">
          <NuxtLink to="/explore" class="px-8 py-4 bg-nature-800 text-nature-50 rounded-full font-medium hover:bg-nature-700 transition-all hover:scale-105 shadow-lg">
            Cari Makan Sekarang
          </NuxtLink>
          <NuxtLink to="/auth/login/umkm" class="px-8 py-4 bg-white text-nature-800 border border-nature-200 rounded-full font-medium hover:bg-nature-50 transition-all hover:scale-105 shadow-sm">
            Gabung Jadi UMKM
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- Featured Categories (Bento Grid) -->
    <section class="py-20 px-6 bg-white/50 backdrop-blur-sm">
      <div class="max-w-7xl mx-auto">
        <div class="mb-12 text-center">
          <h2 class="text-4xl font-serif font-bold mb-4 text-nature-800">Pilihan Mantap</h2>
          <p class="text-nature-600">Cari spot-spot keren di berbagai kategori.</p>
        </div>

        <BentoGrid>
          <NuxtLink 
            v-for="item in bentoItems" 
            :key="item.id" 
            :to="`/foods/${item.id}`"
            :class="{
              'col-span-1 row-span-1': item.span === '1x1',
              'col-span-1 row-span-2': item.span === '1x2',
              'col-span-1 md:col-span-2 row-span-1': item.span === '2x1',
              'col-span-1 md:col-span-2 row-span-2': item.span === '2x2',
              'col-span-1 md:col-span-3 row-span-1': item.span === '3x1',
            }"
          >
            <BentoItem 
              :title="item.title" 
              :description="item.description"
              :span="item.span"
              :theme="item.theme"
              :image="item.image"
              :action="item.action"
              :icon="item.icon"
              class="h-full w-full"
            />
          </NuxtLink>
        </BentoGrid>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="py-24 px-6 relative overflow-hidden">
      <div class="absolute inset-0 bg-nature-800 skew-y-3 transform origin-bottom-right scale-110"></div>
      <div class="relative z-10 max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-12 text-nature-50">
        <div class="md:w-1/2">
          <h2 class="text-4xl md:text-5xl font-serif font-bold mb-6">Lapar tapi bingung mau makan apa?</h2>
          <p class="text-lg opacity-90 mb-8">
            Ceritain aja mood kamu ke AI kami, dan temukan UMKM kuliner terbaik di sekitarmu yang pas banget sama seleramu.
          </p>
          <NuxtLink to="/auth/register/client" class="inline-block px-8 py-4 bg-leaf-500 text-white rounded-full font-medium hover:bg-leaf-600 transition-colors shadow-lg">
            Daftar Sebagai Client
          </NuxtLink>
        </div>
        <div class="md:w-1/2 flex justify-center">
           <OrganicShape color="sand" size="lg" :variant="2" class="opacity-80" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const authStore = useAuthStore()

const { data: recommendations } = await useAsyncData('home-recommendations', async () => {
  try {
    if (authStore.isAuthenticated) {
      const res = await $api<any>('/ai/personalized-recommendations?limit=5')
      return res.recommendations || []
    } else {
      // Fallback to generic foods for guests
      const res = await $api<any[]>('/foods/?limit=5')
      return res || []
    }
  } catch (e) {
    console.error('Failed to fetch recommendations', e)
    return []
  }
})

const getIconForCategory = (category: string) => {
  const icons: Record<string, string> = {
    'main_meals': '🍛',
    'desserts': '🍰',
    'drinks': '🥤',
    'snacks': '🍟'
  }
  return icons[category] || '🍽️'
}

const bentoItems = computed(() => {
  const items = recommendations.value || []
  const spans = ['2x2', '1x1', '1x2', '1x1', '2x1']
  const themes = ['colored', 'light', 'dark', 'light', 'colored']
  
  return items.map((item: any, index: number) => ({
    id: item.id,
    title: item.name,
    description: item.description,
    image: item.image_url,
    span: spans[index % spans.length],
    theme: themes[index % themes.length],
    action: 'Lihat Detail',
    icon: getIconForCategory(item.category)
  }))
})
</script>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

.delay-200 {
  animation-delay: 0.2s;
}

.delay-300 {
  animation-delay: 0.3s;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
