<script setup lang="ts">
definePageMeta({
  layout: 'umkm',
  middleware: ['auth']
})

const route = useRoute()
const router = useRouter()
const storeId = route.params.id

// Fetch Store Details
const { data: store, refresh: refreshStore } = await useApi<any>(`/stores/${storeId}`)

// Fetch Foods
const { data: foods, refresh: refreshFoods } = await useApi<any[]>(`/foods?store_id=${storeId}`)

const isAddingFood = ref(false)
const newFood = ref({
  name: '',
  description: '',
  price: 0,
  category: 'main_course',
  is_available: true
})

const addFood = async () => {
  try {
    await $api('/foods/', {
      method: 'POST',
      body: {
        ...newFood.value,
        store_id: parseInt(storeId as string)
      }
    })

    await refreshFoods()
    isAddingFood.value = false
    newFood.value = { name: '', description: '', price: 0, category: 'main_course', is_available: true }
  } catch (e: any) {
    alert('Gagal nambah menu: ' + (e.data?.detail || e.message))
  }
}

const deleteFood = async (id: number) => {
  if (!confirm('Yakin nih?')) return
  try {
    await $api(`/foods/${id}`, { method: 'DELETE' })
    await refreshFoods()
  } catch (e) {
    alert('Gagal hapus menu')
  }
}

const deleteStore = async () => {
  if (!confirm('Apakah anda yakin ingin menghapus toko ini? Semua data menu dan ulasan akan hilang.')) return
  
  try {
    await $api(`/stores/${storeId}`, { method: 'DELETE' })
    router.push('/umkm')
  } catch (e: any) {
    alert('Gagal menghapus toko: ' + (e.data?.detail || e.message))
  }
}

// --- Edit Store Logic ---
const isEditingStore = ref(false)
const editStoreForm = ref({
  name: '',
  description: '',
  address: '',
  province: '',
  city: '',
  latitude: 0,
  longitude: 0
})

const openEditStore = () => {
  if (!store.value) return
  editStoreForm.value = {
    name: store.value.name,
    description: store.value.description,
    address: store.value.address,
    province: store.value.province,
    city: store.value.city,
    latitude: store.value.latitude,
    longitude: store.value.longitude
  }
  isEditingStore.value = true
}

const updateStore = async () => {
  try {
    await $api(`/stores/${storeId}`, {
      method: 'PUT',
      body: editStoreForm.value
    })

    await refreshStore()
    isEditingStore.value = false
  } catch (e: any) {
    alert('Gagal update toko: ' + (e.data?.detail || e.message))
  }
}

// --- Edit Food Logic ---
const isEditingFood = ref(false)
const editingFoodId = ref<number | null>(null)
const editFoodForm = ref({
  name: '',
  description: '',
  price: 0,
  category: 'main_course',
  is_available: true
})

const openEditFood = (food: any) => {
  editingFoodId.value = food.id
  editFoodForm.value = {
    name: food.name,
    description: food.description,
    price: food.price,
    category: food.category,
    is_available: food.is_available ?? true
  }
  isEditingFood.value = true
}

const updateFood = async () => {
  if (!editingFoodId.value) return
  try {
    await $api(`/foods/${editingFoodId.value}`, {
      method: 'PUT',
      body: {
        ...editFoodForm.value,
        store_id: parseInt(storeId as string)
      }
    })

    await refreshFoods()
    isEditingFood.value = false
    editingFoodId.value = null
  } catch (e: any) {
    alert('Gagal update menu: ' + (e.data?.detail || e.message))
  }
}

// --- Image Upload Logic ---
const fileInput = ref<HTMLInputElement | null>(null)
const isUploadingImage = ref(false)

const triggerImageUpload = () => {
  fileInput.value?.click()
}

const handleImageUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files?.length) return

  const file = target.files[0]
  const formData = new FormData()
  formData.append('file', file)

  isUploadingImage.value = true
  try {
    await $api(`/stores/${storeId}/image`, {
      method: 'PUT',
      body: formData
    })

    await refreshStore()
  } catch (e: any) {
    alert('Gagal upload gambar: ' + (e.data?.detail || e.message))
  } finally {
    isUploadingImage.value = false
    if (fileInput.value) fileInput.value.value = '' // Reset input
  }
}
</script>

