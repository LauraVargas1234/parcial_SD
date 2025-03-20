# parcial_SD
1.​ Captura de pantalla del JSON obtenido en GET /api/extract.
![imagen](https://github.com/user-attachments/assets/775824b5-3a5f-489c-8827-0a2188a92084)

2.​ Captura de pantalla de la transformación de datos.
![imagen](https://github.com/user-attachments/assets/124ebb28-2999-445f-b14d-4e446c25218c)

3.​ Captura de pantalla de la base de datos en PostgreSQL con los datos transformados.
![imagen](https://github.com/user-attachments/assets/0e771202-0ac0-4e4c-a93d-bb65c0b2891a)

4.​ Archivo recap.csv generado.
Este seria es resultado del mi archivo recap.csv 
id,nombre_formateado,categoria_calificacion,decada,puntuacion_ajustada,fecha_procesamiento
1,interstellar,Mala,1990s,5.2,2025-03-20
2,the-shawshank-redemption,Mala,2000s,6.8,2025-03-20
3,jurassic-park,Regular,2000s,10.2,2025-03-20
4,the-matrix,Regular,1990s,11.100000000000001,2025-03-20
5,the-social-network,Buena,1980s,14.099999999999998,2025-03-20
6,schindler's-list,Buena,1980s,14.900000000000002,2025-03-20

**5.​ Explicación detallada de cada paso con instrucciones para ejecutar el proyecto.
Para ejecutar el proyecto se debe hacer:**

1)Verifique que tenga docker y docker compose con los siguientes comandos:
docker --version
docker-compose --version 
Si las tiene instaladas continúe el proceso.

2) Clone el repositorio ejecutando el siguiente comando:
https://github.com/LauraVargas1234/Taller.git

3) Verifique la rama en la que está con el comando "git branch", en este paso debe quedar en master

4) Con el repositorio clonado ejecute el siguiente comando para levantar los contenedores:
docker-compose up --build

Nota: Puedes verificar que los contenedores estén corriendo con el comando: "docker ps"

5) Cree la tabla de los datos de la siguiente manera:
- docker-compose exec postgres psql -U user -d etl_db
- CREATE TABLE etl_data (
	id VARCHAR(255),
	nombre_formateado VARCHAR(255),
	categoria_calificacion VARCHAR(50),
	decada VARCHAR(20),
	puntuacion_ajustada FLOAT,
	fecha_procesamiento DATE
);
- verifique con el comando “\dt”

6) Posteriormente ingrese a “http://localhost:7474” e ingrese con las credenciales 
- Usuario: neo4j
- Contraseña: laura2002
  
7) Use este comando en la consola de neo4j
    
LOAD CSV WITH HEADERS FROM 'file:///dataset_a_peliculas.csv'
AS row
CREATE (:Pelicula {
  id: toInteger(row.id),
  nombre: row.nombre,
  calificacion: toFloat(row.calificacion),
  año_lanzamiento: toInteger(row.año_lanzamiento),
  genero: row.genero
});

para obtener: ![imagen](https://github.com/user-attachments/assets/40f5b4d4-3794-49e8-a810-0e222e4ee4f1)

8) Use el comando curl http://localhost:5000/api/etl para obtener la imagen del punto 2
   
9) Verifique que en su carpeta raíz se haya creado el archivo “recap.csv” el cual es el resultado esperado
    
Nota: para verificar los datos ya transformados ingrese a “http://localhost:5000/api/extract”

