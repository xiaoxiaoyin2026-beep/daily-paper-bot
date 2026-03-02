import arxiv
from google import genai
import datetime
import os
import requests

# 安全读取你在 GitHub Secrets 里配置的密钥
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("未找到 API 密钥，请检查 GitHub Secrets！")

# 使用全新版 SDK 初始化客户端
client = genai.Client(api_key=GOOGLE_API_KEY)
MODEL_ID = 'gemini-2.0-flash'

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
    # Europe PMC 官方接口，同时覆盖 PubMed (MED) 和预印本如 bioRxiv (PPR)
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    query_str = f'("{topic}") AND (SRC:MED OR SRC:PPR)'
    
    params = {
        "query": query_str,
        "format": "json",
        "resultType": "core",
        "pageSize": max_results,
        "sort": "P_DATE_D" # 按发布日期倒序
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
    # 汇总各路数据（ArXiv 抓取 2 篇，PubMed/bioRxiv 抓取 3 篇，可自行调整）
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
    # 设定我们关注的核心交叉学科关键词
    SEARCH_TOPIC = "gene expression prediction"
    
    papers = get_latest_papers(topic=SEARCH_TOPIC)
    daily_report = f"# 📅 基因表达量预测·前沿论文日报 ({datetime.date.today()})\n\n"
    
    for paper in papers:
        summary = generate_summary(paper)
        daily_report += f"**[来源: {paper['source']}]**\n"
        daily_report += f"{summary}\n🔗 原文链接: {paper['url']}\n---\n\n"
        
    print("\n==================== 生成结果 ====================\n")
    print(daily_report)

if __name__ == "__main__":
    main()
