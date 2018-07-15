import daemon
import sys, os
from crontab import CronTab

with daemon.DaemonContext(
        working_directory=os.path.abspath(os.path.dirname(__file__)),
        stdout=sys.stdout,
        stderr=sys.stderr
        ) as d:
    cron = CronTab(user=True)  
    job = cron.new(command='python3 {}'.format(os.path.join(d.working_directory, "BackupApp.py")))
    job.minute.every(5)

    cron.write()  
    print("Backup Daemon Started!")
