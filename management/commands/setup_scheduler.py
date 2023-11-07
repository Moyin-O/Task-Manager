 # tasks/management/commands/setup_scheduler.py
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from tasks.tasks import check_deadlines

class Command(BaseCommand):
  help = 'Sets up the APScheduler'

  def handle(self, *args, **options):
      scheduler = BackgroundScheduler()
      scheduler.add_job(check_deadlines, 'interval', hours=1)
      scheduler.start()

