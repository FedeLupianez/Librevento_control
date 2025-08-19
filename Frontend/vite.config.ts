import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
   plugins: [tailwindcss(), sveltekit()],
   kit: {
      csrf: {
         checkOrigin: false
      }
   },
   server: {
      host: true,
      fs: {
         allow: [
            'src', 'node_modules', '.svelte-kit', './public'
         ]
      },
   },
});
