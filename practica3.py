from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
import mysql.connector as mysql

conexion=mysql.connect(host='localhost',user='root',passwd='',db='datos')
operacion=conexion.cursor()
try:
    operacion.execute("drop table webp;")
except Exception:
    pass
try:
    operacion.execute("create table webp(pagina VARCHAR(255),estatus int)")
except Exception:
    pass
pag_inicial=input('INGRESE URL:  ')
try:
    operacion.execute("insert into webp values('"+pag_inicial+"',0);")
except mysql.errors.IntegrityError:
    sys.exit()
except mysql.errors.DataError:
    sys.exit()
conexion.commit()
conexion.close()

while(1):
    e=""
    i=0
    conexion=mysql.connect(host='localhost',user='root',passwd='',db='datos')
    operacion=conexion.cursor()
    operacion.execute("SELECT * FROM webp;")
    for pagina,estatus in operacion.fetchall():
        print(pagina+" "+str(estatus))
        if(estatus==0):
            try:
                url=urlopen(pagina)
            except urllib.error.HTTPError:
                continue
            except UnicodeEncodeError:
                continue
            bs=BeautifulSoup(url.read(),'html.parser',from_encoding="iso-8859-1")
            for enlaces in bs.find_all("a"):
                s=enlaces.get("href")
                try:
                    if(s[0:4]=="http"):
                        try:
                            operacion.execute("insert into webp values('"+s+"',0);")
                            print(s)
                        except mysql.errors.IntegrityError:
                            pass
                        except mysql.errors.DataError:
                            pass
                    else:
                        try:
                            operacion.execute("insert into webp values('"+pagina+s+"',0);")
                            print(pagina+s)
                        except mysql.errors.IntegrityError:
                            pass
                        except mysql.errors.DataError:
                            pass
                except TypeError:
                    pass
            i=1
            operacion.execute("update webp set estatus=1 where pagina='"+pagina+"';")
            
            conexion.commit()
        
    conexion.close()
    if(i==0):
        sys.exit()
