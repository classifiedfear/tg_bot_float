from abc import ABC

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State


class StateController(ABC):
    _context: FSMContext

    def change_fsm_context(self, fsm_context: FSMContext) -> None:
        self._context = fsm_context

    async def set_state(self, state: State) -> None:
        await self._context.set_state(state)

    async def clear_states(self) -> None:
        current_state = await self._context.get_state()
        if current_state is None:
            return
        await self._context.clear()
