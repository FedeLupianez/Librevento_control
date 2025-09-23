import { writable } from 'svelte/store';
import type User from '../../types/user';
import { API_HOST } from '$lib/routes';

export const user = writable<User | null>(null);

export async function fetchUser() {
   const response = await fetch(`${API_HOST}/usuario/actual`, {
      method: 'GET',
      credentials: 'include'
   });

   console.log("Login status : ", response.ok);
   if (response.ok) {
      const data = await response.json();
      user.set(data);
      console.log("Usuario logueado : ", data);
   } else {
      console.warn('Error al cargar el usuario');
      return null;
   }
}

export async function logoutUser() {
   const response = await fetch(`${API_HOST}/usuario/logout`, {
      method: 'GET',
      credentials: 'include'
   });

   if (response.ok) {
      const data = await response.json();
      console.log(data);
      user.set(null);
      localStorage.removeItem('librevento_user'); // Limpiar localStorage
   } else {
      console.warn('Error al cerrar sesión ');
   }
}
