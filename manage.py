#!/usr/bin/env python3
import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    if os.environ.get("DJANGO") == "DEV":
        print("== DEV ENVIRONMENT ==")
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FireGolem.settings")
    else:
        print("== PROD ENVIRONMENT =")
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FireGolem.settings_prod")
    execute_from_command_line(sys.argv)
