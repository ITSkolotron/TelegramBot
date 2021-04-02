from flask import Flask, render_template, url_for
import sqlalchemy
import psycopg2
app = Flask(__name__)


@app.route('/')
def index():
     return render_template("index1.py")

if __name__ == '__main__':
    app.run(debug=True)

