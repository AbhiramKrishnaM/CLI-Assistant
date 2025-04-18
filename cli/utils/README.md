# CLI Utilities

This directory contains utility functions for the CLI application.

## Loading Spinner

The loading spinner functionality is a user interface enhancement that displays an animated spinner while the CLI is waiting for a response from the backend API.

### Usage

```python
from cli.utils.formatting import loading_spinner

# Basic usage
with loading_spinner("Loading data..."):
    # Your long-running code here
    data = fetch_data()

# Custom spinner style
with loading_spinner("Generating code...", spinner_style="moon"):
    # Your code generation function
    code = generate_code()

# Custom color
with loading_spinner("Analyzing...", spinner_style="dots2", color="green"):
    # Your analysis function
    results = analyze_data()
```

### Available Spinner Styles

The following spinner styles are available (built-in Rich spinners):

- `dots` (default): A simple dots animation
- `dots2`: Alternative dots animation
- `dots3`: Another dots variation
- `dots12`: Multi-dot animation 
- `line`: Simple line animation
- `aesthetic`: Shows a progress-like animation
- `bounce`: Bouncing point animation (maps to Rich's "point" spinner)
- `moon`: Moon phase animation
- `clock`: Clock animation
- `simple`: Arrow animation (maps to Rich's "arrow" spinner)
- `thinking`: Thinking animation (maps to Rich's "dots10" spinner)

### Integration with API Requests

The loading spinner is integrated with API requests through the `api_request` function in `cli/utils/api.py`. You can specify a custom loading message when making an API request:

```python
response = api_request(
    endpoint="/text/generate",
    method="POST",
    data={
        "prompt": "Your prompt here",
        "temperature": 0.7
    },
    loading_message="Generating text..."
)
```

### Customization

You can customize the loading spinner by modifying the following parameters:

- `message`: The text to display next to the spinner
- `spinner_style`: The animation style to use (see available options above)
- `color`: The color of the message and spinner (e.g., "blue", "green", "yellow", "red") 