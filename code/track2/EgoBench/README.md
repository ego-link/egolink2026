# EgoBench Competition - Participant Guide

We propose a framework for evaluating (MLLM) customer service agents (under test), which comprises an interaction sandbox and an automated evaluation pipeline. The interaction sandbox features a simulated user, a tool library, and a database. The simulated user is responsible for issuing tasks to the agents under test. In response, these agents can output two types of content within the sandbox: natural language responses for conversational engagement with the user, and tool calls that either retrieve information or modify the database as requested. Following each task interaction, the automated evaluation pipeline assesses performance by measuring tool-call accuracy and verifying the final state of the database.

![Figure 1](figure/fig1.png)

## Overview

### Timeline

- **Testing Phase**: 2026.05.18 - 2026.06.25
- **Final Evaluation Phase**: 2026.06.18 - 2026.06.25
- **Scenarios**: Retail (10), Kitchen (4), Restaurant (5), Order (2)

### Scenario Availability

During the **Offline Testing Phase (2026.05.18 - 2026.06.25)**, the following scenarios will have tasks available:
| Scenario | Scenario Numbers |
|----------|--------------------------|
| Retail | 1, 2, 3, 4, 5, 7, 8, 9 |
| Kitchen | 1, 2, 3 |
| Restaurant | 1, 2, 3, 4 |
| Order | 1 |


During the **Final Evaluation Phase (2026.06.18 - 2026.06.25)**, 100 tasks will be provided from these scenarios as the final evaluation tasks. The following scenarios will have tasks available:

| Scenario | Scenario Numbers |
|----------|--------------------------|
| Retail | 6, 10 |
| Kitchen | 4 |
| Restaurant | 5 |
| Order | 2 |




## Configuration

### 1. User Agent Configuration (`config/user_agent_config.py`)

We have already implemented the prompts and the corresponding framework for the simulated user. You only need to follow the steps below to configure the LLM that drives the simulated user framework, whether through local deployment or via an API. No other modifications are required.

```python
# Default: Qwen3.5-397B-A17B
USER_MODEL_NAME = "Qwen3.5-397B-A17B"

# Set via environment variable: export API_KEY="your-api-key"
USER_API_KEY = os.environ.get("API_KEY", "")

# Base URL for the API endpoint
USER_API_BASE_URL = os.environ.get("LLM_API_BASE_URL", "https://api.example.com/v1")
```

**Required Environment Variables:**

```bash
export API_KEY="your-user-model-api-key"
export LLM_API_BASE_URL="https://your-api-endpoint.com/v1"
```

> [NOTE]
> This part is not required for setup, but helps developers understand the design.

> The simulated user framework need to ensure that the user's responses satisfy the following points. The simulated user is considered successful when the user completes all instructions without issues in the following dimensions:
> - **Role Consistency**: The user maintains their assigned role throughout the conversation
> - **Instruction Following & Anti-Hallucination**: The user follows the given instructions and does not generate hallucinated information
> - **Resilience & Anti-Interference**: The user is not misled by the agent's confusing responses
> - **Contextual Robustness**: The user maintains context and does not contradict previous statements

> We have evaluated various open-source models for simulating user behavior. The success rate (percentage of tasks where the user successfully completes all instructions) is as follows. To more accurately evaluate the capabilities of the service agent you develop, we recommend using a larger-parameter model to drive the simulated user framework.:

> | Model | Success Rate |
> |-------|----------------------------|
> | Qwen3.5-397B-A17B | 0.9673 |
> | Qwen3-235B-A22B | 0.9375 |
> | Qwen3.5-122B-A10B | 0.8988 |
> | Qwen3.6-35B-A3B | 0.7381 |
> | Qwen3.5-35B-A3B | 0.6786 |

> **Important Note**: In our observations, most interaction issues are NOT caused by the simulated user first, but rather by the service agent's confusing or ambiguous behaviors that mislead the simulated user into generating responses that may violate the above requirements. Therefore, participants should focus on improving their agent's responses rather than blaming the simulated user's behavior.

