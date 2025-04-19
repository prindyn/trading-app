<template>
  <div>
    <StatsWidget />
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <SalesTrendWidget />
      <RecentActivityWidget />
    </div>
    <ProductOverviewWidget />
  </div>
</template>

<script setup>
import StatsWidget from '@/components/dashboard/StatsWidget.vue';
import SalesTrendWidget from '@/components/dashboard/SalesTrendWidget.vue';
import RecentActivityWidget from '@/components/dashboard/RecentActivityWidget.vue';
import ProductOverviewWidget from '@/components/dashboard/ProductOverviewWidget.vue';
</script>
