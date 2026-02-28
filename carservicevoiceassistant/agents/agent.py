from livekit.agents import Agent
from carservicevoiceassistant.prompts import INSTRUCTIONS


class CarServiceAssistant(Agent):
    def __init__(self):
        super().__init__(instructions=INSTRUCTIONS)
