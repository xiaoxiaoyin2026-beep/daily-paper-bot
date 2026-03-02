🤖 Daily AI Paper Bot (全自动学术文献推送机器人)

 A - 案例简介 (About the Project)
本项目是一个全自动的学术交叉学科（计算机与生信医学）文献研读与推送机器人。系统每天早上 8 点（北京时间）自动运行，跨平台检索最新论文，利用大语言模型（LLM）将其翻译为通俗易懂的中文并提炼核心创新点，最终生成排版精美的结构化日报推送到个人微信端。
This project is a fully automated academic cross-disciplinary (Computer Science and Bioinformatics/Medicine) literature reading and push bot. The system runs automatically at 8:00 AM (Beijing Time) every day, retrieves the latest papers across platforms, uses Large Language Models (LLM) to translate them into plain Chinese and extract core innovations, and finally generates a beautifully formatted daily report pushed to WeChat.

 B - 部署指南 (Build & Deployment)
1. Fork 本仓库：将本仓库克隆到你自己的 GitHub 账号下。
2. 配置安全密钥：进入仓库的 `Settings` -> `Secrets and variables` -> `Actions`，点击 `New repository secret`，添加以下两个环境变量：
    `GOOGLE_API_KEY`：填入你的 ChatAi 第三方中转 API 密钥（兼容 OpenAI SDK）。
    `PUSHPLUS_TOKEN`：填入你从 PushPlus 官网获取的一对一微信推送令牌。
3. 激活工作流：进入 `Actions` 面板，点击 `Daily AI Paper Digest`，手动执行一次 `Run workflow` 即可激活每日定时任务。
1. Fork this repository: Clone this repository to your own GitHub account.
2. Configure Security Secrets: Go to the repository's `Settings` -> `Secrets and variables` -> `Actions`, click `New repository secret`, and add the following two environment variables:
    `GOOGLE_API_KEY`: Enter your ChatAi third-party proxy API key (compatible with OpenAI SDK).
    `PUSHPLUS_TOKEN`: Enter your one-to-one WeChat push token obtained from the PushPlus website.
3. Activate Workflow: Go to the `Actions` panel, click `Daily AI Paper Digest`, and manually execute `Run workflow` once to activate the daily scheduled task.

 C - 核心特性 (Core Features)
 多数据源融合：同时对接 `ArXiv`（专注底层算法框架）与 `Europe PMC`（覆盖 PubMed 及 bioRxiv 生信医学文献），打破学科壁垒。
 AI 深度研读：接入基于 OpenAI 格式的第三方 `gemini-3.1-pro` 旗舰大模型，精准提炼每篇文献的 3 大核心创新点，拒绝无效机翻。
 零成本免运维：完全依托 GitHub Actions 的免费云端算力，彻底告别本地服务器部署与维护成本。
 Multi-source Integration: Simultaneously connects to `ArXiv` (focusing on underlying algorithm frameworks) and `Europe PMC` (covering PubMed and bioRxiv bioinformatics/medical literature), breaking disciplinary barriers.
 AI Deep Reading: Integrates the third-party `gemini-3.1-pro` flagship model based on the OpenAI format to accurately extract the 3 core innovation points of each paper, rejecting invalid machine translation.
 Zero-cost & Maintenance-free: Relies entirely on the free cloud computing power of GitHub Actions, completely saying goodbye to local server deployment and maintenance costs.

 D - 定制修改 (DIY Customization)
如果你希望让机器人关注其他研究领域，只需打开 `main.py` 文件，找到 `main()` 函数中的核心变量进行修改即可：
 修改 `SEARCH_TOPIC = "gene expression prediction"` 为你专属的研究方向（如 "single cell RNA-seq" 或 "graph neural networks"）。
 调整 `get_arxiv_papers(max_results=2)` 和 `get_epmc_papers(max_results=3)` 中的数字，以控制每天想要阅读的论文篇数。
If you want the bot to focus on other research fields, simply open the `main.py` file and modify the core variables in the `main()` function:
 Change `SEARCH_TOPIC = "gene expression prediction"` to your specific research direction (e.g., "single cell RNA-seq" or "graph neural networks").
 Adjust the numbers in `get_arxiv_papers(max_results=2)` and `get_epmc_papers(max_results=3)` to control the number of papers you want to read every day.
