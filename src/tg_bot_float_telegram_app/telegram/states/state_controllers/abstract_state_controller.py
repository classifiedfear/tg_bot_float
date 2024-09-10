from abc import ABC

from aiogram.fsm.context import FSMContext


class AbstractStateController(ABC):
    async def clear_states(self, state: FSMContext) -> None:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.clear()
