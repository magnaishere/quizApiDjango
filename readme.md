<p align="center">
  <a href="https://codesandbox.io">
    <img src="https://codesandbox.io/static/img/banner.png?v=2" height="300px">
  </a>
</p>

&nbsp;

<h4 align="center">  Descripción del Desafío:  </h4>
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

## Other CodeSandbox repositories

CodeSandbox consists of several separate servers, some of which are open
sourced.

- Client: the web application
- Server: the [Phoenix](https://github.com/phoenixframework/phoenix) API server
- Nginx: Nginx config files
- [Git Extractor](https://github.com/codesandbox/codesandbox-importers):
  responsible for extracting the source from a GitHub repository
- [CLI](https://github.com/codesandbox/codesandbox-importers/tree/master/packages/cli):
  the CLI to upload a CodeSandbox project from your command line

## Documentation

You can find our documentation on our
[website](https://codesandbox.io/docs/learn/introduction/overview)

## Contributors ✨

Thanks goes to these wonderful people
([emoji key](https://github.com/all-contributors/all-contributors#emoji-key)):

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## Thanks

<a href="https://www.chromaticqa.com/"><img src="https://cdn-images-1.medium.com/letterbox/147/36/50/50/1*oHHjTjInDOBxIuYHDY2gFA.png?source=logoAvatar-d7276495b101---37816ec27d7a" width="120"/></a>

Thanks to [Chromatic](https://www.chromaticqa.com/) for providing the visual
testing platform that helps us catch unexpected changes.
