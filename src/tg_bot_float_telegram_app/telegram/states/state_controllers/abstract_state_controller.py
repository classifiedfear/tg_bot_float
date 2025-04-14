from abc import ABC

from aiogram.fsm.context import FSMContext


class AbstractStateController(ABC):
    def __init__(self) -> None:
        self._context = None

    def set_fsm_context(self, context: FSMContext) -> None:
        self._context = context

    async def clear_states(self) -> None:
        """
        Clears the current state if it is set.

        Raises:
            ValueError: If the state is not set.
        """
        if not self._context:
            raise ValueError("FSMContext state is not set")
        current_state = await self._context.get_state()
        if current_state is None:
            return
        await self._context.clear()
