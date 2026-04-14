# temp_monitor_client.py
# Programa cliente que lee temperaturas de un archivo
# e imprime la racha creciente mas larga.

import temp_monitor


def main():
    # TODO: Pedir el nombre del archivo al usuario usando input()
    
    # TODO: Abrir el archivo y leer el numero de lecturas n

    # TODO: Crear el monitor usando temp_monitor.init(n)
    
    # TODO: Leer las n temperaturas y agregarlas con temp_monitor.add_reading()
    
    # TODO: Imprimir la racha creciente mas larga
    #       usando temp_monitor.longest_rising_streak()
    
    pass


if __name__ == "__main__":
    main()
















import temp_monitor

def main():
    # Pide el nombre del archivo al usuario [cite: 113, 130]
    nombre_archivo = input("Nombre del archivo: ")
    
    try:
        # Abre el archivo en modo lectura [cite: 113]
        archivo = open(nombre_archivo, "r")
        
        # La primera línea es el número de lecturas 'n' [cite: 114]
        n = int(archivo.readline())
        
        # Inicializa el monitor con capacidad n [cite: 113]
        monitor = temp_monitor.init(n)
        
        # Lee las n temperaturas restantes, una por línea [cite: 114]
        for _ in range(n):
            linea = archivo.readline()
            if linea:
                temp = float(linea)
                temp_monitor.add_reading(monitor, temp)
        
        archivo.close()
        
        # Imprime la racha creciente más larga [cite: 113, 131]
        print(temp_monitor.longest_rising_streak(monitor))
        
    except FileNotFoundError:
        print("Archivo no encontrado.")

if __name__ == "__main__":
    main()