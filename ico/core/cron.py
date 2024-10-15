from models import Worker
import os

def my_scheduled_job():
    os.remove("/Users/lzembruzki/Downloads/openintel-open-tld-20220101.tar")
    print("cron job is running")
    worker_obj = Worker.objects.all()
    #Update all workers to is_alive = False
    worker_obj.update(is_alive=False)
  
  