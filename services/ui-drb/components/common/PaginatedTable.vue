<script setup>
import { computed } from 'vue'
import DataTable from '@/volt/DataTable.vue'
import Column from 'primevue/column'

const props = defineProps({
    data: Array,
    columns: Array,
    totalRecords: Number,
    loading: Boolean,
    first: Number,
    rows: Number,
    selection: Object
})

const emit = defineEmits(['update:selection', 'page'])
</script>

<template>
    <DataTable :value="data" :selection="selection" @update:selection="emit('update:selection', $event)"
        selectionMode="single" :loading="loading" :lazy="true" paginator :rows="rows" :first="first"
        :totalRecords="totalRecords" :rowsPerPageOptions="[5, 10, 20]" responsiveLayout="scroll"
        @page="emit('page', $event)">
        <Column v-for="col in columns" :key="col.field" :field="col.field" :header="col.header"
            :sortable="col.sortable ?? false">
            <template v-if="$slots[col.slot]" #body="slotProps">
                <slot :name="col.slot" v-bind="slotProps" />
            </template>
        </Column>
    </DataTable>
</template>
