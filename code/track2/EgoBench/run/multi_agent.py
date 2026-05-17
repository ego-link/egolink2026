import os
import json
import time
import argparse
import sys
import concurrent.futures

# Add the project root directory to Python's module search path
current_file_path = os.path.abspath(__file__)
run_dir = os.path.dirname(current_file_path)
project_root = os.path.dirname(run_dir)
sys.path.insert(0, os.path.abspath(project_root))

# 1. Import initialization data
from tools.retail.retail_db import RetailDB
from tools.retail.retail_init import retail_init_data1, retail_init_data2, retail_init_data3, retail_init_data4, retail_init_data5, retail_init_data6, retail_init_data7, retail_init_data8, retail_init_data9, retail_init_data10
from tools.kitchen.kitchen_db import KitchenDB
from tools.kitchen.kitchen_init import kitchen_init_data
from tools.restaurant.restaurant_db import RestaurantDB
from tools.restaurant.restaurant_init import restaurant_init_data, restaurant_init_data5
from tools.order.order_db import OrderDB
from tools.order.order_init import order_init_data
from run.prompts import (
    USER_TEXT_ONLY_PROMPT_EASY,
    SERVICE_AGENT_PROMPT_BASE,
    USER_TURN_SUMMARY_PROMPT
)
from run.utils import (
    call_llm,
    execute_tool,
    check_tool_call,
    check_user_contradiction,
    build_message_with_image
)
from config.service_agent_config import get_video_path, VIDEO_MODE, SERVICE_MODEL_NAME


def get_video_url_for_model(video_url, model_name):
    """Return corresponding video URL based on model name and VIDEO_MODE"""
    if not video_url:
        return video_url

    import os
    video_filename = os.path.basename(video_url)

    if VIDEO_MODE == "local":
        return get_video_path(video_filename)
    else:
        return get_video_path(video_filename)


