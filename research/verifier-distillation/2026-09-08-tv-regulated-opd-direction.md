# TV-Regulated OPD: Direction Matters in On-Policy Distillation

## 基本信息

- **作者**：Han Xiao、Yifan Niu、Dongyi Liu、Chang Luo、Jia Li
- **首次公开日期**：2026-09-08
- **版本日期**：2026-09-08（v1）
- **原始论文**：[arXiv:2609.08341](https://arxiv.org/abs/2609.08341)
- **代码**：未发现公开代码链接

## 一句话结论

TV-OPD 的控制实验表明，sampled OPD 中 token 级方向比精细幅度更关键；用 teacher–student 总变差距离统一调节全局强度，可降低方差并改善后期保持。

## 真正新增的内容

**论文原文结论：** 把 log-probability gap 只保留符号，仍可获得稳定有效学习；该 sign-only 更新等价于条件分布的 total-variation（TV）下降。TV-OPD 再用整体 TV 距离调节所有 token 的共享更新尺度，使 teacher 与 student 收敛时监督自然衰减，而不恢复高噪声的 token-wise magnitude。

**分析推断：** 这为 verifier × OPD 提供了“方向—幅度解耦”的极简基线：硬真值或 A/B/T 决定符号，分布不确定性决定共享步长；不必把未校准的细粒度分数直接当 advantage。

## 核心方法

在 student 生成的 prefix 上，用 teacher 与 student 对采样 token 的 log-probability 差的符号作为方向信号；理论上对应 stopped state occupancy 下的条件 TV surrogate。再估计 teacher–student TV，并通过平滑调节器形成全局系数，使差异大时保留学习强度、差异小时逐步收缩。

## 关键实验结果

在 JustRL-1.5B→DS-Distill-Qwen-1.5B 上，TV-OPD 的 AIME24 为 51.67±1.18；在较大 Qwen 配对上，AIME24/25 分别为 70.00±1.17、58.33±1.67，两者平均 64.17%，比各行最强基线高 1.67/1.25 点。JustRL 后期窗口的两基准均值为 43.06±0.10，Raw OPD 为 40.87±0.83；PeakDrop 从 3.51±1.13 降至 2.36±0.49。

## 证据质量与局限

**证据质量：中等。** 有受控 magnitude/sign 消融、理论等价与训练曲线，但主比较仅两组模型、AIME24/25，且只有两 seeds。

**论文明确局限：** teacher-relative 方向不保证策略改进；TV 等价只针对不对 rollout distribution 求导的条件 surrogate，不保证序列回报单调；模型、基准与 seeds 有限，证据支持优化稳定性和后期保持，不证明更高能力上限。

## 最接近的相关工作

最接近 sampled reverse-KL OPD、sign advantage、PowerOPD/有界 advantage、entropy-adaptive distillation 与 verifier-gated OPD。与 RouteOPD 的区别是：TV-OPD 简化 token 级幅度并控制全局强度，RouteOPD 进一步指定概率质量的 source→destination。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 输出 A/B/T 或序数分布时，可把期望方向或硬门控映射为 sign，而用总变差、预测熵、校准误差形成共享尺度。生成式 critique 只用于定位状态和提出备选动作；若分数未校准，不应直接生成高方差 token-wise advantage。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析建议：**

1. 新增 hard-sign + distributional-scale 基线：环境真值决定正负/零，ordinal verifier 的 TV 或置信区间决定全局幅度。
2. A/B/T 中 T 映射为零更新或低幅更新；保留完整评分分布用于尺度而非强行二值化。
3. critique state 必须经可执行重放确认方向，避免弱 teacher 的稳定错误。
4. 高熵分叉降低全局系数但继续采样，明确把“保留探索”与“监督收敛”分离。
5. sealed eval 报告最终成功率、训练方差、late-stage retention 与探索覆盖；不能只看 teacher–student TV 下降。