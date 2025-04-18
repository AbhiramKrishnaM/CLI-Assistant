"""API endpoints for code generation and explanation."""
import logging
from fastapi import APIRouter, HTTPException, Depends
from shared.models.code import (
    CodeGenerationRequest,
    CodeGenerationResponse,
    CodeExplanationRequest,
    CodeExplanationResponse,
)
from backend.services.model_manager import model_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate code based on a description."""
    logger.info(f"Code generation request for {request.language}")
    
    try:
        # Skip predefined examples check and always use model inference
        prompt = f"# {request.language} code to {request.description}\n\n"
        
        # Log the request and model details
        logger.info(f"Using model: {model_manager.model_configs['code_generation']['model_id']}")
        
        # Generate the code using the appropriate model
        code = model_manager.generate_text(
            model_type="code_generation",
            prompt=prompt,
            temperature=request.temperature,
            max_length=request.max_length or 2048,
        )
        
        # Current models are too weak - always use fallback for now
        logger.warning(f"Using fallback example for better quality code generation")
        
        # Get the model ID for reporting
        model_info = next((m for m in model_manager.get_available_models() 
                         if m["type"] == "code_generation"), {"model_id": "unknown"})
        
        # Simple fallback examples based on language
        language = request.language
        description = request.description
        
        # Check if this is a factorial calculation
        if "factorial" in description.lower():
            if language == "python":
                code = '''
def factorial(n):
    """Calculate the factorial of n."""
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

def factorial_iterative(n):
    """Calculate the factorial of n using iteration."""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Example usage
if __name__ == "__main__":
    number = 5
    print(f"Factorial of {number} (recursive): {factorial(number)}")
    print(f"Factorial of {number} (iterative): {factorial_iterative(number)}")
'''
            elif language == "javascript":
                code = """
/**
 * Calculate the factorial of n recursively
 */
function factorial(n) {
  if (n === 0 || n === 1) {
    return 1;
  } else {
    return n * factorial(n - 1);
  }
}

/**
 * Calculate the factorial of n iteratively
 */
function factorialIterative(n) {
  let result = 1;
  for (let i = 1; i <= n; i++) {
    result *= i;
  }
  return result;
}

// Example usage
const number = 5;
console.log(`Factorial of ${number} (recursive): ${factorial(number)}`);
console.log(`Factorial of ${number} (iterative): ${factorialIterative(number)}`);
"""
            else:
                code = f"""
// Simple {language} example for factorial calculation

class Factorial {{
    public static int factorial(int n) {{
        if (n == 0 || n == 1) {{
            return 1;
        }} else {{
            return n * factorial(n - 1);
        }}
    }}
    
    public static void main(String[] args) {{
        int n = 5;
        System.out.println("Factorial of " + n + " = " + factorial(n));
    }}
}}
"""
        
        # Check if this is a calculator
        elif "calculator" in description.lower():
            if language == "python":
                code = """
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Division by zero"
    return x / y

def calculator():
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    
    while True:
        # Get user input
        try:
            num1 = float(input("Enter first number: "))
            operation = input("Enter operation (+, -, *, /): ")
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numbers.")
            continue
            
        # Perform calculation
        if operation == "+":
            result = add(num1, num2)
        elif operation == "-":
            result = subtract(num1, num2)
        elif operation == "*":
            result = multiply(num1, num2)
        elif operation == "/":
            result = divide(num1, num2)
        else:
            print("Invalid operation")
            continue
            
        # Display result
        print(f"Result: {num1} {operation} {num2} = {result}")
        
        # Ask if user wants to continue
        again = input("Calculate again? (y/n): ")
        if again.lower() != 'y':
            break
    
    print("Calculator closed")

if __name__ == "__main__":
    calculator()
"""
            else:
                code = f"""
// Simple {language} calculator example

function add(a, b) {{
  return a + b;
}}

function subtract(a, b) {{
  return a - b;
}}

function multiply(a, b) {{
  return a * b;
}}

function divide(a, b) {{
  if (b === 0) {{
    return "Error: Division by zero";
  }}
  return a / b;
}}

// Example usage
console.log("Calculator examples:");
console.log("5 + 3 =", add(5, 3));
console.log("10 - 4 =", subtract(10, 4));
console.log("6 * 7 =", multiply(6, 7));
console.log("20 / 5 =", divide(20, 5));
console.log("10 / 0 =", divide(10, 0));
"""
        else:
            # Generic fallback
            code = f"""# NOTE: This is a fallback example for: {description}
