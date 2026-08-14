# I-SDPO：Instance-Level Adaptive Self-Distillation Policy Optimization

## 基本信息

- **论文标题**：I-SDPO: Instance-Level Adaptive Self-Distillation Policy Optimization
- **作者**：Yubo Zhang、Xinhong Ma、Zezhong Tan、Ziqiang Dong
- **首次公开日期**：2026-08-13
- **版本日期**：2026-08-13（arXiv v1）
- **arXiv ID**：2608.12957
- **DOI**：10.48550/arXiv.2608.12957
- **原始论文**：https://arxiv.org/abs/2608.12957
- **代码**：尚未公开；论文称将在发表时发布

## 一句话结论

I-SDPO 只在一个 prompt 的整组 rollout 全错时启用 privileged self-distillation，一旦组内出现成功样本就保留整组给 GRPO，从而让 teacher 随能力提升自动退出，并在 SciKnowEval 上把 GRPO 的平均 mean@16 从 56.67% 提至 70.31%。

## 真正新增的内容

**论文原文结论**：self-distillation 是低方差但有偏的 reward surrogate；它适合所有 reward 都相同、GRPO 无相对信号的阶段，但在 policy 已能成功时持续模仿会产生非消失的优化偏差下限。

I-SDPO 的新增点是 **instance-level、group-shared routing**：all-incorrect group 整组走 SDPO，any-success group 整组保持 GRPO。它不同于 sample-level SRPO，后者可能把混合组中的错误 rollout 拿去模仿，从而破坏正确/错误之间本来有价值的 reward 对比。

## 核心方法

1. 每个 prompt 采样 (K) 个响应并由可验证 reward 判定。
2. 若整组全错，使用 privileged self-teacher 对这些 on-policy prefix 做前向/反向 KL 混合蒸馏；teacher 是 student 的 EMA，并读取训练期 privileged information。
3. 若组内至少一个成功，整组仅用 GRPO，让成功与失败形成 group-relative reward 证据。
4. 对 SDPO 路由的 token 采用 teacher-entropy 权重：低熵目标权重大，高熵目标被降权；论文明确指出 confidence 不等于 correctness。
5. 对单个 prompt，走 SDPO 的期望概率为 ((1-p)^K)。随成功率 (p) 上升，teacher 影响自动衰减，不需要按训练步手工排 schedule。

## 关键实验结果

**论文报告**（Qwen3-8B，SciKnowEval，训练 2 epochs，mean@16）：

- GRPO：生物 32.12、材料 70.74、化学 62.92、物理 60.88，平均 56.67。
- SDPO：平均 65.74。
- sample-level SRPO：平均 66.01。
- I-SDPO：50.25、74.53、81.16、75.31，平均 70.31。
- I-SDPO 相对 GRPO、SDPO、SRPO 分别提高 13.64、4.57、4.30 点；最大单领域提升是化学相对 GRPO 的 18.24 点。
- 论文的 reward/routing 曲线与“前期 teacher bootstrapping、后期 reward refinement”的解释一致，但不构成全局收敛证明。

## 证据质量与局限

- **证据质量：中等。** 有明确理论动机、routing 对照、KL 与训练动态分析，但实验仅一个 Qwen3-8B 和一个科学推理基准，代码尚未公开。
- **论文原文局限**：模型规模单一；只测 SciKnowEval，开放式、多解和不同 reward 结构下是否成立未知；局部方向恒等式与 reward optimum 附近的二次近似不证明非凸训练的全局收敛。
- all-incorrect 只说明当前采样组没成功，不说明 privileged teacher 正确。EMA 降低方差但带来独立性与陈旧性的权衡。
- mean@16 同时受采样一致性影响；缺少独立 sealed evaluator 与更长 Agent trajectory，不能直接外推到长时程工具任务。

## 最接近的相关工作

最接近 Distill Where You Fail、SRPO、SDPO、OPSD，以及按 pass rate/difficulty 调权的方法。相较“按单条失败轨迹蒸馏”，I-SDPO 强调 prompt/instance 级路由：混合组应完整保留给 reward learning，因为错误 rollout 是有意义的负证据。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：

- 把“组内是否出现环境成功”作为 verifier distillation 的上层门控：只有所有候选都缺乏可判别真值时，才依赖强 teacher verifier；一旦 A/B 间有程序化结果差异，就优先学习真实 pairwise/ordinal evidence。
- 对 score-level student verifier，可在全失败组蒸馏 teacher 的完整评分分布，而非单一均值；teacher entropy 只用来降权，不能替代真值门控。
- 若目标标签是 A/B/T，mixed-outcome group 应保留完整候选集学习相对排序，不应把其中的失败候选拆走单独模仿。
- teacher 退出应按实例能力而非全局步数，以降低不同任务难度造成的过早或过晚退火。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level on-policy verifier distillation**：采用两层 routing：先看环境/程序真值是否产生可辨别结果；无信号组蒸馏 teacher score distribution，有信号组训练 verifier 与 policy 对齐真值排序。
- **pairwise A/B/T 与序数分布**：组内出现成功/失败混合时保留全组，构造 A/B/T 和序数差；全失败时才用 teacher 给出软分布，避免 teacher 覆盖真实相对证据。
- **student-generated critique states**：全失败分支可让 student 生成 critique，再由 privileged teacher 对 critique-conditioned states 打分；但 teacher 信号必须由执行日志或环境反馈过滤。
- **高熵分叉保留探索**：I-SDPO 的 teacher-entropy 权重会压低高熵 token，可能与探索目标冲突。实验中应把“teacher 不可靠的高熵”与“值得探索的 policy 高熵”分开；后者在 any-success/mixed group 中不做蒸馏压缩。
- **sealed eval**：最终用未参与 EMA、routing 或 reward 生成的 evaluator 测试；否则 teacher 与训练 verifier 可能共同适配 SciKnowEval 风格而误判为能力提升。
