import django
from DJANGO_PROJECT import celery_app
from DJANGO_PROJECT.celery import app
from .fetcher import Fetcher
from .models import Page
from .task_pool import ActiveTasks
from celery import shared_task

@shared_task
def run():

    tasks = ActiveTasks().get_tasks()
    print("task in run is:" , tasks)
    for task in tasks:
        if task[1] is None:
            task[0].delay()
        else:
            print("before delaying it the task is ," , task)
            task[0].delay(task[1])




