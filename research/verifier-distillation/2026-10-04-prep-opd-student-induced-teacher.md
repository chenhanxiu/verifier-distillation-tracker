# How Should Teachers Be Prepared? RL on Student-Induced States for On-Policy Distillation

- 作者：Xiaoyu Ma、Haoyue Liu、Zhichao Wang、Jionghao Zhu、Xiaoying Tang
- 首次公开日期：2026-10-04
- 当前版本日期：2026-10-04（v1）
- arXiv：2610.04950
- 原始论文：https://arxiv.org/abs/2610.04950
- Canonical URL：https://doi.org/10.48550/arXiv.2610.04950
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】Prep-OPD 先在固定 student 前缀上用终局正确性强化 teacher 的接管与纠错能力，再让该 teacher 蒸馏 student；“会独立解题”并不等于“会从 student 错误状态教起”。

## 真正新增的内容

【论文原文】teacher preparation 的训练分布明确来自 student-induced states，而非题目起点；优化目标是 teacher continuation 的最终答案正确性，随后再用于轨迹指导和 token-level OPD。

## 核心方法

【论文原文】收集 student 生成前缀，固定前缀对 teacher continuation 做 RL；准备后的 teacher 在这些状态上产生指导并进行 token 监督。作者还比较 problem-start teacher RL、有/无 handoff 的控制组。

## 关键实验结果

【论文原文】八个数学推理基准上，4B teacher→1.7B student 相对标准 OPD 平均提高 8.28 点，相对 Relay-OPD 提高 2.30 点；同一 prepared teacher 也改善 0.6B student。

## 证据质量与局限

【论文原文】有多基准、两种 student 尺度和受控 teacher-RL 对照。局限是最终答案正确性对中间过程约束较弱；数学环境可验证性高，尚未覆盖工具副作用；teacher 在特定 student 状态训练后可能过拟合该 student 分布。

## 最接近的相关工作

最接近 Persistent Teacher Anchoring、RC-OPD、STRIDE，以及 PACT 对 critic–student policy 错位的分析。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】不仅要训练 verifier 评一般轨迹，还要在当前 student 真正访问的失败/歧义状态上做校准；以环境结算训练 verifier 的接管、纠错和 abstention 能力。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：【分析推断】teacher/verifier 先做 student-state adaptation，再蒸馏 score。
- **A/B/T 与序数分布**：【分析推断】同一 student 前缀下多 continuation 形成 A/B/T，并由终局验证校准。
- **硬真值门控**：【分析推断】teacher preparation 的 reward 必须来自程序或环境成功。
- **critique states**：【分析推断】prepared teacher 适合生成针对当前错误前缀的 critique，而非通用参考解释。
- **高熵探索**：【分析推断】训练 teacher 在异常分支恢复，但保留多种经验证的 continuation。
- **sealed eval**：【分析推断】使用新 student checkpoint 和未见状态检验 teacher 是否真正泛化。
