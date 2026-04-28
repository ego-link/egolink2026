from typing import List, Dict, Optional, Any
import json
import requests

# ===================== 评测服务器地址（比赛时统一提供） =====================
BENCHMARK_SERVER = "http://比赛服务器地址/api/agent/interact" 
TIMEOUT = 30


class AgentBenchmark:
    def __init__(self, server_url: str = BENCHMARK_SERVER):
        self.server_url = server_url
        self.session = requests.Session()

    def step(self, candidate_id: str, scenario: str, scenario_id: str, use_tools: bool, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        【唯一核心接口】智能体调用此方法进行单轮交互
        :param candidate_id: 参赛者ID
        :param scenario_id: 当前场景ID
        :param task_id: 当前场景下具体任务ID
        :param use_tools: 如果是true，代表最新一轮交互内容为工具调用json list，; 如果是false, 代表最新一轮的交互内容是给用户的回话string。只能选其一。
        :param messages: 当前episode历史交互轮列表(需要参赛者自己维护)，最终以"assistant"角色结尾。格式
            [
                {"role": "assistant", "content": "第一轮智能体给服务端发出的用户的输出内容"}, 
                {"role": "user", "content": "第一轮服务端返回的用户回复的内容"},
                {"role": "assistant", "content": [{"第一轮智能体给服务端发出的调用工具的json list"}]}
                {"role": "tools", "content": "第一轮服务端返回的调用工具执行结果"}  # 工具返回结果用此角色
                ...
                ...以上都是当前这个episode历史交互记录
                {"role": "assistant", "content": "智能体最新一轮生成的要发给服务端的交互信息"}
            ]
        
        :return: 评测服务端返回 { "stop": bool, "role": "user/tools", "content": str }
        """
        # 修正：使用正确的参数名，完整传递接口要求的所有字段
        payload = {
            "candidate_id": candidate_id,
            "scenario_id": scenario_id,
            "task_id": task_id,
            "use_tools": use_tools,
            "messages": messages
        }

        try:
            resp = self.session.post(
                self.server_url,
                json=payload,
                timeout=TIMEOUT,
                headers={"Content-Type": "application/json"}
            )
            resp.raise_for_status()
            return resp.json()

        except Exception as e:
            return {
                "stop": True,
                "role": "error",
                "content": f"接口调用失败：{str(e)}"
            }

    @staticmethod
    def is_terminated(response: Dict[str, Any]) -> bool:
        """判断是否结束本轮对话（STOP）"""
        return response.get("stop", False)


# ===================== 参赛者调用示例 =====================
if __name__ == "__main__":
    # 初始化接口
    env = AgentBenchmark()

    # 1. 设定参数（严格匹配接口要求）
    candidate_id = "your_test_id"  # 参赛者ID（必填）
    scenario_id = "retail1"           # 场景ID
    task_id = "1"              # 题目ID
    use_tools = False              # 是否使用工具

    # 2. 初始交互消息（角色规范：assistant 为智能体）
    messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

    # 3. 一个episode中包含多轮（round）交互：自动持续交互直到 stop=True 
    # 4. 一个任务的episode最多支持10轮agent-user交互（以服务端返回user的次数计数，针对tool call的服务端返回不算交互轮数）
    round_num = 1  # 记录交互轮数
    is_stop = False
    while not is_stop:
        print(f"\n===== 第 {round_num} 轮交互开始 =====")
        
        # 调用单轮交互接口
        resp = env.step(
            candidate_id=candidate_id,
            scenario=scenario,
            scenario_id=scenario_id,
            use_tools=use_tools, 
            messages=messages
        )

        # 打印当前轮返回结果
        print("当前返回结果：")
        print(json.dumps(resp, ensure_ascii=False, indent=2))
        is_stop = env.is_terminated(resp)
        print(f"是否终止对话：{is_stop}")
        # 判断是否终止：stop=True 则退出循环
        if is_stop:
            print("\n===== 当前episode对话已终止，结束所有交互 =====")
            # 此时，可以将messages中的当前episode的所有历史记录清空，下一次新的episode开启之后，messages中从新开始维护交互历史。

        # 将服务器返回的消息追加到历史列表（必须维护）
        messages.append({
            "role": resp["role"],
            "content": resp["content"]
        })
        
        # 自行实现智能体返回结果
        new_agent_message = get_next_message(messages)
        
        # 将新结果添加进对话messages中, 位于列表的最后
        messages.append({
            "role": "assistant",
            "content/tools_call": new_agent_message
        })
        #如果在新交互内容生成时同时包含了content和tools_call两个信息，只处理tools_call信息。

        # 轮数+1，继续下一轮
        round_num += 1

    # 最终打印当前episode完整的交互历史
    print("\n===== 完整交互历史 =====")
    print(json.dumps(messages, ensure_ascii=False, indent=2))