### 2. Service Agent Configuration (`config/service_agent_config.py`)

You may modify the config/service_agent_config.py file as needed, as long as the function name, input and output of all the provided functions remain consistent. Configure your model that will be evaluated as the customer service agent.

```python
# Default: Qwen3.5-397B-A17B (supports both API and local deployment)
SERVICE_MODEL_NAME = "Qwen3.5-397B-A17B"

# API key for your service model
SERVICE_API_KEY = os.environ.get("SERVICE_API_KEY", os.environ.get("API_KEY", ""))

# Base URL - set to your local deployment if applicable
SERVICE_API_BASE_URL = os.environ.get("SERVICE_API_BASE_URL", "https://api.example.com/v1")
```

Service agents(under test) can only output two types of content within the sandbox: natural language responses for conversational engagement with the user, and tool calls that either retrieve information or modify the database as requested.

#### Tool Call Format
When the service agent needs to invoke tools, it must output **ONLY** a JSON array with the following format:

```json
[{"tool_name": "tool_name_1", "parameters": {"param1": "value1", "param2": "value2"}}, {"tool_name": "tool_name_2", "parameters": {"param1": "value1"}}]
```

Important Rules for Tool Calling:
1. Output **ONLY** the JSON array when calling tools - no extra text, no Markdown formatting, no explanations
2. Multiple independent tools can be called in parallel within the same JSON array
3. All required parameters must be provided for each tool
4. Ensure the JSON is valid and properly formatted

Example Tool Call:
```json
[{"tool_name": "find_ingredient_category", "parameters": {"ingredient_name": "cornmeal"}}, {"tool_name": "get_ingredient_nutrition", "parameters": {"ingredient_name": "cornmeal"}}]
```

#### Response Format for Users

When **NOT** calling tools, the service agent should respond in natural, concise language:

1. **Be concise and professional** - Keep responses short and focused on key information
2. **No technical jargon** - Avoid formatted lists, technical terms, or robotic phrasing
3. **Sound human** - Respond like a helpful customer service representative
4. **Context-aware** - Reference information visible in images/videos to reduce unnecessary questions
5. **Ask targeted questions** - If clarification is needed, ask 1-3 targeted questions maximum

#### Output Rules Summary

| Type | Output Format |
|----------|---------------|
| Calling tools | JSON array only: `[{"tool_name": "...", "parameters": {...}}]` |
| Response for users | Natural language response only |

**Never mix formats** - Either output pure JSON OR pure natural language in a single response 

** Each task interaction has two stopping conditions **:
1. The simulated user determines from the agent’s dialogue that the agent has completed the entire task and returns "STOP".
2. The conversation between the user and the agent reaches 10 turns. Only dialogue turns are counted here; turns involving tool calls made by the user are not included.
The interaction ends when either of the above conditions is met.
This functionality has already been implemented in the sandbox, so participants do not need to implement it themselves. This explanation is provided only to help participants better understand the interaction process.


#### Video Storage Configuration

Choose how videos are accessed:

```python
# Option 1: Use local videos folder (default)
VIDEO_MODE = "local"
VIDEO_LOCAL_PATH = "./videos"

# Option 2: Use public URLs
# Participants need to download the video themselves and upload it to a publicly accessible online location.
VIDEO_MODE = "url"
# Set via environment variable:
export VIDEO_URL_MAPPING='{"retail1.mp4": "https://example.com/retail1.mp4"}'
```

## Running the Competition

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Your Models

Edit the two configuration files to use your preferred models:

```bash
# Edit user agent configuration
vim config/user_agent_config.py

# Edit service agent configuration
vim config/service_agent_config.py
```

### Step 3: Set Environment Variables

Create a `.env` file or export variables directly and set configs in `run_all_scenarios.sh` file:

