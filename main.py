from flask import Flask, jsonify, render_template
import ReadSerial

main = Flask(__name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route('/data')
def data():
    dist = ReadSerial.latest_data
    if dist:
        angle, distance = dist
        print(f'Получены данные: угол={angle}, расстояние={distance}')
        return jsonify({'angle': angle, 'distance': distance})
    else:
        return jsonify({'angle': None, 'distance': None}), 404  # Возвращаем 404, если данных нет



if __name__ == "__main__":
    ReadSerial.start()
main.run(debug=False)  # Включаем режим отладки для получения более подробных сообщений об ошибках
