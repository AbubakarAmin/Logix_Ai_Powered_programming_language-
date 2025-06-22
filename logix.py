#LOGIX VERSION 1

import requests
import json
import subprocess
import os
import sys  # To get command-line arguments
import re  # For better text cleaning with regex

# --- IMPORTANT: Replace with your actual OpenRouter API key ---
OPENROUTER_API_KEY = "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"
OPENROUTER_SITE_URL = "YOUR_SITE_URL_HERE"  # Optional
OPENROUTER_SITE_NAME = "YOUR_SITE_NAME_HERE"  # Optional
# ---


def read_mylang_code(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except UnicodeDecodeError:
        # If UTF-8 fails, try with different encodings
        encodings_to_try = ['latin1', 'cp1252', 'iso-8859-1']
        for encoding in encodings_to_try:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    print(f"Successfully read file using {encoding} encoding")
                    return file.read()
            except UnicodeDecodeError:
                continue
        print(f"Error: Could not decode file '{filename}' with any supported encoding.")
        return None
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return None

def send_to_llm(mylang_code):
    # --- START OF IMPROVED PROMPT ---
    prompt = """
    Your ONLY task is to translate MyLang code into valid, compilable C++ code.
    Your response MUST contain ONLY the translated C++ code.
    DO NOT include any conversational text, explanations, thoughts, or comments (unless they are absolutely essential for clarity within the C++ code itself, which should be rare).
    DO NOT wrap the code in markdown backticks (```cpp, ```c++, ```) or any other formatting.

    Your response MUST start with the exact string "<START_CPP_CODE>" and end with the exact string "<END_CPP_CODE>".
    The translated C++ code MUST be placed strictly between these two markers.

    <START_CPP_CODE>
    #include <iostream>
    #include <string>
    #include <vector>
    #include <map>
    #include <tuple> // For multiple return values
    #include <utility> // For std::pair
    #include <algorithm> // For std::remove_if if needed for string cleaning

    // MyLang Language Specification for Translation:

    // Data Types:
    // * int: Integer numbers (e.g., 10, -5, 0). Translated to C++ `int`.
    // * float: Floating-point numbers (e.g., 3.14, -0.5, 2.0). Translated to C++ `double`.
    // * bool: Boolean values (true or false). Translated to C++ `bool` (`true`, `false`).
    // * string: Textual data (e.g., "hello", "world"). Translated to C++ `std::string`.
    // * list: Ordered collections of items (e.g., `[1, 2, 3]`, `["a", "b"]`). Translated to C++ `std::vector<ElementType>`.
    //     * ElementType Inference: You must infer `ElementType` based on the types of the elements present in the list.
    //         * If all elements are of the same type (e.g., all `int`), use that type.
    //         * If elements are mixed numeric types (e.g., `int` and `float`), use `double`.
    //         * If elements are mixed non-numeric types, or if the types are ambiguous, default to `std::string`.
    // * dictionary: Key-value pairs (e.g., `{ "name": "John", "age": 30 }`). Translated to C++ `std::map<KeyType, ValueType>`.
    //     * KeyType/ValueType Inference: You must infer `KeyType` and `ValueType` based on the types of the keys and values respectively. Apply the same mixed-type inference rules as for `list` elements for both keys and values.

    // Operators:
    // * Arithmetic: `+`, `-`, `*`, `/`, `%` (for integers and floats). Behaves as in C++.
    // * String Concatenation: `+` (for strings). Behaves as in C++.
    // * Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=` (for integers, floats, booleans, and strings). Behaves as in C++.
    // * Logical: `and`, `or`, `not` (for booleans). Translated to C++ `&&`, `||`, `!`.

    // Variables:
    // * Variables are declared using the keyword "acha" followed by the variable name.
    // * The data type of a variable is inferred dynamically at runtime in MyLang. You must choose the appropriate C++ data type based on the initial assigned value and subsequent re-assignments within its scope.
    //     * If a variable is always assigned values of a consistent type (e.g., always `int`), use that C++ type.
    //     * If a variable is assigned mixed numeric types (`int` then `float`), choose `double`.
    //     * If a variable is assigned highly mixed types (e.g., `int` then `string`), default to `std::string`.
    // * Example (MyLang to C++):
    //     * MyLang: `acha age = 30` -> C++: `int age = 30;`
    //     * MyLang: `acha name = "John"` -> C++: `std::string name = "John";`
    //     * MyLang: `acha temp = 25.5` -> C++: `double temp = 25.5;`
    //     * MyLang: `acha item = 10` then `item = "apple"` -> C++: `std::string item = "10";` (or `std::string item = std::to_string(10);`)

    // Output:
    // * The function 'bol(expression)' prints the value of the expression to the console, followed by a newline.
    // * Example: `bol("Hello")` -> `std::cout << "Hello" << std::endl;`

    // Input:
    // * The function 'pusho(prompt)' displays the 'prompt' to the user and reads a line of text input from the console. The translated C++ code should store this input as a `std::string`.
    // * Example: `acha user_input = pusho("Enter name: ")` -> `std::string user_input; std::cout << "Enter name: "; std::getline(std::cin, user_input);`

    // Control Flow:
    // * Loops: "jabtak (condition) {}" -> `while (condition) {}`
    // * Conditionals: "ager(condition){}" -> `if(condition){}`
    // * Conditionals: "nahi to{}" -> `else{}`

    // User-Defined Functions:
    // * Functions are initialized with 'mazdoor'. Syntax: `mazdoor function_name(acha var1, acha var2, ...){}`.
    // * Variables inside a function are local.
    // * 'wapis' returns value(s).
    // * Type Inference for Functions:
    //     * Parameter Types (`acha variable` in signature): Infer C++ type based on usage within the function body. Default to `std::string` for ambiguity or mixed types.
    //     * Return Types (`wapis` statements):
    //         * Single Return Value: Infer C++ type of the expression. If multiple `wapis` statements return different types, default function return type to `std::string`. If no `wapis`, return `void`.
    //         * Multiple Return Values (e.g., `wapis value1, value2`): Translate to `std::tuple<Type1, Type2, ...>` or `std::pair<Type1, Type2>` for two values. Infer types for each value.
    // * Function Placement: All translated C++ functions (except `main`) must be placed before `main` with full definitions. Ensure proper forward declarations if functions call each other or are defined later.

    // Example of Function Translation (MyLang to C++):
    // MyLang:
    // mazdoor process_data(acha input_val, acha is_valid){
    //     bol("Processing: ")
    //     bol(input_val)
    //     ager(is_valid == true){
    //         wapis input_val * 2, "Data processed successfully"
    //     }
    //     nahi to {
    //         wapis 0, "Error: Invalid data"
    //     }
    // }
    // mazdoor get_details(){
    //     wapis "John Doe", 30, true
    // }
    // acha result_num, result_msg = process_data(5, true)
    // bol("Output: " + result_msg + " Number: ")
    // bol(result_num)
    // acha name, age, active = get_details()
    // bol("Name: " + name)
    // bol("Age: ")
    // bol(age)
    // bol("Active: ")
    // bol(active)

    // C++ Equivalent (Conceptual):
    // std::pair<int, std::string> process_data(int input_val, bool is_valid);
    // std::tuple<std::string, int, bool> get_details();
    // int main() {
    //     int result_num;
    //     std::string result_msg;
    //     std::tie(result_num, result_msg) = process_data(5, true);
    //     std::cout << "Output: " << result_msg << " Number: " << std::endl;
    //     std::cout << result_num << std::endl;
    //     std::string name;
    //     int age;
    //     bool active;
    //     std::tie(name, age, active) = get_details();
    //     std::cout << "Name: " << name << std::endl;
    //     std::cout << "Age: " << std::endl;
    //     std::cout << age << std::endl;
    //     std::cout << "Active: " << std::endl;
    //     std::cout << (active ? "true" : "false") << std::endl;
    //     return 0;
    // }
    // std::pair<int, std::string> process_data(int input_val, bool is_valid){
    //     std::cout << "Processing: " << std::endl;
    //     std::cout << input_val << std::endl;
    //     if(is_valid == true){
    //         return std::make_pair(input_val * 2, "Data processed successfully");
    //     }
    //     else{
    //         return std::make_pair(0, "Error: Invalid data");
    //     }
    // }
    // std::tuple<std::string, int, bool> get_details(){
    //     return std::make_tuple("John Doe", 30, true);
    // }

    // End of MyLang Language Specification.

    // Now, translate the following MyLang code into valid, compilable C++ code.
    // Ensure the translated C++ code is a complete, standalone, and runnable program (include necessary headers, a main function, etc.).
    // Follow C++ best practices.
    // Ensure the C++ code produces the same output and has the same behavior as the original MyLang code.
    // If any MyLang constructs cannot be directly translated, use the closest C++ equivalent.
    // If unsure about a translation, make your best reasonable attempt based on the provided examples and specification.

    // MyLang Code to Translate:
    """ + mylang_code + """
    <END_CPP_CODE>
    """
    # --- END OF IMPROVED PROMPT ---

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": OPENROUTER_SITE_URL,  # Optional
        "X-Title": OPENROUTER_SITE_NAME,  # Optional
    }
    data = json.dumps({
        "model": "tngtech/deepseek-r1t-chimera:free",
        "messages": [{"role": "user", "content": prompt}]
    })
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=data
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        cpp_code = response.json()['choices'][0]['message']['content']

        # Enhanced cleaning process for the C++ code
        cleaned_cpp_code = clean_llm_cpp_response(cpp_code)
        return cleaned_cpp_code
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to LLM: {e}")
        return None
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(
            f"Error processing LLM response: {e} - {response.text if 'response' in locals() else 'No response received'}")
        return None

