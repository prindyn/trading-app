import { usePaginated } from '@/composables/use-paginated'
import { useExchanges } from '@/composables/use-exchanges'

const paginated = usePaginated('/trade/assets')
const { onExchangeChange, activeExchange } = useExchanges()

onExchangeChange(() => {
  paginated.fetchData()
})

export function useAssets() {
  return paginated
}