<template>
  <div v-if="store">
    <!-- Hidden File Input -->
    <input type="file" ref="fileInput" class="hidden" accept="image/*" @change="handleImageUpload" />

    <!-- Store Header -->
    <div class="bg-white rounded-2xl shadow-sm border border-nature-100 overflow-hidden mb-8">
      <div class="h-48 bg-nature-200 relative">
        <img :src="(store.image_url && store.image_url !== 'string') ? store.image_url : 'https://via.placeholder.com/1200x300?text=Store+Banner'" class="w-full h-full object-cover" />
        <button @click="triggerImageUpload" :disabled="isUploadingImage" class="absolute bottom-4 right-4 bg-white/80 backdrop-blur px-4 py-2 rounded-lg text-sm font-medium hover:bg-white disabled:opacity-50">
          {{ isUploadingImage ? 'Uploading...' : '📷 Ganti Cover' }}
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
          <div class="flex space-x-2">
            <button @click="openEditStore" class="px-4 py-2 border border-nature-200 rounded-lg text-nature-600 hover:bg-nature-50">
              Edit Info
            </button>
            <button @click="deleteStore" class="px-4 py-2 border border-red-200 rounded-lg text-red-600 hover:bg-red-50">
              Hapus Toko
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Store Modal -->
    <div v-if="isEditingStore" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6">
        <h3 class="text-xl font-bold mb-4">Edit Informasi Toko</h3>
        <form @submit.prevent="updateStore" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-1">Nama Toko</label>
            <input v-model="editStoreForm.name" type="text" required class="w-full px-4 py-2 rounded-lg border border-nature-200" />
          </div>
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-1">Deskripsi</label>
            <textarea v-model="editStoreForm.description" rows="3" class="w-full px-4 py-2 rounded-lg border border-nature-200"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-1">Alamat</label>
            <input v-model="editStoreForm.address" type="text" required class="w-full px-4 py-2 rounded-lg border border-nature-200" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-nature-700 mb-1">Provinsi</label>
              <input v-model="editStoreForm.province" type="text" required class="w-full px-4 py-2 rounded-lg border border-nature-200" />
            </div>
            <div>
              <label class="block text-sm font-medium text-nature-700 mb-1">Kota</label>
              <input v-model="editStoreForm.city" type="text" required class="w-full px-4 py-2 rounded-lg border border-nature-200" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-nature-700 mb-1">Latitude</label>
              <input v-model.number="editStoreForm.latitude" type="number" step="any" class="w-full px-4 py-2 rounded-lg border border-nature-200" />
            </div>
            <div>
              <label class="block text-sm font-medium text-nature-700 mb-1">Longitude</label>
              <input v-model.number="editStoreForm.longitude" type="number" step="any" class="w-full px-4 py-2 rounded-lg border border-nature-200" />
            </div>
          </div>
          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="isEditingStore = false" class="px-4 py-2 text-nature-600 hover:bg-nature-50 rounded-lg">Batal</button>
            <button type="submit" class="px-4 py-2 bg-leaf-600 text-white rounded-lg hover:bg-leaf-500">Simpan Perubahan</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Foods Section -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-nature-800">Daftar Menu</h2>
      <button @click="isAddingFood = true" class="px-4 py-2 bg-leaf-600 text-white rounded-lg font-medium hover:bg-leaf-500">
        + Tambah Menu
      </button>
    </div>

    <!-- Add Food Form -->
    <div v-if="isAddingFood" class="bg-white p-6 rounded-2xl shadow-sm border border-nature-100 mb-8 animate-fade-in-up">
      <h3 class="font-bold text-lg mb-4">Menu Baru</h3>
      <form @submit.prevent="addFood" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <input v-model="newFood.name" placeholder="Nama Menu" required class="w-full px-4 py-2 rounded-lg border border-nature-200" />
          <input v-model="newFood.price" type="number" placeholder="Harga" required class="w-full px-4 py-2 rounded-lg border border-nature-200" />
        </div>
        <textarea v-model="newFood.description" placeholder="Deskripsi" class="w-full px-4 py-2 rounded-lg border border-nature-200"></textarea>
        <div class="flex justify-end space-x-3">
          <button type="button" @click="isAddingFood = false" class="px-4 py-2 text-nature-600">Batal</button>
          <button type="submit" class="px-4 py-2 bg-leaf-600 text-white rounded-lg">Simpan Menu</button>
        </div>
      </form>
    </div>

    <!-- Edit Food Modal -->
    <div v-if="isEditingFood" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl w-full max-w-lg p-6">
        <h3 class="text-xl font-bold mb-4">Edit Menu</h3>
        <form @submit.prevent="updateFood" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-nature-700 mb-1">Nama Menu</label>
              <input v-model="editFoodForm.name" type="text" required class="w-full px-4 py-2 rounded-lg border border-nature-200" />
            </div>
            <div>
              <label class="block text-sm font-medium text-nature-700 mb-1">Harga</label>
              <input v-model.number="editFoodForm.price" type="number" required class="w-full px-4 py-2 rounded-lg border border-nature-200" />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-1">Deskripsi</label>
            <textarea v-model="editFoodForm.description" rows="3" class="w-full px-4 py-2 rounded-lg border border-nature-200"></textarea>
          </div>
          <div class="flex justify-end space-x-3 pt-4">
            <button type="button" @click="isEditingFood = false" class="px-4 py-2 text-nature-600 hover:bg-nature-50 rounded-lg">Batal</button>
            <button type="submit" class="px-4 py-2 bg-leaf-600 text-white rounded-lg hover:bg-leaf-500">Simpan Perubahan</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Food List -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="food in foods" :key="food.id" class="bg-white p-4 rounded-xl border border-nature-100 flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <img :src="food.image_url || 'https://via.placeholder.com/100'" class="w-16 h-16 rounded-lg object-cover bg-nature-100" />
          <div>
            <h4 class="font-bold text-nature-900">{{ food.name }}</h4>
            <div class="text-leaf-600 font-medium">Rp {{ food.price.toLocaleString() }}</div>
            <div class="text-xs text-nature-500">{{ food.category }}</div>
          </div>
        </div>
        <div class="flex space-x-2">
          <button @click="openEditFood(food)" class="p-2 text-nature-400 hover:text-leaf-600">✏️</button>
          <button @click="deleteFood(food.id)" class="p-2 text-nature-400 hover:text-red-600">🗑️</button>
        </div>
      </div>
    </div>
  </div>
</template>
