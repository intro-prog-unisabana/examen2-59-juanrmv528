import temp_monitor

def main():

    nombre_archivo = input("Nombre del archivo: ")
    
    try:

        archivo = open(nombre_archivo, "r")
        
        n = int(archivo.readline())

        monitor = temp_monitor.init(n)
        
        
        for _ in range(n):
            linea = archivo.readline()
            if linea:
                temp = float(linea)
                temp_monitor.add_reading(monitor, temp)
        
        archivo.close()
        

        print(temp_monitor.longest_rising_streak(monitor))
        
    except FileNotFoundError:
        print("Archivo no encontrado")

if __name__ == "__main__":
    main()