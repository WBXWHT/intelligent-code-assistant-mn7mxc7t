import json
import time
import requests
from datetime import datetime
from typing import Optional, Dict, Any

class IntelligentCodeAssistant:
    """智能代码助手核心类"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1/chat/completions"):
        """
        初始化助手
        :param api_key: API密钥
        :param base_url: API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def code_completion(self, code_snippet: str, language: str = "python") -> Optional[str]:
        """
        代码补全功能
        :param code_snippet: 代码片段
        :param language: 编程语言
        :return: 补全后的代码
        """
        prompt = f"""你是一个专业的{language}程序员。请补全以下代码，只返回补全后的完整代码：
        
{code_snippet}

补全要求：
1. 保持代码风格一致
2. 添加必要的注释
3. 确保代码可运行"""
        
        return self._call_gpt(prompt)
    
    def code_review(self, code_snippet: str, language: str = "python") -> Optional[str]:
        """
        代码评审功能
        :param code_snippet: 代码片段
        :param language: 编程语言
        :return: 评审意见
        """
        prompt = f"""你是一个资深的{language}代码审查专家。请评审以下代码，指出潜在问题并提供改进建议：
        
{code_snippet}

评审要点：
1. 代码规范与风格
2. 潜在bug与性能问题
3. 安全性考虑
4. 可读性与维护性"""
        
        return self._call_gpt(prompt)
    
    def _call_gpt(self, prompt: str) -> Optional[str]:
        """
        调用GPT API
        :param prompt: 提示词
        :return: API响应内容
        """
        try:
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                print(f"API调用失败: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"网络请求异常: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"响应解析异常: {e}")
            return None
    
    def log_usage(self, action: str, code_length: int):
        """
        记录使用情况（模拟）
        :param action: 操作类型
        :param code_length: 代码长度
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "code_length": code_length,
            "status": "success"
        }
        print(f"[使用日志] {json.dumps(log_entry, ensure_ascii=False)}")

def main():
    """主函数 - 智能代码助手演示"""
    
    # 注意：实际使用时需要替换为有效的API密钥
    API_KEY = "sk-your-api-key-here"  # 请替换为实际API密钥
    
    # 初始化助手
    assistant = IntelligentCodeAssistant(API_KEY)
    
    print("=" * 50)
    print("智能代码助手 v1.0")
    print("=" * 50)
    
    # 示例1: 代码补全演示
    print("\n[演示1] 代码补全功能")
    print("-" * 30)
    
    incomplete_code = """def calculate_fibonacci(n):
    \"\"\"计算斐波那契数列\"\"\"
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib = [0, 1]
        # 请补全这里的代码"""
    
    print("输入代码片段:")
    print(incomplete_code)
    print("\n补全结果:")
    
    completed_code = assistant.code_completion(incomplete_code, "python")
    if completed_code:
        print(completed_code)
        assistant.log_usage("code_completion", len(incomplete_code))
    
    # 示例2: 代码评审演示
    print("\n[演示2] 代码评审功能")
    print("-" * 30)
    
    code_to_review = """def process_data(data):
    result = []
    for i in range(len(data)):
        item = data[i]
        if item > 100:
            result.append(item * 2)
        else:
            result.append(item)
    return result"""
    
    print("待评审代码:")
    print(code_to_review)
    print("\n评审意见:")
    
    review_result = assistant.code_review(code_to_review, "python")
    if review_result:
        print(review_result)
        assistant.log_usage("code_review", len(code_to_review))
    
    print("\n" + "=" * 50)
    print("演示结束 - 感谢使用智能代码助手")
    print("=" * 50)

if __name__ == "__main__":
    main()