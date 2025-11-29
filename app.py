from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DATABASE MODEL
class StudentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    roll = db.Column(db.String(50))
    total = db.Column(db.Integer)
    percentage = db.Column(db.Float)
    grade = db.Column(db.String(5))

def calculate_grade(percentage):
    if percentage >= 80:
        return "A+"
    elif percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "Fail"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    name = request.form['name']
    roll = request.form['roll']
    s1 = int(request.form['subject1'])
    s2 = int(request.form['subject2'])
    s3 = int(request.form['subject3'])

    total = s1 + s2 + s3
    percentage = round((total / 300) * 100, 2)
    grade = calculate_grade(percentage)

    # SAVE RESULT TO DATABASE
    result = StudentResult(name=name, roll=roll,
                           total=total, percentage=percentage,
                           grade=grade)
    db.session.add(result)
    db.session.commit()

    return render_template('result.html',
                           name=name,
                           roll=roll,
                           total=total,
                           percentage=percentage,
                           grade=grade)

@app.route('/results')
def results():
    all_data = StudentResult.query.all()
    return render_template('all_results.html', results=all_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create tables
    app.run(debug=True)
