<script setup>
import Tag from '@/volt/Tag.vue'
import Button from '@/volt/Button.vue'
const props = defineProps({ trade: Object })
</script>
<template>
  <div
    class="flex flex-col justify-between rounded-border border-surface border p-6 border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800">
    <h3 class="text-xl font-semibold mb-4">Summary</h3>
    <ul class="list-none space-y-4">
      <li class="flex justify-between">
        <span class="text-surface-700 dark:text-surface-200">Subtotal</span>
        <span class="text-surface-900 dark:text-surface-0 font-medium text-lg">
          ${{ (trade.price * trade.amount).toFixed(2) }}
        </span>
      </li>
      <li class="flex justify-between">
        <span class="text-surface-700 dark:text-surface-200">Fee</span>
        <span class="text-surface-900 dark:text-surface-0 font-medium text-lg">{{ trade.fee }}</span>
      </li>
      <li class="flex justify-between">
        <span class="text-surface-700 dark:text-surface-200">Slippage</span>
        <span class="text-surface-900 dark:text-surface-0 font-medium text-lg">{{ trade.slippage }}</span>
      </li>
      <li class="flex justify-between border-t pt-4 border-surface">
        <span class="text-surface-900 dark:text-surface-0 font-medium">PnL</span>
        <Tag :severity="trade.pnl.startsWith('+') ? 'success' : 'danger'">
          {{ trade.pnl }}
        </Tag>
      </li>
    </ul>
    <div class="mt-8 flex gap-4">
      <Button label="View JSON" severity="secondary" outlined @click="console.log(trade)" />
      <Button label="Print" severity="secondary" outlined @click="window.print()" />
    </div>
  </div>
</template>