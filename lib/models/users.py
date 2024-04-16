import sqlite3

CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

class Users:
    def __init__(self,name,high_score = 0,id="none"):
        self.id = id
        self.name = name
        self.high_score = high_score

    @property
    def name(self):
        return self._name
    
    #validate name 
    @name.setter
    def name(self,name):
        if not (isinstance(name,str)):
            raise TypeError("name must be a string")
        else:
            self._name = name.upper()

    def __repr__(self):
        return(f'<id:{self.id} Owner:"{self.name}" hs:{self.high_score} />')
    
    @classmethod
    def create_table(cls):
        sql="""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                high_score INTEGER
            );
            """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        try:
            sql= """
                INSERT INTO Users (name,high_score) VALUES (?,?);
                """
            CURSOR.execute(sql,(self.name,self.high_score))
            # set ID
            self.id = CURSOR.lastrowid
            CONN.commit()
        except Exception as err:
            print(f'Save went wrong,{err}')

    @classmethod
    def create_row(cls,name):
        user = cls(name)
        user.save()
        return user
    
    #deletes row with and id
    @classmethod
    def delete_row(cls,id):
        try:
            sql = """ 
                DELETE FROM users WHERE id = ?;
            """
            CONN.execute(sql, (id,))
            CONN.commit()
            print("success")
        except Exception as err:
            print(f'error:{err}')

    
    def update(self):
        try:
            sql="""
                    UPDATE users SET name = ?, high_score = ?, where id = ? ;
                """
            CURSOR.execute(sql,(self.name, self.high_score,self.id))
            CONN.commit()
            print(f"successfully saved ${self.name}")
        except Exception as err:
            print (f"Error Updating ${self.name}: ${err}" )


    #Create Instance from row where row is a sequence
    @classmethod
    def create_instance(cls,row):
        user = cls(
            id = row[0],
            name = row [1],
            high_score = row[2]
        )
        return user

    @classmethod 
    def find_by_id(cls, id):
        sql = """
                SELECT * FROM users WHERE id=?;
            """
        row = CURSOR.execute(sql,(id,)).fetchone()
        if not row: 
            return None 
        else: 
            return cls.create_instance(row)
    
    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS users;"""
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod 
    def find_or_create_by(cls, name=None, high_score=0):
        select_sql = """ 
            SELECT * FROM users WHERE 
            name = ?;
        """
        row = CURSOR.execute(select_sql, (name,)).fetchone()
        if not row: 
            insert_sql = """ INSERT INTO users (name, high_score) VALUES (?, ?);"""
            CURSOR.execute(insert_sql, (name, high_score))
            CONN.commit()
            return cls.find_by_id(CURSOR.lastrowid)
        else:
            return cls.create_instance(row)
        
    
        
    #TODO Aggregate method to get highest score of all games by user 
    
    #Aggregate See all high scores , show users with the score 
    
        
    @classmethod
    def get_user_high_score(cls, user_id):
        sql = """
            SELECT MAX(final_score) FROM games WHERE user_id = ?;
        """
        high_score = CURSOR.execute(sql, (user_id,)).fetchone()[0]
        return high_score if high_score else 0
        
    @classmethod    
    def get_all_high_scores(cls):
        sql = """
            SELECT u.id, u.name, MAX(g.final_score) as high_score
            FROM games g
            JOIN users u ON g.user_id = u.id
            GROUP BY g.user_id
        """
        high_scores = CURSOR.execute(sql).fetchall()
        return high_scores