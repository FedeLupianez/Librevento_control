import { writable } from 'svelte/store';
import Cookies from 'js-cookie';
import type User from '../../types/user';
import { API_HOST } from '$lib/routes';

export const user = writable<User | null>(null);
const user_from_cookies = Cookies.get('librevento_user');

if (user_from_cookies) {
   console.log("Usuario desde cookies : ", user_from_cookies);
   const decoded_json = atob(user_from_cookies);
   const temp = JSON.parse(decoded_json);
   console.log(temp);
   user.set(temp);
}

export async function fetchUser() {
   const user_cookies = Cookies.get('librevento_user')
   if (!user_cookies) {
      console.warn('Error al cargar el usuario');
      return null
   }
   const decoded_json = atob(user_cookies);
   user.set(JSON.parse(decoded_json))
   console.log("Usuario logueado : ", user);
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
      Cookies.remove('librevento_user');
   } else {
      console.warn('Error al cerrar sesión ');
   }
}
