<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  layout: false
})

const form = ref({
  email: '',
  password: '',
  full_name: '',
  role: 'umkm'
})

const authStore = useAuthStore()
const router = useRouter()
const isLoading = ref(false)
const errorMsg = ref('')

const handleRegister = async () => {
  isLoading.value = true
  errorMsg.value = ''
  
  try {
    const { data, error } = await useApi<any>('/users/', {
      method: 'POST',
      body: form.value
    })

    if (error.value) {
      throw new Error(error.value.data?.detail || 'Registration failed')
    }

    if (data.value) {
      router.push('/auth/login/umkm')
    }
  } catch (e: any) {
    errorMsg.value = e.message
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <NuxtLayout name="auth">
    <template #header>
      <div class="inline-block px-3 py-1 bg-leaf-100 text-leaf-700 rounded-full text-xs font-bold mb-4 tracking-wide uppercase">
        KHUSUS JURAGAN
      </div>
      <h1 class="text-3xl font-serif font-bold text-nature-900 mb-2">Daftar Jadi Mitra</h1>
      <p class="text-nature-600">Mulai kembangin bisnis kulinermu sekarang.</p>
    </template>

    <template #quote>
      Bagikan passion kulinermu ke dunia.
    </template>

    <div>
      <div v-if="errorMsg" class="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label for="name" class="block text-sm font-medium text-nature-700 mb-1">Nama Bisnis/Pemilik</label>
          <input 
            id="name" 
            v-model="form.full_name" 
            type="text" 
            required
            class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:border-leaf-500 focus:ring-2 focus:ring-leaf-200 outline-none transition-all bg-white/50"
            placeholder="Nama Bisnis Kamu"
          />
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-nature-700 mb-1">Email Bisnis</label>
          <input 
            id="email" 
            v-model="form.email" 
            type="email" 
            required
            class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:border-leaf-500 focus:ring-2 focus:ring-leaf-200 outline-none transition-all bg-white/50"
            placeholder="bos@bisnis.com"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-nature-700 mb-1">Kata Sandi</label>
          <input 
            id="password" 
            v-model="form.password" 
            type="password" 
            required
            class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:border-leaf-500 focus:ring-2 focus:ring-leaf-200 outline-none transition-all bg-white/50"
            placeholder="••••••••"
          />
        </div>

        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full py-3 px-4 bg-leaf-600 text-white rounded-xl font-medium hover:bg-leaf-500 focus:outline-none focus:ring-2 focus:ring-leaf-500 focus:ring-offset-2 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isLoading ? 'Lagi Daftar...' : 'Daftarin Bisnis' }}
        </button>
      </form>

      <div class="mt-8 text-center text-sm text-nature-600">
        Udah jadi mitra? 
        <NuxtLink to="/auth/login/umkm" class="text-leaf-600 hover:text-leaf-700 font-medium">Masuk Sini</NuxtLink>
      </div>
    </div>
  </NuxtLayout>
</template>
