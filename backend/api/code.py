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

# Predefined examples for common code tasks
PREDEFINED_EXAMPLES = {
    "python": {
        "fibonacci": '''
def fibonacci(n):
    """Calculate the Fibonacci sequence up to n terms."""
    fib_sequence = [0, 1]
    
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return fib_sequence
    
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    
    return fib_sequence

# Example usage
if __name__ == "__main__":
    n = 10
    result = fibonacci(n)
    print(f"Fibonacci sequence up to {n} terms: {result}")
''',
        "factorial": '''
def factorial(n):
    """Calculate the factorial of a non-negative integer n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result

# Alternate recursive implementation
def factorial_recursive(n):
    """Calculate factorial recursively."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)

# Example usage
if __name__ == "__main__":
    number = 5
    print(f"Factorial of {number} is {factorial(number)}")
    print(f"Factorial of {number} (recursive) is {factorial_recursive(number)}")
''',
        "sort": '''
def bubble_sort(arr):
    """Sort an array using bubble sort algorithm."""
    n = len(arr)
    for i in range(n):
        # Flag to optimize if no swaps occur
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
                
        # If no swapping occurred in this pass, array is sorted
        if not swapped:
            break
    
    return arr

def quick_sort(arr):
    """Sort an array using quick sort algorithm."""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# Using Python's built-in sort
def python_sort(arr):
    """Sort an array using Python's built-in sort."""
    # Create a copy to avoid modifying the original
    sorted_arr = arr.copy()
    sorted_arr.sort()
    return sorted_arr

# Example usage
if __name__ == "__main__":
    # Sample array
    numbers = [64, 34, 25, 12, 22, 11, 90]
    
    # Bubble sort (modifies the original)
    bubble_sorted = bubble_sort(numbers.copy())
    print(f"Bubble sort: {bubble_sorted}")
    
    # Quick sort (returns a new sorted array)
    quick_sorted = quick_sort(numbers)
    print(f"Quick sort: {quick_sorted}")
    
    # Python's built-in sort
    python_sorted = python_sort(numbers)
    print(f"Python sort: {python_sorted}")
    
    # One-liner using sorted() function (returns a new sorted array)
    print(f"Using sorted(): {sorted(numbers)}")
'''
    }
}


@router.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate code based on a description."""
    logger.info(f"Code generation request for {request.language}")
    
    try:
        description_lower = request.description.lower()
        
        # Check for predefined examples first
        if request.language in PREDEFINED_EXAMPLES:
            # Check for Fibonacci pattern
            if "fibonacci" in description_lower or "fib" in description_lower:
                return CodeGenerationResponse(
                    code=PREDEFINED_EXAMPLES[request.language]["fibonacci"], 
                    language=request.language,
                    model_used="predefined_examples"
                )
                
            # Check for Factorial pattern
            elif "factorial" in description_lower or "fact" in description_lower:
                return CodeGenerationResponse(
                    code=PREDEFINED_EXAMPLES[request.language]["factorial"], 
                    language=request.language,
                    model_used="predefined_examples"
                )
                
            # Check for Sorting pattern
            elif "sort" in description_lower:
                return CodeGenerationResponse(
                    code=PREDEFINED_EXAMPLES[request.language]["sort"], 
                    language=request.language,
                    model_used="predefined_examples"
                )
        
        # Fallback to model inference if no predefined example matches
        prompt = f"# {request.language} code to {request.description}\n\n"
        
        # Generate the code using the appropriate model
        code = model_manager.generate_text(
            model_type="code_generation",
            prompt=prompt,
            temperature=request.temperature,
            max_length=request.max_length or 2048,
        )
        
        # If there's an error in the response, return a predefined example or a simple example
        if code.startswith("Error"):
            logger.warning(f"Error in code generation, using fallback. Error: {code}")
            return CodeGenerationResponse(
                code=f"# Simple {request.language} example for: {request.description}\n\n" + 
                     f"# Note: This is a basic example. The AI model encountered an error.\n\n" +
                     f"def example_function():\n    print('Example for: {request.description}')\n\nexample_function()",
                language=request.language,
                model_used="fallback_example"
            )
        
        # Get the model ID
        model_info = next((m for m in model_manager.get_available_models() 
                         if m["type"] == "code_generation"), {"model_id": "unknown"})
        
        # Return the response
        return CodeGenerationResponse(
            code=code,
            language=request.language,
            model_used=model_info["model_id"],
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
        
        # Create a simpler prompt for the model
        prompt = f"# Code to explain:\n\n```\n{request.code}\n```\n\n# Explanation:\n"
        
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
        
        # Get the model ID
        model_info = next((m for m in model_manager.get_available_models() 
                         if m["type"] == "text_generation"), {"model_id": "unknown"})
        
        # Return the response
        return CodeExplanationResponse(
            explanation=explanation,
            language_detected=language,
            model_used=model_info["model_id"],
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