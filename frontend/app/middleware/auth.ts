import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to, from) => {
    const authStore = useAuthStore()

    if (authStore.token && !authStore.user) {
        await authStore.fetchUser()
    }

    if (!authStore.isAuthenticated) {
        if (to.path.startsWith('/umkm')) {
            return navigateTo('/auth/login/umkm')
        }
        return navigateTo('/auth/login/client')
    }
})
