'''
Lab 4: Rock-Paper-Scissor AI Agent

In this lab you will build one AI agent for the game of Rock-Paper-Scissors, that can defeat a few different kinds of 
computer players.

You will update the AI agent class to create your first AI agent for this course.
Use the precept sequence to find out which opponent agent you are facing, 
so that it can beat these three opponent agents:

    Agent Single:  this agent picks a weapon at random at the start, 
                   and always plays that weapon.  
                   For example: 2,2,2,2,2,2,2,.....

    Agent Switch:  this agent picks a weapon at random at the start,
                   and randomly picks a weapon once every 10 rounds.  
                   For example:  2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,...

    Agent Mimic:  this agent picks a weapon at random in the first round, 
                  and then always does what you did the previous round.  
                  For example:  if you played 1,2,0,1,2,0,1,2,0,...  
                   then this agent would play 0,1,2,0,1,2,0,1,2,...

On 11th round, if all 11 had been same weapon: Most likely "Single"; low poss. "Switch"
On 2nd round, if agent played diff. wep from first round: "Mimic"

First round will be random
Second round:
    - if Agent played same wep. as you in first round
        - Guaranteed they will use the same wep. again
    - else
        - Use that weapon again (Single/Switch)
        - Play what you last played (Mimic)
Third round:
    - if Agent played same wep. as you in first round
        - Intentional counter in second:
            - if Agent played your counter in third round
                - Mimic
            - else
                - Not Mimic, keep countering until round 10
    - else
        -

Round 1: Same or different
Round 2: 
    - Same:
        - Agent plays initial again
        - We counter their initial
    - Diff:
        - Agent plays our initial OR Agent plays their initial
        - We counter their initial
Round 3:
    - Same:
        - Agent plays initial again OR Agent plays our Round 2 counter
        - We counter their initial

Discussions in lab:  You don't know ahead of time which opponent you will be facing, 
so the first few rounds will be used to figure this out.   How?

Once you've figured out the opponent, apply rules against that opponent. 
A model-based reflex agent uses rules (determined by its human creator) to decide which action to take.

If your AI is totally random, you should be expected to win about 33% of the time, so here is the requirement:  
In 100 rounds, you should consistently win at least 85 rounds to be considered a winner.

You get a 0 point for beating the single agent, 1 points for beating the switch agent, 
and 4 points for beating the mimic agent.

'''

from rock_paper_scissor import Player
from rock_paper_scissor import run_game
from rock_paper_scissor import random_weapon_select
from collections import defaultdict

class AiPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.initial_weapon = random_weapon_select()
        self.decision_array = [[0, 2, 1], [1, 0, 2], [2, 1, 0]]
        self.against = "unknown"
        self.agent_counters = defaultdict(lambda: lambda: self.opponent_choices[-1], {
            "mimic": lambda: self.action
        })
        self.strategy = defaultdict(lambda: self.counter_agent, {
            0: lambda: self.initial_weapon,
            1: self.test_agent,
            2: self.test_agent,
            3: self.determine_and_counter_agent
        })

    def counter_weapon(self, wep_to_counter):
        return self.decision_array[wep_to_counter].index(2)

    def test_agent(self):
        return self.counter_weapon(self.opponent_choices[0])

    def counter_agent(self):
        return self.counter_weapon(self.agent_counters[self.against]())

    def determine_and_counter_agent(self):
        if self.action == self.opponent_choices[2]:
            self.against = "mimic"
        return self.counter_agent()

    def weapon_selecting_strategy(self):
        return self.strategy[len(self.opponent_choices)]()

if __name__ == '__main__':
    final_tally = [0]*3
    for agent in range(3):
        for i in range(100):
            tally = [score for _, score in run_game(AiPlayer("AI"), 100, agent)]
            if sum(tally) == 0:
                final_tally[agent] = 0
            else:
                final_tally[agent] += tally[0]/sum(tally)

    print("Final tally: ", final_tally)  