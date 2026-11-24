# VeriLogic: Reinforcement Learning over Verifiable Logical Reasoning Traces

- **作者**：ZeLiang Chen, Yunyao Zhang, Xinglang Zhang, Wenbing Li, Junqing Yu, Zikai Song
- **首次公开日期**：2026-11-22
- **版本日期**：2026-11-22（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.29147
- **DOI**：https://doi.org/10.48550/arXiv.2611.29147
- **代码**：未见作者在 arXiv 摘要页给出独立代码链接

## 一句话结论

将推理拆为可形式检查的判断、证明与终局决策，再以全局/局部 verifier 奖励和错误信息修复，可显著优于只奖励最终答案。

## 真正新增的内容

**论文原文结论**：提出 Grounding–Optimization–Refinement 三阶段，把内部推理轨迹变成可验证、可学习、可修复的对象。  
**分析推断**：这提供了“程序真值定方向、生成式 critique 定修复”的完整闭环，但形式逻辑域的 verifier soundness 不能直接外推到开放 Agent 环境。

## 核心方法

构建带显式中间状态与可形式检查 proof obligation 的环境；Logical Structured Policy Optimization 同时使用全局与局部 verifier reward；迭代修复利用 proof state 和 error message 诊断失败路径。

## 关键实验结果

在 6 个逻辑推理 benchmark 上均优于强基线；Qwen3 与 Llama-3.1 的平均提升分别为 6.39% 和 5.00%。

## 证据质量与局限

多 benchmark、两模型族和硬验证器使结果较扎实。局限是逻辑任务可形式化，开放工具 Agent 的规范缺口、环境噪声和不可判定状态更复杂；摘要未给各模块消融与统计区间。

## 最接近的相关工作

最接近 CoVer 的 GT-anchored verifier、ContrAgent 的 LTLf/DFA、Beyond Solver Verdicts 的 oracle-to-generative verifier，以及 PaperDoctor 的证据指针式修复。

## 如何复用或推进 LLM-as-a-Verifier

将 Agent 轨迹表示为 obligation graph：每步 action 产生可检查义务、局部 verdict 和错误 certificate；generative verifier 负责解释/修复，程序 verifier 保留最终否决权。可将局部 verdict 蒸馏成 ordinal process score。

## 对 Agent verifier × OPD 实验路线的具体影响

score-level OPD 应在 obligation 节点而非任意 token 上对齐；A/B/T 分别表示证明成立、反例成立、无法判定。student-generated critique 只有附带可复现 proof/error state 才进入训练。高熵分叉优先选择 obligation 不同的分支；sealed eval 使用冻结规范与独立验证器，暴露 specification gap。