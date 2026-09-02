# EDGE：以反事实验证的错误依赖图做多 Agent 失败归因

## 基本信息

- **论文标题**：EDGE: Error Dependency Graph-Guided Multi-Error Attribution in Multi-Agent LLM Systems
- **作者**：Jun Hou, Priya Pitre, Yi Fang, Xuan Wang
- **首次公开日期**：2026-09-01
- **当前版本日期**：2026-09-01（v1）
- **发表信息**：EMNLP 2026
- **arXiv**：[2609.01360](https://arxiv.org/abs/2609.01360)
- **DOI**：[10.48550/arXiv.2609.01360](https://doi.org/10.48550/arXiv.2609.01360)（DataCite 注册待完成）
- **代码**：截至 v1 未在 arXiv 页面提供公开代码链接

## 一句话结论

EDGE 不再把长轨迹失败简化为单一根因，而是先建错误依赖图、再用反事实 rollout 验证其中的因果子图，可为 trajectory verifier 提供比整段 LLM Judge 更可靠的多错误信用结构。

## 真正新增的内容

**论文原文结论**：Agent 失败常包含相互依赖的多个错误；EDGE 从观测到的错误事件构图，通过干预式反事实 rollout 验证可靠因果子集，再用推断图指导两阶段 LLM-as-a-Judge detector。经验证的子图还用于解释和修复分析。

相较 Who&When、责任 Agent/步骤定位或单根因分类，新增的是显式表示“错误 A 如何导致错误 B”，并将纯 Judge 推断与环境干预证据分层。

## 核心方法

先从多 Agent 轨迹抽取错误事件与候选依赖边；对候选边进行替换、修复或移除等反事实重放，保留能改变下游错误的关系。推断阶段利用图结构分两步完成错误类别归因；解释和修复建议优先依据 intervention-validated subgraph，而不是全部模型猜测边。

## 关键实验结果

**论文报告**：在 TRAIL 与 MAST 上，EDGE 在大多数被评模型和设置中提高 category-level 多错误归因；把图加入改造后的 Who&When 风格 prompt 后，在多种 prompting 策略下仍有收益。arXiv 摘要没有给出统一提升幅度，因此不把“多数设置提升”外推为所有模型、所有错误类型都稳健。

## 证据质量与局限

论文已被 EMNLP 2026 接收，并跨两个基准和多种提示策略比较，证据中等偏强。主要限制是候选错误事件本身可能由 LLM 抽取而遗漏；反事实 rollout 若环境非确定、修复不局部或存在不可观测状态，不能保证识别真实因果。无公开代码链接也增加复现成本。

## 最接近的相关工作

最接近 Who&When、TRAIL、MAST、LongRCA、AgenticRAG-FP，以及 coding-agent 过程评估的三层测量。相较仅用语义相关性或时间先后预测责任，EDGE 用执行干预筛选因果边；相较单步 value，它表达多个错误之间的传播。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：将图中每条边的置信度建模为序数/概率分布，而不是硬保留；同一前缀构造 A=原动作、B=局部修复、T=两者终局无显著差异，以环境重放生成 pairwise 标签。generative verifier 先给候选错误/critique，programmatic runner 决定其是否进入高置信 teacher 集。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：从整轨迹单分数改为节点错误概率与边传播概率；只对反事实支持的边做高权重蒸馏。
- **A/B/T/序数**：用修复/不修复重放形成 A/B/T；多次随机环境重放输出效果大小分布。
- **真值门控**：环境终态和干预结果决定因果方向，LLM Judge 只生成候选与软类别。
- **critique states**：student 生成错误图和修复 critique，再通过局部重放验证；失败 critique 作为 hard negative。
- **探索**：若多个修复分支效果置信区间重叠，保留并行探索，不按单次 Judge 分数剪枝。
- **sealed eval**：冻结隐藏错误注入、干预脚本与人工根因标签，避免 detector 与图生成器共同适配训练集。