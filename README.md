📄 Design Doc RPA - Automated LinkedIn Profile Search

1. Objetivo 🎯:

Automatizar la búsqueda de perfiles en LinkedIn mediante Robotic Process Automation (RPA) para agilizar el proceso de búsqueda de perfiles en la empresa.

2. Sitio Web 🌐:

- [LinkedIn](https://www.linkedin.com/)

3. Extracción de datos

   - URL del perfil
   - Nombre
   - Imagen de perfil
   - Descripción
   - Empresa actual de trabajo
   - Acerca de
   - Idiomas
   - Experiencias
   - Conocimientos
   - Educación
   - Licencias y certificaciones

4. Tecnologías a utilizar 🛠️:

   - Lenguaje de programación: Python 🐍
   - Bibliotecas: Selenium 🤖, Requests 🌐, BeautifulSoap 🍲, Pandas 🐼
   - Backend sistema de errores: Cloudfare Workers ☁️ con base de datos D1

5. Flujo de trabajo 🔄:

- Los datos de búsqueda se ingresan a través de un formulario web.
- Los datos son enviados a una función Lambda de AWS 🚀.
- La función Lambda recibe el evento y crea un diccionario de configuración para el scraper.
- La configuración se envía a un endpoint de Cloudflare Workers.
- En caso de error, se notifica a otro endpoint de Cloudflare Workers.
- Con la configuración, el scraper inicia el proceso de búsqueda.
- El scraper extrae los datos de los perfiles y los guarda en un archivo CSV 📄.
- El tiempo de ejecución por perfil es aproximadamente de 5 segundos ⏱️.

6. Escalabilidad 📈:

- El código se diseñará de manera modular para que sea fácil agregar más sitios web objetivo en el futuro.

7. Plan de implementación 📆:

- Se utilizará un repositorio de GitHub para el control de versiones.
- se hara documentacion de codigo.
