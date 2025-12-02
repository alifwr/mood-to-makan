<template>
  <div class="min-h-screen flex bg-nature-50 relative overflow-hidden">
    <!-- Background Decorations -->
    <OrganicShape color="leaf" size="xl" class="-top-20 -right-20 opacity-20" />
    <OrganicShape color="clay" size="lg" class="bottom-0 left-0 opacity-20 delay-1000" />

    <!-- Left Side: Content/Brand -->
    <div class="hidden lg:flex w-1/2 bg-nature-800 text-nature-50 p-12 flex-col justify-between relative overflow-hidden">
      <div class="absolute inset-0 opacity-10">
        <svg class="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
          <path d="M0 0 C 50 100 80 100 100 0 Z" fill="currentColor"/>
        </svg>
      </div>
      
      <div class="relative z-10">
        <NuxtLink to="/" class="text-3xl font-serif font-bold tracking-tighter">Mood2Makan</NuxtLink>
      </div>

      <div class="relative z-10 max-w-lg">
        <h2 class="text-5xl font-serif font-medium mb-6 leading-tight">
          <slot name="quote">
            Taste the authenticity of local flavors.
          </slot>
        </h2>
        <p class="text-lg opacity-80">
          Join our community of food lovers and discover the best local culinary experiences.
        </p>
      </div>

      <div class="relative z-10 text-sm opacity-60">
        © {{ new Date().getFullYear() }} Mood2Makan
      </div>
    </div>

    <!-- Right Side: Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12 relative z-10">
      <div class="w-full max-w-md bg-white/50 backdrop-blur-xl p-8 rounded-3xl shadow-xl border border-white/40">
        <div class="mb-8 text-center lg:text-left">
          <NuxtLink to="/" class="lg:hidden text-2xl font-serif font-bold text-nature-800 mb-8 block">Mood2Makan</NuxtLink>
          <slot name="header" />
        </div>
        
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Auth Layout
</script>
