import { writable } from 'svelte/store';
import type User from '../../types/user';
import { API_HOST } from '$lib/routes';

export const user = writable<User | null>(null);

export async function initializeUser() {
   const response = await fetch(`${API_HOST}/usuario/auth`, {
      method: 'GET',
      credentials: 'include'
   })

   if (response.ok) {
      const data = await response.json();
      const decripted = JSON.parse(atob(data.usuario));
      console.log("Usuario : ", decripted);
      user.set(decripted);
   } else {
      user.set(null)
   }
}

export async function logoutUser() {
   const response = await fetch(`${API_HOST}/usuario/logout`, {
      method: 'GET',
      credentials: 'include'
   });

   if (response.ok) {
      user.set(null);
      console.log('Logout successful');
   } else {
      console.warn('Error al cerrar sesión');
   }
}

export function getUser() {
   return user;
}
