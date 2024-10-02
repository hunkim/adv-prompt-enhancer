from langchain_core.prompts import ChatPromptTemplate

# Main prompt
MAIN_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "human",
            """
{instruction}
<query_history>
{query_history}
</query_history>

New query:
<new_query>
{new_query}
</new_query>
    """,
        ),
    ]
)

# Initial instruction
INITIAL_INSTRUCTION = """
You are an AI assistant tasked with improving search queries by incorporating relevant context from previous queries.
Your goal is to create a concise, focused search query that captures the intent of the new question while considering relevant past context.

Instructions:
1. Analyze the new query and the query history.
2. Identify any relevant context from the query history that directly relates to the new query.
3. If there's relevant context, incorporate it into a refined search query.
4. If there's no relevant context, focus solely on the new query.
5. Ensure the final query is concise and targeted for effective search retrieval.

Answer only with the succinct search query and nothing else.
"""

# Sample test cases must include all the variables that are in the prompt
SAMPLE_TEST_CASES = test_cases = [
    {
        "name": "Ambiguous pronoun resolution",
        "question_history": [
            "Who was the first person to walk on the moon?",
            "What was the name of his spacecraft?",
            "When did he return to Earth?",
        ],
        "new_query": "What did he say when he stepped onto the surface?",
        "expected": ["Neil Armstrong", "moon landing", "first words"],
        "unexpected": ["spacecraft", "return to Earth"],
    },
    {
        "name": "Irrelevant recent history",
        "question_history": [
            "What's the capital of Japan?",
            "What's the population of Tokyo?",
            "What's the tallest mountain in Japan?",
            "How many islands does Japan have?",
            "What's the national sport of Brazil?",
        ],
        "new_query": "When did Brazil last win the World Cup?",
        "expected": ["Brazil", "World Cup", "last win"],
        "unexpected": ["Japan", "Tokyo", "islands"],
    },
    {
        "name": "Implicit context continuation",
        "question_history": [
            "What's the largest mammal on Earth?",
            "How long can blue whales live?",
            "What do they eat?",
        ],
        "new_query": "How deep can they dive?",
        "expected": ["blue whales", "diving depth"],
        "unexpected": ["eat", "lifespan"],
    },
    {
        "name": "Context switch with similar terms",
        "question_history": [
            "What's the largest planet in our solar system?",
            "How many moons does Jupiter have?",
            "What's the Great Red Spot?",
            "How long is a day on Jupiter?",
        ],
        "new_query": "What's the largest known star in the universe?",
        "expected": ["largest star", "universe"],
        "unexpected": ["Jupiter", "planet", "solar system"],
    },
    {
        "name": "Long-term context recall",
        "question_history": [
            "Who wrote 'Pride and Prejudice'?",
            "When was it published?",
            "What's the plot of 'Sense and Sensibility'?",
            "Who played Elizabeth Bennet in the 2005 movie adaptation?",
            "What's Jane Austen's most famous quote?",
        ],
        "new_query": "Where was the author born?",
        "expected": ["Jane Austen", "birthplace"],
        "unexpected": ["Pride and Prejudice", "Elizabeth Bennet", "movie adaptation"],
    },
]

# Instruction improvement prompt
INSTRUCTION_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant tasked with improving instructions based on test case results.",
        ),
        (
            "human",
            """
Given the following instruction and test cases, suggest an improvement to the instruction that addresses at least one issue:

Current instruction:
{current_instruction}

Test cases:
{test_cases}

Current performance:
Total score: {total_score}

Provide a revised version of the instruction that aims to improve performance on the test cases. Focus on addressing specific weaknesses or adding guidelines that could lead to better results.
Please keep the instruction concise and to the point about the same size as the original instruction.
Output the improved instruction text only, without any additional explanation.
    """,
        ),
    ]
)

# Test case improvement prompt
TEST_CASE_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant tasked with creating a challenging test case for an instruction improvement system.",
        ),
        (
            "human",
            """
Given the following prompt and current test cases, create a new, more challenging test case:

Prompt:
{prompt}

Current test cases:
{test_cases}

Current score: {current_score}

Create 1 new test case that is more likely to expose weaknesses in the prompt. The test case should include:
1. A descriptive name
2. A question history (3-5 questions)
3. A new query
4. Expected keywords (2-4 items)
5. Unexpected keywords (2-4 items)

Focus on creating a scenario that is particularly challenging for contextual query improvement, such as:
- Subtle context switches
- Ambiguous pronouns across multiple questions
- Mixed relevant and irrelevant history
- Implicit context that requires careful analysis

Output the new test case in the following format:
{{
    "name": "Test case name",
    "question_history": ["Question 1", "Question 2", "Question 3"],
    "new_query": "New question",
    "expected": ["expected1", "expected2", "expected3"],
    "unexpected": ["unexpected1", "unexpected2", "unexpected3"]
}}
    """,
        ),
    ]
)
