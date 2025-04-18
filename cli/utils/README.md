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

- `dots` (default): ⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏
- `dots2`: ⣾⣽⣻⢿⡿⣟⣯⣷
- `dots3`: ⣷⣯⣟⡿⢿⣻⣽⣾
- `dots12`: ⢀⡀⠄⠂⠁⠈⠐⠠⢀
- `line`: |/-\
- `aesthetic`: Shows a progress-like animation
- `bounce`: ⠁⠂⠄⡀⢀⠠⠐⠈
- `moon`: 🌑🌒🌓🌔🌕🌖🌗🌘
- `clock`: 🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛
- `simple`: ←↖↑↗→↘↓↙
- `thinking`: 🤔 🧠 💭 💡

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
- `spinner_style`: The animation style to use
- `color`: The color of the message and spinner (e.g., "blue", "green", "yellow", "red") 