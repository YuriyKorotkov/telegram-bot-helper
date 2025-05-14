from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from database import add_user, update_user_activity  # убедись, что путь верный

class UserTrackerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user = event.from_user
        if user:
            await add_user(user.id, user.username or "")
            await update_user_activity(user.id)
        return await handler(event, data)
