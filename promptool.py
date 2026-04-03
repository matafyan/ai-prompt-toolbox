#!/usr/bin/env python3
"""
AI 提示词工具箱 - 命令行版
"""
import json
import os
import sys
import subprocess
from pathlib import Path

# 提示词数据
PROMPTS = {
    "writing": {
        "blog-intro": "你是一个专业博客写手。请为以下主题写一个引人入胜的开头段落（100字以内）：{topic}",
        "blog-outline": "请为主题 '{topic}' 设计一个完整的博客文章大纲，包含引言、3-5个主要章节、结论",
        "seo-title": "请为文章 '{topic}' 生成5个 SEO 友好的标题，要求包含关键词、吸引点击",
        "social-post": "请为产品 '{product}' 生成一段适合微信/微博的推广文案（100字以内），语气亲切有吸引力",
        "email-newsletter": "请写一封每周Newsletter的开场白，介绍本周的 {content_type}，语言简洁有温度",
        "product-desc": "请为产品 '{product}' 写一段产品描述（150字），突出核心卖点",
        "review-ask": "请写一段请求用户好评的文案（50字以内），引导用户给出五星好评",
        "faq-generate": "请为产品 '{product}' 生成10个常见问题及答案",
        "story-hook": "请为 '{topic}' 写一个抓人心的故事开头，吸引读者继续阅读",
        "copy-headline": "请为 '{product}' 生成10个广告标题，要求有冲击力、引发好奇",
        "video-desc": "请为视频 '{topic}' 写一段视频描述（200字），包含核心信息和行动号召",
        "ppt-outline": "请为主题 '{topic}' 设计一份PPT大纲，包含封面、目录、5页核心内容、总结"
    },
    "coding": {
        "code-review": "请审查以下代码，指出潜在问题和改进建议：\n```{language}\n{code}\n```",
        "refactor": "请重构以下代码，提高可读性和性能：\n```{language}\n{code}\n```",
        "explain-bug": "代码如下，请分析并解释这个 bug 的原因：\n```{language}\n{code}\n```",
        "write-test": "请为以下代码编写单元测试：\n```{language}\n{code}\n```",
        "write-doc": "请为以下代码生成详细的文档注释：\n```{language}\n{code}\n```",
        "sql-optimize": "请优化以下 SQL 查询：\n```{sql}\n```",
        "regex-gen": "请生成一个匹配 {pattern} 的正则表达式，并解释各部分含义",
        "algo-explain": "请用通俗易懂的方式解释以下算法/概念：{topic}",
        "debug-helper": "我遇到以下错误：\n{error}\n请帮我分析和解决",
        "api-design": "请为功能 '{feature}' 设计 RESTful API 接口，包含请求/响应格式"
    },
    "translate": {
        "en-to-zh": "请将以下英文翻译成中文，保持原文风格：\n{text}",
        "zh-to-en": "请将以下中文翻译成英文，保持专业风格：\n{text}",
        "formalize": "请将以下文本改写成更正式的风格：\n{text}",
        "casualize": "请将以下文本改写成更口语化的风格：\n{text}",
        "summarize": "请用3句话概括以下内容：\n{text}",
        "tone-adjust": "请将以下文本调整为中国市场风格：\n{text}",
        "localize": "请将以下内容本地化（适合 {region} 市场）：\n{text}",
        "proofread": "请校对以下英文文本的语法和用词：\n{text}"
    },
    "operation": {
        "user-persona": "请为产品 '{product}' 创建3个典型用户画像，包含人口统计、痛点、需求",
        "seo-keywords": "请为行业 '{industry}' 生成20个 SEO 关键词，按搜索热度排序",
        "content-calendar": "请为 {platform} 制定本月的 content calendar，包含每周主题和内容形式",
        "competitor-analysis": "请分析竞争对手 '{competitor}' 的优势、劣势和我们可以借鉴的点",
        "ads-copy": "请为产品 '{product}' 生成信息流广告文案，包含3个版本：吸睛版、痛点版、优惠版",
        "email-sequence": "请为一门课程 '{course}' 设计5封邮件的促销序列",
        "社群规则": "请为产品 '{product}' 的用户社群设计入群欢迎语和群规",
        "活动策划": "请为 '{event}' 策划一场线上活动，包含目标、流程、预算、预期效果",
        "kpi-analysis": "请分析以下数据指标，给出优化建议：\n{metrics}",
        "ugc-prompt": "请为产品 '{product}' 设计一个UGC征集活动方案"
    },
    "life": {
        "meal-plan": "请为 {person_count} 人家庭设计一周健康食谱，注意营养均衡",
        "travel-itinerary": "请为 {days} 天 {destination} 行程设计旅行计划，包含每日安排",
        "fitness-plan": "请为一个久坐上班族设计每周健身计划",
        "study-plan": "请为学习 '{topic}' 制定一个90天学习计划",
        "gift-idea": "请为 {occasion} 场合、受众 '{audience}' 推荐10个礼物选项",
        "interview-prep": "请帮我准备 {position} 岗位的面试，包含常问题目和答题思路",
        "meeting-agenda": "请为会议 '{meeting_name}' 起草议程和时间安排",
        "read-list": "请为想学习 {topic} 的人推荐5本入门书籍",
        "budget-plan": "请为月薪 {salary} 的年轻人制定理财规划",
        "home-decor": "请为 {room} 推荐家居装饰风格和单品推荐"
    }
}