```bash
# Required: API keys
export API_KEY="your-api-key"
export SERVICE_API_KEY="your-service-api-key"

# Optional: API base URLs (if different from defaults)
export LLM_API_BASE_URL="https://your-api-endpoint.com/v1"
export SERVICE_API_BASE_URL="https://your-service-endpoint.com/v1"
```

### Step 4: Run All Scenarios

```bash
# Run all 21 scenarios (retail 1-10, kitchen 1-4, restaurant 1-5, order 1-2)
bash run_all_scenarios.sh

# Or run with limited tasks for testing
bash run_all_scenarios.sh --num_tasks 10
```

### Step 5: Evaluate Results

```bash
# Evaluate all interaction results
bash analysis_scripts/run_eval.sh

# Or specify model name and tasks explicitly
bash analysis_scripts/run_eval.sh --model_name Qwen3.5-397B-A17B --num_tasks 10
```

## Command Line Parameters for multi_agent.py

When running `run/multi_agent.py` directly, the following command line arguments are available:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--service_model_name` | From config | The model name for the service agent being evaluated |
| `--scenario` | `retail` | Task scenario: `retail`, `kitchen`, `restaurant`, or `order` |
| `--scenario_number` | `1` | Task number within the scenario (e.g., 1-10 for retail) |
| `--user_mode` | `easy` | Difficulty mode for user agent (currently only `easy` is supported) |
| `--multi_agent_user` | `False` | Enable LLM-based user response checking and correction |
| `--summary_user` | `False` | Enable dialogue summary to avoid lengthy history |
| `--num_tasks` | `0` | Number of tasks to test (0 means all tasks) |

**Example Usage:**

```bash
python run/multi_agent.py \
  --scenario retail \
  --scenario_number 1 \
  --service_model_name Qwen3.5-397B-A17B \
  --multi_agent_user \
  --summary_user \
  --num_tasks 10
```
> [NOTE]
> The sandbox already resets the database state after each task is completed, ensuring that the database state is correct for the next task interaction. However, please note that only one agent is allowed to interact with the sandbox within a single process. If you need to run experiments in parallel, please launch multiple sandbox instances.

## Prompt Structure

The prompts for both agents are defined in `run/prompts.py`. Below is the structure of each role's prompt:

### User Agent Prompt Structure

The user agent (simulated customer) uses the `USER_TEXT_ONLY_PROMPT_EASY` template.


### Service Agent Prompt Structure

The service agent (your evaluated model) uses the `SERVICE_AGENT_PROMPT_BASE` template.

### Modifying Prompts

Participants are allowed to modify the service agent's prompts in `run/prompts.py` to achieve better performance. However, **modifying the simulated user's prompts is prohibited**.

## Output

### Important Notes on Output Directories

**The `results/` and `eval_result/` directories are automatically generated when running the commands below. You do not need to create them manually.**

**Warning**: Running the same scenario multiple times will **overwrite** previous results in these directories. If you want to preserve previous results, make sure to back them up before re-running scenarios.

### Interaction Results

We only evaluate on easy interaction mode. Results are saved to `results/{model_name}/` with the following format:

```
results/
└── Qwen3.5-397B-A17B/
    ├── retail1_easy.json
    ├── retail2_easy.json
    ├── kitchen1_easy.json
    └── ...
```
The files in the above directory are for reference only and are not the standard answers.

> Note
> This example result was generated by the service agent using Qwen3.5-397B-A17B. Specifically, it used the service agent prompt provided in the run/prompts.py, with thinking mode disabled. Parameters such as temperature were set to the default values for Qwen3.5-397B-A17B. The video was provided as a publicly accessible video_url, rather than being converted to Base64 encoding. 


Each JSON file contains:
- `task_id`: Task identifier
- `dialogue`: Conversation history between user and agent
- `tool_calls`: Tools invoked by the agent
- `rounds_count`: Number of dialogue rounds
- `input_tokens` / `output_tokens`: Token usage
- `execution_time_seconds`: Total execution time

### Evaluation Results

Evaluation results are saved to `eval_result/{model_name}/`:
The files in the following directory are only for reference.
```
eval_result/
└── Qwen3.5-397B-A17B/
    ├── retail1_easy_eval.json
    ├── retail2_easy_eval.json
    └── ...
