<script setup lang="ts">
definePageMeta({
  layout: 'umkm',
  middleware: ['auth']
})

const route = useRoute()
const router = useRouter()
const foodId = route.params.id

const { data: food, refresh: refreshFood } = await useApi<any>(`/foods/${foodId}`)
const { addToast } = useToast()

const form = ref({
  name: '',
  description: '',
  enhanced_description: '',
  price: 0,
  category: 'main_meals',
  is_available: true,
  main_ingredients: [] as string[],
  taste_profile: [] as string[],
  texture: [] as string[],
  mood_tags: [] as string[]
})

// Initialize form when data is loaded
watchEffect(() => {
  if (food.value) {
    form.value = {
      name: food.value.name,
      description: food.value.description,
      enhanced_description: food.value.enhanced_description || '',
      price: food.value.price,
      category: food.value.category,
      is_available: food.value.is_available ?? true,
      main_ingredients: food.value.main_ingredients || [],
      taste_profile: food.value.taste_profile || [],
      texture: food.value.texture || [],
      mood_tags: food.value.mood_tags || []
    }
  }
})

const isSaving = ref(false)

const saveFood = async () => {
  isSaving.value = true
  try {
    await $api(`/foods/${foodId}`, {
      method: 'PUT',
      body: {
        ...form.value,
        store_id: food.value.store_id // Ensure store_id is passed back
      }
    })
    addToast('Menu berhasil diperbarui', 'success')
    router.back()
  } catch (e: any) {
    addToast('Gagal update menu: ' + (e.data?.detail || e.message), 'error')
  } finally {
    isSaving.value = false
  }
}

// Helper for array inputs (comma separated)
const updateArrayField = (field: 'main_ingredients' | 'taste_profile' | 'texture' | 'mood_tags', value: string) => {
  form.value[field] = value.split(',').map(s => s.trim()).filter(s => s)
}

const getArrayString = (field: 'main_ingredients' | 'taste_profile' | 'texture' | 'mood_tags') => {
  return form.value[field]?.join(', ') || ''
}

// Image Upload
const fileInput = ref<HTMLInputElement | null>(null)
const isUploading = ref(false)

const triggerUpload = () => fileInput.value?.click()

const handleImageUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files?.length) return

  const file = target.files[0]
  const formData = new FormData()
  formData.append('file', file)

  isUploading.value = true
  try {
    await $api(`/foods/${foodId}/image`, {
      method: 'PUT',
      body: formData
    })
    await refreshFood()
    addToast('Foto menu berhasil diupdate', 'success')
  } catch (e: any) {
    addToast('Gagal upload foto: ' + (e.data?.detail || e.message), 'error')
  } finally {
    isUploading.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}

// AI Generation
const isGenerating = ref(false)
const generateAiInfo = async () => {
  isGenerating.value = true
  try {
    await $api(`/ai/generate-food-description/${foodId}`, {
      method: 'POST'
    })
    await refreshFood()
    addToast('Informasi menu berhasil digenerate AI', 'success')
  } catch (e: any) {
    addToast('Gagal generate AI: ' + (e.data?.detail || e.message), 'error')
  } finally {
    isGenerating.value = false
  }
}

const isEnhancing = ref(false)
const enhanceDescription = async () => {
  isEnhancing.value = true
  try {
    await $api(`/ai/generate-enhanced-food-description/${foodId}`, {
      method: 'POST'
    })
    await refreshFood()
    addToast('Deskripsi berhasil di-enhance AI', 'success')
  } catch (e: any) {
    addToast('Gagal enhance deskripsi: ' + (e.data?.detail || e.message), 'error')
  } finally {
    isEnhancing.value = false
  }
}
</script>

