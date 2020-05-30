from typing import Tuple, Optional, Mapping, List
from numpy import exp
from numpy.random import binomial
import matplotlib.pyplot as plt

level_param: int = 100
pull_param: float = 0.7  # pull_param should be in the interval [0., 1.]

handy_map: Mapping[Optional[bool], int] = {
    True: -1,
    False: 1,
    None: 0
}


def model1_up_prob(state: Tuple[int]) -> float:
    return 1. / (1 + exp(state[0] - level_param))


def model2_up_prob(state: Tuple[int, Optional[bool]]) -> float:
    return 0.5 * (1 + pull_param * handy_map[state[1]])


def model3_up_prob(state: Tuple[int, int, int]) -> float:
    return state[2] / (state[1] + state[2]) if (state[1] + state[2]) else 0.5


def model1_sample_next_state(state: Tuple[int]) -> Tuple[int]:
    up_move: int = binomial(1, model1_up_prob(state), 1)[0]
    return state[0] + up_move * 2 - 1,


def model2_sample_next_state(state: Tuple[int, Optional[bool]]) -> Tuple[int, bool]:
    up_move: int = binomial(1, model2_up_prob(state), 1)[0]
    return state[0] + up_move * 2 - 1, bool(up_move)


def model3_sample_next_state(state: Tuple[int, int, int]) -> Tuple[int, int, int]:
    up_move: int = binomial(1, model3_up_prob(state), 1)[0]
    return state[0] + up_move * 2 - 1, state[1] + up_move, state[2] + 1 - up_move


if __name__ == '__main__':
    start_price: int = 100
    steps = 100

    model1_states: List[Tuple[int]] = [(start_price,)]
    model2_states: List[Tuple[int, Optional[bool]]] = [(start_price, None)]
    model3_states: List[Tuple[int, int, int]] = [(start_price, 0, 0)]

    for _ in range(steps):
        model1_states.append(model1_sample_next_state(model1_states[-1]))
        model2_states.append(model2_sample_next_state(model2_states[-1]))
        model3_states.append(model3_sample_next_state(model3_states[-1]))

    x_vals = range(steps + 1)
    model1_y_vals = [x[0] for x in model1_states]
    model2_y_vals = [x[0] for x in model2_states]
    model3_y_vals = [x[0] for x in model3_states]
    y_min = min(min(model1_y_vals), min(model2_y_vals), min(model3_y_vals))
    y_max = max(max(model1_y_vals), max(model2_y_vals), max(model3_y_vals))
    plt.figure(figsize=(12, 8))
    plt.plot(x_vals, model1_y_vals, "r", label="Based on current price")
    plt.plot(x_vals, model2_y_vals, "b", label="Based on previous move")
    plt.plot(x_vals, model3_y_vals, "g", label="Based on entire history")
    plt.xlabel("Time Steps", fontsize=20)
    plt.ylabel("Stock Price", fontsize=20)
    plt.title("Simulation for 3 Models", fontsize=25)
    plt.axis((0, steps, y_min, y_max))
    plt.grid(True)
    plt.legend(fontsize=15)
    plt.show()