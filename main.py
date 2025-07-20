from flask import Flask, jsonify, render_template
import ReadSerial

main = Flask(__name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route('/data')
def data():
    dist = ReadSerial.latest_data
    print(f'distance {dist}')
    return jsonify({'distance': dist})



if __name__ == "__main__":
    ReadSerial.start()
main.run(debug= False)
