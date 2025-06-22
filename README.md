# 🚀 Logix - MyLang to C++ Translator

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/yourusername/logix)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**Logix** is an innovative programming language translator that converts **MyLang** code into compilable **C++** code using advanced AI-powered translation. It bridges the gap between a simple, intuitive programming language and powerful C++ compilation.

## 🌟 Features

- **AI-Powered Translation**: Uses OpenRouter API for intelligent code conversion
- **Complete C++ Output**: Generates fully compilable C++ programs
- **Automatic Compilation**: Compiles translated code into executable files
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Easy-to-Learn Syntax**: MyLang provides a simplified programming experience
- **Type Inference**: Automatically determines data types from context

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- g++ compiler (MinGW for Windows, GCC for Linux/macOS)
- OpenRouter API key

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/logix.git
   cd logix
   ```

2. **Install dependencies:**
   ```bash
   pip install requests
   ```

3. **Configure API Key:**
   Edit `logix.py` and replace the placeholder API key:
   ```python
   OPENROUTER_API_KEY = "your-actual-api-key-here"
   ```

4. **Compile with PyInstaller (Optional):**
   ```bash
   pip install pyinstaller
   pyinstaller logix.spec
   ```

## 🎯 Quick Start

1. **Create a MyLang file** (`example.txt`):
   ```mylang
   acha name = "World"
   bol("Hello, " + name)
   
   acha age = pusho("Enter your age: ")
   bol("You are " + age + " years old")
   ```

2. **Run the translator:**
   ```bash
   python logix.py example.txt
   # or if compiled:
   ./logix example.txt
   ```

3. **Execute the generated program:**
   ```bash
   ./example
   ```

## 📚 MyLang Language Documentation

### Overview

MyLang is a simple, intuitive programming language designed for beginners and rapid prototyping. It features dynamic typing, clear syntax, and automatic translation to C++.

### Data Types

| MyLang Type | C++ Equivalent | Example |
|-------------|----------------|---------|
| `int` | `int` | `10`, `-5`, `0` |
| `float` | `double` | `3.14`, `-0.5`, `2.0` |
| `bool` | `bool` | `true`, `false` |
| `string` | `std::string` | `"hello"`, `"world"` |
| `list` | `std::vector<Type>` | `[1, 2, 3]`, `["a", "b"]` |
| `dictionary` | `std::map<KeyType, ValueType>` | `{"name": "John", "age": 30}` |

### Variables

**Declaration:** Use the `acha` keyword
```mylang
acha name = "John"
acha age = 25
acha is_active = true
acha scores = [85, 92, 78]
```

**Type Inference:** Variables automatically determine their type based on assigned values.

### Output

**Print to console:** Use the `bol()` function
```mylang
bol("Hello, World!")
bol(42)
bol("The answer is: " + 42)
```

### Input

**Read from console:** Use the `pusho()` function
```mylang
acha user_input = pusho("Enter your name: ")
acha age = pusho("Enter your age: ")
```

### Control Flow

#### Conditionals
```mylang
ager(age >= 18) {
    bol("You are an adult")
}
nahi to {
    bol("You are a minor")
}
```

#### Loops
```mylang
acha i = 0
jabtak(i < 5) {
    bol("Count: " + i)
    i = i + 1
}
```

### Functions

**Function Declaration:** Use the `mazdoor` keyword
```mylang
mazdoor greet(acha name) {
    bol("Hello, " + name)
    wapis "Greeting sent to " + name
}

mazdoor calculate_sum(acha a, acha b) {
    acha result = a + b
    wapis result
}
```

**Return Values:** Use the `wapis` keyword
```mylang
mazdoor get_user_info() {
    wapis "John Doe", 30, true
}
```

**Function Calls:**
```mylang
acha message = greet("Alice")
acha sum = calculate_sum(10, 20)
acha name, age, active = get_user_info()
```

### Operators

#### Arithmetic
- `+` (addition, string concatenation)
- `-` (subtraction)
- `*` (multiplication)
- `/` (division)
- `%` (modulo, integers only)

#### Comparison
- `==` (equal)
- `!=` (not equal)
- `<` (less than)
- `>` (greater than)
- `<=` (less than or equal)
- `>=` (greater than or equal)

#### Logical
- `and` (logical AND)
- `or` (logical OR)
- `not` (logical NOT)

## 🔧 Advanced Examples

### Example 1: Simple Calculator
```mylang
mazdoor calculator() {
    acha num1 = pusho("Enter first number: ")
    acha num2 = pusho("Enter second number: ")
    acha operation = pusho("Enter operation (+,-,*,/): ")
    
    ager(operation == "+") {
        wapis num1 + num2
    }
    ager(operation == "-") {
        wapis num1 - num2
    }
    ager(operation == "*") {
        wapis num1 * num2
    }
    ager(operation == "/") {
        wapis num1 / num2
    }
    nahi to {
        wapis "Invalid operation"
    }
}

acha result = calculator()
bol("Result: " + result)
```

### Example 2: List Operations
```mylang
acha numbers = [1, 2, 3, 4, 5]
acha sum = 0
acha i = 0

jabtak(i < 5) {
    sum = sum + numbers[i]
    i = i + 1
}

bol("Sum of numbers: " + sum)
bol("Average: " + (sum / 5))
```

### Example 3: Dictionary Usage
```mylang
acha person = {"name": "Alice", "age": 25, "city": "New York"}
bol("Name: " + person["name"])
bol("Age: " + person["age"])
bol("City: " + person["city"])
```

## 🛠️ Technical Details

### Translation Process

1. **Code Reading**: Reads MyLang code from input file
2. **AI Translation**: Sends code to OpenRouter API for C++ conversion
3. **Code Cleaning**: Extracts and cleans the generated C++ code
4. **File Generation**: Saves cleaned C++ code to temporary file
5. **Compilation**: Compiles C++ code using g++ compiler
6. **Cleanup**: Removes temporary files and outputs executable

### API Configuration

The translator uses the OpenRouter API with the following configuration:
- **Model**: `tngtech/deepseek-r1t-chimera:free`
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **Headers**: Authorization, Content-Type, HTTP-Referer, X-Title

### Error Handling

- **File Not Found**: Graceful error messages for missing input files
- **Encoding Issues**: Automatic encoding detection and fallback
- **API Errors**: Comprehensive error reporting for API failures
- **Compilation Errors**: Detailed g++ error output
- **Type Inference**: Fallback to `std::string` for ambiguous types

## 🚀 Performance

- **Translation Speed**: ~2-5 seconds per file (depending on API response time)
- **Compilation**: Near-instantaneous for simple programs
- **Memory Usage**: Minimal overhead
- **File Size**: Generated executables are optimized and compact

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenRouter**: For providing the AI translation API
- **PyInstaller**: For enabling easy distribution
- **C++ Community**: For the robust compilation ecosystem

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/logix/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/logix/discussions)
- **Email**: your-email@example.com

---

**Made with ❤️ by the Logix Team**

*Transform your ideas into code with the power of AI!* 