import serial
import threading
import time

latest_data = None  # здесь будет храниться последний полученный кортеж (angle, distance)
stop_thread = False  # флаг для остановки потока, если нужно

def read_serial():
    global latest_data, stop_thread
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)
        print("Порт открыт!")
    except serial.SerialException as e:
        print(f"Ошибка открытия порта: {e}")
        return
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return

    while not stop_thread:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Ожидаем формат: "angle,distance"
                parts = line.split(',')
                if len(parts) == 2:
                    try:
                        angle = int(parts[0])
                        distance = int(parts[1])
                        # Фильтруем допустимый диапазон расстояния и угла если нужно
                        if 0 <= angle <= 180 and 0 < distance < 2000:
                            latest_data = (angle, distance)
                            print(f"Получено: угол={angle}, расстояние={distance}")
                        else:
                            print(f"Игнорируем некорректные значения: угол={angle}, расстояние={distance}")
                    except ValueError:
                        print(f"Ошибка преобразования чисел: '{line}'")
                else:
                    print(f"Неверный формат данных: '{line}'")
            # else:
            #     pass  # пустая строка, можно игнорировать
            time.sleep(0.01)  # Уменьшаем время сна до 0.01 секунды
        except serial.SerialException as e:
            print(f"Ошибка чтения с порта: {e}")
            break
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            break

    ser.close()
    print("Порт закрыт, поток чтения остановлен.")

def start():
    global thread, stop_thread
    stop_thread = False
    thread = threading.Thread(target=read_serial, daemon=True)
    thread.start()

def stop():
    global stop_thread
    stop_thread = True
    thread.join()

# Пример использования:
if __name__ == "__main__":
    start()
    try:
        while True:
            if latest_data:
                angle, distance = latest_data
                # здесь можно как-то использовать данные
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Выход из программы")
        stop()
