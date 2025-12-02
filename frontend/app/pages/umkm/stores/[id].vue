<script setup lang="ts">
definePageMeta({
  layout: 'umkm',
  middleware: ['auth']
})

const route = useRoute()
const storeId = route.params.id

// Fetch Store Details
const { data: store, refresh: refreshStore } = await useApi<any>(`/stores/${storeId}`)

// Fetch Products
const { data: products, refresh: refreshProducts } = await useApi<any[]>(`/products/?store_id=${storeId}`)

const isAddingProduct = ref(false)
const newProduct = ref({
  name: '',
  description: '',
  price: 0,
  category: 'main_course',
  is_available: true
})

const addProduct = async () => {
  try {
    const { error } = await useApi('/products/', {
      method: 'POST',
      body: {
        ...newProduct.value,
        store_id: parseInt(storeId as string)
      }
    })

    if (error.value) throw new Error(error.value.message)

    await refreshProducts()
    isAddingProduct.value = false
    newProduct.value = { name: '', description: '', price: 0, category: 'main_course', is_available: true }
  } catch (e) {
    alert('Gagal nambah menu: ' + e)
  }
}

const deleteProduct = async (id: number) => {
  if (!confirm('Yakin nih?')) return
  try {
    await useApi(`/products/${id}`, { method: 'DELETE' })
    refreshProducts()
  } catch (e) {
    alert('Gagal hapus menu')
  }
}
</script>

<template>
  <div v-if="store">
    <!-- Store Header -->
    <div class="bg-white rounded-2xl shadow-sm border border-nature-100 overflow-hidden mb-8">
      <div class="h-48 bg-nature-200 relative">
        <img :src="store.image_url || 'https://via.placeholder.com/1200x300?text=Store+Banner'" class="w-full h-full object-cover" />
        <button class="absolute bottom-4 right-4 bg-white/80 backdrop-blur px-4 py-2 rounded-lg text-sm font-medium hover:bg-white">
          📷 Ganti Cover
        </button>
      </div>
      <div class="p-6">
        <div class="flex justify-between items-start">
          <div>
            <h1 class="text-3xl font-serif font-bold text-nature-900 mb-2">{{ store.name }}</h1>
            <p class="text-nature-600 mb-4">{{ store.description }}</p>
            <div class="flex items-center space-x-4 text-sm text-nature-500">
              <span>📍 {{ store.address }}</span>
              <span>🏷️ {{ store.category }}</span>
              <span>💰 {{ store.price_range }}</span>
            </div>
          </div>
          <button class="px-4 py-2 border border-nature-200 rounded-lg text-nature-600 hover:bg-nature-50">
            Edit Info
          </button>
        </div>
      </div>
    </div>

    <!-- Products Section -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-nature-800">Daftar Menu</h2>
      <button @click="isAddingProduct = true" class="px-4 py-2 bg-leaf-600 text-white rounded-lg font-medium hover:bg-leaf-500">
        + Tambah Menu
      </button>
    </div>

    <!-- Add Product Form -->
    <div v-if="isAddingProduct" class="bg-white p-6 rounded-2xl shadow-sm border border-nature-100 mb-8 animate-fade-in-up">
      <h3 class="font-bold text-lg mb-4">Menu Baru</h3>
      <form @submit.prevent="addProduct" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <input v-model="newProduct.name" placeholder="Nama Menu" required class="w-full px-4 py-2 rounded-lg border border-nature-200" />
          <input v-model="newProduct.price" type="number" placeholder="Harga" required class="w-full px-4 py-2 rounded-lg border border-nature-200" />
        </div>
        <textarea v-model="newProduct.description" placeholder="Deskripsi" class="w-full px-4 py-2 rounded-lg border border-nature-200"></textarea>
        <div class="flex justify-end space-x-3">
          <button type="button" @click="isAddingProduct = false" class="px-4 py-2 text-nature-600">Batal</button>
          <button type="submit" class="px-4 py-2 bg-leaf-600 text-white rounded-lg">Simpan Menu</button>
        </div>
      </form>
    </div>

    <!-- Product List -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="product in products" :key="product.id" class="bg-white p-4 rounded-xl border border-nature-100 flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <img :src="product.image_url || 'https://via.placeholder.com/100'" class="w-16 h-16 rounded-lg object-cover bg-nature-100" />
          <div>
            <h4 class="font-bold text-nature-900">{{ product.name }}</h4>
            <div class="text-leaf-600 font-medium">Rp {{ product.price.toLocaleString() }}</div>
            <div class="text-xs text-nature-500">{{ product.category }}</div>
          </div>
        </div>
        <div class="flex space-x-2">
          <button class="p-2 text-nature-400 hover:text-leaf-600">✏️</button>
          <button @click="deleteProduct(product.id)" class="p-2 text-nature-400 hover:text-red-600">🗑️</button>
        </div>
      </div>
    </div>
  </div>
</template>
