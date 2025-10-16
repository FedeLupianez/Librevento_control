import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = ({ cookies }) => {
   const user = cookies.get("librevento_user")
   if (user) {
      throw redirect(307, '/meditions/voltage')
   }
   throw redirect(307, '/loby')
}

