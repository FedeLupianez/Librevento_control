import { writable } from 'svelte/store';
import type User from '../../types/user';
import { API_ROUTES } from '$lib/routes';

export const user = writable<User | null>(null);

export async function initializeUser() {
   const response = await fetch(API_ROUTES.USER.AUTH, {
      method: 'GET',
      credentials: 'include'
   })

   if (response.ok) {
      const data = await response.json();
      const decripted = JSON.parse(atob(data.user));
      console.log("Usuario : ", decripted);
      user.set(decripted);
   } else {
      console.log('No se pudo obtener el usuario');
      user.set(null)
   }
}

export async function logoutUser() {
   const response = await fetch(API_ROUTES.USER.LOGOUT, {
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
