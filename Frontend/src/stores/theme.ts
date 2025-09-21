import { writable } from 'svelte/store';

const dafult_theme = typeof localStorage !== 'undefined' && localStorage.getItem('theme') === 'dark' ? 'dark' : 'light';
export const theme = writable(dafult_theme);

theme.subscribe((value) => {
   if (typeof localStorage !== 'undefined') {
      document.documentElement.classList.remove('light', 'dark');
      document.documentElement.classList.add(value);
      localStorage.setItem('theme', value);
   }
});

