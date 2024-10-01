from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import random

def run_tests(instruction: str, test_cases: List[Dict[str, Any]], llm: Any, main_prompt: ChatPromptTemplate) -> int:
    chain = main_prompt | llm | StrOutputParser()
    print(f"\nRunning tests with {llm.model_name}")
    total_score = 0

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nRunning test {i}: {test_case['name']}")
        
        # Prepare input variables dynamically based on the prompt's expected input
        input_variables = main_prompt.input_variables
        prompt_inputs = {
            var: test_case.get(var, "") for var in input_variables
        }
        
        # Ensure 'instruction' is always present
        prompt_inputs["instruction"] = instruction
        
        
        result = chain.invoke(prompt_inputs)
        print(f"Result: {result}")

        expected_found = sum(1 for expected in test_case["expected"] if expected.lower() in result.lower())
        unexpected_found = sum(1 for unexpected in test_case["unexpected"] if unexpected.lower() in result.lower())

        test_score = expected_found - unexpected_found
        total_score += test_score

        print(f"Expected items found: {expected_found}/{len(test_case['expected'])}")
        print(f"Unexpected items found: {unexpected_found}/{len(test_case['unexpected'])}")
        print(f"Test score: {test_score}")

    print(f"\nTotal score: {total_score}")
    return total_score

def improve_instruction(instruction: str, test_cases: List[Dict[str, Any]], llm: Any, main_prompt: ChatPromptTemplate, improvement_prompt: ChatPromptTemplate) -> str:
    initial_score = run_tests(instruction, test_cases, llm, main_prompt)
    print(f"\nInitial Results:")
    print(f"Total score: {initial_score}")

    print(f"\nImprovement attempt:")

    improvement_chain = improvement_prompt | llm | StrOutputParser()

    test_cases_str = "\n".join([f"- {case['name']}: {str(case)[:100]}..." for case in test_cases])

    improved_instruction = improvement_chain.invoke({
        "current_instruction": instruction,
        "test_cases": test_cases_str,
        "total_score": initial_score,
        "prompt_variables": ", ".join(main_prompt.input_variables)
    })

    new_score = run_tests(improved_instruction, test_cases, llm, main_prompt)
    print(f"Improved Results:")
    print(f"Total score: {new_score}")

    if new_score > initial_score:
        print(f"Improvement successful! Score increased by {new_score - initial_score}")
        return improved_instruction
    else:
        print(f"No improvement achieved. Returning original instruction.")
        return instruction

def improve_test_cases(test_cases: List[Dict[str, Any]], prompt: ChatPromptTemplate, llm: Any, test_case_improvement_prompt: ChatPromptTemplate) -> List[Dict[str, Any]]:
    print("\nImproving test cases:")
    
    # Extract the instruction from the prompt
    instruction = prompt.messages[0].prompt.template if hasattr(prompt.messages[0], 'prompt') else str(prompt.messages[0])
    
    # Create a dummy input that satisfies the prompt's input variables
    dummy_input = {var: "dummy_value" for var in prompt.input_variables}
    dummy_input['instruction'] = instruction  # Ensure 'instruction' is always present
    
    current_score = run_tests(instruction, test_cases, llm, prompt)

    improvement_chain = test_case_improvement_prompt | llm | StrOutputParser()

    new_test_case_str = improvement_chain.invoke({
        "prompt": instruction,
        "test_cases": str(test_cases),
        "current_score": current_score,
        "prompt_variables": ", ".join(prompt.input_variables)
    })

    try:
        new_test_case = eval(new_test_case_str)
    except:
        print("Error parsing new test case. Returning original test cases.")
        return test_cases

    replace_index = random.randint(0, len(test_cases) - 1)
    new_test_cases = test_cases.copy()
    new_test_cases[replace_index] = new_test_case

    new_score = run_tests(instruction, new_test_cases, llm, prompt)

    if new_score < current_score:
        print(f"Improvement successful! Score decreased from {current_score} to {new_score}")
        print(f"Replaced test case at index {replace_index}")
        return new_test_cases
    else:
        print(f"No improvement achieved. Keeping original test cases")
        return test_cases

def adversarial_improvement(
    llm: Any,
    main_prompt: ChatPromptTemplate,
    instruction: str,
    test_cases: List[Dict[str, Any]],
    instruction_improvement_prompt: ChatPromptTemplate,
    test_case_improvement_prompt: ChatPromptTemplate,
    max_iterations: int = 100,
    log_file_path: str = "adversarial_improvement_log.txt"
) -> tuple[str, List[Dict[str, Any]]]:
    improved_instruction = instruction
    improved_test_cases = test_cases

    with open(log_file_path, "w") as log_file:
        for i in range(max_iterations):
            print(f"Iteration {i+1}/{max_iterations}")
            log_file.write(f"\n--- Iteration {i+1} ---\n")

            print("Improving instruction...")
            try:
                new_instruction = improve_instruction(
                    improved_instruction, improved_test_cases, llm, main_prompt, instruction_improvement_prompt
                )
                if new_instruction != improved_instruction:
                    log_file.write(f"Improved instruction:\n{new_instruction}\n\n")
                    improved_instruction = new_instruction
                else:
                    log_file.write("No change in instruction.\n\n")
            except Exception as e:
                print(f"Error improving instruction: {e}")
                log_file.write(f"Error improving instruction: {e}\n\n")

            print("Improving test cases...")
            try:
                new_test_cases = improve_test_cases(
                    improved_test_cases, main_prompt, llm, test_case_improvement_prompt
                )
                if new_test_cases != improved_test_cases:
                    log_file.write(f"Improved test cases:\n{new_test_cases}\n")
                    improved_test_cases = new_test_cases
                else:
                    log_file.write("No change in test cases.\n")
            except Exception as e:
                print(f"Error improving test cases: {e}")
                log_file.write(f"Error improving test cases: {e}\n")

            log_file.flush()

    print(f"Improvement process completed. Results saved in '{log_file_path}'")
    return improved_instruction, improved_test_cases