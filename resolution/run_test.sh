#!/bin/bash

# Run tests until an error occurs
while true; do
    # Generate a random test case
    python3 test_generator.py
    
    # Run the project code with the generated test case
    OUTPUT=$(python3 proj21.py < testfile 2>&1)
    STATUS=$?  # Capture the exit status
    
    # Display output from the project code
    echo "$OUTPUT"

    # Check if an error occurred
    if [ $STATUS -ne 0 ]; then
        echo "Error detected! Halting tests."
        echo "Error Output: $OUTPUT"
        break
    fi

    # Allow manual stop with Ctrl+C
    echo "Test passed. Continuing..."
done
