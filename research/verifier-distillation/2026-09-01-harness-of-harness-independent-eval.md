# Harness-of-Harness：面向多日 Coding Agent 的持续改进与独立评测

## 基本信息

- **论文标题**：Harness-of-Harness: Multi-Day Autonomous Software Development with Continual Improvement
- **作者**：Haoyang Yan, Min-le Su, Hangfan Zhang, Zhanhao Li, Chen Zhang, Shao Zhang, Yang Chen, Lei Bai, Shuyue Hu
- **首次公开日期**：2026-09-01
- **当前版本日期**：2026-09-01（v1）
- **arXiv**：[2609.01481](https://arxiv.org/abs/2609.01481)
- **DOI**：[10.48550/arXiv.2609.01481](https://doi.org/10.48550/arXiv.2609.01481)（DataCite 注册待完成）
- **代码**：[Flesymeb/HarnessOfHarness](https://github.com/Flesymeb/HarnessOfHarness)
- **项目页**：[Harness-of-Harness](https://flesymeb.github.io/HarnessOfHarness/)

## 一句话结论

HoH 证明长时程 Agent 的持续改进需要把实现期测试与独立评测分离，并把大目标拆成可验证增量；它不是 verifier 蒸馏算法，但给 sealed eval 与轨迹级信用边界提供了强工程模板。

## 真正新增的内容

**论文原文结论**：HoH 作为现有 coding-agent harness 的上层控制器，把执行组织为反复的规划—编码—测试循环，同时平衡修复和能力增长、逐步暴露交付物/工具/技能、鼓励复用并保存版本历史。核心设计之一是明确分离实现期测试和独立评价，约束可验证输出而非规定内部工作流。

对 verifier 研究真正新增的是多日、几十轮条件下的“外层 harness”结构：每轮可形成可回放的状态、局部目标、实现结果和独立验收，为轨迹级 verifier 提供天然切片。

## 核心方法

外层控制器将需求拆成小而可验证的增量，在每轮为底层 coding agent 配置角色工具与已有资产；测试反馈进入下一轮规划，同时保留项目版本历史。修复已知缺陷与扩展新能力被显式平衡。独立评价不直接参与实现决策。

## 关键实验结果

**论文报告**：在 GameCraft-Bench、FrontierSWE、ProgramBench 上，以 Codex+GPT-5.5、OpenCode+DeepSeek-V4-Pro、Pi+MiniMax-M3 三种组合测试；三轮后相对独立 harness 平均提升 52.25%，最高 82.86%。一个超过 70 轮的多日部署构建了可供人游玩的第一人称射击游戏。结果说明外层迭代机制跨多个 harness/model 有效，但最终大型游戏案例主要是系统展示。

## 证据质量与局限

证据覆盖三个基准和三种组合，且代码公开，工程可信度较好。局限是相对增益受基线起点影响；论文不以 verifier 蒸馏为目标，也没有直接训练 score/critique 模型。多轮中的测试可能逐步泄露评测结构，只有真正冻结、隔离的外部验收才能排除 evaluator 共适应。

## 最接近的相关工作

接近 SWE-agent/Codex harness、SBCO、EnvHarness、LongWoF-Bench、Thinkingbox 与 Task-CoEvolve。与这些工作相比，HoH 更聚焦将任意底层 harness 置于长期外循环，并把实现测试—独立评价边界写入系统结构。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：把每轮版本差分、测试新增/修复、回归与独立验收构造成轨迹对：A=旧版本，B=新版本，T=无法确定或混合回归。训练 verifier 预测“下一轮是否提升 sealed eval”，而不是预测实现期测试分数。版本历史还能生成反事实 critique state：移除某条建议重放后，比较最终验收变化。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：以轮级 sealed improvement 作为蒸馏门，teacher 评分仅解释哪类变更贡献最大。
- **A/B/T/序数**：对相邻版本建 pairwise/tie 标签，并用通过项、回归项、未覆盖项形成序数分布。
- **真值门控**：编译、测试、运行时状态和最终交付物检查先做硬门；LLM verifier 只评价软质量。
- **critique states**：将计划、测试失败归因、修复理由保存为可执行版本关联的 critique，而非脱离环境的文本。
- **探索**：在多个可行实现分叉上保留并行分支，直到独立验收能区分；避免内部测试首胜即收缩。
- **sealed eval**：冻结隐藏测试与评价 harness，禁止训练期根据其失败逐轮修补；报告实现测试与 sealed 指标的差距。