#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import configurations

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onair.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Settings')


configurations.setup()


if __name__ == '__main__':
    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