def clean_llm_cpp_response(raw_code):
    """
    Advanced cleaning of LLM response to extract only valid C++ code
    using explicit start and end markers.
    """
    start_marker = "<START_CPP_CODE>"
    end_marker = "<END_CPP_CODE>"

    start_index = raw_code.find(start_marker)
    end_index = raw_code.find(end_marker)

    if start_index != -1 and end_index != -1 and end_index > start_index:
        # Extract content strictly between markers
        extracted_code = raw_code[start_index + len(start_marker):end_index]
        # Remove any remaining markdown backticks or leading/trailing whitespace
        extracted_code = re.sub(r'```cpp|```c\+\+|```|`', '', extracted_code).strip()
        return extracted_code
    else:
        print("Warning: Markers not found in LLM response. Falling back to regex cleaning.")
        # Fallback to the previous regex cleaning if markers are not found
        # (This should ideally not be hit with the new prompt, but good for robustness)
        code = re.sub(r'```cpp|```c\+\+|```|`', '', raw_code)

        cpp_patterns = [
            r'#include\s*<[a-zA-Z0-9_./]+>',
            r'using\s+namespace\s+std;',
            r'int\s+main\s*\(',
        ]

        start_index = len(code)
        for pattern in cpp_patterns:
            matches = re.search(pattern, code)
            if matches and matches.start() < start_index:
                start_index = matches.start()

        if start_index < len(code):
            code = code[start_index:]

        # Find the last significant C++ syntax element (e.g., closing brace of main or last semicolon)
        # and truncate anything after it.
        last_code_elements = list(re.finditer(r'}\s*$|;\s*$', code, re.MULTILINE))
        if last_code_elements:
            last_pos = max(match.end() for match in last_code_elements)
            code = code[:last_pos]

        # Clean whitespace and standardize line endings
        lines = [line.strip() for line in code.splitlines()]
        code = '\n'.join(line for line in lines if line)

        # Basic validation
        has_include = re.search(r'#include', code) is not None
        has_main = re.search(r'int\s+main\s*\(', code) is not None

        if not (has_include and has_main):
            print("Warning: Extracted code may not be complete C++ (missing #include or main function)")

        return code

