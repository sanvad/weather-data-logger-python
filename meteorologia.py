
import struct
import random
import os

# ==========================================
# CONSTANTES DEL SISTEMA
# ==========================================

ARCHIVO_BINARIO = "datos_meteorologicos.bin"
ARCHIVO_REPORTE = "reporte_diario.txt"

# < = little-endian, i = entero de 4 bytes,
# f = flotante de 4 bytes
FORMATO_REGISTRO = "<ifff"
TAMANO_REGISTRO = struct.calcsize(FORMATO_REGISTRO)
TOTAL_REGISTROS = 24


# ==========================================
# 1. GENERAR Y GUARDAR DATOS BINARIOS
# ==========================================

def simular_y_guardar_datos_binarios():
    """
    Genera 24 lecturas meteorologicas simuladas,
    las empaqueta en un buffer y las guarda
    en un archivo binario.
    """
    print("\n--- 1. Generacion y almacenamiento ---")

    buffer = bytearray()

    try:
        for hora in range(TOTAL_REGISTROS):
            # Generar datos simulados
            temp = round(random.uniform(12.0, 22.0), 2)
            hum = round(random.uniform(40.0, 90.0), 2)
            viento = round(random.uniform(5.0, 30.0), 2)

            # Empaquetar los datos en bytes
            registro = struct.pack(
                FORMATO_REGISTRO,
                hora,
                temp,
                hum,
                viento
            )

            # Agregar el registro al buffer
            buffer.extend(registro)

        # Escribir todo el buffer en una operacion
        with open(ARCHIVO_BINARIO, "wb") as archivo:
            bytes_escritos = archivo.write(buffer)

        print(f"Archivo creado: {ARCHIVO_BINARIO}")
        print(f"Registros generados: {TOTAL_REGISTROS}")
        print(f"Bytes escritos: {bytes_escritos}")
        print(f"Tamano por registro: {TAMANO_REGISTRO} bytes")

        if bytes_escritos == TOTAL_REGISTROS * TAMANO_REGISTRO:
            print("Verificacion del tamano: correcta.")
        else:
            print("Advertencia: el tamano escrito es inesperado.")

    except (OSError, struct.error) as e:
        print(f"Error al generar o guardar los datos: {e}")

    except Exception as e:
        print(f"Error inesperado: {e}")


# ==========================================
# 2. LEER Y MOSTRAR DATOS BINARIOS
# ==========================================

def leer_y_mostrar_datos_binarios():
    """
    Lee el archivo binario, recupera cada registro
    y devuelve una lista con los datos.
    """
    print("\n--- 2. Lectura de datos binarios ---")

    registros = []

    try:
        with open(ARCHIVO_BINARIO, "rb") as archivo:
            while True:
                bloque = archivo.read(TAMANO_REGISTRO)

                # Fin del archivo
                if not bloque:
                    break

                # Detectar registro incompleto
                if len(bloque) != TAMANO_REGISTRO:
                    print(
                        "Advertencia: se encontro un "
                        "registro incompleto al final."
                    )
                    break

                # Desempaquetar los bytes
                hora, temp, hum, viento = struct.unpack(
                    FORMATO_REGISTRO,
                    bloque
                )

                # Validar los datos recuperados
                if not (0 <= temp <= 60):
                    print(f"Advertencia: temperatura invalida en hora {hora}.")

                if not (0 <= hum <= 100):
                    print(f"Advertencia: humedad invalida en hora {hora}.")

                if viento < 0:
                    print(f"Advertencia: viento invalido en hora {hora}.")

                # Guardar el registro en una lista
                registros.append({
                    "hora": hora,
                    "temp": temp,
                    "hum": hum,
                    "viento": viento
                })

                # Mostrar los datos
                print(
                    f"Hora {hora:02d}: "
                    f"Temp: {temp:.2f} C, "
                    f"Hum: {hum:.2f} %, "
                    f"Viento: {viento:.2f} km/h"
                )

        print(f"\nRegistros recuperados: {len(registros)}")

        if len(registros) != TOTAL_REGISTROS:
            print(
                f"Advertencia: se esperaban {TOTAL_REGISTROS} "
                f"registros, pero se recuperaron {len(registros)}."
            )

    except FileNotFoundError:
        print(f"Error: no existe el archivo '{ARCHIVO_BINARIO}'.")

    except (OSError, struct.error) as e:
        print(f"Error al leer el archivo binario: {e}")

    return registros


