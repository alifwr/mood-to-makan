<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  layout: 'umkm',
  middleware: ['auth']
})

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
  name: '',
  description: '',
  address: '',
  province: '',
  city: '',
  latitude: 0,
  longitude: 0
})

const isLoading = ref(false)

const createStore = async () => {
  isLoading.value = true
  try {
    const payload = {
      name: form.value.name,
      description: form.value.description,
      enhanced_description: "",
      province: form.value.province,
      city: form.value.city,
      address: form.value.address,
      latitude: form.value.latitude,
      longitude: form.value.longitude,
      image_url: "",
      suggestion: "",
      suggestion_complete: false,
      umkm_id: authStore.user?.id
    }

    const data = await $api('/stores/', {
      method: 'POST',
      body: payload
    })

    if (data) {
      router.push('/umkm')
    }
  } catch (e: any) {
    alert('Failed to create store: ' + (e.data?.detail || e.message))
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-serif font-bold text-nature-900 mb-8">Buka Toko Baru</h1>

    <div class="bg-white p-8 rounded-2xl shadow-sm border border-nature-100">
      <form @submit.prevent="createStore" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-nature-700 mb-1">Nama Toko</label>
          <input v-model="form.name" type="text" required class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="Contoh: Warung Bu Siti" />
        </div>

        <div>
          <label class="block text-sm font-medium text-nature-700 mb-1">Deskripsi</label>
          <textarea v-model="form.description" rows="4" class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="Ceritain dikit tentang tokomu..."></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-nature-700 mb-1">Alamat</label>
          <input v-model="form.address" type="text" required class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="Alamat lengkap" />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-1">Provinsi</label>
            <input v-model="form.province" type="text" required class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="Jawa Barat" />
          </div>
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-1">Kota</label>
            <input v-model="form.city" type="text" required class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="Bandung" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-1">Latitude</label>
            <input v-model.number="form.latitude" type="number" step="any" class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="-6.9175" />
          </div>
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-1">Longitude</label>
            <input v-model.number="form.longitude" type="number" step="any" class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" placeholder="107.6191" />
          </div>
        </div>

        <div class="pt-4 flex justify-end space-x-4">
          <NuxtLink to="/umkm" class="px-6 py-3 rounded-xl text-nature-600 hover:bg-nature-50 font-medium">Batal</NuxtLink>
          <button type="submit" :disabled="isLoading" class="px-6 py-3 bg-leaf-600 text-white rounded-xl font-medium hover:bg-leaf-500 disabled:opacity-50">
            {{ isLoading ? 'Lagi Bikin...' : 'Bikin Toko' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
