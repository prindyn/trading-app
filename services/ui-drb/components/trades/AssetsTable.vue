<script setup>
import { ref } from 'vue'
import Tag from '@/volt/Tag.vue'
import InputText from '@/volt/InputText.vue'
import PaginatedTable from '@/components/common/PaginatedTable.vue'

const selectedAsset = ref(null)
const columns = [
    { field: 'image', header: 'Logo', slot: 'logo' },
    { field: 'symbol', header: 'Symbol' },
    { field: 'name', header: 'Name' },
    { field: 'is_fiat', header: 'Type', slot: 'type' }
]

const props = defineProps({
    assets: Array,
    loading: Boolean,
    first: Number,
    rows: Number,
    totalRecords: Number,
})
const emit = defineEmits(['page'])
</script>

<template>
    <PaginatedTable :data="assets" :columns="columns" :totalRecords="totalRecords" :loading="loading" :first="first"
        :rows="rows" :selection="selectedAsset" @update:selection="selectedAsset = $event" @page="emit('page', $event)">
        <template #logo="{ data }">
            <img :src="data.image" alt="logo" class="w-6 h-6 rounded-full" />
        </template>
        <template #type="{ data }">
            <Tag :severity="data.is_fiat ? 'warning' : 'info'">
                {{ data.is_fiat ? 'Fiat' : 'Crypto' }}
            </Tag>
        </template>
    </PaginatedTable>
</template>