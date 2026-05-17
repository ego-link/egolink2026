#!/bin/bash

# ==============================================================================
# EgoBench Competition - Evaluation Script
# ==============================================================================
#
# This script evaluates all the interaction results and generates evaluation
# reports for the competition.
#
# Usage:
#   bash run_eval.sh
#
# Optional: Specify model name and number of samples
#   bash run_eval.sh --model_name Qwen3.5-397B-A17B --num_samples 10
# ==============================================================================

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANALYSIS_DIR="$SCRIPT_DIR"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to analysis scripts directory
cd "$ANALYSIS_DIR"

# Default values
MODEL_NAME="Qwen3.5-397B-A17B"
NUM_SAMPLES=0

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --model_name)
            MODEL_NAME="$2"
            shift 2
            ;;
        --num_samples)
            NUM_SAMPLES="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# If model name is not provided, try to get it from service_agent_config.py
if [ -z "$MODEL_NAME" ]; then
    # Try to read from config
    if [ -f "$PROJECT_ROOT/config/service_agent_config.py" ]; then
        MODEL_NAME=$(grep "SERVICE_MODEL_NAME" "$PROJECT_ROOT/config/service_agent_config.py" | head -1 | cut -d'"' -f2)
        if [ -z "$MODEL_NAME" ]; then
            MODEL_NAME=$(grep "SERVICE_MODEL_NAME" "$PROJECT_ROOT/config/service_agent_config.py" | head -1 | cut -d"'" -f2)
        fi
    fi

    # Default to Qwen3.5-397B-A17B if still not found
    if [ -z "$MODEL_NAME" ]; then
        MODEL_NAME="Qwen3.5-397B-A17B"
    fi
fi

echo "=========================================="
echo "EgoBench Competition - Evaluation"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  Model Name: $MODEL_NAME"
echo "  Num Samples: $NUM_SAMPLES"
echo ""

# Check if results directory exists
RESULTS_DIR="$PROJECT_ROOT/results/$MODEL_NAME"
if [ ! -d "$RESULTS_DIR" ]; then
    echo "Error: Results directory '$RESULTS_DIR' does not exist."
    echo "Please run the simulations first using: bash run_all_scenarios.sh"
    exit 1
fi

# Check if there are any JSON files in the results directory
JSON_COUNT=$(find "$RESULTS_DIR" -maxdepth 1 -name "*.json" | wc -l)
if [ "$JSON_COUNT" -eq 0 ]; then
    echo "Error: No JSON files found in '$RESULTS_DIR'."
    echo "Please run the simulations first using: bash run_all_scenarios.sh"
    exit 1
fi

echo "Found $JSON_COUNT result files."
echo "Starting evaluation..."
echo ""

# Run evaluation
python evaluate_interaction.py --model_name "$MODEL_NAME" --num_samples "$NUM_SAMPLES"

echo ""
echo "=========================================="
echo "Evaluation completed!"
echo "=========================================="
echo ""
echo "Evaluation results saved to: eval_result/$MODEL_NAME/"
echo ""
echo "To view detailed results, check the eval_result/$MODEL_NAME/ directory."