def save_cpp_code(cpp_code, output_filename="temp.cpp"):
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(cpp_code)
        return output_filename
    except IOError:
        print(f"Error: Could not save C++ code to '{output_filename}'")
        return None

def compile_cpp_code(cpp_filename, executable_name='output'):
    try:
        command = ['g++', cpp_filename, '-o', executable_name]
        subprocess.run(command, check=True, capture_output=True)
        os.remove(cpp_filename)
        return executable_name
    except subprocess.CalledProcessError as e:
        print(f"Error compiling C++ code:")
        print(e.stderr.decode())
        return None
    except FileNotFoundError:
        print(
            "Error: g++ command not found. Make sure MinGW is installed and in your system's PATH.")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./logix <your_filename.txt>")
        sys.exit(1)

    mylang_filename = sys.argv[1]
    mylang_code = read_mylang_code(mylang_filename)
    print("Compiling your Code .....")
    if mylang_code:
        cpp_code = send_to_llm(mylang_code)
        if cpp_code:
            cpp_filename = save_cpp_code(cpp_code)
            if cpp_filename:
                base_name = os.path.splitext(mylang_filename)[0]
                executable_name = compile_cpp_code(cpp_filename, base_name)
                if executable_name:
                    print(
                        f"\nSuccessfully compiled. You can run the executable '{executable_name}'.")