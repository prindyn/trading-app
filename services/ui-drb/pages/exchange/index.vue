// File: pages/exchanges/MyExchangesPage.vue
<script setup>
import { ref, onMounted, watch } from 'vue'
import exchangesData from '@/data/exchanges.json'
import Tag from '@/volt/Tag.vue'
import Button from '@/volt/Button.vue'
import InputText from '@/volt/InputText.vue'
import DataTable from '@/volt/DataTable.vue'
import Column from 'primevue/column'
import AddIntegrationDialog from '@/components/dialogs/AddIntegrationDialog.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const exchanges = ref([])
const activeExchange = ref(null)
const searchQuery = ref('')
const loading = ref(false)
const filteredExchanges = ref([])
const showAddDialog = ref(false)

const searchExchanges = () => {
    loading.value = true
    filteredExchanges.value = exchanges.value.filter((ex) =>
        [ex.name, ex.mode, ex.label].some((field) =>
            field?.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
    )
    setTimeout(() => {
        loading.value = false
    }, 300)
}

watch(searchQuery, () => {
    searchExchanges()
})

onMounted(() => {
    exchanges.value = exchangesData
    filteredExchanges.value = [...exchanges.value]
})
</script>

<template>
    <div
        class="bg-surface-0 dark:bg-surface-900 p-6 rounded-xl border border-surface-200 dark:border-surface-700 flex flex-col gap-4">
        <div class="flex flex-wrap justify-between items-center mb-4 gap-2">
            <div class="flex gap-2">
                <Button label="Add New" icon="pi pi-plus" severity="primary" @click="showAddDialog = true" />
            </div>
            <div class="relative">
                <i class="pi pi-search absolute top-1/2 -mt-2 text-surface-400 leading-none start-3 z-1" />
                <InputText v-model="searchQuery" placeholder="Search exchanges..." pt:root="ps-10"
                    @keyup.enter="searchExchanges" />
            </div>
        </div>

        <div class="flex flex-col gap-2">
            <DataTable :value="filteredExchanges" v-model:selection="activeExchange" selectionMode="single"
                :loading="loading" :rows="5">
                <Column field="name" header="Exchange" sortable />
                <Column field="mode" header="Mode">
                    <template #body="{ data }">
                        <Tag :severity="data.mode === 'live' ? 'success' : 'info'">{{ data.mode }}</Tag>
                    </template>
                </Column>
                <Column field="label" header="Label" />
                <Column header="Actions">
                    <template #body="{ data }">
                        <div class="flex gap-2">
                            <Button label="Edit" size="small" @click="router.push(`/exchanges/edit/${data.id}`)" />
                            <Button label="Disconnect" size="small" severity="danger" outlined />
                        </div>
                    </template>
                </Column>
            </DataTable>
        </div>

        <AddIntegrationDialog v-model:visible="showAddDialog" />
    </div>
</template>