CATEGORIES = {
    "writing": "写作辅助",
    "coding": "编程开发",
    "translate": "翻译",
    "operation": "运营营销",
    "life": "生活实用"
}

def list_categories():
    """列出所有分类"""
    print("\n📁 可用分类：\n")
    for cat, desc in CATEGORIES.items():
        count = len(PROMPTS.get(cat, {}))
        print(f"  {cat:12} - {desc} ({count}个)")
    print()

def list_prompts(category):
    """列出某分类下的所有提示词"""
    if category not in PROMPTS:
        print(f"❌ 未找到分类: {category}")
        return
    
    prompts = PROMPTS[category]
    print(f"\n📂 {CATEGORIES.get(category, category)} ({len(prompts)}个)：\n")
    for key in prompts.keys():
        print(f"  {key}")
    print()

def get_prompt(category, key):
    """获取指定提示词"""
    if category not in PROMPTS:
        return None, f"❌ 未找到分类: {category}"
    
    if key not in PROMPTS[category]:
        return None, f"❌ 未找到提示词: {key}"
    
    return PROMPTS[category][key], None

def copy_to_clipboard(text):
    """复制到剪贴板"""
    try:
        # macOS
        subprocess.run(['pbcopy'], input=text.encode(), check=True)
        return True
    except Exception:
        try:
            # Linux
            subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode(), check=True)
            return True
        except Exception:
            return False

def main():
    if len(sys.argv) == 1:
        print("""
🤖 AI 提示词工具箱

用法：
  promptool.py list                      查看所有分类
  promptool.py list <分类>               查看某分类下的提示词
  promptool.py get <分类> <提示词>       获取提示词内容
  promptool.py copy <分类> <提示词>      复制提示词到剪贴板
  promptool.py cat <分类> <提示词>       查看并填入占位符示例

示例：
  promptool.py list writing
  promptool.py copy writing blog-intro
  promptool.py get coding code-review
""")
        return

    cmd = sys.argv[1]

    if cmd == "list":
        if len(sys.argv) == 2:
            list_categories()
        else:
            list_prompts(sys.argv[2])
    
    elif cmd == "get":
        if len(sys.argv) < 4:
            print("❌ 用法: promptool.py get <分类> <提示词>")
            return
        category, key = sys.argv[2], sys.argv[3]
        prompt, err = get_prompt(category, key)
        if err:
            print(err)
        else:
            print(f"\n📝 {category}/{key}:\n")
            print(prompt)
            print()
    
    elif cmd == "copy":
        if len(sys.argv) < 4:
            print("❌ 用法: promptool.py copy <分类> <提示词>")
            return
        category, key = sys.argv[2], sys.argv[3]
        prompt, err = get_prompt(category, key)
        if err:
            print(err)
        elif copy_to_clipboard(prompt):
            print(f"✅ 已复制到剪贴板: {category}/{key}")
        else:
            print("❌ 复制失败，请手动复制：")
            print(prompt)
    
    elif cmd == "cat":
        if len(sys.argv) < 4:
            print("❌ 用法: promptool.py cat <分类> <提示词>")
            return
        category, key = sys.argv[2], sys.argv[3]
        prompt, err = get_prompt(category, key)
        if err:
            print(err)
        else:
            print(f"\n📝 {category}/{key} (含占位符示例):\n")
            print(prompt.format(topic="示例主题", product="示例产品"))
            print()
    
    else:
        print(f"❌ 未知命令: {cmd}")
        print("用 'promptool.py' 查看帮助")

if __name__ == "__main__":
    main()
