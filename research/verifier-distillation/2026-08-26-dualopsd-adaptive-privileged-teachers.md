# DualOPSD：自适应特权 Teacher 的 On-Policy Self-Distillation

## 基本信息

- **论文标题**：DualOPSD: Adaptive Privileged Teachers for On-Policy Self-Distillation
- **作者**：Yutong Chen、Guangfu Guo、Zhichao Xu、Kunpeng Liu
- **首次公开日期**：2026-08-26
- **版本日期**：2026-08-26（v1）
- **原始论文**：[arXiv:2608.26019](https://arxiv.org/abs/2608.26019)
- **DOI**：[10.48550/arXiv.2608.26019](https://doi.org/10.48550/arXiv.2608.26019)
- **代码链接**：论文未提供公开代码仓库

## 一句话结论

DualOPSD 不再把带参考答案的 privileged teacher 当作固定 oracle，而是在每次 student 更新后让 teacher 反向适应 student 当前分布；该闭环在 4B/8B 上大幅优于固定 OPSD，但在 1.7B 上反而退化，说明 teacher 共适应具有明显的容量门槛和共塌缩风险。

## 真正新增的内容

**论文原文结论：**

- 固定 OPSD 只能裁掉不兼容的 teacher 风格信号，却不能让 teacher 学会停止反复提供这些信号。
- DualOPSD 采用非对称交替更新：student 先以 clipped forward-KL 学 privileged teacher；teacher 再在同一条 student rollout 上以完整 reverse-KL 向更新后的 student 靠拢，无需额外 rollout。
- teacher 和 student 用同一冻结基座上的两个独立 LoRA adapter；只部署 student。
- 收益随模型规模强烈变化：4B、8B 提升，1.7B 失败。

**分析推断：**

它把 student-generated states 下 teacher target 的“陈旧性”变成可训练变量，适合 Agent verifier 在不断变化的失败轨迹分布上自适应；但 teacher 向 student 靠拢也会削弱 privileged evidence 的纠错独立性，因此不能替代环境真值和 sealed evaluator。

## 核心方法

1. student 仅观察任务，在当前策略上生成一条 rollout。
2. privileged teacher 观察任务与经过验证的参考解，在相同 student prefix 上输出全词表分布。
3. student 使用逐词表项裁剪的 forward-KL 更新，减少风格 token 主导。
4. 在不重新采样的前提下，用更新后的 student 分布作为目标，以 reverse-KL 更新 privileged teacher。
5. 下一训练步使用已适应的 teacher 提供新 target。

## 关键实验结果

**论文原文结果：**

- Qwen3-8B 上，相比 OPSD，DualOPSD 的 avg@12 在 AIME24、AIME25、HMMT25 分别提高 23.61、13.89、10.00 点；对应成绩为 59.44、41.67、26.67。
- Qwen3-4B 上，DualOPSD 为 41.67、31.11、22.22，固定 OPSD 为 28.61、26.11、15.56。
- Qwen3-1.7B 上 DualOPSD 低于固定 OPSD，三个任务分别为 11.94 vs 15.56、8.06 vs 10.00、4.44 vs 6.39。
- 三个规模均降低截断；4B 的双向 KL 下降，但论文明确指出 KL 下降本身不等价于推理能力增强。
- 训练仅使用一条 student rollout；teacher 更新增加一次 privileged 前向与反向计算。

## 证据质量与局限

**证据质量：中等。** 方法对照清晰且主动报告 1.7B 反例，但只使用一个模型家族、一个训练 seed、90 道竞赛数学题。8B 大增益尚需跨 seed 复现。没有长轨迹工具 Agent、序数 Judge 或环境副作用实验，也没有证明 teacher 继续真正利用参考解而非只适应 student 风格。

## 最接近的相关工作

- OPSD：固定的同模型 privileged teacher。
- Latent OPSD：学习 privileged context 的潜变量表示。
- RecurSE：同步 Judge–Checker 共演化，并用独立 PAV 限制有效窗口。
- OPDVR / CrEST：由 verifier 决定方向、teacher 调节幅度；DualOPSD 未使用 verifier 门控。
- DAgger / interactive imitation learning：监督随 learner 所访问状态变化。

## 如何复用或推进 LLM-as-a-Verifier

- 让 teacher verifier 在 student 当前高分歧轨迹上适应“表达风格和状态分布”，但冻结与环境真值相关的 head 或校准层。
- 把 teacher 更新拆为两部分：可适应的表示/风格层与不可向 student 共适应的证据门控层。
- 持续监控 teacher–student KL、序数校准误差、pairwise A/B/T 一致性，以及独立 Judge 的胜率；仅看 KL 下降不够。
- 把每次 teacher 更新后的能力放到独立人工锚点或 executable truth 上验证，出现 fidelity 下降立即停止。

## 对现有 Agent verifier × OPD 实验路线的具体影响

### Score-level on-policy verifier distillation

可增加“fixed teacher vs adaptive teacher”对照。建议只让 teacher 适应 student 轨迹分布，不允许其改变由硬真值确定的评分方向。

### Pairwise A/B/T 与序数评分分布

原文未覆盖。可让 teacher 适应 student 的评分表述，同时用固定的序数校准损失和 Tie 锚点防止分布变尖或胜负边界漂移。

### 程序化/环境真值门控 teacher 信号

论文没有门控，这是迁移到 Agent 时必须补上的部分。teacher 可适应软维度，但 success/failure、安全与副作用方向应由环境真值锁定。

### Student-generated critique states

高度相关：teacher 正是在 student 自生成 prefix 上学习。可把同样更新作用于 student critique state，但只有经反事实重放验证有效的 critique 才允许 teacher 吸收。

### 高熵分叉下保留探索

teacher 向 student 靠拢可能加快分布收缩。必须额外报告 pass@K、分支熵和新路径覆盖率，并对高熵分叉限制 teacher 更新强度。

### 独立 sealed eval

强制需要。Adaptive teacher 与 student 存在共适应，训练内一致性升高不能视为能力提升；sealed Judge、环境快照和人工锚点均不得参与交替更新或 checkpoint 选择。