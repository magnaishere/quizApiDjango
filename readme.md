<h1 align="center"> Api Quiz </h1>
&nbsp;

<h4 align="center">  Descripción del Desafío  </h4>
El objetivo es desarrollar una API para un sistema de "Quiz" que permita gestionar cuestionarios, calcular puntos de los usuarios, y enviar un correo con los resultados al finalizar. Los detalles son los siguientes:


<p> Modelos Principales </p>

- :heavy_check_mark: Quiz: Contendrá el título y la descripción del cuestionario.
- :heavy_check_mark: Question: Asociada a un Quiz, incluirá la pregunta, las opciones de respuesta, y la opción correcta.
- :heavy_check_mark: Answer: Guardará las respuestas seleccionadas por un usuario para un Quiz.
- :heavy_check_mark: UserResult: Guardará los puntos obtenidos por cada usuario al finalizar un Quiz.

<p> Requisitos Técnicos </p>

- :heavy_check_mark: Autenticación: Implementar un sistema de autenticación basado en tokens (puedes usar JWT o el sistema predeterminado de Django Rest Framework).

<p> Endpoints CRUD </p>

- :heavy_check_mark: CRUD para Quizzes y Questions solo accesible por administradores autenticados.
- :heavy_check_mark: Los usuarios autenticados podrán responder Quizzes a través de un endpoint específico.

<p> Lógica de Puntos </p>

- :heavy_check_mark: Calcular los puntos de un usuario en base a las respuestas correctas.
- :heavy_check_mark: Guardar los puntos en el modelo UserResult asociado al usuario y al Quiz.

<p> Envío de Correos </p>

- :heavy_check_mark: Enviar un correo al usuario con sus puntos obtenidos al finalizar el Quiz. 

<p> Documentación: </p>

- :heavy_check_mark: Usar Swagger (o DRF Spectacular) para documentar todos los endpoints.
- :heavy_check_mark: Mostrar ejemplos de entrada y salida para los endpoints.

<p> Extras (Opcionales, pero se valorarán): </p>

- :heavy_check_mark: Permitir agregar preguntas con imágenes.
- :heavy_check_mark: Implementar un sistema de temporizador para limitar el tiempo de respuesta de un Quiz.
- :heavy_check_mark: Escribir pruebas unitarias y de integración para verificar la lógica de puntos y el envío de correos.


<h4 align="center">  Como empezar  </h4>

Tras ser instalado el entorno de desarrollo (importar del repositorio, instalación de paquetes, etc) se debe tener en cuenta que el proyecto incluye la base de datos sqlite con algunos datos de pruebas (un Quiz registrado y algunas preguntas). Sin embargo acá se incluye una guía rápida de pruebas.


<h4 align="center">  Guía rápida para realizar un quiz  </h4>

La ruta de <strong>Swagger</strong> para realizar operaciones iniciales

```
  http://localhost:8000/doc/
```

El sistema de autenticación esta programado por bloques. El metodo `Register` puede crear usuarios capaces de realizar quiz en el sistema, mas no ejecutar los CRUD de escritura. Solamente usarios bajo la condición de `STAFF` pueden realizar cambios en los registros de todos los métodos. Este tipo de usuario puede crease mediante el siguiente comando:

```
  python manage.py createsuperuser
```

Sin embargo, existe un usuario en la base de datos ya registrado al cual se puede acceder mediante las siguientes credenciales en el método `Login`:

```
  {
    "username": "admin",
    "password": "20155558"
  }
```
Para esta prueba crearemos un usuario tradicional para realizar un quiz, por tanto el primer método a consultar debe ser `Register` 

<image src="https://i.ibb.co/JQDdFPR/Captura-de-pantalla-2024-12-14-085302.png" alt="Paso1">

Esto generará un valor string token el cual tambien puede obtenerse por el método `Login`

Esta estructura de autenticación está generada con el sistema predeterminado de Django Rest Framework y por tanto debe agregarse en la parte superior de Swagger en el botón `Authorize` e integrarse a la autorizacion de la siguiente manera:

<image src="https://i.ibb.co/YtSZcsV/Captura-de-pantalla-2024-12-14-090050.png" alt="Paso2">

:warning: Importante: Debe dejarse un espacio entre la palabra `Token` y el token generado. ejemplo: 

```
Token {mygeneratedtoken}
```

Tras autenticarse puede realizarse un quiz registrado previamente en la base de datos (o alguno creado por un usuario `STAFF`)

Ubicamos el método "Método para hacer un quiz" el cual presenta la siguiente estructura:

<image src="https://i.ibb.co/hM5w8NC/Captura-de-pantalla-2024-12-14-095215.png" alt="Paso3">

Se indican 3 paremetros:

- `user:` indica el id del usuario entregado tras el registro o login.
- `quiz:` indica el id del quiz registrado (Usaremos el valor `1` para la prueba rápida).
- `answer:` la respuesta a la pregunta indicada (En la primera ejecución no es necesario ya que no estamos respondiendo ninguna pregunta, por tanto podemos enviarlo vacío o con cualquier valor puesto que será ignorado en esta primera ejecución).

Nuestra petición queda de la siguiente manera:

<image src="https://i.ibb.co/QQYTHC4/Captura-de-pantalla-2024-12-14-095819.png" alt="Paso4">

El servidor responderá con el siguiente formato

<image src="https://i.ibb.co/cDmgqZF/Captura-de-pantalla-2024-12-14-100023.png" alt="Paso5">

Se ubican multiples paremetros:

- `status:` indica la el resultado de la transacción.
- `question:` el objeto con los datos de la pregunta y sus posibles respuestas.

En la información de la pregunta podemos encontrar la pregunta en formato string `question`, `image` el cual es un campo opcional dependiendo de si se agregó una imagen a la pregunta o no y el array `answers` el cual incluye todas las posibles respuestas.

para la siguiente vuelta tomaremos una de las respuestas posibles y la colocaremos en el campo anteriormente ignorado `answer`, de la siguiente manera:

<image src="https://i.ibb.co/vQ9m9Nf/Captura-de-pantalla-2024-12-14-100918.png" alt="Paso6">

Si realizamos esta petición nos devolverá la siguiente pregunta y proseguimos con el mismo proceso hasta que no quede ninguna, en tal caso solamente devolverá `status: 'success'` y los resultados llegaran al correo electrónico del usuario registrado con el siguiente formato:

<image src="https://i.ibb.co/G0FcK1t/Captura-de-pantalla-2024-12-14-101928.png" alt="Paso7">

¡Felicidades realizaste tu primer quiz!

<p> Estructura de calificación </p>

La calificación se basa en 100 puntos lo cuales se dividen entre la cantidad de preguntas del quiz.

```
  (preguntascertadas*100)/cantidaddepreguntas
```

## Autor

| [<img src="https://i.ibb.co/1MmV43j/Captura-de-pantalla-2024-12-14-102432.png" style="border-radius: 50%;" width=115><br><sub>Dehiker Corro</sub>](https://dehikershere.netlify.app/) | 
| :---: |