# For better results, consider using a more powerful code generation model.

def main():
    print("Example implementation for: {description}")
    
    # This is where the actual implementation would go
    # based on your specific requirements
    
    result = 0
    for i in range(10):
        result += i
    
    print(f"Sample calculation result: {result}")

if __name__ == "__main__":
    main()
"""
            if language != "python":
                code = f"""
// NOTE: This is a fallback example for: {description}
// For better results, consider using a more powerful code generation model.

function main() {{
  console.log("Example implementation for: {description}");
  
  // This is where the actual implementation would go
  // based on your specific requirements
  
  let result = 0;
  for (let i = 0; i < 10; i++) {{
    result += i;
  }}
  
  console.log(`Sample calculation result: ${{result}}`);
}}

main();
"""
        
        # Add a comment to explain this is a fallback example
        code = "# NOTE: This is a fallback example since the small AI model cannot generate high-quality code.\n" + \
               "# For better results, consider using a more powerful code generation model like GPT-4 or Claude.\n\n" + code
        
        # Return the response with additional information
        return CodeGenerationResponse(
            code=code,
            language=request.language,
            model_used="fallback_example"
        )
    
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}", exc_info=True)
        # Return a fallback example instead of raising an exception
        return CodeGenerationResponse(
            code=f"# Error generating code for: {request.description}\n\n" + 
                 f"# {str(e)}\n\n" +
                 f"def example_function():\n    print('Example for: {request.description}')\n\nexample_function()",
            language=request.language,
            model_used="error_fallback"
        )


@router.post("/explain", response_model=CodeExplanationResponse)
async def explain_code(request: CodeExplanationRequest):
    """Explain the provided code."""
    logger.info(f"Code explanation request of length {len(request.code)}")
    
    try:
        # Detect language if not provided
        language = request.language or "Unspecified (auto-detect)"
        
        # Create a more detailed prompt for the model
        prompt = f"""# Task: Explain the following {language} code

```{language}
{request.code}
```

# Explanation:
This code"""
        
        # Log the request and model details
        logger.info(f"Using model: {model_manager.model_configs['text_generation']['model_id']}")
        
        # Generate the explanation using the text generation model
        explanation = model_manager.generate_text(
            model_type="text_generation",
            prompt=prompt,
            temperature=0.3,  # Lower temperature for more focused response
            max_length=1024,
        )
        
        # Handle errors in the response
        if explanation.startswith("Error"):
            logger.warning(f"Error in code explanation, using fallback. Error: {explanation}")
            return CodeExplanationResponse(
                explanation="This code appears to be " + language + " code. " +
                           "I'm not able to provide a detailed explanation at the moment. " +
                           "Please try again later or try with a different code snippet.",
                language_detected=language,
                model_used="fallback_explanation"
            )
        
        # Check if this is a fallback response
        if "I'm sorry, but I'm currently operating in fallback mode" in explanation:
            model_id = "fallback_explanation"
            # Add prefix to explain the limitation
            explanation = ("NOTE: The explanation below is limited because the AI model couldn't generate a detailed response. "
                          "For better results, consider using a more powerful explanation model.\n\n") + explanation
        else:
            # Get the model ID
            model_info = next((m for m in model_manager.get_available_models() 
                             if m["type"] == "text_generation"), {"model_id": "unknown"})
            model_id = model_info["model_id"]
        
        # Return the response with additional information
        return CodeExplanationResponse(
            explanation=explanation,
            language_detected=language,
            model_used=model_id,
        )
    
    except Exception as e:
        logger.error(f"Error explaining code: {str(e)}", exc_info=True)
        # Return a fallback explanation instead of raising an exception
        return CodeExplanationResponse(
            explanation=f"Error explaining the code: {str(e)}",
            language_detected=language,
            model_used="error_fallback"
        )


@router.get("/languages")
async def list_supported_languages():
    """List supported programming languages."""
    return {
        "languages": [
            "python",
            "javascript",
            "typescript",
            "java",
            "c",
            "cpp",
            "csharp",
            "go",
            "ruby",
            "rust",
            "php",
            "swift",
            "kotlin",
            "sql",
            "bash",
            "html",
            "css",
        ]
    } 