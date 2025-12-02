<template>
  <div 
    class="absolute -z-10 opacity-40 mix-blend-multiply filter blur-3xl animate-float"
    :class="[colorClass, sizeClass, positionClass]"
    :style="{ animationDelay: delay }"
  ></div>
</template>

<script setup lang="ts">
const props = defineProps({
  color: {
    type: String,
    default: 'leaf' // leaf, clay, sand
  },
  size: {
    type: String,
    default: 'md' // sm, md, lg
  },
  delay: {
    type: String,
    default: '0s'
  },
  variant: {
    type: Number,
    default: 1
  }
})

const colorClass = computed(() => {
  const colors = {
    leaf: 'bg-leaf-400',
    clay: 'bg-nature-400',
    sand: 'bg-sand-400',
    stone: 'bg-stone-400'
  }
  return colors[props.color as keyof typeof colors] || colors.leaf
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'w-32 h-32',
    md: 'w-64 h-64',
    lg: 'w-96 h-96',
    xl: 'w-[30rem] h-[30rem]'
  }
  return sizes[props.size as keyof typeof sizes] || sizes.md
})

const positionClass = computed(() => {
  // Randomize border radius slightly based on variant
  return props.variant === 1 ? 'rounded-organic' : 'rounded-organic-2'
})
</script>