# ==========================================
# 3. GENERAR REPORTE DIARIO
# ==========================================

def generar_reporte_diario(registros):
    """
    Calcula estadisticas meteorologicas y genera
    un reporte de texto.
    """
    print("\n--- 3. Generacion del reporte diario ---")

    if not registros:
        print("No hay registros para generar el reporte.")
        return

    try:
        temperaturas = [r["temp"] for r in registros]
        humedades = [r["hum"] for r in registros]
        vientos = [r["viento"] for r in registros]

        # Promedios
        prom_temp = sum(temperaturas) / len(temperaturas)
        prom_hum = sum(humedades) / len(humedades)
        prom_viento = sum(vientos) / len(vientos)

        # Maximos y minimos
        max_temp = max(temperaturas)
        min_temp = min(temperaturas)

        max_hum = max(humedades)
        min_hum = min(humedades)

        max_viento = max(vientos)
        min_viento = min(vientos)

        with open(ARCHIVO_REPORTE, "w", encoding="utf-8") as archivo:
            archivo.write("=" * 55 + "\n")
            archivo.write("       REPORTE METEOROLOGICO DIARIO\n")
            archivo.write("=" * 55 + "\n\n")

            archivo.write(
                f"Total de lecturas registradas: {len(registros)}\n\n"
            )

            archivo.write("ESTADISTICAS GENERALES\n")
            archivo.write("-" * 55 + "\n")

            archivo.write(f"Temperatura promedio: {prom_temp:.2f} C\n")
            archivo.write(f"Temperatura maxima:   {max_temp:.2f} C\n")
            archivo.write(f"Temperatura minima:   {min_temp:.2f} C\n\n")

            archivo.write(f"Humedad promedio:     {prom_hum:.2f} %\n")
            archivo.write(f"Humedad maxima:       {max_hum:.2f} %\n")
            archivo.write(f"Humedad minima:       {min_hum:.2f} %\n\n")

            archivo.write(f"Viento promedio:      {prom_viento:.2f} km/h\n")
            archivo.write(f"Viento maximo:        {max_viento:.2f} km/h\n")
            archivo.write(f"Viento minimo:        {min_viento:.2f} km/h\n\n")

            archivo.write("DETALLE HORA A HORA\n")
            archivo.write("-" * 55 + "\n")
            archivo.write(
                f"{'Hora':<8}{'Temp (C)':<13}"
                f"{'Humedad (%)':<15}{'Viento (km/h)':<15}\n"
            )
            archivo.write("-" * 55 + "\n")

            for r in registros:
                archivo.write(
                    f"{r['hora']:02d}:00   "
                    f"{r['temp']:<13.2f}"
                    f"{r['hum']:<15.2f}"
                    f"{r['viento']:<15.2f}\n"
                )

            archivo.write("=" * 55 + "\n")

        print(f"Reporte generado correctamente: {ARCHIVO_REPORTE}")

    except OSError as e:
        print(f"Error al escribir el reporte: {e}")

    except (ValueError, KeyError, TypeError) as e:
        print(f"Error al calcular las estadisticas: {e}")


# ==========================================
# 4. PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("=" * 55)
    print(" SISTEMA DE REGISTRO METEOROLOGICO")
    print("=" * 55)

    simular_y_guardar_datos_binarios()

    datos_recuperados = leer_y_mostrar_datos_binarios()

    generar_reporte_diario(datos_recuperados)

    print("\nProceso finalizado.")
