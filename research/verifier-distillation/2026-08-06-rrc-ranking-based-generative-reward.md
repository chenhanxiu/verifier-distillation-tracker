# RRC：用排序构造释放生成式奖励模型的 RL 能力

## 基本信息

- **论文标题**：RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction
- **作者**：Chenglong Wang、Ziming Zhu、Yifu Huo、Bei Li、Qiaozhi He、Yan Ding、Xiaoyang Hao、Yuxin Gao、Tianhua Zhou、Xiaojia Chang、Tongran Liu、Jingbo Zhu、Zhengtao Yu、Tong Xiao
- **首次公开日期**：2026-08-06
- **版本日期**：2026-08-06（arXiv v1）
- **arXiv ID**：2608.06310
- **原始论文**：https://arxiv.org/abs/2608.06310
- **DOI**：https://doi.org/10.48550/arXiv.2608.06310（arXiv/DataCite，论文页标注待注册）
- **代码**：https://github.com/wangclnlp/RRC
- **记录类型**：scheduler 新发现

## 一句话结论

RRC 认为生成式奖励模型的原生输出是“谁优于谁”的比较判断，而不是可靠的绝对标量；它将多响应 pairwise 排名转成 GRPO 可用的相对奖励，比直接使用 preference-token 概率更有效，直接对应现有方案中的 pairwise A/B/T、score-level verifier distillation 与锚点校准。

## 真正新增的内容

### 论文原文结论

1. 通过受控实验指出：generative reward model（GRM）在 RM-Bench/JudgeBench 排序上优于 discriminative RM，但把偏好 token 概率直接当作 RL 标量奖励时，这个优势明显缩小。
2. 提出 Ranking-based Reward Construction（RRC），完全从相对排序构造标量奖励，不依赖偏好 token 的概率值。
3. 提供两种机制：
   - **Self-Competitive Ranking（SCR）**：当前 policy 的多条响应两两比较，以胜场数形成奖励；
   - **Anchor-Guided Ranking（AGR）**：将响应与少量稳定 reference-policy anchors 比较，以战胜锚点数量形成奖励。
4. 通过 majority voting 与 conflict-aware ranking adjustment 缓解生成式 judge 的随机性和循环偏好。
5. 展示增加 judge 投票次数与 anchor 数量可提升训练结果，但收益递减，anchor 过多甚至可能轻微退化。

### 分析推断

RRC 不是 verifier distillation 本身，而是一个非常实用的“比较式 verifier → 可优化 reward”接口。它提醒我们不要把 generative verifier 的 A/B token 概率误当作校准后的绝对质量分；更合理的做法是保留比较结构，再用 Bradley–Terry、序数后验或锚点位置将其映射到 score-level signal。

## 核心方法

SCR 对同一输入采样 (m) 条当前 policy 响应，让 GRM 判断每一对响应的偏好关系；响应 (o_i) 的奖励为胜场数乘缩放系数：

[
r(x,o_i)=alphasum_{j
eq i}mathbf 1[o_isucc o_j].
]

论文用多次随机 judge 投票聚合边，并对互相冲突、会形成环的偏好进行 conflict-aware 调整，得到一致的 tournament ranking。

AGR 为每个输入从固定 reference policy 生成 (n) 个 anchor。每个当前响应仅与 anchors 比较：

[
r(x,o_i)=alphasum_{k=1}^{n}mathbf 1[o_isucc a_k].
]

这样以固定锚点避免 reward scale 随当前 policy 共漂移，并把比较成本控制为 (O(mn))。构造的相对奖励可直接接入 GRPO/DAPO。

## 关键实验结果

### 论文报告

- RM backbone：LLaMA-3.2-3B-Instruct 与 LLaMA-3.1-8B-Instruct；policy：LLaMA-3.1-8B-Instruct，并在 Qwen2.5-7B 上补充验证。
- RM 数据：HelpSteer3 的 40.5K 偏好样本；RL 数据约 7.5K。
- 评估包括 AlpacaEval2、ArenaHardV2、WildBench、MMLU-Redux、MATH-500；policy 同时测试带/不带显式 thinking。
- 8B GRM、thinking policy 下：
  - probability-based reward construction：AlpacaEval2 **35.8**、ArenaHardV2 **7.8**；
  - RRC-AGR + voting@8：分别为 **41.3**、**11.2**。
- 同一设置下 WildBench 从 PRC 的 48.3 提升到 **59.8**；MMLU-Redux 从 51.4 提升到 **56.9**；MATH 从 41.2 提升到 **48.6**。
- 在 3B/8B reward model、带/不带 thinking 的多个组合中，SCR/AGR 整体优于 DRM、GRM+PRC、DPO、SimPO。
- 增加 judge votes 和 anchors 带来近似单调、但逐渐饱和的增益；8–16 个 anchors 已产生明显收益，256 anchors 出现饱和或轻微下降。
- CARA 消融显示，移除冲突调整会在多个 benchmark 上造成下降。

## 证据质量与局限

### 证据较强之处

