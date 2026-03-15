#!/usr/bin/env python
"""
Скрипт для создания дампа базы данных с человекочитаемым именем файла.

Использование:
    python manage_dump.py
    python manage_dump.py --filename my_backup

Аргументы:
    --filename: Имя файла дампа (без расширения .tar.gz)
                Если не указано, используется формат dump_15-03-2026_12-30-857
"""
import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command


def main():
    parser = argparse.ArgumentParser(
        description='Создание дампа базы данных с человекочитаемым именем.'
    )
    parser.add_argument(
        '--filename',
        type=str,
        default=None,
        help='Имя файла дампа (без расширения .tar.gz)'
    )
    args = parser.parse_args()

    timestamp = datetime.now().strftime(
        '%d-%m-%Y_%H-%M-%f'
    )[:-3]

    if args.filename:
        filename = f'{args.filename}.tar.gz'
    else:
        filename = f'dump_{timestamp}.tar.gz'

    dump_path = Path(settings.DISKETTE_DUMP_PATH)
    temp_filename = f'dump_{timestamp}_temp.tar.gz'

    original_filename = settings.DISKETTE_DUMP_FILENAME
    settings.DISKETTE_DUMP_FILENAME = temp_filename

    print(f'Creating dump: {filename}')
    call_command('diskette_dump')

    settings.DISKETTE_DUMP_FILENAME = original_filename

    temp_path = dump_path / temp_filename

    if temp_path.exists():
        new_path = dump_path / filename

        if new_path.exists():
            print(f'Error: file {filename} already exists')
            temp_path.unlink()
            sys.exit(1)

        shutil.move(str(temp_path), str(new_path))
        print(f'Dump saved: {filename}')
    else:
        print('Error: dump file not found')
        sys.exit(1)


if __name__ == '__main__':
    main()
