from openai import OpenAI
client = OpenAI()
import json
import os
from pydantic_ai import RunContext
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings

class BaseAgent:
    def __init__(self, system_prompt: str, name: str, result_type, tools: dict):
        """
        tools: a mapping of tool names to actual function implementations.
        """
        self.system_prompt = system_prompt
        self.tools = tools
        # Create an agent instance using pydantic_ai
        from agent_factory import get_text_model_instance  # import our model factory
        self.agent = Agent(
            model=get_text_model_instance(),
            system_prompt=system_prompt,
            name=name,
            result_type=result_type,
            retries=2,
            model_settings=ModelSettings(temperature=0.2)
        )

    def generate_plan(self, user_input: str) -> str:
        prompt = f"{self.system_prompt}\nUser Input: {user_input}\nPlan:"
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=200)
        plan = response.choices[0].message.content
        return plan

    def critique_result(self, plan: str, result: str) -> bool:
        critique_prompt = (
            f"Plan: {plan}\nResult: {result}\nCritique: Is the result acceptable? Answer 'Yes' or 'No' with a brief explanation."
        )
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Critique Agent evaluating the execution of a plan."},
            {"role": "user", "content": critique_prompt}
        ],
        max_tokens=50)
        critique = response.choices[0].message.content
        return "Yes" in critique

    async def execute(self, input_data: dict, context_extra: str = ""):
        # Use the system prompt as a plain string
        context = RunContext(
            deps={}, 
            model=self.agent.model, 
            usage={}, 
            prompt=self.agent.system_prompt
        )
        # Convert input_data to a JSON string so it’s a plain string too
        context.input = json.dumps(input_data)
        result = await self.agent.run(context)
        return result