def run_simulation(input_path, tool_info_path, output_path, args=None, service_model_name="qwen3-vl-225b"):
    """
    Interactive Mode: Multi-round conversation (Easy mode only)
    """
    use_vision = False

    with open(tool_info_path, 'r', encoding='utf-8') as f:
        tools_list = json.load(f)
        tool_descriptions = json.dumps(tools_list, indent=2, ensure_ascii=False)

    if not os.path.exists(input_path):
        print(f"Can't find the file {input_path}.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

    if args.num_tasks > 0:
        scenarios = scenarios[:args.num_tasks]

    all_results = []

    for idx, sc in enumerate(scenarios):
        task_id = idx + 1

        print(f"\n{'='*20} Scenario {args.scenario}{args.scenario_number}: {task_id} {'='*20} ")
        if args.scenario == "retail":
            db = RetailDB()
            if args.scenario_number == 1:
                db.init_from_json(retail_init_data1)
            elif args.scenario_number == 2:
                db.init_from_json(retail_init_data2)
            elif args.scenario_number == 3:
                db.init_from_json(retail_init_data3)
            elif args.scenario_number == 4:
                db.init_from_json(retail_init_data4)
            elif args.scenario_number == 5:
                db.init_from_json(retail_init_data5)
            elif args.scenario_number == 6:
                db.init_from_json(retail_init_data6)
            elif args.scenario_number == 7:
                db.init_from_json(retail_init_data7)
            elif args.scenario_number == 8:
                db.init_from_json(retail_init_data8)
            elif args.scenario_number == 9:
                db.init_from_json(retail_init_data9)
            elif args.scenario_number == 10:
                db.init_from_json(retail_init_data10)
        elif args.scenario == "kitchen":
            db = KitchenDB()
            db.init_from_json(kitchen_init_data)
        elif args.scenario == "restaurant":
            db = RestaurantDB()
            if args.scenario_number == 5:
                db.init_from_json(restaurant_init_data5)
            else:
                db.init_from_json(restaurant_init_data)
        elif args.scenario == "order":
            db = OrderDB()
            db.init_from_json(order_init_data)

        user_instruction = sc.get("Instruction", "")
        image_path = sc.get("image_path", None)
        image_path = get_video_url_for_model(image_path, args.service_model_name)
        image_description = sc.get("image_description", "")

        start_time = time.time()

        history_log = {
            "task_id": task_id,
            "mode": "text",
            "instruction": user_instruction,
            "image_description": image_description,
            "dialogue": [],
            "tool_calls": [],
            "rounds_count": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "tool_calls_count": 0,
            "user_response_time_seconds": 0.0,
            "agent_response_time_seconds": 0.0,
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        }

        user_agent_sys_prompt = USER_TEXT_ONLY_PROMPT_EASY.format(
            user_instruction=user_instruction,
            image_description=image_description,
            original_user_response="",
            evaluation_feedback="",
            history_summary="",
            service_agent_response="Dear customer, how can I help you?"
        )

        user_messages = [
            {"role": "system", "content": user_agent_sys_prompt},
            {"role": "user", "content": "You are a customer in the environment shown in the video, and you need to complete the instructions in **Task**. I am your AI customer service representative; please interact with me in the first person. Let's begin the conversation.\nDear customer, how can I help you?"}
        ]

        service_agent_sys_prompt = SERVICE_AGENT_PROMPT_BASE.format(tool_descriptions=tool_descriptions)
        service_history = []

        max_turns = 10
        rounds_count = 0
        input_tokens_total = 0
        output_tokens_total = 0
        tool_calls_count = 0

        accumulated_original_scores = {}
        accumulated_final_scores = {}
        valid_evaluation_count = 0

        last_agent_response_for_check = "Dear customer, how can I help you?"
        summarized_history_str = ""

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

        for turn in range(max_turns):
            user_start_time = time.time()
            user_reply, user_input_tok, user_output_tok = call_llm(user_messages, agent_type="user", service_model_name=args.service_model_name)
            user_gen_time = time.time() - user_start_time
            print(f"[Time] User response generation (Turn {turn}): {user_gen_time:.3f} seconds")
            history_log["user_response_time_seconds"] += user_gen_time

            evaluation_info = None
            check_start_time = time.time()
            if args.multi_agent_user:
                original_user_reply = user_reply
                user_reply, evaluation_info = check_user_contradiction(
                    user_response=original_user_reply,
                    user_instruction=user_instruction,
                    image_description=image_description if not use_vision else "",
                    multi_agent_user=args.multi_agent_user,
                    last_agent_response=last_agent_response_for_check,
                    history=history_log["dialogue"],
                    summarized_history=summarized_history_str if getattr(args, "summary_user", False) else None,
                    user_mode="easy"
                )

                if evaluation_info:
                    print(f"\n[User Response Evaluation]")
                    if "scores" in evaluation_info:
                        print(f"  Original Scores: {json.dumps(evaluation_info['scores'], ensure_ascii=False)} (Average: {evaluation_info.get('average_score', 'N/A')})")
                    if "corrected_scores" in evaluation_info:
                        print(f"  Corrected Scores: {json.dumps(evaluation_info['corrected_scores'], ensure_ascii=False)} (Average: {evaluation_info.get('corrected_average_score', 'N/A')})")
                    if "reasoning" in evaluation_info:
                        print(f"  Original Reasoning: {json.dumps(evaluation_info['reasoning'], ensure_ascii=False, indent=2)}")
                    if "corrected_reasoning" in evaluation_info:
                        print(f"  Corrected Reasoning: {json.dumps(evaluation_info['corrected_reasoning'], ensure_ascii=False, indent=2)}")

                    if "scores" in evaluation_info:
                        valid_evaluation_count += 1
                        original_scores_dict = evaluation_info["scores"]
                        final_scores_dict = evaluation_info.get("corrected_scores", original_scores_dict)

                        for k, v in original_scores_dict.items():
                            try:
                                accumulated_original_scores[k] = accumulated_original_scores.get(k, 0.0) + float(v)
                            except ValueError:
                                pass

                        for k, v in final_scores_dict.items():
                            try:
                                accumulated_final_scores[k] = accumulated_final_scores.get(k, 0.0) + float(v)
                            except ValueError:
                                pass
                if user_reply != original_user_reply:
                    print(f"User Response Corrected: {user_reply}")

            check_time = time.time() - check_start_time
            if args.multi_agent_user:
                print(f"[Time] Check phase (Turn {turn}): {check_time:.3f} seconds")
                history_log["user_response_time_seconds"] += check_time

            print(f"Final User Response: {user_reply}")

            log_entry = {"role": "user", "turn": turn, "content": user_reply}
            if evaluation_info:
                log_entry["evaluation"] = evaluation_info

            history_log["dialogue"].append(log_entry)

            if "STOP" in user_reply:
                print("Stop signal detected")
                break

            service_history.append({"role": "user", "content": user_reply})
            user_messages.append({"role": "assistant", "content": user_reply})

            current_user_reply_for_task = user_reply
            current_agent_response_for_task = last_agent_response_for_check
            current_service_history = [msg for msg in service_history]
            current_summarized_history = summarized_history_str

            def generate_summary_task():
                if not getattr(args, "summary_user", False):
                    return None

                sum_start_time = time.time()
                sum_prompt = USER_TURN_SUMMARY_PROMPT.format(
                    user_instruction=user_instruction,
                    agent_response=current_agent_response_for_task,
                    user_response=current_user_reply_for_task,
                    previous_summary=current_summarized_history if current_summarized_history else "None"
                )
                print(f"Generating dialogue summary (Turn {turn})...")
                sum_msgs = [{"role": "user", "content": sum_prompt}]
                turn_summary, _, _ = call_llm(sum_msgs, agent_type="user", service_model_name=args.service_model_name)
                sum_time = time.time() - sum_start_time
                print(f"[Time] Summary generation (Turn {turn}): {sum_time:.3f} seconds")
                print(f"Turn {turn} Summary: {turn_summary}")
                return turn_summary

            def process_agent_task():
                agent_start = time.time()
                inner_input_tokens = 0
                inner_output_tokens = 0
                inner_calls = 0
                inner_rounds = 0
                agent_final_reply = ""
                local_tool_logs = []
                local_dialogue_logs = []
                local_service_history = [msg for msg in current_service_history]
                total_tool_calls_so_far = tool_calls_count

                while True:
                    current_service_msgs = [{"role": "system", "content": service_agent_sys_prompt}]
                    for i, msg in enumerate(local_service_history):
                        if i == 0 and msg["role"] == "user":
                            current_service_msgs.append({
                                "role": "user",
                                "content": build_message_with_image(msg["content"], image_path, use_vision=True, service_model_name=args.service_model_name)
                            })
                        else:
                            current_service_msgs.append(msg)

                    if args.service_model_name == "manual":
                        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] --- Manual Service Agent Turn ---")
                        print("Latest User Input:")
                        if service_history and service_history[-1]["role"] == "user":
                            print(service_history[-1]["content"])
                        print("Enter your response (text or JSON tool calls). Type 'END' on a new line to finish:")
                        ml_input = []
                        while True:
                            try:
                                line = input()
                                if line.strip() == "END":
                                    break
                                ml_input.append(line)
                            except EOFError:
                                break
                        agent_reply = "\n".join(ml_input)
                        agent_input_tokens = 0
                        agent_output_tokens = 0
                    else:
                        agent_reply, agent_input_tokens, agent_output_tokens = call_llm(current_service_msgs, agent_type="service", service_model_name=args.service_model_name)
                        inner_input_tokens += agent_input_tokens
                        inner_output_tokens += agent_output_tokens
                    print(f"Tested Agent: {agent_reply}")

                    is_tool, tool_call_obj = check_tool_call(agent_reply)

                    if is_tool:
                        if isinstance(tool_call_obj, list):
                            inner_calls += len(tool_call_obj)
                        else:
                            inner_calls += 1

                        tool_results = execute_tool(db, tool_call_obj)

                        local_tool_logs.append({
                            "turn": turn,
                            "calls": tool_call_obj if isinstance(tool_call_obj, list) else [tool_call_obj],
                            "results": tool_results
                        })

                        result_strings = []
                        for res in tool_results:
                            result_strings.append(res.get("content", str(res)))
                        combined_result = "; ".join(result_strings)

                        local_service_history.append({"role": "assistant", "content": agent_reply})
                        local_service_history.append({"role": "user", "content": f"Tool execution result: {combined_result}"})

                        if total_tool_calls_so_far + inner_calls > 200:
                            print(f"Tool calls count ({total_tool_calls_so_far + inner_calls}) exceeded 200, stopping interaction.")
                            agent_final_reply = "[Interaction stopped: tool calls exceeded 200]"
                            break

                        continue
                    else:
                        inner_rounds += 1
                        local_dialogue_logs.append({"role": "agent", "turn": turn, "content": agent_reply})
                        local_service_history.append({"role": "assistant", "content": agent_reply})
                        agent_final_reply = agent_reply
                        break

                agent_time = time.time() - agent_start
                print(f"[Time] Agent response generation (Turn {turn}): {agent_time:.3f} seconds")
                return {
                    "reply": agent_final_reply,
                    "input_tokens": inner_input_tokens,
                    "output_tokens": inner_output_tokens,
                    "calls": inner_calls,
                    "rounds": inner_rounds,
                    "tool_logs": local_tool_logs,
                    "dialogue_logs": local_dialogue_logs,
                    "time": agent_time,
                    "updated_history": local_service_history
                }

            future_summary = executor.submit(generate_summary_task)
            future_agent = executor.submit(process_agent_task)

            turn_summary = future_summary.result()
            agent_res = future_agent.result()

            input_tokens_total += agent_res["input_tokens"]
            output_tokens_total += agent_res["output_tokens"]
            tool_calls_count += agent_res["calls"]
            rounds_count += agent_res["rounds"]
            history_log["agent_response_time_seconds"] += agent_res["time"]
            history_log["tool_calls"].extend(agent_res["tool_logs"])
            history_log["dialogue"].extend(agent_res["dialogue_logs"])
            service_history = agent_res["updated_history"]

            last_agent_response_for_check = agent_res["reply"]

            if getattr(args, "summary_user", False) and turn_summary:
                summarized_history_str = f"Turn {turn} Dialogue Summary of completed steps: {turn_summary}\n"

            user_agent_sys_prompt = USER_TEXT_ONLY_PROMPT_EASY.format(
                user_instruction=user_instruction,
                image_description=image_description,
                original_user_response="",
                evaluation_feedback="",
                history_summary=summarized_history_str,
                service_agent_response=last_agent_response_for_check
            )

            user_messages[0]["content"] = user_agent_sys_prompt

            if getattr(args, "summary_user", False) and turn_summary:
                next_content = f"Please continue the conversation in the first person according to the original settings based on the summary and latest response."
                user_messages = [
                    {"role": "system", "content": user_agent_sys_prompt},
                    {"role": "user", "content": build_message_with_image(next_content, image_path, use_vision)}
                ]
            else:
                user_messages.append({"role": "user", "content": last_agent_response_for_check})

        executor.shutdown(wait=True)

        history_log["rounds_count"] = rounds_count
        history_log["input_tokens"] = input_tokens_total
        history_log["output_tokens"] = output_tokens_total
        history_log["tool_calls_count"] = tool_calls_count

        user_performance = {}
        if valid_evaluation_count > 0:
            for k, v in accumulated_original_scores.items():
                user_performance[f"original_{k}_avg"] = round(v / valid_evaluation_count, 2)
            for k, v in accumulated_final_scores.items():
                user_performance[f"final_{k}_avg"] = round(v / valid_evaluation_count, 2)
        history_log["user_performance"] = user_performance

        end_time = time.time()
        execution_time = round(end_time - start_time, 3)
        history_log["execution_time_seconds"] = execution_time
        all_results.append(history_log)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\nCompleted! Results saved to: {output_path}")
    print(f"Statistics Summary: ")
    for idx, result in enumerate(all_results):
        print(f"  Task {idx+1}: {result['rounds_count']} dialogue rounds, {result['input_tokens']} input tokens, {result['output_tokens']} output tokens, {result['tool_calls_count']} tool calls, {result['execution_time_seconds']} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run dialogue simulation in easy mode")
    parser.add_argument(
        "--service_model_name",
        default=SERVICE_MODEL_NAME,
        help="Tested agent model name (default: configured in service_agent_config.py)"
    )

    parser.add_argument(
        "--scenario",
        choices=["retail", "kitchen", "restaurant", "order"],
        default="retail",
        help="Task scenario"
    )

    parser.add_argument(
        "--scenario_number",
        type=int,
        default=1,
        help="Scenario number"
    )

    parser.add_argument(
        "--multi_agent_user",
        action="store_true",
        help="When True, use LLM to check if user response contradicts the task and correct if contradictory"
    )

    parser.add_argument(
        "--summary_user",
        action="store_true",
        help="When True, add a summary module after the user answers to avoid lengthy history information"
    )

    parser.add_argument(
        "--num_tasks",
        type=int,
        default=0,
        help="Number of tasks to test from the beginning of the scenario. 0 means test all tasks."
    )

    args = parser.parse_args()

    INPUT_JSON = f"./scenarios/final/{args.scenario}{args.scenario_number}.json"
    TOOL_INFO_JSON = f"./tools/{args.scenario}/{args.scenario}_tools.json"
    OUTPUT_JSON = f"./results/{args.service_model_name}/{args.scenario}{args.scenario_number}_easy.json"
    if not os.path.exists(os.path.dirname(OUTPUT_JSON)):
        os.makedirs(os.path.dirname(OUTPUT_JSON))

    run_simulation(INPUT_JSON, TOOL_INFO_JSON, OUTPUT_JSON, args=args, service_model_name=args.service_model_name)
