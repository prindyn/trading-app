<script setup>
import DataTable from '@/volt/DataTable.vue'
import InputText from '@/volt/InputText.vue'
import Tag from '@/volt/Tag.vue'
import Button from '@/volt/Button.vue'
import Column from 'primevue/column'
import { onMounted, ref, watch } from 'vue'
import tradesData from '@/data/trades.json'
import { useRouter } from 'vue-router'

const trades = ref([])
const selectedTrade = ref(null)
const searchQuery = ref('')
const loading = ref(false)
const filteredTrades = ref([])
const router = useRouter()

const searchTrades = () => {
  loading.value = true
  filteredTrades.value = trades.value.filter((trade) =>
    [trade.asset, trade.status, trade.type].some((field) =>
      field.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  )
  setTimeout(() => {
    loading.value = false
  }, 300)
}

watch(searchQuery, () => {
  searchTrades()
})

onMounted(() => {
  trades.value = tradesData
  filteredTrades.value = [...trades.value]
})
</script>

<template>
  <div
    class="bg-surface-0 dark:bg-surface-900 p-6 rounded-xl border border-surface-200 dark:border-surface-700 flex flex-col gap-4"
  >
    <div class="flex sm:items-center justify-between mb-4 sm:flex-row flex-col gap-2">
      <span class="font-medium text-base">Trade History</span>
      <div class="relative">
        <i class="pi pi-search absolute top-1/2 -mt-2 text-surface-400 leading-none start-3 z-1" />
        <InputText
          v-model="searchQuery"
          placeholder="Search trades..."
          pt:root="ps-10"
          @keyup.enter="searchTrades"
        />
      </div>
    </div>
    <div class="flex flex-col gap-2">
      <DataTable
        :value="filteredTrades"
        v-model:selection="selectedTrade"
        selectionMode="single"
        :loading="loading"
        :rows="5"
      >
        <Column field="asset" header="Asset" sortable />
        <Column field="type" header="Type" sortable />
        <Column field="amount" header="Amount" sortable>
          <template #body="{ data }"> {{ data.amount }} </template>
        </Column>
        <Column field="status" header="Status">
          <template #body="{ data }">
            <Tag
              :severity="
                data.status === 'Open' ? 'success' :
                data.status === 'Closed' ? 'info' :
                'warn'
              "
            >
              {{ data.status }}
            </Tag>
          </template>
        </Column>
        <Column field="timestamp" header="Time" sortable />
        <Column header="Actions">
          <template #body="{ data }">
            <Button label="View" size="small" @click="router.push(`/trades/${data.id}`)" />
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>