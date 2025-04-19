<script setup>
import { ref } from 'vue'
import Tag from '@/volt/Tag.vue'
import { useTradePairs } from '@/composables/use-trade-pairs'
import PaginatedTable from '@/components/common/PaginatedTable.vue'

const selectedPair = ref(null)
const columns = [
    { field: 'image', header: 'Logo', slot: 'logo' },
    { field: 'pair_symbol', header: 'Pair Symbol', slot: 'pair-symbol' },
    { field: 'base_symbol', header: 'Base Symbol' },
    { field: 'quote_symbol', header: 'Quote Symbol' },
    { field: 'type', header: 'Type', slot: 'type' }
]

const props = defineProps({
    pairs: Array,
    loading: Boolean,
    first: Number,
    rows: Number,
    totalRecords: Number,
})
const emit = defineEmits(['page'])
</script>

<template>
    <PaginatedTable :data="pairs" :columns="columns" :totalRecords="totalRecords" :loading="loading" :first="first"
        :rows="rows" :selection="selectedPair" @update:selection="selectedPair = $event" @page="emit('page', $event)">
        <template #logo="{ data }">
            <img :src="data.image" alt="logo" class="w-6 h-6 rounded-full" />
        </template>
        <template #pair-symbol="{ data }">
            <span>{{ data.base_symbol }}/{{ data.quote_symbol }}</span>
        </template>
        <template #type="{ data }">
            <Tag :severity="data.is_fiat ? 'warning' : 'info'">
                {{ data.type ? 'Spot' : 'Futures' }}
            </Tag>
        </template>
    </PaginatedTable>
</template>
