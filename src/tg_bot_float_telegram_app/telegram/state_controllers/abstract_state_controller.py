from abc import ABC
from typing import Any, Dict

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State


class StateController(ABC):
    _context: FSMContext

    def change_fsm_context(self, fsm_context: FSMContext) -> None:
        self._context = fsm_context

    async def set_state(self, state: State) -> None:
        await self._context.set_state(state)

    async def create_user_in_state(self, telegram_id: int) -> None:
        await self._context.update_data({str(telegram_id): {}})

    async def _get_sub_data(self, telegram_id: int) -> Dict[str, Any]:
        """
        Get the subscription data for a specific user.

        Args:
            telegram_id (int): The Telegram ID of the user.

        Returns:
            Dict[str, Any]: The subscription data for the user.
        """
        context_data = await self._context.get_data()
        return context_data.get(str(telegram_id), {})

    async def clear_states(self) -> None:
        current_state = await self._context.get_state()
        if current_state is None:
            return
        await self._context.clear()
