import { ref } from 'vue'
import { useFetchData } from '@/composables/use-data'

export function usePaginated(endpoint: string) {
  const data = ref([])
  const totalRecords = ref(0)
  const searchQuery = ref('')
  const first = ref(0)
  const rows = ref(10)

  const {
    data: fetched,
    fetchData,
    loading
  } = useFetchData<{ data: any[]; total: number }>()

  const run = async (params: Record<string, any> = {}) => {
    await fetchData(endpoint, {
      offset: first.value,
      limit: rows.value,
      search: searchQuery.value,
      ...params
    })

    if (fetched.value) {
      data.value = fetched.value.data || []
      totalRecords.value = fetched.value.total || 0
    }
  }

  const handlePage = (e: { first: number; rows: number }) => {
    run({ offset: e.first, limit: e.rows })
  }

  const handleSearch = (e: { query: string }) => {
    run({ searchQuery: e.query })
  }

  return {
    data,
    totalRecords,
    searchQuery,
    first,
    rows,
    loading,
    handlePage,
    handleSearch,
    fetchData: run
  }
}
