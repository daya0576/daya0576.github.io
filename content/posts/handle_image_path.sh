#!/bin/bash

for file in *; do
    if [[ -f "$file" ]]; then
        sed -i '' 's#](\.\./images/blog#](/images/blog#g' "$file"
        echo "Fixed $file"
    fi
done
