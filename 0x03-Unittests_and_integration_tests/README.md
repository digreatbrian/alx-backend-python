# Unittests and Integration Tests

## Testing Overview

### Unit Testing

Unit testing is the process of verifying that individual functions produce the expected results for a variety of inputs, including standard and edge cases. Key points include:
- **Focus**: Test only the logic within the function.
- **Mocking**: Mock most calls to external functions, especially those involving network or database interactions.

The primary goal of a unit test is to determine: **Does this function work as expected if everything outside it works as expected?**

### Integration Testing

Integration tests validate the end-to-end functionality of a code path. Key points include:
- **Scope**: Test interactions between all components of your code.
- **Mocking**: Generally, only mock low-level functions making external calls (e.g., HTTP requests, file I/O, database I/O).

Integration tests ensure that all parts of your application work together seamlessly.

---