"""
Lab 13: My first AI agent.
In this lab, you will create your first AI agent.
You will use the run_episode function from lab 12 to run a number of episodes
and collect the returns for each state-action pair.
Then you will use the returns to calculate the action values for each state-action pair.
Finally, you will use the action values to calculate the optimal policy.
You will then test the optimal policy to see how well it performs.
Sidebar-
If you reward every action you may end up in a situation where the agent
will always choose the action that gives the highest reward. Ironically,
this may lead to the agent losing the game.
"""
import sys
from pathlib import Path

# line taken from turn_combat.py
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab11.pygame_combat import PyGameComputerCombatPlayer
from lab11.turn_combat import CombatPlayer
from lab12.episode import run_episode

from collections import defaultdict
import random
import numpy as np


class PyGameRandomCombatPlayer(PyGameComputerCombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        self.weapon = random.randint(0, 2)
        return self.weapon


class PyGamePolicyCombatPlayer(CombatPlayer):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy

    def weapon_selecting_strategy(self):
        self.weapon = self.policy[self.current_env_state]
        return self.weapon


def run_random_episode(player, opponent):
    player.health = random.choice(range(10, 110, 10))
    opponent.health = random.choice(range(10, 110, 10))
    return run_episode(player, opponent)


def get_history_returns(history):
    total_return = sum([reward for _, _, reward in history])
    returns = {}
    for i, (state, action, reward) in enumerate(history):
        if state not in returns:
            returns[state] = {}
        returns[state][action] = total_return - sum(
            [reward for _, _, reward in history[:i]]
        )
    return returns


def run_episodes(n_episodes):
    """Run 'n_episodes' random episodes and return the action values for each state-action pair.
    Action values are calculated as the average return for each state-action pair over the 'n_episodes' episodes.
    Use the get_history_returns function to get the returns for each state-action pair in each episode.
    Collect the returns for each state-action pair in a dictionary of dictionaries where the keys are states and
        the values are dictionaries of actions and their returns.
    After all episodes have been run, calculate the average return for each state-action pair.
    Return the action values as a dictionary of dictionaries where the keys are states and
        the values are dictionaries of actions and their values.
    """

    action_values = defaultdict(lambda: defaultdict(float))
    state_action_count = defaultdict(lambda: defaultdict(float))

    random_player = PyGameRandomCombatPlayer("Random Player")
    opponent = PyGameComputerCombatPlayer("Computer")

    for _ in range(n_episodes):
        history = run_random_episode(random_player, opponent)
        history_returns = get_history_returns(history)

        for state, actions_returns in history_returns.items():
            for action, return_ in actions_returns.items():
                action_values[state][action] += float(return_)
                state_action_count[state][action] += 1.0

    for state in action_values:
        for action in action_values[state]:
            action_values[state][action] /= state_action_count[state][action]

    return action_values


def get_optimal_policy(action_values):
    optimal_policy = defaultdict(float)
    for state in action_values:
        optimal_policy[state] = max(action_values[state], key=action_values[state].get)
    return optimal_policy


def test_policy(policy):
    names = ["Legolas", "Saruman"]
    total_reward = 0
    for _ in range(100):
        player1 = PyGamePolicyCombatPlayer(names[0], policy)
        player2 = PyGameComputerCombatPlayer(names[1])
        temp = [reward for _, _, reward in run_episode(player1, player2)]
        print(temp)
        total_reward += sum([reward for _, _, reward in run_episode(player1, player2)])
        print(total_reward)
    return total_reward / 100


if __name__ == "__main__":
    action_values = run_episodes(100000)
    # print("action values", action_values)
    optimal_policy = get_optimal_policy(action_values)
    print("optimal policy", optimal_policy)
    print("test policy", test_policy(optimal_policy))
