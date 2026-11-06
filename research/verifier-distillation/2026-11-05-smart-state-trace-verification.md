# SMART: State-based Multi Agent Reasoning Traces for Verification-oriented Problem-Solving

- **作者**：Sai Vallurupalli, Francis Ferraro
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.08196
- **DOI**：https://doi.org/10.48550/arXiv.2611.08196
- **代码**：论文页面未给出公开代码链接

## 一句话结论

SMART 让多 Agent 先构造参与实体的结构化“状态前提”，再以现实知识验证和筛选这些前提；在三类科学 claim validation 上最高提升 20%，其中 grounding 本身贡献最高 5%。

## 真正新增的内容

它不是直接让 Judge 对完整自由文本推理打分，而是把隐式世界状态外化为多 Agent 生成的、互补且与解答相关的 premises，并在进入最终推理前进行现实知识 grounding。

## 核心方法

不同角色/模型从问题上下文推断实体状态，聚合并筛选成多样、互补、solution-salient 的结构化 premises；用现实知识验证这些 premises，再以其引导最终 claim validation。

## 关键实验结果

在 3 个复杂科学 claim 数据集上，SMART 的知识引导推理最高提升 **20%** validation performance；消融显示 real-world grounding 最高贡献 **5%**。

## 证据质量与局限

**论文原文结论**：跨三数据集，并对 grounding 有独立消融。  
**局限**：摘要未给出全部基线、方差和具体指标；任务多为静态 claim，而非长时程环境交互；“现实验证”若仍由同源 LLM 完成，可能残留相关错误；未公开代码。

## 最接近的相关工作

最接近的是 generative verifier、evidence-grounded critique、PaperDoctor、DENSE、multi-agent debate 与结构化 state tracking。

## 如何复用或推进 LLM-as-a-Verifier

把 student-generated critique state 规范为可核验字段：实体、时刻、属性、证据指针、来源与置信度。仅将通过独立检索、工具或环境 oracle 的 premises 写入 verifier memory；未验证项保留为分布而非事实。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 可蒸馏“状态前提质量分布 + 终局 verdict”，避免单一分数隐藏证据错误。
2. pairwise A/B/T 可比较两个轨迹的状态账本；证据不足或状态不可观测时标 T。
3. critique states 应以结构化 premise 为单位，并经过程序/环境真值门控。
4. 高熵分叉可由多个互斥但尚未证伪的 state hypotheses 驱动，保留探索。
5. sealed eval 要用独立证据源和隐藏状态核验，防止多 Agent 只是形成相关共识。