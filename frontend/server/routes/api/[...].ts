export default defineEventHandler((event) => {
  const config = useRuntimeConfig()
  const target = config.apiProxyTarget
  const path = event.path.replace(/^\/api/, '')
  
  return proxyRequest(event, `${target}${path}`)
})
