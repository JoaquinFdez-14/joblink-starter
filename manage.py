#!/usr/bin/env python3
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django no está instalado. Instálalo con `pip install django`."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
