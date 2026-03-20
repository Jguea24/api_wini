#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""  # comentario
import os  # comentario
import sys  # comentario


def main():  # comentario
    """Run administrative tasks."""  # comentario
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_wini.settings')  # comentario
    try:  # comentario
        from django.core.management import execute_from_command_line  # comentario
    except ImportError as exc:  # comentario
        raise ImportError(  # comentario
            "Couldn't import Django. Are you sure it's installed and "  # comentario
            "available on your PYTHONPATH environment variable? Did you "  # comentario
            "forget to activate a virtual environment?"  # comentario
        ) from exc  # comentario
    execute_from_command_line(sys.argv)  # comentario


if __name__ == '__main__':  # comentario
    main()  # comentario
