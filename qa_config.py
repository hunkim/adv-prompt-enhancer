from langchain_core.prompts import ChatPromptTemplate

# Main prompt
MAIN_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("human", """{instruction}
Context:
----------------
{context}
----------------
Question: {input}
----------------
Helpful Answer:""")
    ]
)

# Initial instruction
INITIAL_INSTRUCTION = """You are a helpful AI assistant designed to provide accurate information based solely on the given context. Your primary goals are:
1. Answer questions using only the information provided in the context, key-value pairs, and knowledge graph.
2. If the provided information doesn't contain enough details to fully answer the question, clearly state what you can answer and what you cannot.
3. Never make up or infer information that is not explicitly stated in the given sources.
4. If you're unsure or the information is insufficient, admit that you don't have enough information to answer confidently.
5. Provide direct quotes from the context when applicable, using quotation marks.
6. If the question cannot be answered based on the provided information, clearly state that the information is not available in the given sources.
7. If key-value pairs are provided, use them to enhance your answer with specific facts or data points.
8. If a knowledge graph is provided, use the relationships and connections it describes to provide a more comprehensive answer.

Please answer the question below using only the information provided in the following context, key-value pairs, and knowledge graph (if available). Do not use any external knowledge or make assumptions beyond what is explicitly stated.
"""

# Sample test cases
SAMPLE_TEST_CASES = [
    {
        "name": "Basic fact retrieval",
        "context": "The Eiffel Tower, located in Paris, France, was completed in 1889. It stands 324 meters tall and was designed by engineer Gustave Eiffel.",
        "input": "When was the Eiffel Tower completed?",
        "expected": ["1889", "completed in 1889"],
        "unexpected": ["1888", "1890", "20th century"],
    },
    {
        "name": "Multiple facts and inference",
        "context": "Jupiter is the largest planet in our solar system. It has a Great Red Spot, which is a giant storm that has been raging for at least 400 years. The planet has at least 79 moons.",
        "input": "What are some interesting facts about Jupiter?",
        "expected": ["largest planet", "Great Red Spot", "79 moons"],
        "unexpected": ["rings", "life", "Earth-like"],
    },
    {
        "name": "Insufficient information",
        "context": "The human brain contains approximately 86 billion neurons. Neurons communicate with each other through electrical and chemical signals.",
        "input": "How does the number of neurons in the human brain compare to other animals?",
        "expected": ["insufficient information", "can't compare", "only human brain information provided"],
        "unexpected": ["more than", "less than", "similar to"],
    },
    {
        "name": "Key-value pair usage",
        "context": "The novel '1984' was written by George Orwell.",
        "input": "Who wrote '1984' and when was it published?",
        "key_value_pairs": {"Publication Year": "1949"},
        "expected": ["George Orwell", "1949"],
        "unexpected": ["Aldous Huxley", "1948", "1950"],
    },
    {
        "name": "Knowledge graph integration",
        "context": "Photosynthesis is a process used by plants to convert light energy into chemical energy.",
        "input": "What are the main components involved in photosynthesis?",
        "knowledge_graph": {
            "Photosynthesis": ["requires", "produces"],
            "requires": ["Light", "Water", "Carbon Dioxide"],
            "produces": ["Glucose", "Oxygen"]
        },
        "expected": ["Light", "Water", "Carbon Dioxide", "Glucose", "Oxygen"],
        "unexpected": ["Nitrogen", "Chlorophyll", "Roots"],
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

Provide a revised version of the instruction that aims to improve performance on the test cases. Focus on addressing specific weaknesses or adding guidelines that could lead to better results. Consider the following aspects:
1. Accuracy: Emphasize the importance of providing correct information based solely on the given context.
2. Completeness: Encourage comprehensive answers that address all aspects of the question when possible.
3. Clarity: Stress the need for clear communication, especially when information is insufficient or unavailable.
4. Source attribution: Reinforce the importance of citing the context or provided sources.
5. Handling of key-value pairs and knowledge graphs: Provide clearer guidance on integrating this information into answers.

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
            "You are an AI assistant tasked with creating a challenging test case for a question-answering system.",
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
2. A context paragraph (2-4 sentences)
3. An input question
4. Expected keywords (3-5 items)
5. Unexpected keywords (3-5 items)
6. (Optional) Key-value pairs or a simple knowledge graph

Focus on creating a scenario that is particularly challenging for question-answering, such as:
- Questions requiring careful interpretation of the context
- Scenarios with potential for misinterpretation or over-inference
- Complex relationships between facts in the context
- Situations where the system must admit to insufficient information
- Integration of key-value pairs or knowledge graph information

Output the new test case in the following format:
{{
    "name": "Test case name",
    "context": "Context paragraph",
    "input": "Input question",
    "expected": ["expected1", "expected2", "expected3", "expected4", "expected5"],
    "unexpected": ["unexpected1", "unexpected2", "unexpected3", "unexpected4", "unexpected5"],
    "key_value_pairs": {{"key1": "value1", "key2": "value2"}} # Optional
    "knowledge_graph": {{"node1": ["relation1", "relation2"], "relation1": ["node2", "node3"]}} # Optional
}}
    """,
        ),
    ]
)