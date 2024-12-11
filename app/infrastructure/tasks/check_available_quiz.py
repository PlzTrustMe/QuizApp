from dishka import AsyncContainer

from app.core.commands.quiz.check_available_quiz import CheckAvailableQuiz


async def check_available_quiz_task(container: AsyncContainer):
    async with container() as cnt:
        check_available_quiz_cmd = await cnt.get(CheckAvailableQuiz)

        await check_available_quiz_cmd()
