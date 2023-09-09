import time
from typing import Any, Optional

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django comman to pause executauin until database is available"""

    def handle(self, *args: Any, **options):
        self.stdout.write('Waitin for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('database unavailable, waiting 1 secont...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('daatabase available!'))