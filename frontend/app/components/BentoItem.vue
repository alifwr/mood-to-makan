<template>
  <div 
    class="relative overflow-hidden rounded-2xl p-6 transition-all duration-300 hover:shadow-lg group"
    :class="[
      spanClass,
      bgClass,
      textColorClass
    ]"
  >
    <!-- Background Pattern/Image -->
    <div v-if="image" class="absolute inset-0 z-0">
      <img :src="image" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" alt="" />
      <div class="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors"></div>
    </div>

    <!-- Content -->
    <div class="relative z-10 h-full flex flex-col justify-between">
      <div>
        <div v-if="icon" class="mb-4 text-2xl">{{ icon }}</div>
        <h3 class="text-xl font-serif font-medium mb-2">{{ title }}</h3>
        <p class="text-sm opacity-90 line-clamp-3">{{ description }}</p>
      </div>
      
      <div v-if="action" class="mt-4">
        <span class="inline-flex items-center text-sm font-medium hover:underline cursor-pointer">
          {{ action }}
          <svg class="w-4 h-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  title: String,
  description: String,
  icon: String,
  image: String,
  action: String,
  span: {
    type: String,
    default: '1x1' // 1x1, 1x2, 2x1, 2x2
  },
  theme: {
    type: String,
    default: 'light' // light, dark, colored
  }
})

const spanClass = computed(() => {
  const spans = {
    '1x1': 'col-span-1 row-span-1',
    '1x2': 'col-span-1 row-span-2',
    '2x1': 'col-span-1 md:col-span-2 row-span-1',
    '2x2': 'col-span-1 md:col-span-2 row-span-2',
    '3x1': 'col-span-1 md:col-span-3 row-span-1',
  }
  return spans[props.span as keyof typeof spans] || spans['1x1']
})

const bgClass = computed(() => {
  if (props.image) return 'bg-nature-800 text-white'
  
  const themes = {
    light: 'bg-white/60 backdrop-blur-sm border border-white/20',
    dark: 'bg-nature-800 text-white',
    colored: 'bg-leaf-400/20 border border-leaf-400/30'
  }
  return themes[props.theme as keyof typeof themes] || themes.light
})

const textColorClass = computed(() => {
  if (props.image || props.theme === 'dark') return 'text-nature-50'
  return 'text-nature-900'
})
</script>
