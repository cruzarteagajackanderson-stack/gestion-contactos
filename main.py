from pathlib import Path
import json
import struct


# Ubicación de los archivos del proyecto.
BASE = Path(__file__).resolve().parent
CARPETA_DATOS = BASE / "datos"

ARCHIVO_TEXTO = CARPETA_DATOS / "contactos.txt"
ARCHIVO_BINARIO = CARPETA_DATOS / "contactos.bin"

# Formato binario propio:
# firma + longitud del contenido + contactos codificados.
FIRMA = b"CT01"
MAX_BYTES = 10_000_000


def pedir_dato(mensaje):
    """Solicita un dato y evita campos vacíos."""
    while True:
        dato = input(mensaje).strip()

        if dato:
            return dato

        print("El campo no puede estar vacío.")


def contacto_valido(contacto):
    """Comprueba que un contacto tenga los campos esperados."""
    campos = ("nombre", "telefono", "correo")

    return (
        isinstance(contacto, dict)
        and all(
            isinstance(contacto.get(campo), str)
            and contacto[campo].strip()
            for campo in campos
        )
    )


def ingresar_contacto():
    """Recibe los datos del contacto por teclado."""
    print("\n--- INGRESAR CONTACTO ---")

    contacto = {
        "nombre": pedir_dato("Nombre: "),
        "telefono": pedir_dato("Teléfono: "),
        "correo": pedir_dato("Correo: "),
    }

    return contacto


def agregar_contacto():
    """Añade un contacto al texto sin borrar los anteriores."""
    contacto = ingresar_contacto()

    with open(ARCHIVO_TEXTO, "a", encoding="utf-8") as archivo:
        linea = json.dumps(contacto, ensure_ascii=False)
        archivo.write(linea + "\n")

    print("\nContacto guardado correctamente.")


def mostrar_lineas():
    """Lee y muestra el archivo de texto línea por línea."""
    print("\n--- CONTENIDO DEL ARCHIVO DE TEXTO ---")

    if not ARCHIVO_TEXTO.exists():
        print("Todavía no hay archivo. Primero agrega un contacto.")
        return

    cantidad = 0

    with open(ARCHIVO_TEXTO, "r", encoding="utf-8") as archivo:
        for numero, linea in enumerate(archivo, start=1):
            print(f"Línea {numero}: {linea.rstrip()}")
            cantidad += 1

    if cantidad == 0:
        print("El archivo está vacío.")


def leer_contactos():
    """Lee el texto y recupera los contactos válidos."""
    contactos = []

    if not ARCHIVO_TEXTO.exists():
        return contactos

    with open(ARCHIVO_TEXTO, "r", encoding="utf-8") as archivo:
        for numero, linea in enumerate(archivo, start=1):
            if not linea.strip():
                continue

            try:
                contacto = json.loads(linea)
            except json.JSONDecodeError:
                print(
                    f"Aviso: la línea {numero} tiene un formato incorrecto."
                )
                continue

            if contacto_valido(contacto):
                contactos.append(contacto)
            else:
                print(
                    f"Aviso: la línea {numero} no contiene "
                    "un contacto válido."
                )

    return contactos


def mostrar_contacto(contacto, numero):
    """Muestra un contacto de forma ordenada."""
    print(f"\nContacto {numero}")
    print(f"Nombre: {contacto['nombre']}")
    print(f"Teléfono: {contacto['telefono']}")
    print(f"Correo: {contacto['correo']}")


def buscar_contactos():
    """Busca contactos por nombre o parte del nombre."""
    print("\n--- BUSCAR CONTACTOS ---")

    termino = pedir_dato(
        "Escribe el nombre o parte del nombre: "
    ).casefold()

    contactos = leer_contactos()

    resultados = [
        contacto
        for contacto in contactos
        if termino in contacto["nombre"].casefold()
    ]

    if not resultados:
        print("No se encontraron contactos.")
        return

    for numero, contacto in enumerate(resultados, start=1):
        mostrar_contacto(contacto, numero)

    print(f"\nCoincidencias encontradas: {len(resultados)}")