- 覆盖两种 RM 尺度、两种 policy reasoning mode、多个开放式和可验证 benchmark。
- 同时比较 DRM、GRM 的 probability-based 用法、offline preference optimization 和两种 RRC。
- 有 voting、CARA、reward scale、anchor/vote scaling，以及 compute-matched/效率分析。
- 代码已经公开。

### 局限

- 仍是 v1 preprint，尚未同行评审。
- 开放式评测主要依赖自动 judge；AlpacaEval2/ArenaHardV2 最终使用 GPT-5，仍可能存在 evaluator bias。
- 训练 GRM 只评估**最终回答**，带 thinking 的 policy 中间推理没有交给 reward model，因此不能证明方法能评价长时程轨迹。
- SCR/AGR 只输出严格胜负，未原生支持 tie/abstain/uncertain；将低置信比较强行计为胜场可能制造虚假 margin。
- 胜场数只是离散相对位置，并非经过校准的绝对质量或序数概率分布。
- anchors 由 reference policy 生成，虽然减少随 policy 漂移，但仍可能覆盖不足、携带系统性偏差。
- 训练 evaluator 与最终自动 evaluator 都属于强 LLM judge 范式，尚未达到真正独立的 sealed eval。

## 最接近的相关工作

- **Generative Verifiers / GenRM**：将 verification 训练为 next-token prediction；RRC 解决其偏好 token 概率作为 RL scalar 时的错配。
- **GRAM、POLAR 及 generative reward reasoning**：强化 GRM 的比较与解释能力；RRC 保留比较范式而不是去掉 reasoning 以求标量化。
- **Bradley–Terry / RRHF / GRPO**：都利用相对偏好；RRC 的区别是由生成式 judge 在线构造当前 policy 样本的 ranking。
- **OPRM**：把绝对质量建模为序数概率分布；RRC 提供 pairwise/anchor 证据，可作为 OPRM 的在线观测来源。
- **SPOT**：用 verifier-scored branch outcomes 校准局部 teacher distribution；RRC 则用比较式 GRM 给整条响应排序。

## 如何复用或推进 LLM-as-a-Verifier

1. 将严格 A/B 扩展为 **A/B/T/abstain**，让 judge 输出胜/负/平/证据不足的概率或多次投票后验。
2. 不直接用胜场数，可用 Bradley–Terry–Luce、Thurstone 或 ordinal logistic 将 pairwise edges 与 anchors 拟合成带不确定性的 latent score。
3. 使用程序化/环境真值对部分 edges 做硬门控：若两个 Agent 分支终局状态可验证，则环境结果优先于 GRM；仅在真值不可得时调用 GRM。
4. 把 GRM 的生成式 critique 作为 judge evidence 保存，但分离“解释文本”与“最终比较标签”，避免漂亮 critique 被误当作可靠 margin。
5. 蒸馏轻量 verifier 时同时训练 pairwise head、ordinal distribution head 和 abstention head，使 student 保留 teacher 排名结构与不确定性。

## 对 Agent verifier × OPD 实验路线的具体影响

### Score-level on-policy verifier distillation

RRC 说明 score 不应来自单次偏好 token 概率。建议由同一 prompt 下的 student-generated trajectories 在线形成 comparison graph，再用 anchor-calibrated latent score 作为 OPD 权重或 advantage。

### Pairwise A/B/T 与序数评分分布

这是最直接的启示。保留 A/B/T 原始后验，在满足传递性与 anchor 约束后再投影到 1–5 级序数分布；不要只存最终胜场数，否则会丢失不确定性和循环偏好信息。

### 程序化/环境真值门控

对可验证 Agent 结果，可将硬真值 edge 锁定，再让 GRM 只补充不可判定 edge。若 GRM 与环境真值冲突，应降权或进入审计集，而不是多数票覆盖真值。

### Student-generated critique states

可让 judge 对 pairwise 轨迹先生成 critique，再以 critique 为条件重新比较；但 critique-enhanced judgment 必须在 sealed 环境结果上验证是否更准确，防止 evaluator self-persuasion。

### 高熵分叉下保留探索

SCR/AGR 的 group ranking 比单一 scalar 更适合保留多个近似候选。若 top candidates 的 posterior 重叠，应保留探索；只有显著落后于多个 anchors 的分支才剪枝。

### 独立 sealed eval

训练期 GRM、anchor policy 和最终 evaluator 应三者隔离。最终报告除任务成功外，还应包括与环境/人工 sealed labels 的 pairwise accuracy、tie calibration、循环率、anchor drift 和 evaluator swap 后的排名翻转率。

## 建议的最小复现实验

- 每个 Agent 任务采样 4–8 条轨迹；
- 构造环境真值 edge + GRM A/B/T edge；
- 比较 preference-token scalar、胜场数、BT posterior、OPRM ordinal posterior 四种 reward；
- 分别用于 score-weighted OPD 与 rollout selection；
- 在隐藏任务和独立 evaluator 上报告 task success、Brier/ECE、pairwise accuracy、support coverage 与 evaluator-swap 稳定性。
