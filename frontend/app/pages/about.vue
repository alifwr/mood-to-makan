<script setup lang="ts">
definePageMeta({
  layout: 'default'
})
</script>

<template>
  <div class="py-12">
    <!-- Hero Section -->
    <section class="text-center max-w-4xl mx-auto mb-20 px-6">
      <h1 class="text-4xl md:text-6xl font-serif font-bold text-nature-900 mb-6">
        Tentang <span class="text-leaf-600">Mood2Makan</span>
      </h1>
      <p class="text-xl text-nature-600 leading-relaxed">
        Kami percaya makanan bukan cuma soal kenyang, tapi soal <span class="font-bold text-nature-800">perasaan</span>. 
        Mood2Makan hadir buat ngejodohin mood kamu sama kuliner UMKM terbaik di sekitarmu.
      </p>
    </section>

    <!-- Mission Section -->
    <section class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-24">
      <div class="relative h-96 rounded-3xl overflow-hidden shadow-xl group">
        <img src="https://images.unsplash.com/photo-1556910103-1c02745a30bf?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="UMKM Cooking" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
        <div class="absolute inset-0 bg-gradient-to-t from-nature-900/60 to-transparent"></div>
        <div class="absolute bottom-8 left-8 text-white">
          <h3 class="text-2xl font-serif font-bold mb-2">Dukung UMKM Lokal</h3>
          <p class="opacity-90">Bantu usaha kecil tumbuh dan dikenal lebih luas.</p>
        </div>
      </div>
      <div class="space-y-6">
        <h2 class="text-3xl font-serif font-bold text-nature-800">Misi Kami</h2>
        <p class="text-nature-600 text-lg">
          Mood2Makan bukan sekadar direktori makanan. Kami adalah jembatan digital yang menghubungkan:
        </p>
        <ul class="space-y-4">
          <li class="flex items-start gap-4">
            <div class="bg-leaf-100 p-3 rounded-full text-leaf-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
            <div>
              <h4 class="font-bold text-nature-800">Pencari Kuliner (Client)</h4>
              <p class="text-nature-600">Yang bingung mau makan apa dan butuh rekomendasi yang ngerti mood mereka.</p>
            </div>
          </li>
          <li class="flex items-start gap-4">
            <div class="bg-clay-100 p-3 rounded-full text-clay-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
            </div>
            <div>
              <h4 class="font-bold text-nature-800">Penjual Makanan (UMKM)</h4>
              <p class="text-nature-600">Para pahlawan rasa yang punya masakan enak tapi butuh lebih banyak pelanggan.</p>
            </div>
          </li>
        </ul>
      </div>
    </section>

    <!-- AI Section -->
    <section class="bg-nature-800 rounded-3xl p-12 text-center text-nature-50 relative overflow-hidden mb-24">
      <OrganicShape color="leaf" size="xl" class="top-0 left-0 opacity-10" />
      <OrganicShape color="sand" size="xl" class="bottom-0 right-0 opacity-10" />
      
      <div class="relative z-10 max-w-3xl mx-auto">
        <h2 class="text-3xl md:text-4xl font-serif font-bold mb-6">Kenapa Pakai AI?</h2>
        <p class="text-lg opacity-90 mb-8">
          Karena rasa itu personal. Algoritma kami gak cuma cari kata kunci, tapi berusaha ngerti konteks dan perasaan kamu. 
          Mau "makan yang bikin melek" atau "tempat nugas yang tenang", AI kami siap bantu.
        </p>
        <NuxtLink to="/explore" class="inline-block px-8 py-4 bg-white text-nature-900 rounded-full font-bold hover:bg-nature-100 transition-colors shadow-lg">
          Cobain AI Sekarang
        </NuxtLink>
      </div>
    </section>

    <!-- Team/Contact (Optional placeholder) -->
    <section class="text-center">
      <h2 class="text-2xl font-serif font-bold text-nature-800 mb-4">Punya Pertanyaan?</h2>
      <p class="text-nature-600 mb-6">Kami siap bantu kamu atau UMKM kamu buat berkembang.</p>
      <a href="mailto:halo@mood2makan.com" class="text-leaf-600 font-bold hover:underline">Hubungi Kami →</a>
    </section>
  </div>
</template>
