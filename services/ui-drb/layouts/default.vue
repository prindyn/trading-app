<template>
    <div class="bg-surface-50 dark:bg-surface-950 min-h-screen p-8 flex flex-col gap-6">
      <AppTopbar />
      <div class="flex flex-col w-full max-w-7xl mx-auto gap-6 flex-1">
        <slot />
      </div>
      <AppFooter />
    </div>
  </template>
  
  <script setup>
  import AppFooter from "@/components/AppFooter.vue";
  import AppTopbar from "@/components/AppTopbar.vue";
  </script>
  