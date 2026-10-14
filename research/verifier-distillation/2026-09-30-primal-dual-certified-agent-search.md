# 用 Primal–Dual 证书审计 LLM Program Search

- **论文标题**：Auditing LLM Program Search for Bermudan Stopping with Primal--Dual Certificates
- **作者**：Yuhua Qian
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.14063
- **代码**：论文摘要未给出公开链接
- **标识符**：arXiv:2610.14063；DOI: https://doi.org/10.48550/arXiv.2610.14063

## 一句话结论

当 Agent 直接优化搜索分数时，可信 evaluator、上下界证书、冻结选择后的 holdout 与失败计数能揭示“看似改进”其实未超过统计不确定性。

## 真正新增的内容

**论文原文结论**：作者在 Bermudan option 的 Python 策略搜索中让可信 evaluator 持有模拟器和对偶上界，审计 24 次生成、六组反馈/记忆消融及冻结后 holdout；没有被选程序稳定超过 Ridge LSMC，holdout gap 与基线相差不超过 0.002。结构化记忆在该消融中无收益。

**分析推断**：这是 sealed eval 的小规模、证书化反例：闭环 reward 改善不能替代独立上界/下界与冻结后验证。

## 核心方法

- 用 primal 下界与 dual 上界夹住最优策略差距，并报告 Monte Carlo 误差。
- 比较反馈表示和记忆方式。
- 先冻结选择，再在 holdout 上评估，并保留初始参考与失败尝试。

## 关键实验结果

- 24 次生成中无稳定、超出 Monte Carlo 不确定性的改进。
- holdout gap 分数距 Ridge LSMC 不超过 0.002。
- 一维 put 中估计 gap 的 99% 来自 dual bound 松弛。

## 证据质量与局限

证书和冻结 holdout 提供高质量反证，但样本仅 24 次、领域单一，且 dual bound 在改进尺度上过松；不能外推到所有 coding agent。

## 最接近的相关工作

与 AutoTuneBench、Ground-truth-as-code、Reality Is the Final Verifier、ImpossibleRubrics 以及 reward hacking 监测工作相近。

## 如何复用或推进 LLM-as-a-Verifier

- 为可程序验证任务记录 reward、可信下界、可信上界及统计误差。
- 只有当改进超出证书/重采样区间时，才作为强 A/B teacher 信号。
- 无法分辨时输出 T，而不是将极小分差硬排序。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：将 sealed eval 明确拆成“冻结候选选择”和“独立证书结算”。score-level OPD 中硬真值/证书决定更新方向，LLM verifier 只能在证书未覆盖维度调节幅度。高熵分叉需计入失败和未选分支，避免只汇报 winner。student critique 若不能指出可复现证书或环境事实，不进入高权重蒸馏集。