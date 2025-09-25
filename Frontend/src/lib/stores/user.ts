import { writable } from 'svelte/store';
import Cookies from 'js-cookie';
import type User from '../../types/user';
import { API_HOST } from '$lib/routes';
import { browser } from '$app/environment';

export const user = writable<User | null>(null);

export function initializeUser() {
   if (!browser) return; // Ensure this only runs on the client

   const userCookie = Cookies.get('librevento_user');
   if (!userCookie) {
      user.set(null);
      return;
   }
   try {
      const decodedJson = atob(userCookie);
      const userData = JSON.parse(decodedJson);
      user.set(userData);
   } catch (error) {
      console.error('Failed to parse user cookie:', error);
      user.set(null);
      Cookies.remove('librevento_user');
   }
}

export async function fetchUser() {
   if (!browser) return;
   const data = Cookies.get('librevento_user');
   console.log(data);
   if (!data) return;
   user.set(JSON.parse(atob(data)));
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

