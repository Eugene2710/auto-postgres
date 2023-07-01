from typing import NewType

"""
Added an optional refined str type; a ResultPrompt

It represents a ResultPrompt meant to be passed to openai, 

to interpret the SQL results with reference to the original operation professional's instructions
"""
ResultPrompt = NewType("ResultPrompt", str)

class ResultPromptFormatter:
    """
    Responsible for formatting the
    - instructions from the operations professional
    - results from the SQL query

    to be sent to openai, so openai interpretes the results for us
    """
    @staticmethod
    def format(instructions: str, results: str) -> ResultPrompt:
        return ResultPrompt(f"""
Instruction from user: "{instructions}"

Query to PostgreSQL:

SELECT COALESCE(SUM(usage_duration), INTERVAL '0 minutes') AS total_usage_duration
FROM usage_data
JOIN user_data ON usage_data.user_id = user_data.user_id
WHERE user_data.name = 'John' AND usage_data.usage_date >= CURRENT_DATE - INTERVAL '30 days';

Results from the Query:
{results}

Please format the results of the query, to answer the user's instruction.
""")