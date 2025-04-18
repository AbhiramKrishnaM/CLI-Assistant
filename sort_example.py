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