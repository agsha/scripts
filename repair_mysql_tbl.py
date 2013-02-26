import MySQLdb

con = MySQLdb.connect('localhost','root','<DB PASSWORD>');
l = ['information_schema','mysql','performance_schema']
cur = con.cursor()
cur.execute("show databases")
all_db = cur.fetchall()
for i in all_db:
 db_name = i[0]
 print db_name
 if db_name in l:
  continue
 cur1 = con.cursor()
 cur1.execute("select table_name from information_schema.tables where table_schema='" + db_name +"';")
 all_tables = cur1.fetchall()
 for tbl in all_tables:
  table_name = tbl[0]
  print table_name
  cur2 = con.cursor()
  query = "repair table `%s`.`%s`" %(db_name, table_name)
  print query
  cur2.execute(query)
  print cur2.fetchall()
