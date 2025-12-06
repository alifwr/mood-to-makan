import { defineStore } from 'pinia'

interface User {
    id: number
    email: string
    full_name: string
    role: string
    image_url?: string
    preferences?: Record<string, any>
}

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as User | null,
        token: useCookie('auth_token').value || null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
        isUmkm: (state) => state.user?.role === 'umkm',
        isAdmin: (state) => state.user?.role === 'admin',
    },
    actions: {
        setToken(token: string) {
            this.token = token
            // Persist token (e.g., in cookie or local storage - for now simple state)
            // In a real app, use useCookie() for persistence
            const cookie = useCookie('auth_token')
            cookie.value = token
        },
        setUser(user: User) {
            this.user = user
        },
        logout() {
            this.user = null
            this.token = null
            const cookie = useCookie('auth_token')
            cookie.value = null
            navigateTo('/auth/login/client')
        },
        async fetchUser() {
            if (!this.token) return

            try {
                const data = await $api<User>('/users/me')
                if (data) {
                    this.setUser(data)
                }
            } catch (e) {
                this.logout()
            }
        }
    }
})
