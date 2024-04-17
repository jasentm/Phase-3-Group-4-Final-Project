#lib/models/question.py
import sqlite3
import pickle
from seed.question_seed import seed_questions


CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

class Question:
    
    #list of objects saved to the database
    all = []
        
    def __init__(self, question="", answers = None, correct_answer="", difficulty={}, id=None, quiz_id = None):
        self.question = question 
        self.answers = answers
        self.correct_answer = correct_answer
        self.difficulty = difficulty['difficulty']
        self.id = id
        self.quiz_id = quiz_id
        type(self).all.append(self)
        self.save()

        
    @property
    def answers(self):
        return self._answers
    
    @answers.setter
    def answers(self, answers):
        if answers is None:
            self._answers = []
        elif isinstance(answers, list) and len(answers) == 4:
            self._answers = answers
        else:
            raise Exception("Answers should be a list of 4 answers")
        
            
    @classmethod
    def create_table(cls):
        """create a new table to persist the attributes of the question instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question TEXT,
                answers TEXT,
                correct_answer TEXT,
                difficulty BLOB);
                """
        CURSOR.execute(sql)
        CONN.commit()


    #Save - Insert into table
    def save(self):
        db_answers = pickle.dumps(self.answers)
        db_difficulty = pickle.dumps(self.difficulty)

        try:
            sql="""
                    INSERT INTO questions (question, answers, correct_answer, difficulty) VALUES (?,?,?,?);
                """
            CURSOR.execute(sql,(self.question, db_answers,self.correct_answer, db_difficulty)).fetchone()
            self.id = CURSOR.lastrowid
            CONN.commit()
           
        except Exception as err:
            print(f'Save went wrong,{err}')

    @classmethod
    def create_row(cls,question,answer,correct_answer,difficulty):
        newQuestion = cls(question,answer,correct_answer,difficulty)
        newQuestion.save()
        return newQuestion
    
    @classmethod
    def del_row(cls,id):
        try:
            sql = """
                    DELETE FROM questions WHERE id = ?;
                """
            CURSOR.execute(sql,(id,))
            CONN.commit()
            print(f"Success!! Deleted row of  id:{id}")
        except Exception as err:
            print(f"Error Deleting {id} error:{err}")
    

    @classmethod
    def drop_table(cls):
        sql=""" DROP TABLE IF EXISTS questions; """
        CURSOR.execute(sql)
        CONN.commit()
    
    
    
    
    