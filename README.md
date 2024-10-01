# adv-prompt-enhancer: Supercharge Your AI Prompts Automatically!

Hey there, fellow developers! 👋 Are you ready to take your AI prompts to the next level? Say hello to adv-prompt-enhancer, your new secret weapon for creating razor-sharp, battle-tested prompts that can handle anything you throw at them!

## Listen to the sample

<audio controls>
  <source src="https://github.com/hunkim/adv-prompt-enhancer/raw/refs/heads/main/audio/podcast.wav" type="audio/wav">
  Your browser does not support the audio element.
</audio>
## What's adv-prompt-enhancer?

adv-prompt-enhancer is a powerful tool that automatically improves your AI prompts through an adversarial process. It's like having a tireless AI assistant that keeps refining your prompts and test cases until they're optimized for peak performance.

## How Does It Work?

<img width="617" alt="image" src="https://github.com/user-attachments/assets/74cd2c09-112c-4ef7-8078-5e8868c9c87b">


The magic of adv-prompt-enhancer lies in its clever adversarial approach:

1. It starts with your initial prompt and a set of test cases.
2. It alternates between improving the prompt and making the test cases more challenging.
3. This process continues for a set number of iterations, constantly pushing the boundaries of what your prompt can handle.

The result? A super-optimized prompt that's been battle-tested against increasingly difficult scenarios!

## Getting Started: The All-Important Config File

The heart of adv-prompt-enhancer is the `config.py` file. This is where you define your initial prompt, test cases, and improvement strategies. Let's break it down step by step:

### 1. Import the necessary modules

```python
from langchain_core.prompts import ChatPromptTemplate
```

### 2. Define your main prompt template

```python
MAIN_PROMPT = ChatPromptTemplate.from_messages([
    ("human", """
    {instruction}
    <document>
    {PAGE_CONTENT}
    </document>
    <chunk>
    {CHUNK_CONTENT}
    </chunk>
    """),
])
```

This template defines the structure of your prompt. Notice the placeholders in curly braces - these are crucial!

### 3. Set your initial instruction

```python
INITIAL_INSTRUCTION = """
Your initial prompt goes here. Be clear and concise!
"""
```

This is your starting point. It should clearly state what you want the AI to do.

### 4. Create sample test cases

```python
SAMPLE_TEST_CASES = [
    {
        "name": "Basic context",
        "PAGE_CONTENT": "The solar system consists of the Sun and the celestial objects bound to it by gravity. This includes the eight planets, their moons, and numerous smaller objects such as dwarf planets, asteroids, and comets.",
        "CHUNK_CONTENT": "The eight planets in order from the Sun are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.",
        "expected": ["planets", "solar system", "order"],
        "unexpected": ["moons", "dwarf planets", "asteroids"],
    },
    # Add more test cases here...
]
```

This is where the magic happens! A few key points:

- The keys in each test case (`PAGE_CONTENT`, `CHUNK_CONTENT`) must match the placeholders in your `MAIN_PROMPT`.
- `expected` lists keywords that should appear in the AI's response.
- `unexpected` lists keywords that shouldn't appear.
- Create diverse test cases to cover different scenarios your prompt might encounter.

### 5. Define improvement prompts

```python
INSTRUCTION_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant tasked with improving instructions based on test case results. Your goal is to enhance the instruction's ability to generate concise, relevant contextual information for document chunks."),
    ("human", """
    Given the following instruction and test cases, suggest an improvement to the instruction that addresses at least one issue:
    Current instruction:
    {current_instruction}
    Test cases:
    {test_cases}
    Current performance:
    Total score: {total_score}
    Provide a revised version of the instruction that aims to improve performance on the test cases. Consider the following aspects:
    Clarity: Ensure the instruction is clear and unambiguous.
    Specificity: Add guidelines for handling different types of content (e.g., technical, narrative, contrasting information).
    Relevance: Emphasize the importance of identifying key concepts that situate the chunk within the larger document.
    Conciseness: Stress the need for brevity in the generated context.
    Adaptability: Include guidance on how to handle implicit or inferred relationships between the chunk and the document.
    Output the improved instruction text only, without any additional explanation. Maintain the overall structure and purpose of the original instruction while incorporating these enhancements.
    """),
])

TEST_CASE_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant tasked with creating a challenging test case for a contextual chunk improvement system. Your goal is to create a diverse, nuanced scenario that pushes the limits of the system's capabilities."),
    ("human", """
    Given the following prompt and current test cases, create a new, more challenging test case:
    Prompt:
    {prompt}
    Current test cases:
    {test_cases}
    Current score: {current_score}
    Create 1 new test case that is more likely to expose weaknesses in the prompt. The test case should include:
    A descriptive name that hints at the challenge it presents
    PAGE_CONTENT (a paragraph of text representing the full document)
    CHUNK_CONTENT (a smaller portion of text to be contextualized within the document)
    Expected keywords (3-5 items) that should appear in the context
    Unexpected keywords (3-5 items) that should not appear in the context
    Focus on creating a scenario that is particularly challenging for contextual chunk improvement, such as:
    Subtle relationships between the chunk and the document that require deep understanding
    Implicit context that requires inference or domain knowledge
    Technical or domain-specific content with specialized vocabulary
    Contrasting or seemingly unrelated information that tests discrimination ability
    Ambiguous or multi-faceted contexts that could be interpreted in multiple ways
    Edge cases that test the boundaries of the system's capabilities
    Output the new test case in the following format:
    {{
    "name": "Test case name - Brief description of challenge",
    "PAGE_CONTENT": "Full document content (1-3 sentences)",
    "CHUNK_CONTENT": "Chunk to be contextualized (1 sentence)",
    "expected": ["expected1", "expected2", "expected3", "expected4", "expected5"],
    "unexpected": ["unexpected1", "unexpected2", "unexpected3", "unexpected4", "unexpected5"]
    }}
    Ensure that all keys are present in the test case and that the format is strictly followed.
    """),
])
```

