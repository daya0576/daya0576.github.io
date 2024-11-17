#!/bin/bash

for file in *; do
    # Check if the item is a file and its name starts with a date in the format YYYY-MM-DD-
    if [[ -f "$file" && "$file" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}-(.+)$ ]]; then
        # Capture the new file name without the date prefix
        new_name="${BASH_REMATCH[1]}"
        # Check if a file with the new name already exists
        if [ -e "$new_name" ]; then
            echo "Error: The file '$new_name' already exists. Skipping '$file'."
        else
            # Rename the file by removing the date prefix
            mv "$file" "$new_name"
            echo "Renamed '$file' to '$new_name'."
        fi
    fi
done
