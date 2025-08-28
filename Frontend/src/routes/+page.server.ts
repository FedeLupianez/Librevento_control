import { redirect } from "@sveltejs/kit";
import { get } from 'svelte/store'
import { user } from "../stores/user";

export function load() {
   const user_data = get(user);
   if (user_data) {
      throw redirect(307, "/meditions/voltage");
   } else {
      throw redirect(307, '/loby')
   }
}

