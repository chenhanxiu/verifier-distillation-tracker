# Certified Selective Automation of LLM Agent Evaluation

- **作者**：Chengguang Gan, Yunhao Liang, Qinghao Zhang, Shiwen Ni
- **首次公开日期**：2026-09-28
- **版本日期**：2026-09-28（v1）
- **原始论文**：https://arxiv.org/abs/2609.34320
- **代码**：未在 arXiv 页面提供

## 一句话结论

【论文原文】Agent 自动评价必须按任务簇而非轨迹 i.i.d. 做误差认证；task-level bootstrap 可在目标错误预算下证明哪些轨迹能安全自动判，其余交给人工。

## 真正新增的内容

【论文原文】论文把问题从 Judge 平均准确率改为“在错误率预算 α 下可自动化多少”，并指出同任务多 Agent 轨迹强相关，朴素证书会严重高估安全覆盖。其证书还可用于控制伪标签污染。

## 核心方法

1. 按 task cluster 重采样构造选择性判断证书。\n2. 训练 4B logprob Judge，并用 SFT 与 reject-weighted GRPO 优化。\n3. 只自动判定落入认证区域的轨迹。\n4. 将认证区域内输出作为有污染上界的自训练伪标签。

## 关键实验结果

【论文原文】朴素证书声称 98% 自动化时，在 17.5% task resample 中真实错误超预算。task-level bootstrap 在所有测试 regime 有效。α=0.1 时，4B Judge 在 tool-use/web corpora 认证覆盖 0.30–0.59；六次伪标签 harvest 的实际污染为 0–0.041。

## 证据质量与局限

【论文原文】直接针对 Agent 数据的聚类依赖并报告覆盖—风险，工程价值高。局限是 bootstrap 仍依赖任务簇代表性；“认证”针对观测分布与当前 Judge，不等于对新环境或对抗策略的形式保证。

## 最接近的相关工作

最接近 Robust Conformal Consensus、JEV selective routing、Agent 轨迹可诊断性与 ClaimReceipt；区别是显式处理同任务轨迹相关性。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】在你的 3,800 case 中以 case/task 为簇，而不是把多模型、多次 rollout 当独立样本；输出认证自动判定区、人工复核区和 abstain 区，并限制自动伪标签污染。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：只在认证区域蒸馏 teacher score。\n- **A/B/T 与序数分布**：未认证样本输出 T/人工路由，而非硬判。\n- **真值门控**：认证依赖独立人工/程序标签。\n- **Critique states**：仅认证 critique 可进入自训练池。\n- **探索**：高熵状态保留但不自动判定。\n- **Sealed eval**：按 task cluster 做 bootstrap，禁止轨迹级随机拆分泄漏。
