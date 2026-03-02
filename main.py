import arxiv
import datetime
import os
import requests
from google import genai
import time

# 1. 密钥读取
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("未找到 GOOGLE_API_KEY 环境变量，请检查 GitHub Secrets！")

client = genai.Client(api_key=GOOGLE_API_KEY)
# 切回 Gemini 3.1 Pro 模型
MODEL_ID = "gemini-3.1-pro"

def get_arxiv_papers(topic, max_results=2):
    print(f"正在检索 ArXiv (计算机方向) ...")
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    arxiv_client = arxiv.Client()
    papers = []
    for result in arxiv_client.results(search):
        papers.append({
            "title": result.title,
            "abstract": result.summary,
            "url": result.entry_id,
            "source": "ArXiv"
        })
    return papers

def get_epmc_papers(topic, max_results=3):
    print(f"正在检索 PubMed/bioRxiv (生信医学方向) ...")
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    query_str = f'("{topic}") AND (SRC:MED OR SRC:PPR)'
    params = {
        "query": query_str,
        "format": "json",
        "resultType": "core",
        "pageSize": max_results,
        "sort": "P_DATE_D"
    }
    papers = []
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("resultList", {}).get("result", [])
        for res in results:
            source_db = res.get("source", "EPMC")
            ext_id = res.get("id", "")
            papers.append({
                "title": res.get("title", ""),
                "abstract": res.get("abstractText", "该论文未提供摘要文本。"),
                "url": f"https://europepmc.org/article/{source_db}/{ext_id}",
                "source": f"PubMed/bioRxiv"
            })
    except Exception as e:
        print(f"生物医学数据库检索失败: {e}")
    return papers

def get_latest_papers(topic="gene expression prediction"):
    papers = []
    papers.extend(get_arxiv_papers(topic, max_results=2))
    papers.extend(get_epmc_papers(topic, max_results=3))
    return papers

def generate_summary(paper):
    print(f"正在研读论文：{paper['title']} ...")
    prompt = f"""
    You are an expert academic researcher in Bioinformatics. 
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
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"解读失败，错误信息：{e}"

def main():
    SEARCH_TOPIC = "gene expression prediction"
    papers = get_latest_papers(topic=SEARCH_TOPIC)
    
    daily_report = f"# 📅 基因表达量预测·前沿论文日报 ({datetime.date.today()})\n\n"
    
    for paper in papers:
        summary = generate_summary(paper)
        daily_report += f"**[来源: {paper['source']}]**\n"
        daily_report += f"{summary}\n🔗 原文链接: {paper['url']}\n---\n\n"
        time.sleep(5) # 保护 API 速率限制
        
    print("\n==================== 生成结果 ====================\n")
    print(daily_report)

if __name__ == "__main__":
    main()
