// composables/use-active-exchange.ts
import { ref, watch } from 'vue'

const STORAGE_KEY = 'exchange_id'
const activeExchange = ref<any>(null)
const listeners = new Set<(exchange: any) => void>()

export function useActiveExchange() {
  const setSelectedExchange = (exchange: any) => {
    activeExchange.value = exchange
    if (process.client && exchange?.id) {
      localStorage.setItem(STORAGE_KEY, exchange.id)
    }
  }

  const restoreSelectedExchange = (exchanges: any[]) => {
    if (!process.client) return

    const storedId = localStorage.getItem(STORAGE_KEY)
    const fallback = exchanges[0]

    activeExchange.value =
      exchanges.find((e) => e.id === storedId) || fallback || null
  }

  const onExchangeChange = (handler: (exchange: any) => void) => {
    listeners.add(handler)
  }

  return {
    activeExchange,
    setSelectedExchange,
    restoreSelectedExchange,
    onExchangeChange,
  }
}

watch(activeExchange, (newVal) => {
  listeners.forEach((fn) => fn(newVal))
})
