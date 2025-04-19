import { ref } from 'vue'
import axios from 'axios'
import { useExchanges } from '@/composables/use-exchanges'
const { activeExchange } = useExchanges()

export function useFetchData<T = any>() {
  const data = ref<T | null>(null)
  const error = ref<string | null>(null)
  const loading = ref(false)

  const fetchData = async (url: string, params: Record<string, any> = {}) => {
    try {
      if (activeExchange.value) {
        params.exchange_id = activeExchange.value.id
      }
      loading.value = true
      const response = await axios.get<T>(`http://localhost:8000${url}`, { params })
      data.value = response.data
    } catch (err: any) {
      console.error('Fetch error:', err)
      error.value = err?.message || 'Failed to fetch'
    } finally {
      loading.value = false
    }
  }

  return {
    data,
    error,
    loading,
    fetchData,
  }
}
