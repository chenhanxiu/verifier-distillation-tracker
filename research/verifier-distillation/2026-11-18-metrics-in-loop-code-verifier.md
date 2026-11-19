# Metrics-in-the-Loop: Complexity Feedback Reshapes Agent-Written Code

- **作者**：Nicolas Chapados、Jean-François Gagné、Nouha Dziri
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：https://arxiv.org/abs/2611.23817
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.23817；DOI: 10.48550/arXiv.2611.23817

## 一句话结论

【论文原文】在长时程 coding rollout 中逐步注入复杂度与覆盖率的程序化反馈，可在不损害 held-out 正确性的情况下减少复杂度集中，说明 verifier 最有价值的时点可能是缺陷固化前。

## 真正新增的内容

【论文原文】提出 metrics-in-the-loop：每次代码变更后，向 Agent 上下文插入短反馈，指出超出 cyclomatic-complexity 阈值的函数或测试未覆盖的变更行，让 Agent 在继续构建之前重构或补测；在三个长时程 coding benchmark、四个强模型上做干预和消融。

## 核心方法

1. 变更后运行确定性静态复杂度和覆盖率工具。
2. 仅反馈可执行、局部、可操作的异常，而非自然语言泛评。
3. 用 erosion 衡量复杂度向少数函数集中，并以 held-out correctness 防止“指标变好、功能变坏”。

## 关键实验结果

【论文原文】复杂度反馈显著降低 erosion，同时未影响 held-out 代码正确性。论文将其解释为 Agent re-railing：在弱点成为后续代码基础前用及时测量改变轨迹。摘要未给出统一数值效应量。

## 证据质量与局限

【论文原文】跨三基准、四模型并含消融，且用 held-out correctness 检查副作用；但复杂度/覆盖率只是代理指标，未证明真实维护成本下降。反馈进入同一 rollout，可能使 Agent 针对公开指标做局部游戏。

## 最接近的相关工作

接近 process reward、runtime code quality guard、test-coverage feedback、FLARE、coding-agent early stopping 与 Goodhart 审计。区别是低成本程序指标在轨迹中实时回注。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把确定性指标作为每步 teacher anchor，生成 `问题位置—指标证据—修复建议—复跑结果` critique state；LLM verifier 负责组合与解释，不能改写原始测量。蒸馏目标应同时保留功能与可维护性两个轴。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：加入逐步 complexity/coverage score，与终局测试分开蒸馏，避免平均成单 reward。
- **pairwise A/B/T 与序数分布**：功能相同的分支再按维护性比较；功能与复杂度冲突时保留多轴或 T。
- **程序化/环境真值门控**：静态工具与 held-out tests 作为硬证据，LLM critique 只作解释。
- **student-generated critique states**：每条 critique 必须关联具体 changed function/line，并以修复后指标验证。
- **高熵分叉探索**：在功能通过但复杂度快速恶化的状态保留重构与继续实现两个分支。
- **sealed eval**：隐藏复杂度阈值、测试与维护任务，验证模型未仅针对公开 metrics 优化。
