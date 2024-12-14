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


<h4 align="center">  Guía rápida de pruebas  </h4>

<p> La ruta de <strong>Swagger</strong> para realizar operaciones iniciales

```
  http://localhost:8000/doc/
```

La autenticación en necesaria por tanto el primero método a consultar debe ser `Register` 

<image src="https://i.ibb.co/JQDdFPR/Captura-de-pantalla-2024-12-14-085302.png" alt="Paso1">