import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware((to, from) => {
    const authStore = useAuthStore()

    if (!authStore.isAuthenticated) {
        if (to.path.startsWith('/umkm')) {
            return navigateTo('/auth/login/umkm')
        }
        return navigateTo('/auth/login/client')
    }
})
