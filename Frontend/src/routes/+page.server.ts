import { redirect } from "@sveltejs/kit";
import { user } from '$lib/stores/user';

export function load() {
   if (user != null) {
      throw redirect(307, '/meditions/voltage')
   }
   throw redirect(307, '/loby')
}

