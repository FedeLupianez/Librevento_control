# Backend

## Librerías : 
 - *fastApi*: Sirve para crear APIs, es sencilla y fácil de entender.

 - SQLmodel : Es una librería para manejar tablas sql, conexiones a bases de datos, etc.

 - Uvicorn : Sirve para correr el servidor de fastApi.

## Comandos :
 - *uvicorn main:app --reload* --> Corre el servidor en localhost
 - *uvicorn main:app --reload --host 0.0.0.0 --port 8000*
   Este comando corre la API en localhost pero permite la conexión desde cualquier computadora, lo que
   permitiria probar la API desde la esp32.
   Para poder probar la API en este modo, se debe conocer la ip de la máquina en la que está corriendo 
   con el comando `ipconfig` en la terminal de la computadora. Después para hacer las pruebas solo 
   tenemos que cambiar en la url `http://localhost:8000` por `http://<ip>:8000`.
