export default defineEventHandler(async (event) => {
    const config = useRuntimeConfig()
    const body = await readBody(event)

    console.log(body);

    // Backend expects FormData (application/x-www-form-urlencoded)
    const formData = new URLSearchParams()
    formData.append('username', body.username)
    formData.append('password', body.password)

    try {
        const response = await $fetch(`${config.apiProxyTarget}/auth/login`, {
            method: 'POST',
            body: formData,
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        return response
    } catch (error: any) {
        throw createError({
            statusCode: error.response?.status || 500,
            statusMessage: error.response?.statusText || 'Internal Server Error',
            data: error.data
        })
    }
})
