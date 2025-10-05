import os
import random
from flask import Flask,jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from openai import OpenAI
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    #level = db.Column(Integer,nullable=True)

class Questioneer(db.Model):
    __tablename__ = 'questioneer'
    QR_ID = Column(Integer, primary_key=True, autoincrement=True)
    QR_CODE = Column(String, unique=True)
    Level = Column(Integer)
    questions = relationship("Question", back_populates="questioneer")

class Question(db.Model):
    __tablename__ = 'question'
    Q_ID = Column(Integer, primary_key=True)#, unique=True)
    q_number = Column(Integer)
    QR_ID = Column(Integer, ForeignKey('questioneer.QR_ID'))
    questioneer = relationship("Questioneer", back_populates="questions")
    sections = relationship("QuestionSection", back_populates="question")

class QuestionSection(db.Model):
    __tablename__ = 'q_section'
    QS_ID = Column(Integer, primary_key=True, autoincrement=True)
    IS_Link = Column(Boolean, nullable=False)
    Q_Text = Column(Text, nullable=False)
    OPT_Answer = Column(Text)
    Q_ID = Column(Integer, ForeignKey('question.Q_ID'))
    Level = Column(Integer)
    question = relationship("Question", back_populates="sections")


def add_questions_with_sections():
    questioneer = Questioneer(QR_ID = 1)
    #db.session.add(questioneer)
    #
    # question = Question( q_number=1, Q_ID=1 ,QR_ID=1)
    # db.session.add(question)
    #
    question2 = Question(   q_number=2, Q_ID=2, QR_ID=1)
    db.session.add(question2)
    #
    question3 = Question(   q_number=3, Q_ID=3,QR_ID=1)
    db.session.add(question3)
    #
    question4 = Question(  q_number=4, Q_ID=4,QR_ID=1)
    db.session.add(question4)


    # q_section = QuestionSection(IS_Link=False,
    #     Q_Text="מהם השורשים של המשוואה: X^2 - 15 + 2X",
    #     Q_ID=question.Q_ID)

  #  db.session.add(q_section)
    q_section2 = QuestionSection(
                         IS_Link=False,
                         Q_Text="מהו הערך של פאי?",
                         Q_ID=question2.Q_ID)

    q_section3 = QuestionSection(
                         IS_Link=False,
                         Q_Text="מהם השורשים של המשוואה: ( X^2 - 4X + 4 = 0 )?",
                         Q_ID=question3.Q_ID)

    q_section4 = QuestionSection(
                         IS_Link=False,
                         Q_Text="מהם השורשים של המשוואה: ( 2X ^ 2 - 8X + 6 = 0 )?",
                         Q_ID=question4.Q_ID)
    db.session.add(q_section2)
    db.session.add(q_section3)
    db.session.add(q_section4)
    return

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
api_key = os.getenv('API_KEY', 'default_value')

def get_feedback(exercise, user_answer):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=api_key,
    )

    prompt = f" בהינתן התרגיל - {exercise} והתשובה של המשתמש -  {user_answer} ענה במספר בלבד , תן לו ציון בין 0 ל 100"
    print(f"prompt::::{prompt}")
    response = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    feedback = response.choices[0].message.content.strip()
    score = feedback[0:3]
    #pdb.set_trace()
    return (feedback,score)

def create_db():

    try:
        db.session.query(User).first()
        return "Table already exists!"
    except OperationalError:
        db.create_all()
        if not User.query.filter_by(username='user').first():
            regular_user = User(username='shiri', password='lilian1234')#,Level=None)
            db.session.add(regular_user)
            regular_user2 = User(username='rami', password='pass1234')#,Level=None)
            db.session.add(regular_user2)
            add_questions_with_sections()
        db.session.commit()

    return "Database and users created!"

@app.route('/', methods=['GET', 'POST'])
def login():
    create_db();
    questions = Question.query.all()
    for q in questions:
        print(f"Q_ID: {q.Q_ID}")
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


def checkSolution(exercise,user_solution):
    print("exercise::::", exercise,"..............")
    (feedback,score) = get_feedback(exercise, user_solution);  # "Correct!" if is_correct else "Incorrect, try again."

    print("feedback::::", feedback)
    print("score::::", score)
    return [feedback,score]
    # score = 0
    # if is_correct:
    #     score = 100
    # return score

@app.route('/resolve/<username>', methods=['GET','POST'])
def resolve(username):
    exercise = request.form.get('exercise')
    print("exercise::::", exercise)
    #exercise = request.form.get('exercise')
    if exercise is None:
        exercise = get_random_question()#"2 * 2"
   # correct_answer = 4

    if request.method == 'POST':
        user_answer = request.form.get('exercise-solution')
        print("user_answer::::", user_answer)

        feedback,score = checkSolution(exercise, user_answer)


        return render_template('result.html',
                               username = username,
                               exercise=exercise,
                               user_answer=user_answer,
                               score = score,
                               feedback = feedback )

    return render_template('resolve.html', username=username, exercise=exercise)

@app.route('/random-question')
def get_random_question():
        # Get the list of QR_IDs
        qs_ids = [q.q_number for q in Question.query.all()]

        if not qs_ids:
            print("No questions available")
            return "No questions available"

        # Generate a random QR_ID
        random_qs_id = random.choice(qs_ids)

        print("random_qs_id::::", random_qs_id)
        # Fetch the question and section with the random QR_ID
        question = Question.query.filter_by(Q_ID=random_qs_id).first()

        if not question:
            # Fetch the first question if none found
            question = Question.query.first()

        # Fetch the section linked to the question
        q_section = QuestionSection.query.filter_by(Q_ID=question.Q_ID).first()

        print(f"Returned q_section of id:{q_section.Q_ID}")
        return q_section.Q_Text if q_section else "No section available"

    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     return render_template('thanks.html', name=name)
    # return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)