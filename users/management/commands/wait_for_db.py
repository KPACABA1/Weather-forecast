import time
import os
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Ожидаем PostgreSQL (макс. 30 сек)...")
        for i in range(30):
            try:
                conn = connections['default']
                conn.cursor().execute("SELECT 1")
                self.stdout.write("✅ PostgreSQL доступен!")
                return
            except OperationalError:
                self.stdout.write(f"⌛ Попытка {i+1}/30... (host: {os.getenv('DB_HOST')})")
                time.sleep(1)
        self.stdout.write("❌ Не удалось подключиться к PostgreSQL!")
        exit(1)