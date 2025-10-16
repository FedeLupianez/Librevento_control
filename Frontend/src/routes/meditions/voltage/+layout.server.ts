import { redirect } from "@sveltejs/kit";
import type { LayoutServerLoad } from "./$types";
import { ROUTES } from "$lib/routes";

export const load: LayoutServerLoad = ({ cookies }) => {
   const user = cookies.get("librevento_user");
   if (!user) {
      throw redirect(302, `${ROUTES.USER.LOGIN}`);
   }
};
