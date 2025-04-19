import { ref } from 'vue'
import axios from 'axios'
import { useActiveExchange } from './use-active-exchange'

export function useExchanges() {
  const exchanges = ref<any[]>([])
  const loading = ref(false)
  const error = ref<null | string>(null)

  const {
    activeExchange,
    setSelectedExchange,
    restoreSelectedExchange,
    onExchangeChange
  } = useActiveExchange()

  const fetchExchanges = async () => {
    loading.value = true
    try {
      const res = await axios.get('http://localhost:8000/trade/exchanges')
      exchanges.value = res.data
      restoreSelectedExchange(exchanges.value)
    } catch (err) {
      console.error('Failed to fetch exchanges:', err)
      error.value = 'Failed to fetch exchanges'
    } finally {
      loading.value = false
    }
  }

  return {
    exchanges,
    loading,
    error,
    activeExchange,
    fetchExchanges,
    setSelectedExchange,
    onExchangeChange,
  }
}