<template>
  <div v-if="food" class="max-w-3xl mx-auto">
    <div class="flex items-center gap-4 mb-8">
      <button @click="router.back()" class="p-2 hover:bg-nature-100 rounded-full transition-colors">
        <svg class="w-6 h-6 text-nature-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
      </button>
      <h1 class="text-2xl font-serif font-bold text-nature-900">Edit Menu</h1>
    </div>

    <div class="bg-white rounded-2xl shadow-sm border border-nature-100 overflow-hidden">
      <!-- Image Section -->
      <div class="relative h-64 bg-nature-100 group">
        <img :src="food.image_url || 'https://via.placeholder.com/800x400'" class="w-full h-full object-cover" />
        <div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <button @click="triggerUpload" :disabled="isUploading" class="bg-white/90 backdrop-blur px-6 py-3 rounded-full font-medium hover:bg-white transition-all transform hover:scale-105">
            {{ isUploading ? 'Uploading...' : '📷 Ganti Foto' }}
          </button>
        </div>
        <input type="file" ref="fileInput" class="hidden" accept="image/*" @change="handleImageUpload" />
      </div>

      <form @submit.prevent="saveFood" class="p-8 space-y-6">
        <!-- Basic Info -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-2">Nama Menu</label>
            <input v-model="form.name" type="text" required class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none transition-all" />
          </div>
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-2">Harga (Rp)</label>
            <input v-model.number="form.price" type="number" required class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none transition-all" />
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-2">
            <label class="block text-sm font-medium text-nature-700">Deskripsi</label>
            <button type="button" @click="generateAiInfo" :disabled="isGenerating" class="text-xs font-medium text-purple-600 bg-purple-50 hover:bg-purple-100 px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5">
              <span v-if="isGenerating" class="animate-spin">✨</span>
              <span v-else>✨</span>
              {{ isGenerating ? 'Generating...' : 'Generate with AI' }}
            </button>
          </div>
          <textarea v-model="form.description" rows="4" class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none transition-all"></textarea>
        </div>

        <div>
          <div class="flex justify-between items-center mb-2">
            <label class="block text-sm font-medium text-nature-700">Enhanced Description (AI)</label>
            <button type="button" @click="enhanceDescription" :disabled="isEnhancing" class="text-xs font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5">
              <span v-if="isEnhancing" class="animate-spin">✨</span>
              <span v-else>✨</span>
              {{ isEnhancing ? 'Enhancing...' : 'Enhance Description' }}
            </button>
          </div>
          <textarea v-model="form.enhanced_description" rows="4" class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none transition-all" placeholder="Deskripsi yang lebih menarik hasil generate AI..."></textarea>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-nature-700 mb-2">Kategori</label>
            <select v-model="form.category" class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none bg-white">
              <option value="main_meals">Makanan Berat</option>
              <option value="snacks">Cemilan</option>
              <option value="desserts">Penutup</option>
              <option value="drinks">Minuman</option>
            </select>
          </div>
          <div class="flex items-center pt-8">
            <label class="flex items-center gap-3 cursor-pointer">
              <input v-model="form.is_available" type="checkbox" class="w-5 h-5 text-leaf-600 rounded focus:ring-leaf-500 border-gray-300" />
              <span class="text-nature-700 font-medium">Tersedia untuk dipesan</span>
            </label>
          </div>
        </div>

        <!-- Advanced Details -->
        <div class="border-t border-nature-100 pt-6">
          <h3 class="font-bold text-lg mb-4 text-nature-800">Detail Rasa & Karakter</h3>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-nature-700 mb-2">Bahan Utama (pisahkan dengan koma)</label>
              <input 
                :value="getArrayString('main_ingredients')"
                @input="e => updateArrayField('main_ingredients', (e.target as HTMLInputElement).value)"
                placeholder="Contoh: Ayam, Bawang, Kecap"
                class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" 
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-nature-700 mb-2">Profil Rasa (pisahkan dengan koma)</label>
              <input 
                :value="getArrayString('taste_profile')"
                @input="e => updateArrayField('taste_profile', (e.target as HTMLInputElement).value)"
                placeholder="Contoh: Gurih, Pedas, Manis"
                class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" 
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-nature-700 mb-2">Tekstur (pisahkan dengan koma)</label>
              <input 
                :value="getArrayString('texture')"
                @input="e => updateArrayField('texture', (e.target as HTMLInputElement).value)"
                placeholder="Contoh: Lembut, Renyah"
                class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" 
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-nature-700 mb-2">Mood Tags (pisahkan dengan koma)</label>
              <input 
                :value="getArrayString('mood_tags')"
                @input="e => updateArrayField('mood_tags', (e.target as HTMLInputElement).value)"
                placeholder="Contoh: Happy, Comfort, Energetic"
                class="w-full px-4 py-3 rounded-xl border border-nature-200 focus:ring-2 focus:ring-leaf-500 outline-none" 
              />
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-4 pt-6 border-t border-nature-100">
          <button type="button" @click="router.back()" class="px-6 py-3 text-nature-600 font-medium hover:bg-nature-50 rounded-xl transition-colors">
            Batal
          </button>
          <button type="submit" :disabled="isSaving" class="px-8 py-3 bg-leaf-600 text-white font-bold rounded-xl hover:bg-leaf-500 transition-all shadow-lg hover:shadow-xl disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-2">
            <span v-if="isSaving" class="animate-spin">⏳</span>
            {{ isSaving ? 'Menyimpan...' : 'Simpan Perubahan' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
