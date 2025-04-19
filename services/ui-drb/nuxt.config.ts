// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
    compatibilityDate: "2024-11-01",
    devtools: { enabled: true },
    css: [
        "~/assets/css/main.css",
        "primeicons/primeicons.css",
    ],
    vite: {
        plugins: [tailwindcss()],
    },
    components: [
        { path: '~/volt', pathPrefix: false }
    ]
});
