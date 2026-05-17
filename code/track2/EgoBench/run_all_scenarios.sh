#!/bin/bash

# ==============================================================================
# EgoBench Competition - Run All Scenarios
# ==============================================================================
#
# This script runs all scenarios for the competition.
# Participants should configure their models in:
#   - config/user_agent_config.py (for user simulation)
#   - config/service_agent_config.py (for service agent)
#
# Usage:
#   bash run_all_scenarios.sh
#
# Optional: Specify number of tasks per scenario
#   bash run_all_scenarios.sh --num_tasks 10
# ==============================================================================

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default number of tasks (0 = all tasks)
NUM_tasks=0

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --num_tasks)
            NUM_tasks="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Source environment variables if .env exists
if [ -f ".env" ]; then
    source ".env"
fi

# Your settings here
export USER_MODEL_NAME="Qwen3.5-397B-A17B"
export SERVICE_MODEL_NAME="Qwen3.5-397B-A17B"
export USER_API_BASE_URL=""
export SERVICE_API_BASE_URL=""
export API_KEY=""
export SERVICE_API_KEY=""
export VIDEO_MODE="url"


# Print configuration
echo "=========================================="
echo "EgoBench Competition - Running All Scenarios"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  User Model: $USER_MODEL_NAME"
echo "  Service Model: $SERVICE_MODEL_NAME"
echo "  User API URL: $USER_API_BASE_URL"
echo "  Service API URL: $SERVICE_API_BASE_URL"
echo "  Video Mode: $VIDEO_MODE"
$0
echo "  Num tasks: $NUM_tasks"
echo ""



# Check if required environment variables are set
# if [ -z "$API_KEY" ] && [ -z "$SERVICE_API_KEY" ]; then
#     echo "Error: API_KEY or SERVICE_API_KEY environment variable is not set."
#     echo "Please set your API key in .env file or as environment variable."
#     exit 1
# fi

# Create results directory if it doesn't exist
mkdir -p results

# Function to run a scenario
run_scenario() {
    local scenario=$1
    local scenario_number=$2

    echo "Running: $scenario$scenario_number (easy mode)"

    python run/multi_agent.py \
        --scenario "$scenario" \
        --scenario_number "$scenario_number" \
        --service_model_name "$SERVICE_MODEL_NAME" \
        --multi_agent_user \
        --summary_user \
        --num_tasks "$NUM_tasks"

    echo "Completed: $scenario$scenario_number (easy mode)"
    echo ""
}

# Retail scenarios (1-10)
echo "=========================================="
echo "Running Retail Scenarios (1-10)"
echo "=========================================="
for i in $(seq 1 10); do
    run_scenario "retail" $i
done

# Kitchen scenarios (1-4)
echo "=========================================="
echo "Running Kitchen Scenarios (1-4)"
echo "=========================================="
for i in $(seq 1 4); do
    run_scenario "kitchen" $i
done

# Restaurant scenarios (1-5)
echo "=========================================="
echo "Running Restaurant Scenarios (1-5)"
echo "=========================================="
for i in $(seq 1 5); do
    run_scenario "restaurant" $i
done

# Order scenarios (1-2)
echo "=========================================="
echo "Running Order Scenarios (1-2)"
echo "=========================================="
for i in $(seq 1 2); do
    run_scenario "order" $i
done

echo "=========================================="
echo "All scenarios completed!"
echo "=========================================="
echo ""
echo "Results saved to: results/$SERVICE_MODEL_NAME/"
echo ""
echo "To evaluate results, run:"
echo "  bash analysis_scripts/run_eval.sh"