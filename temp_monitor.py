# temp_monitor.py
# Libreria de funciones para registrar lecturas de temperatura.
#
# Estructura del diccionario (monitor):
#   - 'max':      numero maximo de lecturas permitidas (int)
#   - 'readings': lista con las temperaturas de cada lectura (list)
#   - 'total':    suma total de todas las temperaturas (float)





def init(max_readings):
    # Crea un diccionario con las claves requeridas: max, readings y total [cite: 34, 35, 36]7
    monitor = {
        'max': max_readings,
        'readings': [],
        'total': 0.0
    }
    return monitor

def add_reading(monitor, temp):
    
    monitor['readings'].append(temp)
    monitor['total'] += temp
    return monitor

def count(monitor):

    return len(monitor['readings'])

def average_temp(monitor):

    if count(monitor) == 0:
        return 0.0
    return monitor['total'] / count(monitor)

def format_readings(monitor):

    return str(monitor['readings'])

def highest_temp(monitor):

    return max(monitor['readings'])

def coldest_window(monitor, k):

    readings = monitor['readings']
    
    primer_ventana = readings[0:k]
    min_promedio = sum(primer_ventana) / k
    
    
    for i in range(len(readings) - k + 1):
        ventana_actual = readings[i : i + k]
        promedio_actual = sum(ventana_actual) / k
        if promedio_actual < min_promedio:
            min_promedio = promedio_actual
            
    return min_promedio

def longest_rising_streak(monitor):
    
    readings = monitor['readings']
    if not readings:
        return 0
    
    max_racha = 1
    racha_actual = 1
    
    for i in range(1, len(readings)):
        if readings[i] > readings[i-1]:
            racha_actual += 1
        else:
            if racha_actual > max_racha:
                max_racha = racha_actual
            racha_actual = 1
            
    if racha_actual > max_racha:
        max_racha = racha_actual
        
    return max_racha

def main():

    monitor = init(12)
    lecturas = [8.0, 9.5, 11.0, 13.5, 15.0, 17.5, 19.0, 20.0, 19.5, 18.0, 16.5, 15.0]
    for t in lecturas:
        add_reading(monitor, t)
    
    print("numero de lecturas", count(monitor))
    print(f"temp promedio = {average_temp(monitor)}")
    print("temp mas alta", highest_temp(monitor))
    print("ventana mas fria (3) =", coldest_window(monitor, 3))
    print("racha creciente", longest_rising_streak(monitor))
    print(format_readings(monitor))

if __name__ == "__main__":
    main()