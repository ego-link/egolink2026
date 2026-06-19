## Final Evaluation Phase

The final evaluation test set will be released on **June 16, 2026 at 20:00 (GMT+8)**. All participants are required to submit their result files and technical report by the deadline of **June 22, 2026 at 20:00 (GMT+8)**.

> ⚠️ **Important Notice on Schedule Adjustment**
> Since the detailed technical report deadline for outstanding teams is June 25, 2026, we have advanced both the test set release date and the submission deadline. To prevent direct tampering with interaction answers, we are releasing the **entire test set**. Participants are expected to complete testing on all samples within this six-day window. If you have any questions or concerns regarding this timeline, please raise an issue or contact us via email.

The following 309 tasks in 5 scenarios constitute the **final test set**:

| Scenario | Scenario Number |
|----------|-----------------|
| Retail   | 6, 10           |
| Kitchen  | 4               |
| Restaurant | 5             |
| Order    | 2               |

The corresponding task files (`retail6.json`, `retail10.json`, `kitchen4.json`, `restaurant5.json`, `order2.json`) are located in the `scenarios/final/` directory. These files do **not** contain the `ground_truth` field.

⏰ Deadline: June 22, 2026 at 20:00 (GMT+8)

## Public Responses to Participant Questions(Continuously updated) :
#### Q1:
In the June 16 version, although the ground-truth annotations have been removed from the evaluation JSON files under EgoBench/scenarios/final, the files still contain certain keys and values. Can the service agent access or use this information?
#### A1:
No. The JSON files under EgoBench/scenarios/final, as well as any information contained in them, must not be directly accessed or used by the service agent. The service agent is only allowed to obtain information from the video and the Simulated User’s feedback. In the evaluation workflow, the files under EgoBench/scenarios/final are intended to be used only by the Simulated User. Moreover, the remaining key-value pairs in these files were included merely as supplementary information to assist human annotators’ understanding, and they do not represent the ground truth used in the final evaluation.
To avoid causing similar confusion for other participants, we will remove irrelevant information from the files under EgoBench/scenarios/final. In addition, during the evaluation phase, we will also strictly examine whether the service agent designed by any participant directly uses information from the files under EgoBench/scenarios/final. Any such use will be considered cheating and handled accordingly.

#### Q2:
In the order2 scenario, we still found that the descriptions of four tasks contain taste attributes that do not belong to the predefined enum list. How should we handle these cases?
#### A2:
For the final evaluation, when selecting the 50–100 tasks to be included in the participant answer assessment, we will avoid choosing tasks with this issue. Therefore, there is no need to be overly concerned about the answers to these few tasks. You may handle them in whatever way you consider most appropriate.

### How to Run the Final Evaluation Scenarios (has released on 2026.06.16)

