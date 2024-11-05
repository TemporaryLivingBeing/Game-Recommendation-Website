from flask import Flask, render_template

app = Flask(__name__, template_folder='../www')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/hello")
def hello():
    return render_template('index.html')

def create_app(test_config=False):
    app = Flask(__name__, template_folder='../www')
    app.config['TESTING'] = test_config
    msg_file = 'messages.csv' if app.config['TESTING'] else "test_messages.csv"
    return app
if __name__ == "__main__":
    app.run(debug=True)