```

Each evaluation file contains:
- `tool_based.success_rate`: Whether correct tools were called
- `result_based.success_rate`: Whether tool results are correct
- `joint_success.success_rate`: Both tool and result are correct
- `micro_tool_stats.micro_accuracy`: Tool call accuracy

> [NOTE]
> Evaluation is based on the benchmark-provided database and tool outputs in this repository. In some cases, the dataset values may differ from external real-world knowledge sources. During evaluation, the benchmark database/tool results are treated as the only ground truth. 

### Evaluation Criteria

The final ranking is determined by the **`avg_joint_success_rate`** field in the evaluation results. A task is considered fully correct **only when** it passes both:

1. **Tool-call-based process evaluation** (`tool_based.success_rate`): The service agent called the correct tools with correct parameters.
2. **Database-result-based evaluation** (`result_based.success_rate`): The tool execution produced the correct results against the ground-truth database state.

If a task fails either evaluation, it is not counted as a success. The `joint_success.success_rate` is `1` only when both evaluations pass, and `0` otherwise. The `avg_joint_success_rate` is the average of `joint_success.success_rate` across all tasks.

## Project Structure

```
EgoBench/
├── config/                          # Configuration files (modify these)
│   ├── __init__.py
│   ├── user_agent_config.py        # User simulation model config
│   └── service_agent_config.py     # Service agent model config
├── run/                             # Core simulation code
│   ├── multi_agent.py              # Main entry point
│   ├── utils.py                    # Utility functions
│   ├── prompts.py                  # Prompt templates
│   └── apis/                       # API integrations
├── scenarios/
│   └── final/                      # Task definitions (ground truth)
│       ├── retail1.json - retail10.json
│       ├── kitchen1.json - kitchen4.json
│       ├── restaurant1.json - restaurant5.json
│       └── order1.json - order2.json
├── tools/                          # Tool definitions & databases
│   ├── retail/                     # Retail scenario tools
│   ├── kitchen/                    # Kitchen scenario tools
│   ├── restaurant/                 # Restaurant scenario tools
│   └── order/                      # Order scenario tools
├── videos/                         # Video files for scenarios
├── analysis_scripts/               # Evaluation scripts
│   ├── evaluate_interaction.py    # Main evaluation script
│   ├── run_eval.sh                 # Evaluation runner
│   └── ...
├── results/                        # Interaction results (auto-generated)
├── eval_result/                    # Evaluation results (auto-generated)
├── run_all_scenarios.sh            # Run all scenarios
└── README.md                       # This file
```

## Submission

After completing all interactions:

**Interaction Trajectories**: Submit all files in `results/{model_name}/`. You should only submit results for tasks released after June 18, 2026, and the detailed submission method will be announced after that date. We have provided an example file in the folder for reference.

Example submission format:

```
submission/
├── results/
│   └── Qwen3.5-397B-A17B/
│       ├── retail1_easy.json
│       ├── retail2_easy.json
│       └── ...
```

## Troubleshooting

### API Key Not Set

```
Error: API_KEY environment variable is not set
```

**Solution**: Set the API key before running:
```bash
export API_KEY="your-api-key"
```

### Connection Timeout

If API calls timeout, the system will automatically retry up to 3 times with exponential backoff.

### Video File Not Found

If using local video mode, ensure videos are in the `videos/` folder:
```bash
ls videos/
```

If using URL mode, verify your `VIDEO_URL_MAPPING` is correct:
```bash
export VIDEO_URL_MAPPING='{"retail1.mp4": "https://your-url.com/retail1.mp4"}'
```

## Support

For issues or questions, please refer to the main documentation or contact the competition organizers.

## License

Released under the MIT License.
