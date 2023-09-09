from flask import Flask
import main
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/search_history/<history_id>")
def search_history(history_id):
    th = threading.Thread(target=main.search_history, args=(history_id, False))
    th.start()
    return {"message": "Received", "status": 200 }

if __name__ == '__main__':
    app.run(debug=False, port='8080', host='0.0.0.0')