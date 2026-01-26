import random
from prompts import create_advice_prompt, create_balance_prompt, create_linear_prompt

options = {
    "linear": {
        "cards_count": 3,
        "prompt_func": create_linear_prompt
    },
    "balance": {
        "cards_count": 4,
        "prompt_func": create_balance_prompt
    },
    "advice": {
        "cards_count": 2,
        "prompt_func": create_advice_prompt
    },
}

class TarotModel:

    def __init__(self, option: str, query: str, data: dict = None):
        if option not in options:
            raise ValueError(f"Invalid option: {option}. Must be one of {list(options.keys())}")
        self.option = option

        self.cards = random.sample(data["cards"], options[option]["cards_count"])
        for card in self.cards:
            card["reversed"] = random.random() < 0.2
        self.query = query
        self.prompt = options[option]["prompt_func"](self.query, self.cards)



