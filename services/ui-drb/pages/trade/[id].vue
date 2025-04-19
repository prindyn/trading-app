<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import trades from '@/data/trades.json'
import TradeHeader from '@/components/trades/TradeHeader.vue'
import TradeDetailsCard from '@/components/trades/TradeDetailsCard.vue'
import TradeSummaryCard from '@/components/trades/TradeSummaryCard.vue'
import SecondaryButton from '@/volt/SecondaryButton.vue'

const route = useRoute()
const router = useRouter()
const trade = ref(null)

onMounted(() => {
  const id = route.params.id
  trade.value = trades.find((t) => t.id === id)
})
</script>

<template>
  <div
    class="bg-surface-0 dark:bg-surface-900 p-6 rounded-xl border border-surface-200 dark:border-surface-700 flex flex-col gap-4">
    <div class="card max-w-screen-2xl py-0">
      <div class="mb-6">
        <SecondaryButton label="← Back to Trades" @click="router.back()" />
      </div>
      <template v-if="trade">
        <TradeHeader :trade="trade" />
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 space-y-6">
            <TradeDetailsCard :trade="trade" />
          </div>
          <TradeSummaryCard :trade="trade" />
        </div>
      </template>
      <template v-else>
        <div class="text-center text-surface-500 mt-8">Trade not found.</div>
      </template>
    </div>
  </div>
</template>