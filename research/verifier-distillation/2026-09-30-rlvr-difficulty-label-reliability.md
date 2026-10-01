# Unlearnable, or Unmeasured? On the Reliability of Difficulty Labels in RLVR

- **作者**：Chandak Chakma, Syed Nazmus Sakib, Nafiul Haque, Shifat E. Arman
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2609.40115
- **代码**：未发现公开代码链接

## 一句话结论

所谓 RLVR“不可学习”样本仍以约可学习样本三分之一的速度改善，而有限 rollout 得到的难度标签本身高度不稳定。

## 真正新增的内容

【论文原文】跨 seed 合并采样不一定只减少噪声，还会改变被选为困难样本的集合。作者提出采样框架量化标签复现性与所需评测量，并指出部分梯度差异源于困难题正确 rollout 更少。

【分析推断】用稀疏 success rate 给高熵 Agent 状态贴“难例/不可学”标签，可能误导分叉预算和 teacher 路由；应保存难度后验而非硬分组。

## 核心方法

重复抽样估计 prompt 难度标签稳定性和所需样本量；控制正确 rollout 数量后重新分析梯度相似度证据。

## 关键实验结果

【论文原文】被称为不可学习的 prompt 仍改善，速度约为可学习组的三分之一；匹配正确 rollout 样本数会削弱但不能完全消除梯度差异。摘要未给统一准确率增益。

## 证据质量与局限

重点是测量再分析，纠正了选择偏差；但摘要未说明跨模型、长轨迹环境和非二元 reward 的覆盖，困难度仍依赖具体采样策略。

## 最接近的相关工作

One-Shot OPD、Data-free OPD、EPIG-Tree、Belief-Shift Branching、DEEPO。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 输出任务/状态难度的 posterior 与置信区间，按期望信息价值分配额外 rollout，达到复现阈值后才用于课程或蒸馏门控。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：难度只作不确定性特征，不能直接决定 teacher 权重。
- **A/B/T 与序数分布**：样本不足的难度比较应标 T，保留 beta/ordinal 后验。
- **硬真值门控**：用真实执行 success，但同时报告采样误差。
- **student-generated critique states**：不要因少量失败将 critique state 永久判为不可恢复。
- **高熵分叉**：分叉预算依据信息价值和置信区间，而非一次硬标签。
- **sealed eval**：预注册采样量、seed 合并规则和难度阈值，避免事后选组。
