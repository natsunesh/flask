import serial
import threading
import time

latest_data = None

def read_serial():
    global latest_data
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)
        print("Порт открыт!")
    except serial.SerialException as e:
        print(f"Ошибка открытия порта: {e}")
        return
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    distance = int(line)
                    # Фильтрация значений по диапазону
                    if 0 < distance < 2000:
                        latest_data = distance
                        print(f"Получено: {distance}")
                    else:
                        print(f"Игнорируем некорректное значение: {distance}")
                except ValueError:
                    print(f"Не число: '{line}'")
            else:
                # Можно убрать для уменьшения шума в логах
                # print("Пустая строка...")
                pass
            time.sleep(0.05)
        except serial.SerialException as e:
            print(f"Ошибка чтения с порта: {e}")
            break
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            break

def start():
    global thread
    thread = threading.Thread(target=read_serial, daemon=True)
    thread.start()
