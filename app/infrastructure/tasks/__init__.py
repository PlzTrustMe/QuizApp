from datetime import UTC, datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from dishka import AsyncContainer

from app.infrastructure.tasks.check_available_quiz import (
    check_available_quiz_task,
)


def setup_tasks(
    scheduler: AsyncIOScheduler, container: AsyncContainer
) -> None:
    scheduler.add_job(
        check_available_quiz_task,
        trigger=CronTrigger(hour=0, minute=0, timezone=UTC),
        args=(container,),
    )
