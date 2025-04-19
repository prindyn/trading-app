<script setup>
import Dialog from '@/volt/Dialog.vue'
import InputText from '@/volt/InputText.vue'
import Button from '@/volt/Button.vue'

const visible = defineModel({ type: Boolean })
const form = ref({ name: '', apiKey: '', secret: '' })

const submit = () => {
    console.log('Form submitted:', form.value)
    visible.value = false
}
</script>

<template>
    <Dialog v-model:visible="visible" modal header="Add Integration" :style="{ width: '32rem' }" class="rounded-xl">
        <div class="flex flex-col gap-4">
            <div>
                <label class="block mb-1 text-sm font-medium text-surface-700 dark:text-surface-200">Name</label>
                <InputText v-model="form.name" class="w-full" />
            </div>

            <div>
                <label class="block mb-1 text-sm font-medium text-surface-700 dark:text-surface-200">API Key</label>
                <InputText v-model="form.apiKey" class="w-full" />
            </div>

            <div>
                <label class="block mb-1 text-sm font-medium text-surface-700 dark:text-surface-200">Secret</label>
                <InputText v-model="form.secret" class="w-full" type="password" />
            </div>

            <div class="flex justify-end mt-4 gap-2">
                <Button label="Cancel" severity="secondary" outlined @click="visible = false" />
                <Button label="Add" @click="submit" />
            </div>
        </div>
    </Dialog>
</template>