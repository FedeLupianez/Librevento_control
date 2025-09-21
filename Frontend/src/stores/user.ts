import { writable } from 'svelte/store';
import type User from '../types/user';
import { API_HOST, ROUTES } from '$lib/routes';
import { goto } from '$app/navigation';

export const user = writable<User | null>(null);

export async function fetchUser() {
   try {
      const response = await fetch(`${API_HOST}/usuario/actual`, {
         method: 'GET',
         credentials: 'include'
      });

      if (response.ok) {
         const data = await response.json();
         user.set(data);
      } else {
         console.warn('Error al cargar el usuario');
      }
   } catch (error) {
      console.error('Error al cargar el usuario : ', error);
      return null;
   }
}

export async function logoutUser() {
   try {
      const response = await fetch(`${API_HOST}/usuario/logout`, {
         method: 'GET',
         credentials: 'include'
      });

      if (response.ok) {
         const data = await response.json();
         console.log(data);
         user.set(null);
         goto(ROUTES.USER.LOGIN);
      } else {
         console.warn('Error al cerrar sesión : ');
      }
   } catch (error) {
      console.warn('Error al cerrar sesión : ', error);
   }
}
