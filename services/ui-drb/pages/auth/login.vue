<script setup>
definePageMeta({
  layout: 'auth'
})

import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const remember = ref(false)

const router = useRouter()

const login = async () => {
  try {
    // TODO: implement real login
    console.log('Logging in with', email.value, password.value, 'Remember:', remember.value)
    router.push('/dashboard')
  } catch (err) {
    console.error('Login error:', err)
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
          <h2 class="text-2xl font-bold text-surface-900 dark:text-white">Login</h2>
          <p class="text-surface-500 dark:text-surface-400 mt-3.5">Please enter your details</p>
        </div>

        <!-- Divider -->
        <div class="flex items-center gap-3.5 my-7">
          <span class="flex-1 h-px bg-surface-200 dark:bg-surface-800" />
        </div>

        <!-- Form -->
        <form @submit.prevent="login" class="flex flex-col gap-4">
          <InputText v-model="email" placeholder="Email" class="w-full" />
          <Password v-model="password" placeholder="Password" class="w-full" input-class="w-full" toggle-mask />

          <div class="flex justify-between items-center text-sm mt-4">
            <div class="flex items-center gap-2">
              <Checkbox v-model="remember" input-id="remember" />
              <label for="remember" class="text-surface-600 dark:text-surface-400">Remember me</label>
            </div>
            <NuxtLink to="/auth/forgot-password" class="text-primary-500 hover:underline">
              Forgot password?
            </NuxtLink>
          </div>

          <Button type="submit" label="Login" class="w-full mt-4" />
        </form>

        <!-- Footer link -->
        <div class="mt-8 text-sm text-center lg:text-left text-surface-600 dark:text-surface-400">
          Not registered?
          <NuxtLink to="/auth/register" class="text-primary-500 hover:underline">Create an Account</NuxtLink>
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
