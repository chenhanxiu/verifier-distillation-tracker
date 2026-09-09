# Distillation as Probability Transport: Routed On-Policy Distillation

## 基本信息

- **作者**：Tianle Xia、Lingxiang Hu、Yiding Sun、Linfang Shang、Ming Xu、Lan Xu、Ning Zheng、Wei Xu、Jie Jiang
- **首次公开日期**：2026-09-08
- **版本日期**：2026-09-08（v1）
- **原始论文**：[arXiv:2609.08337](https://arxiv.org/abs/2609.08337)
- **代码**：未发现公开代码链接

## 一句话结论

RouteOPD 把 sampled OPD 中“单 token 标量信用但概率质量去向不明”的问题改写为 teacher 指导的显式 source→destination 概率运输，并用可实现的 pairwise log-odds 目标显著降低无关词表泄漏。

## 真正新增的内容

**论文原文结论：** sampled reverse-KL 虽能给被采样 token 正负信用，却把释放/吸收的概率质量交给 student softmax 几何；RouteOPD 显式分解 student-excess source 与 teacher-deficit destination，并从两者耦合中采样运输边。所有边目标来自同一个有界 teacher potential，因此满足循环一致性；预算随 teacher deficit 的集中度自适应。

**分析推断：** 这不是普通的 loss reweighting，而是把 score-level OPD 从“标量好坏”提升为“动作替代关系”。它天然可承载局部 A/B/T：source 为较差动作、destination 为较好动作，而 teacher demand 分散时可对应 T/不确定状态。

## 核心方法

在 student 访问的 prefix 上取 teacher 与 behavior student 的 top-k 并集，计算归一化分布差异：正差形成 excess source，负差形成 deficit destination；以二者独立乘积构造最大熵耦合并稀疏采样边。每条边优化 destination 与 source 的 log-odds 差，直接 logit 梯度只作用于这两个 token。共享 tanh-bounded potential 保证多边目标联合可实现，Herfindahl 集中度控制运输预算。

## 关键实验结果

论文在 4 组 teacher–student 与 MATH500、AMC23、AIME24、AIME25 上比较：相对 sampled-RKL，四基准平均提升 2.19–3.61 点，平均增益 2.70 点；相对 full-vocabulary reverse-KL 平均高 1.24 点。固定诊断集上 routing fidelity 从 35.4% 升至 90.4%，background leakage 从 68.3% 降至 13.8%。top-32 并集保留两侧超过 97% 概率质量，端到端开销约 2.5%。

## 证据质量与局限

**证据质量：较高（预印本内部）。** 有四组模型配对、四个基准、匹配样本置信区间、destination 随机/匹配干预、循环一致性与效率消融。

**局限：** 仅验证数学推理 token 级动作，尚未覆盖工具调用、长时程环境状态或跨 tokenizer；top-k 重归一化仍可能遗漏长尾；因果干预只验证局部运输机制，不等于证明序列级或 Agent 成功率必然提升。尚无公开代码，独立复现缺失。

## 最接近的相关工作

最接近 sampled reverse-KL OPD、full-vocabulary reverse-KL、PowerOPD、TOP-D、RG-OPD、TIP/TRACE 与 TurnOPD。前者调目标/幅度/可靠性，后者选样本、位置或 turn；RouteOPD 主要回答固定状态下“概率应从哪个动作移向哪个动作”。

## 如何复用或推进 LLM-as-a-Verifier

可让 verifier 输出候选动作的序数分布，再把 student-excess→verifier-deficit 直接转为稀疏 A/B 边；对 T 概率高或 deficit 分散的状态自动缩小预算。生成式 verifier 的 critique 可用于解释 destination，但训练方向应由可执行结果或独立评分校准。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析建议：**

1. 将现有 score-level OPD 增加“显式动作运输”分支，与 scalar gating、full-distribution KL 做等预算对照。
2. pairwise A/B/T 中，A/B 由 source/destination 构成，T 用 deficit entropy 或运输集中度定义；保留完整序数分布而非仅胜负标签。
3. 对工具动作先以程序化/环境真值否决不可执行 destination，再由 teacher/verifier 决定剩余质量分配。
4. student-generated critique state 只作为 destination 解释特征，不允许覆盖硬真值。
5. 高熵分叉使用小预算或不运输，避免过早压平探索。
6. sealed eval 必须单独测 Agent 成功率、恢复率和分支多样性，防止 routing fidelity 成为自洽但不可迁移的代理指标。