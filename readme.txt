
1° la creacion del entorno virtual 
py -m venv venv

2° activacion del entorno virtual
venv/Scripts/activate

3° instalar las librerias necesarias
pip install -r requirements.txt

4° crear super usuario
py manage.py createsuperuser

5° correr el servidor
py manage.py runserver

(para los usuarios que vayan a ser staff se les asigna su rol de staff desde el admin)