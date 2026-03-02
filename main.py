import arxiv
import google.generativeai as genai
import datetime
import os

# 安全读取你在 GitHub Secrets 里配置的密钥
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("未找到 API 密钥，请检查 GitHub Secrets！")

genai.configure(api_key=GOOGLE_API_KEY)

# 已升级为 Gemini 3.1 Pro 模型
model = genai.GenerativeModel('gemini-3.1-pro')

def get_latest_papers(topic="Large Language Models", max_results=2):
    print(f"正在检索关于 {topic} 的最新论文...")
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers_data = []
    for result in search.results():
        papers_data.append({
            "title": result.title,
            "abstract": result.summary,
            "url": result.entry_id,
        })
    return papers_data

def generate_summary(paper):
    print(f"正在研读论文：{paper['title']} ...")
    prompt = f"""
    You are an expert academic researcher. Please analyze the following paper metadata.
    Title: {paper['title']}
    Abstract: {paper['abstract']}
    Requirements:
    1. Translate title to Simplified Chinese.
    2. Summarize core content (100-150 words) in Chinese.
    3. List exactly 3 key innovation points.
    4. Provide 2-3 tags.
    5. Output strictly in Markdown format.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"解读失败，错误信息：{e}"

def main():
    papers = get_latest_papers(topic="LLM", max_results=2)
    daily_report = f"# 📅 AI 前沿论文日报 ({datetime.date.today()})\n\n"
    
    for paper in papers:
        summary = generate_summary(paper)
        daily_report += f"{summary}\n🔗 原文链接: {paper['url']}\n---\n\n"
        
    print("\n==================== 生成结果 ====================\n")
    print(daily_report)

if __name__ == "__main__":
    main()
