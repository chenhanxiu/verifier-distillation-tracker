# RISE：Recursive Improvement via Self-Extrapolating Policy Distillation

- **作者**：Yang Li、Semih Yavuz、Shafiq Joty
- **首次公开日期**：2026-09-04
- **当前版本日期**：2026-09-04（v1）
- **原始论文**：[arXiv:2609.05295](https://arxiv.org/abs/2609.05295)
- **DOI**：[10.48550/arXiv.2609.05295](https://doi.org/10.48550/arXiv.2609.05295)
- **代码**：截至本次记录未发现作者公开代码

## 一句话结论

RISE 把 RLVR 相邻检查点的更新方向外推成动态 teacher，再在当前 student 轨迹上做密集 token 蒸馏，是无需外部 teacher 或 privileged context 的 score-level on-policy distillation 新基线。

## 真正新增的内容

**论文原文结论**：作者将当前模型与滞后锚点之间的训练位移，在参数空间或输出 logit 空间外推，构造“未来模型”teacher；teacher 每轮刷新，把一次性自蒸馏改成递归改进循环。

**分析推断**：最值得复用的不是单纯“更强 teacher”，而是把由可验证奖励确定的更新方向转译为密集分布监督。它可直接迁移到 verifier：先由环境真值确定 score 更新方向，再外推 verifier 的序数评分分布供 student 蒸馏。

## 核心方法

1. RLVR/GRPO 在 student 自生成样本上产生稀疏但有真值锚定的参数更新。
2. 维护 trailing anchor（EMA 或旧检查点），计算 current 相对 anchor 的位移。
3. 在 weight space 用 task arithmetic，或在 logit space 用几何混合外推；以 Jensen–Shannon divergence 将外推 teacher 蒸回 student。
4. 迭代刷新 teacher；无需外部模型、正确兄弟解答或额外 rollout。

## 关键实验结果

**论文报告**：

- Qwen2.5-3B-Instruct 上，ALFWorld 成功率由 GRPO 的 75.0 提升到 weight-RISE 的 84.4；WebShop Acc 由 63.3 提升到 74.2。
- 混合数学与 STEM 训练中，weight-RISE 的 Math/STEM 平均分为 44.8/47.5，GRPO 为 40.2/45.5。
- Qwen3-8B 数学实验中 logit-RISE 的域内平均 62.5，高于 GRPO 的 60.0。
- 训练墙钟开销约为 GRPO 的 1.3–1.6 倍，但不增加采样成本。

## 证据质量与局限

**证据质量：中高。** 覆盖数学、STEM、代码和两个多轮 Agent 环境，并与 GRPO、SDPO、SDAR、RLSD 比较；Agent 增益较直接。

**论文局限**：方法依赖训练轨迹局部低维、近线性；外推过远会失真；若 RLVR reward 可被 hack，错误方向会被放大。代码尚未公开，独立复现不足。

**进一步风险（分析）**：teacher 与 student 同源、同步演化，在线指标可能共同漂移；必须由固定、不可训练的环境真值和 sealed eval 判断外推是否真的朝正确方向。

## 最接近的相关工作

最接近的是 SDPO/OPSD、SDAR、RLSD，以及以可验证奖励门控的 OPDVR、RA-OPD。相较 privileged teacher，RISE 从真实训练位移生成 teacher；相较仅过滤 teacher 信号的方法，它改变的是 teacher 分布本身。

## 如何复用或推进 LLM-as-a-Verifier

- 对 verifier 输出保留完整序数分布，而非只外推期望分数；对每个等级的 logit 做受限外推并校准。
- 仅用程序化/环境真值产生的更新作为位移来源；主观 Judge 分数最多控制幅度，不能决定方向。
- 在 student-generated critique states 上计算 teacher–student 分歧，把外推监督集中到真正改变后续成功率的状态。
- 外推系数应随 teacher entropy、分支 disagreement 和校准误差衰减；高熵区保留探索，不强行尖化。

## 对 Agent verifier × OPD 实验路线的具体影响

1. 新增强基线：GRPO/RLVR → checkpoint displacement → score-distribution teacher → on-policy verifier distillation。
2. A/B/T 标签可由外推后的序数分布导出，但同时保存 tie 与不确定性质量，避免标量化。
3. 设硬门控：只有真实执行奖励改善的检查点位移可进入 teacher；失败或 reward 不可信时不外推。
4. critique state 只作为输入状态，不凭其自洽性直接定方向。
5. 对高熵分叉比较“固定 teacher”“RISE teacher”“不蒸馏探索”三组，检查覆盖率而非只看平均回报。
6. sealed eval 固定环境版本、任务集和独立 evaluator；报告闭环 verifier 分数与真实成功率的差距。