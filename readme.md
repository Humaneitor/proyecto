El proyecto se estructura con Flask, WTforms, Jinja, Sqlite y una mínimísima parte de CSS.
Las instrucciones que aparecen a continuación se deben realizar en Windows.
Para poder instalar el proyecto es necesario instalar lo que viene descrito en el documento requitements.txt
Esta operación se puede realizar con la instrucción "pip install -r requirements.txt"
Para que el proyecto funcione es necesario instalar un entorno virtual dentro de VSC con la instrucción "python -m venv venv"
Además de instalarlo hay que activarlo con la siguiente instrucción "venv\Scripts\activate".
Para asignar la variable de entorno habrá que realizar la siguiente operación "set FLASK_APP=run.py"
A continuación, será necesario crear un fichero con el nombre ".emv" donde se deberán incluir las varibles de entorno "FLASK_APP=run.py
FLASK_ENV=development"
Finalmente para arrancar el servidor web, es necesario procesar la orden en el terminal "flask run"

La base de datos se genera en Sqlite con la siguiente sentencia "
CREATE TABLE "movimientos" (
	"id"	INTEGER,
	"date"	TEXT,
	"time"	TEXT,
	"from_currency"	INTEGER,
	"from_quantity"	BLOB,
	"to_currency"	INTEGER,
	"to_quantity"	REAL,
	"precio"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
)
"

