from langchain_core.prompts import ChatPromptTemplate

# Main prompt
MAIN_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "human",
            """
    {instruction}
    
    <document> 
    {PAGE_CONTENT} 
    </document> 
  
    <chunk> 
    {CHUNK_CONTENT} 
    </chunk> 
    """,
        ),
    ]
)

# Initial instruction
INITIAL_INSTRUCTION = """
<document/> is the chunk we want to situate within the whole document. 
<chunk/> is the chunk we are situating. 

Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else. 
"""

# Sample test cases must include all the variables that are in the prompt
SAMPLE_TEST_CASES = [
    {
        "name": "Basic context",
        "PAGE_CONTENT": "The solar system consists of the Sun and the celestial objects bound to it by gravity. This includes the eight planets, their moons, and numerous smaller objects such as dwarf planets, asteroids, and comets.",
        "CHUNK_CONTENT": "The eight planets in order from the Sun are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.",
        "expected": ["planets", "solar system", "order"],
        "unexpected": ["moons", "dwarf planets", "asteroids"],
    },
    {
        "name": "Partial overlap",
        "PAGE_CONTENT": "Machine learning is a subset of artificial intelligence that focuses on the development of algorithms and statistical models that enable computer systems to improve their performance on a specific task through experience.",
        "CHUNK_CONTENT": "Supervised learning is a type of machine learning where the algorithm learns from labeled training data, attempting to minimize the error between its predictions and the true labels.",
        "expected": ["machine learning", "algorithm", "type"],
        "unexpected": ["artificial intelligence", "computer systems", "performance"],
    },
    {
        "name": "Implicit context",
        "PAGE_CONTENT": "The human body is a complex system of organs, tissues, and cells working together to maintain life. The circulatory system pumps blood throughout the body, delivering oxygen and nutrients to cells.",
        "CHUNK_CONTENT": "The heart is a muscular organ about the size of a fist, located just behind and slightly left of the breastbone.",
        "expected": ["circulatory system", "organ", "body"],
        "unexpected": ["blood", "oxygen", "nutrients"],
    },
    {
        "name": "Contrasting information",
        "PAGE_CONTENT": "Climate change refers to long-term shifts in global weather patterns and average temperatures. While natural factors can influence climate, human activities, particularly the emission of greenhouse gases, are the primary drivers of current climate change.",
        "CHUNK_CONTENT": "Some skeptics argue that climate change is solely caused by natural cycles and variations in the Earth's orbit and solar activity.",
        "expected": ["climate change", "skeptics", "natural factors"],
        "unexpected": ["greenhouse gases", "human activities", "long-term shifts"],
    },
    {
        "name": "Technical detail",
        "PAGE_CONTENT": "Quantum computing leverages the principles of quantum mechanics to perform complex calculations. Unlike classical bits, quantum bits or qubits can exist in multiple states simultaneously, a property known as superposition.",
        "CHUNK_CONTENT": "Quantum entanglement is a phenomenon where two or more qubits become correlated in such a way that the quantum state of each qubit cannot be described independently of the others.",
        "expected": ["quantum computing", "qubits", "phenomenon"],
        "unexpected": ["classical bits", "superposition", "complex calculations"],
    },
]

# Instruction improvement prompt
INSTRUCTION_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant tasked with improving instructions based on test case results. Your goal is to enhance the instruction's ability to generate concise, relevant contextual information for document chunks.",
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

Provide a revised version of the instruction that aims to improve performance on the test cases. Consider the following aspects:
1. Clarity: Ensure the instruction is clear and unambiguous.
2. Specificity: Add guidelines for handling different types of content (e.g., technical, narrative, contrasting information).
3. Relevance: Emphasize the importance of identifying key concepts that situate the chunk within the larger document.
4. Conciseness: Stress the need for brevity in the generated context.
5. Adaptability: Include guidance on how to handle implicit or inferred relationships between the chunk and the document.
Please keep the instruction concise and to the point and keep it about the same size as the original instruction.
Output the improved instruction text only, without any additional explanation. Maintain the overall structure and purpose of the original instruction while incorporating these enhancements.
        """,
        ),
    ]
)

# Test case improvement prompt
TEST_CASE_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant tasked with creating a challenging test case for a contextual chunk improvement system. Your goal is to create a diverse, nuanced scenario that pushes the limits of the system's capabilities.",
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
1. A descriptive name that hints at the challenge it presents
2. PAGE_CONTENT (a paragraph of text representing the full document)
3. CHUNK_CONTENT (a smaller portion of text to be contextualized within the document)
4. Expected keywords (3-5 items) that should appear in the context
5. Unexpected keywords (3-5 items) that should not appear in the context

Focus on creating a scenario that is particularly challenging for contextual chunk improvement, such as:
- Subtle relationships between the chunk and the document that require deep understanding
- Implicit context that requires inference or domain knowledge
- Technical or domain-specific content with specialized vocabulary
- Contrasting or seemingly unrelated information that tests discrimination ability
- Ambiguous or multi-faceted contexts that could be interpreted in multiple ways
- Edge cases that test the boundaries of the system's capabilities

Output the new test case in the following format:
{{
    "name": "Test case name - Brief description of challenge",
    "PAGE_CONTENT": "Full document content (1-3 sentences)",
    "CHUNK_CONTENT": "Chunk to be contextualized (1 sentence)",
    "expected": ["expected1", "expected2", "expected3", "expected4", "expected5"],
    "unexpected": ["unexpected1", "unexpected2", "unexpected3", "unexpected4", "unexpected5"]
}}

Ensure that all keys are present in the test case and that the format is strictly followed.
            """,
        ),
    ]
)
