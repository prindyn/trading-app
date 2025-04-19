<script setup>
definePageMeta({
  layout: 'auth'
})

import { ref } from 'vue'
import { useRouter } from 'vue-router'

const name = ref('')
const email = ref('')
const password = ref('')
const agree = ref(false)

const router = useRouter()

const register = async () => {
  try {
    if (!agree.value) {
      alert('You must accept the terms to proceed.')
      return
    }

    // TODO: implement real registration
    console.log('Registering:', { name: name.value, email: email.value, password: password.value })
    router.push('/dashboard')
  } catch (err) {
    console.error('Registration error:', err)
  }
}
</script>

<template>
  <section class="min-h-screen flex items-center justify-center px-4 py-20 max-w-[100rem] mx-auto">
    <div class="flex w-full flex-col lg:flex-row items-center gap-12">
      <!-- Left Panel -->
      <div class="flex flex-col justify-center w-full lg:max-w-md">
        <!-- Title -->
        <div class="text-center lg:text-left">
          <h2 class="text-2xl font-bold text-surface-900 dark:text-white">Create Account</h2>
          <p class="text-surface-500 dark:text-surface-400 mt-3.5">Register below to get started</p>
        </div>

        <!-- Divider -->
        <div class="flex items-center gap-3.5 my-7">
          <span class="flex-1 h-px bg-surface-200 dark:bg-surface-800" />
        </div>

        <!-- Form -->
        <form @submit.prevent="register" class="flex flex-col gap-4">
          <InputText v-model="name" placeholder="Full Name" class="w-full" />
          <InputText v-model="email" placeholder="Email" class="w-full" />
          <Password v-model="password" placeholder="Password" class="w-full" input-class="w-full" toggle-mask />

          <div class="flex items-center gap-2 text-sm mt-2">
            <Checkbox v-model="agree" input-id="agree" />
            <label for="agree" class="text-surface-600 dark:text-surface-400">
              I agree to the <NuxtLink to="/terms" class="text-primary-500 hover:underline">terms and conditions</NuxtLink>
            </label>
          </div>

          <Button type="submit" label="Create Account" class="w-full mt-4" />
        </form>

        <!-- Footer link -->
        <div class="mt-8 text-sm text-center lg:text-left text-surface-600 dark:text-surface-400">
          Already have an account?
          <NuxtLink to="/auth/login" class="text-primary-500 hover:underline">Sign in</NuxtLink>
        </div>

        <div class="mt-8 text-center text-sm text-surface-400 dark:text-surface-500">
          ©2025 YourCompany
        </div>
      </div>

      <!-- Right Panel -->
      <div class="hidden lg:flex flex-1 items-center justify-center h-full py-20">
        <div class="rounded-3xl overflow-hidden border border-surface shadow-md w-full max-w-[32.5rem] xl:max-w-[60.5rem]">
          <img
            src="/images/landing/auth-image.svg"
            alt="Auth Illustration"
            class="w-full h-full object-contain object-left"
          />
        </div>
      </div>
    </div>
  </section>
</template>
