#!/usr/bin/env python



"""Django's command-line utility for administrative tasks."""  # Agrega un literal a la estructura.



import os  # Importa os.



import sys  # Importa sys.











def main():  # Define la funcion `main`.



    """Run administrative tasks."""  # Agrega un literal a la estructura.



    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_wini.settings')  # Define la variable de entorno `DJANGO_SETTINGS_MODULE` si no existe.

    try:  # Inicia un bloque `try`.



        from django.core.management import execute_from_command_line  # Importa execute_from_command_line desde `django.core.management`.



    except ImportError as exc:  # Maneja una excepcion en `except`.



        raise ImportError(  # Lanza una excepcion (`raise`).



            "Couldn't import Django. Are you sure it's installed and "  # Agrega un literal a la estructura.



            "available on your PYTHONPATH environment variable? Did you "  # Agrega un literal a la estructura.



            "forget to activate a virtual environment?"  # Agrega un literal a la estructura.



        ) from exc  # Encadena la excepcion original (raise ... from ...).



    execute_from_command_line(sys.argv)  # Ejecuta `execute_from_command_line`.











if __name__ == '__main__':  # Evalua la condicion del `if`.



    main()  # Ejecuta `main`.



