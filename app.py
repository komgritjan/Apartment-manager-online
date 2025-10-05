from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dorm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer, nullable=False)
    number = db.Column(db.String(10), nullable=False)
    tenant = db.Column(db.String(100))

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    month = db.Column(db.String(20))
    water_unit = db.Column(db.Integer)
    electric_unit = db.Column(db.Integer)
    water_rate = db.Column(db.Float, default=18.0)
    electric_rate = db.Column(db.Float, default=8.0)
    rent = db.Column(db.Float, default=2500.0)
    total = db.Column(db.Float)

@app.route('/')
def index():
    rooms = Room.query.all()
    return render_template_string('''
    <h2>🏠 Dorm Manager Dashboard</h2>
    <p>Total rooms: {{ rooms|length }}</p>
    <a href="{{ url_for('add_bill') }}">➕ Create Bill</a>
    <ul>
    {% for r in rooms %}
        <li>Room {{ r.number }} (Floor {{ r.floor }}) - Tenant: {{ r.tenant or 'Vacant' }}</li>
    {% endfor %}
    </ul>
    ''', rooms=rooms)

@app.route('/add_bill', methods=['GET','POST'])
def add_bill():
    if request.method == 'POST':
        room_id = request.form['room_id']
        month = request.form['month']
        water = int(request.form['water'])
        electric = int(request.form['electric'])
        bill = Bill(room_id=room_id, month=month, water_unit=water, electric_unit=electric)
        bill.total = bill.rent + (bill.water_unit * bill.water_rate) + (bill.electric_unit * bill.electric_rate)
        db.session.add(bill)
        db.session.commit()
        return redirect(url_for('index'))
    rooms = Room.query.all()
    return render_template_string('''
    <h3>Create Bill</h3>
    <form method="post">
        Room:
        <select name="room_id">
            {% for r in rooms %}<option value="{{r.id}}">{{r.number}}</option>{% endfor %}
        </select><br>
        Month: <input name="month"><br>
        Water units: <input name="water"><br>
        Electric units: <input name="electric"><br>
        <button type="submit">Save</button>
    </form>
    ''', rooms=rooms)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
