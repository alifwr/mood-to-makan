// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    apiProxyTarget: 'http://localhost:8000/api/v1',
    public: {
      apiBase: '/api'
    }
  },
  routeRules: {
    
  }
})