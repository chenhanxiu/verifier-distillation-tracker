# Bootstrapped On-Policy Distillation

- **作者**：Yue Wu、Xueyu Zhou、Yangrong Hu、Jian Huang
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.13680
- **代码**：未找到可核验的公开代码地址
- **标识符**：arXiv:2611.13680

## 一句话结论

【论文原文】持续 OPSD 会因 reference-free student 与冻结 privileged teacher 的分布错位而由早期增益转为退化；BOPD 先让 privileged teacher 教出中间模型，再用这个不依赖 reference 的中间模型教一份全新的 student。

## 真正新增的内容

【论文原文】论文把 OPSD 的失效定位为随训练累积的 teacher–student mismatch，而不是仅归因于优化不稳定。其两阶段“先吸收特权信息、再无特权转蒸馏”将 privileged context 的知识提取与最终 student 的 on-policy 学习解耦。

## 核心方法

1. 第一阶段以 reference-conditioned 同权重副本为 privileged teacher，运行常规 OPSD，得到任务适配的中间模型。
2. 第二阶段重新从初始 checkpoint 启动 fresh student。
3. 中间模型以 reference-free 形式充当固定 teacher，在 fresh student 自己的 rollout 上进行 OPD。
4. 通过第二阶段避免后期 student 继续追逐已经错位的 privileged teacher。

## 关键实验结果

【论文原文】跨多个模型的数学推理与代码生成实验中，BOPD 同时超过初始模型和第一阶段构造出的 OPSD teacher。公开摘要未给出逐 benchmark 数字、seed 方差或训练成本，因此不据此推断提升幅度和统计显著性。

## 证据质量与局限

【论文原文】研究同时包含训练动态诊断和替代方法，因果链条比只报告最终分数更完整；但公开信息未说明 mismatch 的统一阈值、teacher 刷新频率和长时程 Agent 环境表现。两阶段需要额外训练，优势是否在等算力下保持尚未由摘要证明。

## 最接近的相关工作

最接近 RetireOPD、Train Ahead, Distill Back、OPD 训练—推理偏差预算，以及 Coupled Calibration and Learning。BOPD 的区别是主动丢弃第一阶段优化状态，以 reference-free 中间 teacher 重新蒸馏初始模型。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可先用环境真值和完整轨迹训练 privileged verifier，再冻结为无特权中间 verifier，最后对 fresh verifier student 做 score-level OPD。这样可减少“teacher 依赖训练期额外证据、student 在部署时无法复现”的共适应。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：增加“两阶段 fresh-student”基线，并跟踪 privileged teacher 与 student 的 score 分布距离。
- **A/B/T 与序数分布**：第二阶段蒸馏完整分布而非仅均值；错位升高时扩大 T/abstain 质量。
- **程序化/环境真值**：只在第一阶段用于提取可靠方向，第二阶段 teacher 不再读取隐藏答案。
- **student-generated critique states**：先由 privileged 阶段筛选，再用无特权中间 teacher 重放，检验 critique 是否可独立成立。
- **高熵分叉**：fresh student 可避免后期追随单一冻结 teacher 收缩探索，但需报告分支覆盖率。
- **sealed eval**：冻结独立 evaluator，并用等算力对比“一阶段继续训练”与 BOPD。