<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  layout: false
})

const form = ref({
  username: '',
  password: ''
})

const authStore = useAuthStore()
const router = useRouter()
const isLoading = ref(false)
const errorMsg = ref('')

const handleLogin = async () => {
  isLoading.value = true
  errorMsg.value = ''

  try {
    const formData = new FormData()
    formData.append('username', form.value.username)
    formData.append('password', form.value.password)

    const data = await $api<any>('/auth/login', {
      method: 'POST',
      body: formData
    })

    if (data) {
      authStore.setToken(data.access_token)
      await authStore.fetchUser()

      // Check if user is actually UMKM
      if (authStore.user?.role !== 'umkm' && authStore.user?.role !== 'admin') {
        throw new Error('Access denied. Not a partner account.')
      }

      router.push('/umkm')
    }
  } catch (e: any) {
    errorMsg.value = e.data?.detail || e.message || 'Login failed'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <NuxtLayout name="auth">
    <template #header>
      <div
        class="inline-block px-3 py-1 bg-leaf-100 text-leaf-700 rounded-full text-xs font-bold mb-4 tracking-wide uppercase">
        KHUSUS JURAGAN
      </div>
      <h1 class="text-3xl font-serif font-bold text-nature-900 mb-2">Makin Laris Manis</h1>
      <p class="text-nature-600">Masuk dashboard buat atur tokomu.</p>
    </template>

    <template #quote>
      Ketemu pelanggan yang nyari rasa otentik.
    </template>

    <div>
      <div v-if="errorMsg" class="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-nature-700 mb-1">Email Bisnis</label>
          <input id="email" v-model="form.username" type="email" required
            class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:border-leaf-500 focus:ring-2 focus:ring-leaf-200 outline-none transition-all bg-white/50"
            placeholder="bos@bisnis.com" />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-nature-700 mb-1">Kata Sandi</label>
          <input id="password" v-model="form.password" type="password" required
            class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:border-leaf-500 focus:ring-2 focus:ring-leaf-200 outline-none transition-all bg-white/50"
            placeholder="••••••••" />
        </div>

        <div class="flex items-center justify-between text-sm">
          <label class="flex items-center text-nature-600 cursor-pointer">
            <input type="checkbox" class="rounded border-nature-300 text-leaf-600 focus:ring-leaf-500 mr-2" />
            Ingetin Gue
          </label>
          <a href="#" class="text-leaf-600 hover:text-leaf-700 font-medium">Lupa Sandi?</a>
        </div>

        <button type="submit" :disabled="isLoading"
          class="w-full py-3 px-4 bg-leaf-600 text-white rounded-xl font-medium hover:bg-leaf-500 focus:outline-none focus:ring-2 focus:ring-leaf-500 focus:ring-offset-2 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed">
          {{ isLoading ? 'Lagi Masuk...' : 'Masuk Juragan' }}
        </button>
      </form>

      <div class="mt-8 text-center text-sm text-nature-600">
        Baru di Mood2Makan?
        <NuxtLink to="/auth/register/umkm" class="text-leaf-600 hover:text-leaf-700 font-medium">Daftarin Bisnis Kamu
        </NuxtLink>
      </div>
    </div>
  </NuxtLayout>
</template>
