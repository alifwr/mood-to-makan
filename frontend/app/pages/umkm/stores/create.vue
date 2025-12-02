<script setup lang="ts">
definePageMeta({
  layout: 'umkm',
  middleware: ['auth']
})

const form = ref({
  name: '',
  description: '',
  address: '',
  category: 'restaurant', // Default
  price_range: '$$'
})

const isLoading = ref(false)
const router = useRouter()

const createStore = async () => {
  isLoading.value = true
  try {
    const { data, error } = await useApi('/stores/', {
      method: 'POST',
      body: form.value
    })

    if (error.value) throw new Error(error.value.message)

    if (data.value) {
      router.push('/umkm')
    }
  } catch (e) {
    alert('Failed to create store: ' + e)
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
            <label class="block text-sm font-medium text-nature-700 mb-1">Kategori</label>
            <select v-model="form.category" class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none">
              <option value="restaurant">Restoran</option>
              <option value="cafe">Kafe</option>
              <option value="street_food">Kaki Lima</option>
              <option value="bakery">Roti & Kue</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-1">Kisaran Harga</label>
            <select v-model="form.price_range" class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none">
              <option value="$">$ (Murah)</option>
              <option value="$$">$$ (Sedang)</option>
              <option value="$$$">$$$ (Mahal)</option>
            </select>
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
