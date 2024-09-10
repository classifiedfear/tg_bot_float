from aiogram.fsm.state import StatesGroup, State


class DeleteSubscriptionStates(StatesGroup):
    CHOOSE_SUBSCRIPTION = State()
