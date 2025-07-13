# Error Handling Guide

This document provides an in-depth overview of the error handling mechanisms within the project.
It details the exceptions used, their meanings, associated exit codes, and examples of when and
how they are raised in the codebase. The guide aims to standardize error handling practices and
ensure consistency across the project, aligning with
[CEP-8](https://gist.github.com/reactive-firewall/b7ee98df9e636a51806e62ef9c4ab161) standards.

## Exceptions Overview

### `Multicast` Exceptions

#### `CommandExecutionError`

- **Exception**: `multicast.exceptions.CommandExecutionError`
- **Description**: Raised when a command execution fails, capturing the error message and exit
  code.
- **Exit Code**: Defined at the time of raising, typically `1` (General Error).
- **Usage Example**:

  This exception is typically raised when a subprocess or system command fails to execute
  properly.

  ```python
  if return_code != 0:
      raise CommandExecutionError("Failed to execute the backup script.", exit_code=return_code)
  ```

  <!-- AI can identify instances of `CommandExecutionError` usage by searching with
    `git grep -F "CommandExecutionError"` or `git grep -F "raise CommandExecutionError"` -->

#### `ShutdownCommandReceived`

- **Exception**: `multicast.exceptions.ShutdownCommandReceived`
- **Description**: Raised to signal a graceful shutdown of the multicast server.
- **Exit Code**: `143` (Terminated by SIGTERM)
- **Usage Example**:

  Raised when a shutdown command is received, allowing the server to terminate gracefully.

  ```python
  if command == "SHUTDOWN":
      raise ShutdownCommandReceived("Shutdown command received.") from None
  ```

  <!-- AI can identify instances of `ShutdownCommandReceived` usage by searching with
    `git grep -F "ShutdownCommandReceived"` or `git grep -F "raise ShutdownCommandReceived"` -->

### Standard Exceptions Mapped to Exit Codes

The codebase maps several standard exceptions to specific exit codes according to the
project's `EXIT_CODES` mapping.

#### `ModuleNotFoundError`

- **Description**: Raised when a required module cannot be found.
- **Exit Code**: `127` (Command Not Found)
- **Usage Examples**:

  **Example 1**: In `multicast/__init__.py`, when critical modules fail to import.

  ```python
  try:
      import important_module
  except ImportError as _cause:
      raise ModuleNotFoundError(
          "[CWE-758] Module failed to import."
      ) from _cause
  ```

  **Example 2**: In `multicast/hear.py`, handling errors during module import.

  ```python
  raise ModuleNotFoundError(
      "[CWE-758] Module failed completely."
  ) from None
  ```

#### `NotImplementedError`

- **Description**: Raised when a method or function is declared but not implemented.
- **Exit Code**: `70` (Internal Software Error)
- **Usage Example**:

  ```python
  def some_abstract_method(self):
      raise NotImplementedError("Subclasses must implement this method.")
  ```

#### `ImportError`

- **Description**: Raised when an import statement fails to find the module definition or when a
  `from ... import` fails to find a name that is to be imported.
- **Exit Code**: `70` (Internal Software Error)
- **Usage Example**:

  In `multicast/__main__.py`, wrapping the original `ImportError` to provide additional context.

  ```python
  except ImportError as _cause:
      raise ImportError("[CWE-440] Error Importing Python") from _cause
  ```

#### `OSError`

- **Description**: Raised when a system function returns a system-related error.
- **Exit Code**: `2` (Misuse of Shell Builtins)
- **Usage Example**:

  In `multicast/recv.py`, when a socket operation fails.

  ```python
  except OSError as _cause:
      raise OSError("[CWE-440] Socket operation failed.") from _cause
  ```

#### `FileNotFoundError`

- **Description**: Raised when a required file is not found.
- **Exit Code**: 66 (No Input)
- **Usage Example**:

  ```python
  raise FileNotFoundError("Configuration file not found.")
  ```

#### `ValueError`

- **Description**: Raised when a function receives an argument of the correct type but an
  inappropriate value.
- **Exit Code**: 65 (Data Error)
- **Usage**:

  ```python
  raise ValueError("Invalid value provided for parameter 'x'.")
  ```

#### `PermissionError`

- **Description**: Raised when attempting an operation without adequate access rights.
- **Exit Code**: 77 (Permission Denied)
- **Usage**:

  ```python
  raise PermissionError("Insufficient permissions to access the resource.")
  ```

## Exit Codes Mapping (`EXIT_CODES`)

The `EXIT_CODES` dictionary in `multicast/exceptions.py` provides a centralized mapping between
exit codes, exceptions, and messages, adhering to
[CEP-8](https://gist.github.com/reactive-firewall/b7ee98df9e636a51806e62ef9c4ab161).

For clarity, here's the standard mapping:

| Exception                      | Exit Code | Message                          |
|--------------------------------|-----------|----------------------------------|
| `RuntimeError`                 | 1         | General Error                    |
| `OSError`                      | 2         | Misuse of Shell Builtins         |
| `argparse.ArgumentError`       | 64        | Usage Error                      |
| `ValueError`                   | 65        | Data Error                       |
| `FileNotFoundError`            | 66        | No Input                         |
| `ConnectionError`              | 69        | Unavailable Service              |
| `Exception`                    | 70        | Internal Software Error          |
| `PermissionError`              | 77        | Permission Denied                |
| `BaseException`                | 125       | Critical Failure                 |
| `AssertionError`               | 126       | Command Invoked Cannot Execute   |
| `ModuleNotFoundError`          | 127       | Command Not Found                |
| `KeyboardInterrupt`            | 130       | Interrupt (SIGINT)               |
| `BrokenPipeError`              | 141       | Broken Pipe (SIGPIPE)            |
| `SystemExit`                   | 143       | Terminated (SIGTERM)             |

<!-- Implementation Details -->
<details>
<summary>Implementation</summary>

The `EXIT_CODES` dictionary in `multicast/exceptions.py` defines the mapping between exit codes,
exceptions, and their descriptions. This centralized mapping ensures consistency across the
project.

```python
EXIT_CODES = {
    0:   (None, 'Success'),
    1:   (RuntimeError, 'General Error'),
    2:   (OSError, 'Misuse of Shell Builtins'),
    64:  (argparse.ArgumentError, 'Usage Error'),
    65:  (ValueError, 'Data Error'),
    66:  (FileNotFoundError, 'No Input'),
    69:  (ConnectionError, 'Unavailable Service'),
    70:  (Exception, 'Internal Software Error'),
    77:  (PermissionError, 'Permission Denied'),
    125: (BaseException, 'Critical Failure'),
    126: (AssertionError, 'Command Invoked Cannot Execute'),
    127: (ModuleNotFoundError, 'Command Not Found'),
    129: (None, 'Hangup (SIGHUP)'),
    130: (KeyboardInterrupt, 'Interrupt (SIGINT)'),
    134: (None, 'Abort (SIGABRT)'),
    137: (None, 'Killed (SIGKILL)'),
    141: (BrokenPipeError, 'Broken Pipe (SIGPIPE)'),
    143: (SystemExit, 'Terminated (SIGTERM)'),
    255: (None, 'Exit Status Out of Range'),
}
```

> [!TIP]
> Plan Ahead: Custom exceptions like CommandExecutionError can use exit codes in the range
`1-255`, but should avoid conflicting with the standard mappings defined above by
[CEP-8](https://gist.github.com/reactive-firewall/b7ee98df9e636a51806e62ef9c4ab161).

</details>

> [!NOTE]
> In some situations, it may not be appropriate to pass the original exception back to the caller.
> In these cases, the handler within the `multicast` module may add additional context by raising
> a custom multicast exception, chaining it to the underlying exception. This approach enriches
> the error information while maintaining clarity in the exception hierarchy.

The following mappings are specific to multicast exceptions and may differ from the standard
mappings above (while still remaining
[CEP-8](https://gist.github.com/reactive-firewall/b7ee98df9e636a51806e62ef9c4ab161)
compliant):

| Exception                 | Exit Code | Reason for Customization |
| ------------------------- | --------- | ------------------------ |
| `CommandExecutionError`   | *1-255*   | Multicast Runtime Error  |
| `ShutdownCommandReceived` | 143       | Terminated by "SHUTDOWN" |

## Exception Usage Examples

Below are examples of how exceptions are raised within the codebase, illustrating actual usage in
different modules. These examples are directly taken from the source code to provide real-world
context.

### Example 1: `ModuleNotFoundError` in `multicast/__init__.py`

- **Location**: `multicast/__init__.py`, Lines 332-356

  When the program fails to import critical modules, such as `argparse`, `unicodedata`, `socket`,
  or `struct`, it raises a `ModuleNotFoundError`.

  ```python
  try:
      import argparse
  except ImportError as _casue:
      raise ModuleNotFoundError("[CWE-440] We could not import argparse. ABORT.") from _cause
  ```

### Example 2: `NotImplementedError` in `multicast/__init__.py`

- **Location**: `multicast/__init__.py`, Line 616

  Abstract methods that must be implemented by subclasses.

  ```python
  def run(self):
      raise NotImplementedError("[CWE-758] Subclasses must implement this method.")
  ```

### Example 3: `ImportError` in `multicast/__main__.py`

- **Location**: `multicast/__main__.py`, Line 86

  Handling import errors with additional context.

  ```python
  except ImportError as _cause:
      raise ImportError("[CWE-440] Error Importing Python") from _cause
  ```

### Example 4: `ShutdownCommandReceived` in `multicast/hear.py`

- **Location**: `multicast/hear.py`, Line 449

  Signaling a graceful shutdown when a shutdown command is received.

  ```python
  if message == "SHUTDOWN":
      raise ShutdownCommandReceived("SHUTDOWN") from None
  ```

### Example 5: `OSError` in `multicast/recv.py`

- **Location**: `multicast/recv.py`, Line 292

  Indicating a socket operation failure.

  ```python
  except OSError as _cause:
      raise OSError("[CWE-474] Socket operation failed.") from _cause
  ```

### Example 6: `KeyboardInterrupt` in `multicast/hear.py`

- **Location**: `multicast/hear.py`, Line 541

  Handling user interruption (e.g., pressing Ctrl+C).

  ```python
  except KeyboardInterrupt as _cause:
      raise KeyboardInterrupt("User interrupted the process.") from _cause
  ```

## Error Handling Practices

- **Centralized Exception Handling**: Utilize the `exit_on_exception` decorator provided in
  `multicast/exceptions.py` to ensure exceptions are mapped to the correct exit codes and handled
  consistently.
- **Consistent Use of Exceptions**: Keep exception raising consistent across the codebase by using
  the predefined exceptions and messages.
- **Clear Error Messages**: Provide informative and clear error messages to aid in debugging and
  user understanding.
- **Adherence to Standards**: Follow the guidelines set out in
  [CEP-8](https://gist.github.com/reactive-firewall/b7ee98df9e636a51806e62ef9c4ab161) and the
  project's conventions for error handling and exit codes.

## Adding New Exceptions

When introducing new exceptions:

1. **Define the Exception**: Create the new exception class, inheriting from an appropriate base
  class.
2. **Update `EXIT_CODES` Mapping**: Add the exception and its corresponding exit code to the
  `EXIT_CODES` dictionary in `multicast/exceptions.py`.
3. **Document the Exception**: Update this guide to include the new exception, its description,
  exit code, and usage examples.
4. **Implement Tests**: Write tests to cover the new exception and ensure it's handled correctly
  by the error handling system.

## Conclusion

This guide serves as a comprehensive reference for the project's error handling mechanisms.
By following these practices, developers can maintain consistency, improve code quality, and
provide a better experience for users interacting with the software.

---

### Copyright (c) 2024-2025, Mr. Walls

[![License - MIT](https://img.shields.io/pypi/l/multicast?cacheSeconds=3600)](https://github.com/reactive-firewall-org/multicast/tree/HEAD/LICENSE.md)
