# CivBench：300+ 轮 MCP Agent 的长期规划与承诺执行评测

## 基本信息

- **论文标题**：CivBench: A Long-Horizon Benchmark for Tool-Mediated Agents in Civilization VI
- **作者**：Austin Tudor David Andrews, Liam Wilkinson, Jamie Heagerty, Harry Coppock, Jakob Nicolaus Foerster, Rui Ponte Costa
- **首次公开日期**：2026-09-02
- **当前版本日期**：2026-09-02（v1）
- **arXiv**：[2609.02459](https://arxiv.org/abs/2609.02459)
- **DOI**：[10.48550/arXiv.2609.02459](https://doi.org/10.48550/arXiv.2609.02459)（DataCite 注册待完成）
- **代码/环境/日志**：[lmwilki/civ6-mcp](https://github.com/lmwilki/civ6-mcp)

## 一句话结论

CivBench 提供单局 300+ 轮、数千次工具调用和 76 个 MCP 工具的可回放环境，并用主动状态监控率与“计划承诺十步内兑现率”暴露长时程 Agent 的知道—做到鸿沟。

## 真正新增的内容

**论文原文结论**：该基准不是用 23 次 pilot run 排模型名次，而是刻画部分可观测、大动作空间、延迟后果下的接口行为。PMR 测 Agent 是否主动查询潜在战略状态；RAG@10 测 structured reflection 中写下的近期承诺是否在后续十轮执行。

新增价值是同时释放环境、scenario、全日志、指标和分析管线，并把宏观成败拆成可以从真实工具轨迹确定性计算的过程指标。

## 核心方法

Civilization VI 状态经 narration layer 转成结构化文本，Agent 通过 76 个 MCP 工具观察和行动。单局超过 300 轮并生成数千调用。共享 playbook 要求周期性监测关键状态和结构化规划；分析器从日志计算查询频率、败局前警告窗口和承诺兑现率。

## 关键实验结果

**论文报告**：四个模型家族共 23 个有效 run，作者明确称为 pilot、不能可靠区分模型。尽管 playbook 要求每 20 轮查询 victory progress，实际间隔为 30–75 轮；20 个可检测败局中有 7 个在结束前 20 轮警告窗口内未查询。各模型 RAG@10 为 48.2%–65.8%，显示近半承诺可能未及时执行。

## 证据质量与局限

轨迹深度、开放环境和完整工件很有价值，但样本只有 23 局，作者正确避免排名和能力归因。游戏环境虽复杂，仍受 narration、playbook、随机性和 Civilization 特定机制影响；PMR/RAG@10 衡量的是受指令条件下偏差，不证明模型没有潜在能力，也不直接等价于最终贡献度。

## 最接近的相关工作

接近长时程 CivBench（Civilization V）、LongRCA、Thinkingbox、LongWoF-Bench、Parsing the Stream 与 trajectory process evaluation。区别在于它使用真实 MCP 接口并提供 300+ 轮连续执行，尤其适合检测计划—行动失配。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：将每次 planning reflection 解析为未来十步义务清单，程序 tracker 计算兑现/延迟/撤销；LLM verifier 只评估承诺是否合理及撤销解释。PMR 和 RAG@10 可作为低层硬信号，训练序数 process verifier 预测“推进、停滞、偏航、可恢复”的分布。下一步动作贡献度可结合状态势能变化和是否完成既有承诺。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：用每十轮窗口的监控与兑现分数蒸馏，不等待整局终局。
- **A/B/T 与序数分布**：同一游戏状态比较多个行动分支；长期效果重叠时保留 T。
- **真值门控**：MCP 日志、游戏状态和承诺 tracker 提供程序真值；Judge 评价战略软质量。
- **critique states**：structured reflection 是天然 student critique state，可用后十步兑现结果监督。
- **高熵探索**：部分可观测状态下不能只保留即时高分动作，应维持多步战略分叉。
- **sealed eval**：使用隐藏地图、文明、胜利条件和随机种子；冻结分析管线，避免针对 PMR/RAG@10 表面刷分。