# Teacher-Student Gaps Are Not Enough: Outcome-Guided On-Policy Distillation for Multi-Turn Autonomous Agents

- **作者**：Tong Zhang, Zhou Liu, Yihao Liu, Jiahua Bao, Xuchen Li, Honglin Lin, Tao Cheng, Zhihan Yu, Kai Tang, Xiaoxi Jiang, Guanjun Jiang
- **首次公开日期**：2026-09-28
- **版本日期**：2026-09-28（v1）
- **原始论文**：https://arxiv.org/abs/2609.35319
- **代码**：未在 arXiv 页面提供

## 一句话结论

【论文原文】OG-OPD 证明 teacher–student token gap 并不等于监督收益，并用成对 student continuation 的最终结果校准 teacher 监督权重。

## 真正新增的内容

【论文原文】论文揭示 supervision-benefit mismatch：大 gap 可能无害，小 gap 却可能决定成败；teacher 偏好动作也可能把当前 student 带入其无法完成的后继状态。新增点是用当前 student 的可执行终局收益，而非局部 gap，判断 teacher 指导是否值得加强。

## 核心方法

1. 在多轮 Agent rollout 中记录 teacher–student gap。\n2. 对关键 turn 构造原始/teacher-guided 的成对 student continuation。\n3. 用最终任务结果估计 teacher 指导对当前 student 的实际收益。\n4. 以 trajectory-relative 权重回标原始轨迹上的蒸馏损失。

## 关键实验结果

【论文原文】在 ALFWorld、ScienceWorld、WebShop 的多种设置中，成功率比 vanilla OPD 高 3.6–17.7 个百分点，比最强基线最高高 7.0 点。

## 证据质量与局限

【论文原文】直接覆盖三类多轮 Agent 环境并使用成对 continuation，因果指向比单纯相关 gap 更强。局限是反事实 rollout 昂贵且有采样方差；只校准当前 policy，对快速漂移的 student 需反复重估；未验证开放式 Judge 任务。

## 最接近的相关工作

最接近 TISD、AC-OPD、Legibility is Not Interpretability 与反事实 rollout advantage；区别是明确以当前 student 的终局可执行性作为监督收益。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 A/B 分支都交回同一 student 执行，使用环境结算产生 A/B/T；teacher 只提议动作，最终 score-level 更新由实际 outcome 差决定。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：按 paired outcome benefit 重加权，而非按 logit gap。\n- **A/B/T 与序数分布**：成对 continuation 可直接生成 A/B/T，并保留置信区间。\n- **真值门控**：环境结果决定监督方向。\n- **Critique states**：teacher critique 需由 student 后续执行验证。\n- **探索**：gap 大但 outcome 等价时保留 student 路径。\n- **Sealed eval**：用于权重校准的 continuation 与最终评测分离。
