export const ROUTES = {
   HOME: '/',
   USER: {
      LOGIN: '/login',
      SIGN_UP: '/signup'
   },
   VOLTAGE: '/meditions/voltage',
   GET_GENERATOR: '/get_generator',
   CONSUMPTION: '/consumption',
   ALERTS: '/alertas'
}
export const API_HOST = import.meta.env.VITE_API_HOST;
