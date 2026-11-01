# Sistema de gestión de contactos

## Datos del estudiante

- Nombre: [Anderson Cruz Arteaga]
- Materia: [FUNDAMENTOS DE PROGRAMACION]
- Fecha: [03/11/26]

## Objetivo

Desarrollar un sistema de contactos en Python que permita ingresar
datos por teclado, almacenarlos en un archivo de texto, consultarlos,
buscarlos y contarlos.

También permite guardar y recuperar una copia binaria con formato propio.

## Herramientas utilizadas

- Python 3.
- Visual Studio Code.
- GitHub Desktop.
- GitHub.
- Un editor externo para revisar el archivo de texto.

## Archivos del proyecto

- main.py: programa principal.
- README.md: documentación del proyecto.
- .gitignore: exclusiones del repositorio.
- datos/contactos.txt: archivo de contactos en texto.
- datos/contactos.bin: copia binaria.

La carpeta datos se crea al ejecutar el programa.
El archivo de texto se genera al agregar el primer contacto.
El archivo binario se genera al utilizar la opción 5.

## Ejecución

Abrir main.py en Visual Studio Code y ejecutarlo en la terminal.

También se puede ejecutar desde la carpeta del proyecto:

```bash
python main.py
```

Según la instalación, puede utilizarse:

```bash
py main.py
```

O bien:

```bash
python3 main.py
```

No requiere instalar paquetes adicionales.

## Opciones del menú

1. Agregar contacto.
2. Mostrar archivo de texto línea por línea.
3. Buscar contactos por nombre.
4. Contar contactos.
5. Guardar copia binaria.
6. Leer copia binaria.
0. Salir.

## Ingreso de datos

Cada contacto contiene:

- Nombre.
- Teléfono.
- Correo.

Los datos se solicitan por teclado y no se permiten campos vacíos.
El teléfono se almacena como texto.

## Almacenamiento en texto

Se guarda un contacto por línea mediante JSON.
La codificación utilizada es UTF-8.

El archivo se abre en modo a para añadir nuevos contactos
sin sobrescribir los anteriores.

## Lectura y procesamiento

El programa permite mostrar el archivo línea por línea.

También convierte las líneas válidas en diccionarios para:

- Buscar coincidencias en el nombre.
- Contar los contactos guardados.

Las líneas con registros incorrectos se omiten con un aviso.

## Archivo binario

Se utiliza un formato propio formado por:

1. Una firma de cuatro bytes: CT01.
2. Un entero sin signo de cuatro bytes con la longitud del contenido,
   en orden big-endian.
3. La lista de contactos representada como JSON en UTF-8.

La copia binaria se guarda con la opción 5.
Los datos se recuperan y muestran con la opción 6.

La copia no se actualiza automáticamente al agregar contactos.
La lectura del binario no modifica el archivo de texto.

## Verificación con editor externo

Abrir datos/contactos.txt con Bloc de notas u otro editor externo
y comprobar que los contactos se conservan y son legibles.

- Editor utilizado: [Completar]
- Resultado de la revisión: [Completar después de verificar]

## Cierre de archivos

Se utiliza with en todas las operaciones de lectura y escritura
para cerrar automáticamente los archivos al finalizar cada bloque.

## Limitaciones

- No permite editar ni eliminar contactos.
- No evita contactos duplicados.
- No comprueba que el teléfono o el correo existan.
- La búsqueda se realiza únicamente por nombre.
- El contenido de la copia binaria tiene un límite de 10 000 000 bytes.

## Publicación en GitHub

Los archivos se registran con un commit en GitHub Desktop.
Después se publican mediante Publish repository o se envían
las actualizaciones mediante Push origin.

Para los ejemplos deben utilizarse datos ficticios.


