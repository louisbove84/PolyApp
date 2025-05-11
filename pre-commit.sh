#!/bin/bash

echo "Running isort (import sorter)..."
isort .
if [ $? -ne 0 ]; then
    echo "❌ isort failed"
    exit 1
fi

echo "Running Ruff linter..."
ruff check .
if [ $? -ne 0 ]; then
    echo "❌ Ruff check failed"
    exit 1
fi

echo "Running Ruff formatter..."
ruff format .
if [ $? -ne 0 ]; then
    echo "❌ Ruff format failed"
    exit 1
fi

echo "Running MyPy type checker..."
mypy generate_llm_yaml
if [ $? -ne 0 ]; then
    echo "❌ MyPy check failed"
    exit 1
fi

echo "✅ All checks passed!" 