<script setup>
import { ref } from 'vue'
import InputText from '@/volt/InputText.vue'
import AssetsTable from '@/components/trades/AssetsTable.vue'
import { useAssets } from '@/composables/use-assets'

const {
    data: assets,
    totalRecords,
    loading,
    searchQuery,
    first,
    rows,
    handlePage,
    handleSearch,
    fetchData: fetchAssets
} = useAssets()
</script>

<template>
    <div
        class="bg-surface-0 dark:bg-surface-900 p-6 rounded-xl border border-surface-200 dark:border-surface-700 flex flex-col gap-4">
        <div class="flex sm:items-center justify-between mb-4 sm:flex-row flex-col gap-2">
            <span class="font-medium text-base">Assets</span>
            <div class="relative">
                <i class="pi pi-search absolute top-1/2 -mt-2 text-surface-400 leading-none start-3 z-1" />
                <InputText v-model="searchQuery" @keyup="handleSearch" placeholder="Search assets..." pt:root="ps-10" />
            </div>
        </div>

        <AssetsTable :assets="assets" :loading="loading" :first="first" :rows="rows" :totalRecords="totalRecords"
            @page="handlePage" />
    </div>
</template>
