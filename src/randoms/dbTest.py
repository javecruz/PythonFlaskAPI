import pymysql.cursors

# Abro conexion bbdd
db = pymysql.connect(host='localhost',
                    user='root',
                    password='root',
                    db='empresa',
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor)

#necesito un cursos para hacer queries
cursor = db.cursor()

#pruebo una query
cursor.execute("Select * from cliente")

#cojo el data
data = cursor.fetchall()

print(data)

db.close()

