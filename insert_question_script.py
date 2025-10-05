import sqlite3
# import os
# import random
# from flask import Flask,jsonify, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import OperationalError
# from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from dotenv import load_dotenv
# from openai import OpenAI

# התחברות לבסיס הנתונים
# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()
#
# #הדפסת Q_TEXT מהטבלה QUESTION_SECTION
# cursor.execute("SELECT Q_TEXT FROM QUESTION_SECTION")
# questions = cursor.fetchall()
#
# # הדפסת השורות החוזרות
# question_count = {}
# for question in questions:
#     if question in question_count:
#         question_count[question] += 1
#     else:
#         question_count[question] = 1
#
# # הדפסת השורות שחוזרות
# for question, count in question_count.items():
#     if count > 1:
#         print(f"question: {question[0]}, count: {count}")
#
#
#     question2 = question(   q_number=2, q_id=2, qr_id=1)
#     db.session.add(question2)
#     #
#     question3 = question(   q_number=3, q_id=3,qr_id=1)
#     db.session.add(question3)
#     #
#     question4 = question(  q_number=4, q_id=4,qr_id=1)
#     db.session.add(question4)
#
#
#     # q_section = questionsection(is_link=false,
#     #     q_text="מהם השורשים של המשוואה: x^2 - 15 + 2x",
#     #     q_id=question.q_id)
#
#   #  db.session.add(q_section)
#     q_section2 = questionsection(
#                          is_link=false,
#                          q_text="מהו הערך של פאי?",
#                          q_id=question2.q_id)

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

DATABASE_URL = "sqlite:///users.db"  # שנה את ה-URL בהתאם
engine = create_engine(DATABASE_URL)
metadata = MetaData()
tables = metadata.tables.keys()
print("List of tables:")
for table in tables:
    print(table)
# Session = sessionmaker(bind=engine)
# session = Session()
#
# Base = declarative_base()
#
# class Questioneer(Base):
#     __tablename__ = 'questioneer'
#     QR_ID = Column(Integer, primary_key=True, autoincrement=True)
#     QR_CODE = Column(String, unique=True)
#     questions = relationship("Question", back_populates="questioneer")
#
# class Question(Base):
#     __tablename__ = 'QUESTION'
#     Q_ID = Column(Integer, primary_key=True)
#     q_number = Column(Integer)
#     QR_ID = Column(Integer, ForeignKey('questioneer.QR_ID'))
#     questioneer = relationship("Questioneer", back_populates="questions")
#
# new_question = Question(q_number=1, Q_ID=1, QR_ID=1)
# session.add(new_question)
#
# class QuestionSection(Base):
#     __tablename__ = 'QUESTION_SECTION'
#     QS_ID = Column(Integer, primary_key=True, autoincrement=True)
#     IS_Link = Column(Boolean, nullable=False)
#     Q_Text = Column(Text, nullable=False)
#     OPT_Answer = Column(Text)
#     Q_ID = Column(Integer, ForeignKey('question.Q_ID'))
#
# q_section = QuestionSection(IS_Link=False,
#                             Q_Text="מהם השורשים של המשוואה: X^2 - 15 + 2X",
#                             Q_ID=new_question.Q_ID)
#
# session.add(q_section)
# session.commit()
# session.close()
# הכנסת השורות לטבלה QUESTION_SECTION אם צריך (דוגמה להוספה)
# cursor.execute("INSERT INTO QUESTION_SECTION (Q_TEXT) VALUES (?)", (new_question,))

# שמירת השינויים
# conn.commit()
#
# # סגירת החיבור
# conn.close()