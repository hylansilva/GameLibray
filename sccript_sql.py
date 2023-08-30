import mysql.connector
from mysql.connector import errorcode

print('Conecting...')
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('User or password not like')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("USE `jogoteca`;")

# # Adicionando coluna url_image à tabela games
# alter_table_sql = '''
#     ALTER TABLE `games`
#     ADD COLUMN `url_image` varchar(200) DEFAULT NULL
# '''
#
# try:
#     cursor.execute(alter_table_sql)
#     print('Coluna url_image adicionada com sucesso.')
# except mysql.connector.Error as err:
#     print('Erro ao adicionar coluna:', err)
#
# # commitando se não nada tem efeito
# conn.commit()


cursor.execute('select * from jogoteca.games')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])


cursor.close()
conn.close()