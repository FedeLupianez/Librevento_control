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
// export const API_HOST = 'http://localhost:8000';

export const API_ROUTES = {
   USER: {
      AUTH: `${API_HOST}/user/auth`,
      LOGOUT: `${API_HOST}/user/logout`,
      LOGIN: `${API_HOST}/user/login`,
      CREATE: `${API_HOST}/user/create`,
      GET: `${API_HOST}/user/get`,
      GET_ID: `${API_HOST}/user/get_id`,
      DELETE: `${API_HOST}/user/delete`,
   },
   MEASUREMENT: {
      VOLTAGES: `${API_HOST}/measurement/get_voltages`,
      CONSUMPTIONS: `${API_HOST}/measurement/get_consumptions`,
      ALL_VOLTAGES: `${API_HOST}/measurement/get_all_voltages`,
      ALL_CONSUMPTIONS: `${API_HOST}/measurement/get_all_consumptions`
   },
   GENERATOR: {
      CREATE: `${API_HOST}/generator/create`,
      GET: `${API_HOST}/generator/get`,
      DELETE: `${API_HOST}/generator/delete`,
      GET_MACADDRESS: `${API_HOST}/generator/get_macaddress`,
   }
}
