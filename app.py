from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from openai import OpenAI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# defaults to os.environ.get("OPENAI_API_KEY")
api_key = "private"

def get_feedback(exercise, user_answer):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=api_key,
    )

    prompt = f" האם {exercise} == {user_answer}  במידה ולא, הסבר מה הטעות ?"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    feedback = response.choices[0].message.content.strip()
    return feedback

def create_db():
    try:
        db.session.query(User).first()
        return "Table already exists!"
    except OperationalError:
        db.create_all()
        if not User.query.filter_by(username='user').first():
            regular_user = User(username='shiri', password='lilian1234')
            db.session.add(regular_user)
            regular_user2 = User(username='rami', password='pass1234')
            db.session.add(regular_user2)

        db.session.commit()

    return "Database and users created!"

@app.route('/', methods=['GET', 'POST'])
def login():
    create_db();
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            #TBD: we need to pass user id from somewhere, to fetch user history.
            return render_template('welcome.html', username=username)

           # return resolve_exercise();
           #return render_template('welcome.html', username=username)
        else:
            return "Login Failed. Please check your username and password."
    return render_template('login.html')


@app.route('/resolve/<username>', methods=['GET', 'POST'])
def resolve(username):
    exercise = "2 * 2"
    correct_answer = 4

    if request.method == 'POST':
        user_answer = request.form.get('exercise-solution', type=int)
        print("user_answer::::", user_answer)

        is_correct = (user_answer == correct_answer)
        feedback = get_feedback(exercise, user_answer);#"Correct!" if is_correct else "Incorrect, try again."
        score = 100 if is_correct else 0

        return render_template('result.html', exercise=exercise, user_answer=user_answer, feedback=feedback,
                               score=score)

    return render_template('resolve.html', username=username, exercise=exercise)



    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     return render_template('thanks.html', name=name)
    # return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)