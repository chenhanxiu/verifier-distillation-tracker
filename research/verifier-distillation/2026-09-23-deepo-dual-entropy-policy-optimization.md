# DEEPO: Dual-Entropy Enhanced Policy Optimization for Hallucination in MLLMs

## 基本信息

- **作者**：Yingxuan Zhuang、Miao Pan、Wangjie Gan、Jingxiao Yang、Fan Wang、Weiming Liu、Cheng Tan、Xuhong Zhang、Jintao Chen
- **首次公开日期**：2026-09-23
- **版本日期**：2026-09-23（v1）
- **原始论文**：https://arxiv.org/abs/2609.28570
- **DOI**：https://doi.org/10.48550/arXiv.2609.28570
- **代码**：论文页面未给出公开仓库

## 一句话结论

DEEPO 同时修补“高语义熵问题全组答错导致零优势”和“高置信错误 token 梯度消失”，为高熵 Agent 分叉提供了 teacher 介入与梯度修正的双层模板。

## 真正新增的内容

【论文原文】把 hallucination 的纠正链分成 rollout 信号缺失与优化饱和两处：以语义熵触发 expert prefix，为全错组注入有根据的 continuation；再用按 advantage 符号调整的 Rényi 预条件，让更新触达高置信错误 token。

【分析推断】它不是 verifier distillation 本身，但给出了“何时调用 teacher”与“如何避免错误置信度吞掉梯度”的可迁移机制，直接补足高熵分叉下的 OPD 门控。

## 核心方法

【论文原文】第一支路对高语义熵查询注入专家前缀，恢复组内 advantage 方差；第二支路用 advantage-sign-aware Rényi preconditioning 抵消 categorical policy 在尖锐分布下的梯度范数衰减。

【分析推断】在 Agent 中可把“查询语义熵”替换为状态分叉熵、verifier 分歧和 recoverability 风险的组合，只对无法由环境自救的分叉调用 teacher。

## 关键实验结果

【论文原文】两支路单独均优于 GRPO；在最复杂的长时程 VideoMMMU 上交互项提升 4.0 点，95% 置信区间为 [1.1, 6.9]，其他任务近似相加；作者报告 hallucination 下降且准确率和训练稳定性得以保持。

## 证据质量与局限

有置信区间且包含分支消融，证据强于只报最佳值；但主要是多模态问答而非真实工具 Agent，expert prefix 的正确性、调用成本和 teacher 污染风险未由独立环境 oracle 充分覆盖。

## 最接近的相关工作

接近 SAGE 的熵触发教师、AC-OPD 的有限 continuation、EPIG-Tree 的分叉预算和 Unified Per-Token OPD Gating。DEEPO 的独特点是把 rollout 级零方差与 token 级梯度饱和联合处理。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】让 verifier 输出 `P(A), P(B), P(T)` 与序数风险分布；高熵且非 T 的状态触发 teacher continuation，环境可执行检查决定 advantage 符号，Rényi/温度项只控制幅度。teacher prefix 未通过真值门控时不得写入 critique memory。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- 把“全组失败率”和“高置信错误率”加入 score-level OPD 诊断。
- 对高熵分叉先自采样，再有限 teacher prefix，避免过早收缩探索。
- 程序真值定正负方向，verifier 分布与 teacher 熵只定更新强度。
- sealed eval 单独测 hallucination、任务成功率和 abstention，防止只优化同源 Judge。