# When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better

- **作者**：Siyan Zhao；Yonggan Fu；Jindong Jiang；Shih-Yang Liu；Song Bian；Byung-Kwan Lee；Sharath Turuvekere Sreenivas；Wenliang Dai；Hanrong Ye；Aditya Grover；Pavlo Molchanov
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.11291
- **Canonical URL**：https://arxiv.org/abs/2610.11291
- **代码**：未发现公开代码链接

## 一句话结论

论文系统性挑战“蒸馏必须持续 on-policy”的默认假设：固定使用初始 student 的离线 rollout 往往更准、更快，而真正决定 OPD 是否有益的是 teacher 与 student 在当前状态上的输出 token 重叠。

## 真正新增的内容

【论文原文】提出 Semi-OPD：先由初始 student 生成并缓存 rollout，之后在固定轨迹上蒸馏 teacher；并给出预测 OPD 何时优于该离线方案的经验判据——初始 teacher–student 输出 token overlap 较高时，on-policy 更新更有价值。

【分析推断】“on-policy”应被拆成策略状态覆盖与在线重新采样两件事。对 Agent verifier，可采用周期性 refresh 的 replay，而非每步都昂贵重采样。

## 核心方法

1. 用训练开始时的 student 生成 rollout 数据集。
2. 在这些 student-originated、但训练期间固定的状态上计算 teacher supervision。
3. 与持续从当前 student 采样的标准 OPD 对照，并分析 token overlap、序列长度和 teacher–student 配对。
4. 将 rollout 来源与 KL 蒸馏目标解耦，从而减少在线生成成本。

## 关键实验结果

【论文原文】在 17 个 teacher–student 组合（1.5B–235B）中，Semi-OPD 在 14 个组合上优于 OPD，最高准确率优势 13.6%，训练加速最高 11.4 倍。作者还发现长上下文会使 student rollout 相对 teacher 更偏离，因此“对 student on-policy”不等于“对 teacher 有效”。

## 证据质量与局限

【论文原文】模型规模和配对覆盖广，且同时报告质量与效率。  
【局限】主要是静态推理任务；未直接检验工具调用后环境状态变化、不可逆副作用、长期 credit assignment 或 verifier 共适应。固定 replay 在快速演化的 Agent 策略上可能过时。

## 最接近的相关工作

与标准 OPD、Data-free OPD、One-Shot OPD、RL Starts before RL、AC-OPD 和 STRIDE 最接近。它补充了这些工作的状态覆盖讨论：覆盖多不等于必须每轮刷新，关键是 teacher 信号在所访问状态上仍有支持。

## 如何复用或推进 LLM-as-a-Verifier

可为 verifier 蒸馏建立三种数据臂：实时 on-policy、周期刷新 replay、固定初始 replay；以 teacher–student 判决重叠、环境状态漂移和 critique 分布漂移作为切换条件。对长轨迹尤其应按阶段评估 replay staleness，而非只看 token overlap。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：加入 Semi-OPD 作为必要基线，并比较同等 teacher 调用预算。
- **A/B/T 与序数分布**：用分布重叠（而非 argmax 一致率）判断何时刷新；T 概率上升可触发新采样。
- **程序化/环境真值门控**：缓存轨迹必须保存可重放环境快照与 oracle 结果，防止环境变化使旧标签失真。
- **student-generated critique states**：缓存的是 student 自己的 critique 状态，周期性抽样检验其是否仍覆盖当前错误模式。
- **高熵分叉**：不要因转向 replay 而删除高熵分支；按分支新颖度与 oracle 结果保留探索样本。
- **sealed eval**：在线和离线方案共用同一冻结评测集、harness 与 evaluator，避免计算预算差异伪装成方法收益。

总体判断：【分析推断】现有路线不应把“全程在线采样”视为原则；更稳妥的是以分布漂移和环境真值触发的混合 replay/refresh 机制。