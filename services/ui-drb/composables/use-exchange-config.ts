import { ref } from 'vue'

const config = ref<Record<string, any>>({})

export function useExchangeConfig() {
  const updateConfig = (exchangeId: string, newConfig: Record<string, any>) => {
    config.value[exchangeId] = {
      ...(config.value[exchangeId] || {}),
      ...newConfig,
    }
  }

  const getConfig = (exchangeId: string) => {
    return config.value[exchangeId] || {}
  }

  return {
    updateConfig,
    getConfig,
    config,
  }
}
