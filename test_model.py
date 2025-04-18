import logging
import sys
from backend.services.model_manager import model_manager

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger(__name__)

def test_code_generation():
    """Test code generation with the CodeGen model."""
    logger.info("Testing code generation...")
    
    # Set prompt
    prompt = "# Python code to calculate factorial"
    
    # Get code
    logger.info(f"Generating code for prompt: {prompt}")
    code = model_manager.generate_text(
        model_type="code_generation",
        prompt=prompt,
        temperature=0.7,
        max_length=1024,
    )
    
    # Print results
    logger.info("Generated code:")
    print("\n" + "="*40 + "\n")
    print(code)
    print("\n" + "="*40)
    
    return code

if __name__ == "__main__":
    test_code_generation() 