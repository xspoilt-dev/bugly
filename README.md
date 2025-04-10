
# Bugly - Live Debugger for Python

![Bugly UI](https://github.com/xspoilt-dev/bugly/blob/main/ss/Screenshot%20from%202025-04-10%2011-53-37.png?raw=true)

Bugly is a lightweight live debugger for Python that tracks variable changes, function calls, and return values in real-time. It provides a rich, interactive UI powered by the `rich` library, making debugging more intuitive and efficient.

## Features

- **Variable Inspection**: Track changes to variables and view their history.
- **Function Call Tracking**: Log function calls, arguments, and memory usage before and after execution.
- **Return Value Monitoring**: Observe return values of functions along with memory usage.
- **Live UI**: A dynamic, real-time debugging panel with a clean and organized layout.
- **Memory Usage**: Monitor current and peak memory usage during program execution.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/xspoilt-dev/bugly.git
   cd bugly
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Import `var_ins`, `func_ins`, and `live_trace` from bugly.py in your Python script:
   ```python
   from bugly import var_ins, func_ins, live_trace
   ```

2. Use `var_ins` to track variables:
   ```python
   x = 0
   var_ins("x")
   ```

3. Decorate functions with `@func_ins` to track their calls and return values:
   ```python
   @func_ins
   def greet(name):
       return f"Hello, {name}"
   ```

4. Start the live debugger by calling `live_trace()`:
   ```python
   live_trace()
   ```

5. Run your script, and the live debugger panel will display real-time updates.

## Example

Here is an example script using Bugly:

```python
from bugly import var_ins, func_ins, live_trace
import time

x = 0
var_ins("x")

@func_ins
def greet(name):
    return f"Hello, {name}"

for i in range(3):
    x = i
    msg = greet(f"User{i}")
    print(msg)
    time.sleep(1)

live_trace()
```

## Output

The live debugger panel will look like this:

![Bugly UI](https://github.com/xspoilt-dev/bugly/blob/main/ss/Screenshot%20from%202025-04-10%2011-53-37.png?raw=true)

## Logging

Bugly logs all variable changes, function calls, and return values to a file named debug_logs.log. You can review this file for a detailed history of the debugging session.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve Bugly.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