These prompts guide the AI in improving your instruction and creating more challenging test cases.

## Running adv-prompt-enhancer

Once your `config.py` is set up, running adv-prompt-enhancer is a breeze:

1. Ensure you have all required dependencies installed.
2. Open your terminal and navigate to the adv-prompt-enhancer directory.
3. Run the following command:

```bash
python main.py your_config.py
```

Replace `your_config.py` with the name of your config file (without the .py extension).

## What to Expect

As adv-prompt-enhancer runs, you'll see a flurry of activity in your terminal:

1. It'll run through the test cases, scoring how well the current prompt performs.
2. Then it'll attempt to improve the instruction and test cases.
3. You'll see updated scores and whether improvements were successful.
4. This process will repeat for the specified number of iterations.

At the end, you'll have:
- A supercharged, optimized prompt instruction
- A set of challenging test cases that push your prompt to its limits
- A detailed log file showing the improvement process

All of this will be saved in the `results` directory for your review and use!

### Quick Example

Here's a glimpse of what you can expect from adv-prompt-enhancer. Given an initial prompt and test cases, it can generate an improved prompt like this:

```
Revise the instruction to generate a concise, relevant context for this document chunk, adhering to the following: For technical content, summarize the main idea, highlight a unique, crucial aspect, and provide a real-world application example using clear language; for narrative content, outline the main idea and a unique, impactful aspect; for contrasting information, emphasize the main idea and a unique, implication-filled aspect, clearly comparing and contrasting; for complex concepts, simplify them, their main applications, and provide a specific example, breaking down complex ideas into understandable parts; for implicit or inferred relationships, explicitly state the connection between the chunk and the document in one sentence, using clear language and specific examples. Prioritize: a) Core context: distill essential information, its importance, and the key concept that directly links it to the larger document; b) Implicit and suggested context: ensure the relationship is explicitly stated, easily understood, and directly addresses the content type's requirements, including handling implicit or inferred relationships. Generate a context that: 1. Clearly adheres to these guidelines, handling specific content types with clarity and specificity; 2. Accurately represents and is relevant to the content type, emphasizing key concepts that situate the chunk within the larger document; 3. Is concise, limited to one sentence; 4. Clearly states the relationship between the chunk and the document, handling implicit or inferred relationships, edge cases, and domain-specific jargon when necessary, ensuring adaptability to various scenarios. Specifically, when dealing with advanced technical content, ensure the context captures the essence of the complex concepts, their real-world application, and any implicit connections to the larger document, all while maintaining clarity, relevance, and conciseness. To improve performance on test cases, ensure: 1. Clarity: The instruction is clear and unambiguous; 2. Specificity: Guidelines are provided for handling different types of content; 3. Relevance: Identifying key concepts that situate the chunk within the larger document is emphasized; 4. Conciseness: The need for brevity in the generated context is stressed; 5. Adaptability: Guidance on handling implicit or inferred relationships between the chunk and the document is included.
```

This improved prompt is more detailed, specific, and adaptable to various content types and scenarios, leading to better performance on the test cases.

## Why adv-prompt-enhancer is Awesome

Here's why adv-prompt-enhancer is a game-changer:

1. **Time-saving**: It automates the tedious process of prompt refinement.
2. **Thorough**: It tests against a wide range of scenarios you might not have thought of.
3. **Continuous improvement**: The adversarial approach ensures your prompt keeps getting better.
4. **Adaptable**: You can easily customize it for different types of prompts and use cases.
5. **Insight-generating**: The improvement process can reveal nuances about your task you hadn't considered.

## Pro Tips for Getting the Most out of adv-prompt-enhancer

1. **Start broad, then narrow down**: Begin with a general instruction and let adv-prompt-enhancer help you refine it.
2. **Diverse test cases are key**: The more varied your initial test cases, the more robust your final prompt will be.
3. **Pay attention to the logs**: They can provide valuable insights into how your prompt is evolving.
4. **Iterate and experiment**: Don't be afraid to run adv-prompt-enhancer multiple times with different starting points.
5. **Fine-tune the improvement prompts**: Adjusting these can significantly impact the direction of improvements.

## Wrapping Up

adv-prompt-enhancer is more than just a tool - it's your partner in crafting AI prompts that are truly exceptional. By automating the improvement process, it frees you up to focus on the creative aspects of your AI projects.

So, what are you waiting for? Give adv-prompt-enhancer a spin and watch your prompts evolve before your eyes! Happy enhancing, and may your AI assistants be ever more clever! 🚀🤖

## Contributing

We welcome contributions! If you have ideas for improvements or find any issues, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.