def contar_contactos():
    """Cuenta los contactos válidos guardados en el texto."""
    contactos = leer_contactos()

    print(f"\nTotal de contactos válidos: {len(contactos)}")


def guardar_binario():
    """Guarda una copia con un formato binario propio."""
    contactos = leer_contactos()

    if not contactos:
        print("No hay contactos válidos para guardar.")
        return

    contenido = json.dumps(
        contactos,
        ensure_ascii=False
    ).encode("utf-8")

    if len(contenido) > MAX_BYTES:
        print("Los datos superan el tamaño permitido.")
        return

    if ARCHIVO_BINARIO.exists():
        respuesta = input(
            "La copia binaria ya existe. ¿Reemplazarla? (s/n): "
        ).strip().lower()

        if respuesta != "s":
            print("Operación cancelada.")
            return

    with open(ARCHIVO_BINARIO, "wb") as archivo:
        archivo.write(FIRMA)
        archivo.write(struct.pack(">I", len(contenido)))
        archivo.write(contenido)

    print(
        f"\nCopia binaria guardada con {len(contactos)} contactos."
    )


def leer_binario():
    """Recupera y muestra los contactos del archivo binario."""
    if not ARCHIVO_BINARIO.exists():
        print("Primero debes guardar una copia con la opción 5.")
        return

    with open(ARCHIVO_BINARIO, "rb") as archivo:
        firma = archivo.read(4)

        if firma != FIRMA:
            raise ValueError(
                "El archivo no tiene el formato binario esperado."
            )

        longitud_bytes = archivo.read(4)

        if len(longitud_bytes) != 4:
            raise ValueError(
                "El encabezado del archivo está incompleto."
            )

        longitud = struct.unpack(">I", longitud_bytes)[0]

        if longitud > MAX_BYTES:
            raise ValueError(
                "El archivo supera el tamaño permitido."
            )

        contenido = archivo.read(longitud)

        if len(contenido) != longitud:
            raise ValueError(
                "El contenido del archivo está incompleto."
            )

        if archivo.read(1):
            raise ValueError(
                "El archivo contiene datos adicionales inesperados."
            )

    contactos = json.loads(contenido.decode("utf-8"))

    if not isinstance(contactos, list) or not all(
        contacto_valido(contacto) for contacto in contactos
    ):
        raise ValueError(
            "El archivo no contiene una lista válida de contactos."
        )

    print("\n--- CONTACTOS RECUPERADOS DEL BINARIO ---")

    for numero, contacto in enumerate(contactos, start=1):
        mostrar_contacto(contacto, numero)

    print(f"\nTotal recuperado: {len(contactos)}")


def mostrar_menu():
    """Muestra las opciones del sistema."""
    print("\n========== GESTIÓN DE CONTACTOS ==========")
    print("1. Agregar contacto")
    print("2. Mostrar archivo de texto línea por línea")
    print("3. Buscar contactos por nombre")
    print("4. Contar contactos")
    print("5. Guardar copia binaria")
    print("6. Leer copia binaria")
    print("0. Salir")


def main():
    """Prepara la carpeta y controla el menú principal."""
    try:
        CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"No se pudo crear la carpeta de datos: {error}")
        return

    acciones = {
        "1": agregar_contacto,
        "2": mostrar_lineas,
        "3": buscar_contactos,
        "4": contar_contactos,
        "5": guardar_binario,
        "6": leer_binario,
    }

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "0":
            print("\nPrograma finalizado.")
            break

        accion = acciones.get(opcion)

        if accion is None:
            print("\nOpción inválida. Inténtalo nuevamente.")
            continue

        try:
            accion()
        except (OSError, UnicodeError, ValueError) as error:
            print(f"\nNo se pudo completar la operación: {error}")


if __name__ == "__main__":
    main()