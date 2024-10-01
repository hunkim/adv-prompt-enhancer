import sys
import importlib
import os
from langchain_upstage import ChatUpstage
from improvements import adversarial_improvement

def load_config(config_file):
    # Remove .py extension if present
    config_name = config_file[:-3] if config_file.endswith('.py') else config_file
    
    # Import the config module dynamically
    config = importlib.import_module(config_name)
    return config

def main(config_file):
    # Load the configuration
    config = load_config(config_file)

    # results will be in results directory. Create it if it doesn't exist
    results_dir = 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Create output filename based on config filename
    output_filename = f"{results_dir}/{os.path.splitext(config_file)[0]}_results.txt"

    llm = ChatUpstage(model_name="solar-pro")

    final_instruction, final_test_cases = adversarial_improvement(
        llm,
        config.MAIN_PROMPT,
        config.INITIAL_INSTRUCTION,
        config.SAMPLE_TEST_CASES,
        config.INSTRUCTION_IMPROVEMENT_PROMPT,
        config.TEST_CASE_IMPROVEMENT_PROMPT,
        log_file_path=output_filename
    )

    #Optionally, you can also print the results to the console
    print("Final improved instruction:", final_instruction)
    print("Final improved test cases:", final_test_cases)

    print(f"Final improved instruction saved to: {output_filename}")
    print(f"Final improved test cases saved to: {output_filename}")

   
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    main(config_file)