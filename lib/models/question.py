#lib/models/question.py
import sqlite3
from seed.question_seed import questions_easy


CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

class Question:
    
    #list of objects saved to the database
    all = []
    DEFAULT_QUESTIONS = questions_easy
    
    def __init__(self, question="", answers = [], correct_answer="", difficulty={}, id=None):
        self.question = question 
        self.answers = answers
        self.correct_answer = correct_answer
        self.difficulty = difficulty.difficulty
        self.id = id
        self.save()
        type(self).all.append(self)
        
    @property
    def answers(self):
        return self._answers
    
    @answers.setter
    def answers(self, answers):
        if isinstance (answers, list) and len(answers) == 4:
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
                answers BLOB,
                correct_answer TEXT,
                difficulty TEXT);
                """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        try:
            sql="""
                    INSERT INTO question VALUES (?,?,?,?);
                """
            sql_return = CURSOR.execute(sql,(self.question, self.answers,self.correct_answer, self.difficulty)).fetchone()
            self.id = sql_return.lastrowid
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
    
    
    # def display_question(self):
    #     #displays question and its answer
    #     print(self.question)
    #     print("A." + self.answer1)
    #     print("B." + self.answer2)
    #     print("C." + self.answer3)
    #     print("D." + self.answer4)
        
    # def check_answer(self, user_answer):
    #     #check is the user's answer is correct and return the result
    #     if user_answer.lower() == self.correct_answer.lower():
    #         return True
    #     else:
    #         print("Sorry, that is not the correct answer.")
    #         return False # but needs more functionality // might be handled in Game class?
        
    
    
    