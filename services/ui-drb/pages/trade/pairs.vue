<script setup>
import { ref } from 'vue'
import InputText from '@/volt/InputText.vue'
import TradePairsTable from '@/components/trades/TradePairsTable.vue'
import { useTradePairs } from '@/composables/use-trade-pairs'

const {
    data: pairs,
    totalRecords,
    loading,
    searchQuery,
    first,
    rows,
    handlePage,
    handleSearch,
    fetchData: fetchPairs
} = useTradePairs()
</script>
<template>
    <div
        class="bg-surface-0 dark:bg-surface-900 p-6 rounded-xl border border-surface-200 dark:border-surface-700 flex flex-col gap-4">
        <div class="flex sm:items-center justify-between mb-4 sm:flex-row flex-col gap-2">
            <span class="font-medium text-base">Trade Pairs</span>
            <div class="relative">
                <i class="pi pi-search absolute top-1/2 -mt-2 text-surface-400 leading-none start-3 z-1" />
                <InputText v-model="searchQuery" @keyup="handleSearch" placeholder="Search pairs..." pt:root="ps-10" />
            </div>
        </div>
        <TradePairsTable :pairs="pairs" :loading="loading" :first="first" :rows="rows" :totalRecords="totalRecords"
            @page="handlePage" />
    </div>
</template>
