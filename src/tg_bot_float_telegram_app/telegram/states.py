from aiogram.fsm.state import StatesGroup, State


class AddSubscriptionStates(StatesGroup):
    CHOOSE_WEAPON = State()
    CHOOSE_SKIN = State()
    CHOOSE_QUALITY = State()
    CHOOSE_STATTRAK = State()

class DeleteSubscriptionStates(StatesGroup):
    CHOOSE_SUBSCRIPTION = State()


