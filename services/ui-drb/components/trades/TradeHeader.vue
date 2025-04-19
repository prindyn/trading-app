<script setup>
const props = defineProps({ trade: Object })
</script>
<template>
  <div class="flex flex-col gap-2 mb-8">
    <span class="text-surface-700 dark:text-surface-100 text-xl">Status</span>
    <div class="text-surface-900 dark:text-surface-0 font-bold text-4xl">
      {{ trade.asset }} • {{ trade.type }}
    </div>
    <p class="text-surface-700 dark:text-surface-100 text-xl mt-0 mb-6">Executed on {{ trade.timestamp }}</p>
    <div class="h-[3px] bg-gradient-to-r from-primary from-10% via-transparent to-transparent"></div>
  </div>
</template>