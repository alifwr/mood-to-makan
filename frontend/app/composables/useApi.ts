import { useAuthStore } from '~/stores/auth'

export const useApi = <T>(url: string, options: any = {}) => {
    const config = useRuntimeConfig()
    const authStore = useAuthStore()

    const defaults = {
        baseURL: config.public.apiBase, // Now points to /api/v1 which is proxied
        key: url,
        headers: {
            Authorization: authStore.token ? `Bearer ${authStore.token}` : undefined
        },
        ...options
    }

    return useFetch<T>(url, defaults)
}
