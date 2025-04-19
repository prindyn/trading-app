<script setup>
import Tag from '@/volt/Tag.vue'
const props = defineProps({ trade: Object })
</script>
<template>
  <div
    class="rounded-border border-surface border border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800">
    <div class="p-6 border-b border-surface">
      <h3 class="text-xl font-semibold mb-2">Trade Summary</h3>
      <div class="grid grid-cols-2 gap-4 text-surface-900 dark:text-surface-0">
        <div><strong>Trade ID:</strong> {{ trade.tradeId }}</div>
        <div><strong>Order ID:</strong> {{ trade.orderId }}</div>
        <div><strong>Exchange:</strong> {{ trade.exchange }}</div>
        <div><strong>Market:</strong> {{ trade.market }}</div>
        <div><strong>Strategy:</strong> {{ trade.strategy }}</div>
        <div><strong>Status:</strong>
          <Tag :severity="trade.status === 'Open' ? 'success' : trade.status === 'Closed' ? 'info' : 'warn'">{{
            trade.status }}</Tag>
        </div>
      </div>
    </div>
    <div class="p-6">
      <h3 class="text-xl font-semibold mb-2">Execution</h3>
      <div class="grid grid-cols-2 gap-4 text-surface-900 dark:text-surface-0">
        <div><strong>Amount:</strong> {{ trade.amount }}</div>
        <div><strong>Price:</strong> ${{ trade.price }}</div>
        <div><strong>Total:</strong> ${{ (trade.price * trade.amount).toFixed(2) }}</div>
        <div><strong>Fee:</strong> {{ trade.fee }}</div>
        <div><strong>Slippage:</strong> {{ trade.slippage }}</div>
      </div>
    </div>
  </div>
</template>