**Step 1**: Make sure your model configuration and environment variables are properly set (refer to the [Configuration](#configuration) section above).

**Step 2**: Run the final evaluation scenarios using the `--final_eval` flag:

```bash
bash run_all_scenarios.sh --final_eval
```

You can also limit the number of tasks per scenario for a quick test before running all tasks:

```bash
bash run_all_scenarios.sh --final_eval --num_tasks 5
```

**Step 3**: After execution completes, the interaction results will be saved under the `results/{model_name}/` directory:

```
results/
└── {model_name}/
    ├── retail6_easy.json
    ├── retail10_easy.json
    ├── kitchen4_easy.json
    ├── restaurant5_easy.json
    └── order2_easy.json
```

### Submission
Please rename the results/{model_name}/ folder containing the above 5 result files to results/{your_team_name}/ before submission. The submission email address is:


> **egolink.challenge@gmail.com**

Note: To increase the cost of manual tampering and reduce the possibility of human-edited interaction trajectories, we have released all examples from these five scenarios. However, during the final evaluation, we will only score a randomly selected subset of 50–100 tasks from them (the evaluated tasks will be the same for every participating team).

In addition, to ensure transparency and openness in the evaluation process, we plan to release the ground-truth answers for the finally selected evaluation tasks after the submission deadline, so that all participants can verify and inspect the results.

Submission requirements:

1. Only submit the interaction results for the final evaluation scenarios: retail6, retail10, kitchen4, restaurant5, and order2. Please keep the original file names and place these 5 result files under results/{your_team_name}/.

2. In addition to the result files, **all participants are required to submit a technical report**. We recommend that participants prepare this report in **ACM MM format** (official template: https://www.acm.org/publications/proceedings-template). **Due to the limited timeline, for the submission due by June 22, 2026 at 20:00 (GMT+8), we do not require participants to provide a fully polished technical report, nor do we strictly require the full 6 pages of main content.** Instead, the report should **focus on describing the implementation method**. The implementation details should include, but are not limited to: **the GitHub code repository link (required)**, the agent construction framework, the training method of the backbone/foundation model, experimental settings, and other essential details needed to reproduce the experiments.
   - The technical report should be named `{your_team_name}.pdf`.

3. Place the result folder and the technical pdf report into one folder, compress it, and send it as an email attachment.

4. The email subject and the attachment name must follow the format: {your_team_name}_track2.

5. After comprehensively evaluating the implementation approach, code quality, and benchmark results, teams with outstanding performance will be contacted by email **by June 23, 2026 at 20:00 (GMT+8)** and invited to **submit a complete and polished technical report in ACM MM format before 23:59 AOE on June 25, 2026**. The **official ACM MM submission link and detailed submission instructions will be provided in the invitation email**.

6. Each team is strongly encouraged to submit only once. If the same team submits multiple times, only the latest submission received before June 22, 2026 at 20:00 (GMT+8) will be considered. During the submission period, the organizers will not provide real-time feedback on the accuracy of your submitted answers. However, after receiving your email, we will send a confirmation of receipt within 24 hours. If you do not receive a reply within 24 hours, please feel free to contact us by email.

7. If you have any other questions or encounter any difficulties, please feel free to contact us by email at any time.

Example submission structure:

```
{your_team_name}_track2.zip
└──your_team_name.pdf
└──results/
    └──your_team_name/
        ├── retail6_easy.json
        ├── retail10_easy.json
        ├── kitchen4_easy.json
        ├── restaurant5_easy.json
        └── order2_easy.json

```



# EgoBench Competition - Participant Guide

We propose a framework for evaluating (MLLM) customer service agents (under test), which comprises an interaction sandbox and an automated evaluation pipeline. The interaction sandbox features a simulated user, a tool library, and a database. The simulated user is responsible for issuing tasks to the agents under test. In response, these agents can output two types of content within the sandbox: natural language responses for conversational engagement with the user, and tool calls that either retrieve information or modify the database as requested. Following each task interaction, the automated evaluation pipeline assesses performance by measuring tool-call accuracy and verifying the final state of the database.

![Figure 1](figure/fig1.png)

## Competition Overview

### Timeline

- **Offline Testing Phase**: 2026.05.18 - 2026.06.25
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

We have already implemented the prompts and corresponding framework for the simulated user; you only need to configure the specific deployment of the simulated user themselves, whether via local deployment or by using an API. Configure the model used to simulated user behavior.

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

> We need to ensure that our user's responses satisfy the following points. The simulated user is considered successful when the user completes all instructions without issues in the following dimensions:
> - **Role Consistency**: The user maintains their assigned role throughout the conversation
> - **Instruction Following & Anti-Hallucination**: The user follows the given instructions and does not generate hallucinated information
> - **Resilience & Anti-Interference**: The user is not misled by the agent's confusing responses
> - **Contextual Robustness**: The user maintains context and does not contradict previous statements

> We have evaluated various open-source models for simulating user behavior. The success rate (percentage of tasks where the user successfully completes all instructions) is as follows:

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

Service agents(under test) can output two types of content within the sandbox: natural language responses for conversational engagement with the user, and tool calls that either retrieve information or modify the database as requested.

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

| Scenario | Output Format |
|----------|---------------|
| Calling tools | JSON array only: `[{"tool_name": "...", "parameters": {...}}]` |
| Not calling tools | Natural language response only |

**Never mix formats** - Either output pure JSON OR pure natural language in a single response 

#### Video Storage Configuration

Choose how videos are accessed:

```python
# Option 1: Use local videos folder (default)
VIDEO_MODE = "local"
VIDEO_LOCAL_PATH = "./videos"

# Option 2: Use public URLs
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

Each JSON file contains:
- `task_id`: Task identifier
- `dialogue`: Conversation history between user and agent
- `tool_calls`: Tools invoked by the agent
- `rounds_count`: Number of dialogue rounds
- `input_tokens` / `output_tokens`: Token usage
- `execution_time_seconds`: Total execution time

### Evaluation Results

Evaluation results are saved to `eval_result/{model_name}/`:

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

## Update on Kitchen Scenario Ground Truth Fixes

We reviewed the relevant ground truth annotations across **all kitchen scenarios** and corrected confirmed quantity bugs, along with several ambiguous cases where the original instruction did not clearly specify the required amount.

### What was updated

- Corrected quantity errors in `add_to_shopping_list` annotations to make them consistent with:
  - recipe requirements,
  - inventory conditions,
  - ingredient categories,
  - storage locations,
  - and task semantics.
- Updated related function arguments where necessary (such as `compute_total_nutritions`) to keep them aligned with the corrected ingredient quantities.
- Revised ambiguous cases in which the instruction asked the agent to add ingredients to the shopping list but did not clearly define the quantity rule.

### Clarification on quantity interpretation

For Kitchen tasks, when an instruction refers to adding an ingredient according to the **original usage amount**, it means:

> the **total amount of that ingredient used in the recipe**

This refers to the total quantity required by the recipe, rather than the current stock level, remaining quantity, or the amount used in a single step.

### Notes

- These updates have been applied to the relevant Kitchen scenario annotations.
- The purpose of this revision is to improve consistency, correctness, and interpretability of quantity-related ground truth labels used for evaluation.


## Support

For issues or questions, please refer to the main documentation or contact the competition organizers.

## License

Released under the MIT License.
