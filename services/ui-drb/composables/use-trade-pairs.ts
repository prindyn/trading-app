import { usePaginated } from '@/composables/use-paginated'
import { useExchanges } from '@/composables/use-exchanges'

const paginated = usePaginated('/trade/pairs')
const { onExchangeChange, activeExchange } = useExchanges()

onExchangeChange(() => {
  paginated.fetchData()
})

export function useTradePairs() {
  return paginated
}