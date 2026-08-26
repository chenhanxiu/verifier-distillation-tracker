# On-policy Distillation with Verifiable Reward

## 基本信息

- 作者：Wenze Lin、Jiale Zhao、Xitai Jiang、Songde Rao、Yining Li、Shenzhi Wang、Bingxiang He、Gao Huang
- 首次公开日期：2026-08-25
- 版本日期：2026-08-25（v1）
- arXiv：2608.24696
- 原始论文：https://arxiv.org/abs/2608.24696
- DOI：https://doi.org/10.48550/arXiv.2608.24696
- 代码：https://github.com/LeapLabTHU/OPDVR

## 一句话结论

OPDVR 用可验证的轨迹正确性决定每个 token 更新的正负方向、用 teacher–student log-ratio 决定幅度，从而无需新增权重超参即可融合 OPD 与 RLVR，并在六个推理 benchmark 上稳定优于标准 OPD。

## 真正新增的内容

**论文原文结论：** 把 sampled-token OPD 的隐式奖励按轨迹正确性重写，并以 ReLU 门控：正确轨迹只保留非负奖励，错误轨迹只保留非正奖励；由此可直接接入 GRPO 等 policy-gradient 方法。

**分析推断：** 这是现有 Agent verifier × OPD 路线最直接的训练原型：程序化/环境真值控制梯度方向，teacher 只提供稠密强度，能降低 teacher 对错误路径的强化。

## 核心方法

标准 OPD 使用 teacher/student token log-ratio。OPDVR 用 verifier 的二元轨迹结果选择方向，并屏蔽与该方向冲突的 token 信号；GRPD 变体进一步用组相对 advantage 缩放门控后的奖励。

## 关键实验结果

在 AIME24/25、AMC、MATH500、Minerva、OlympiadBench 上均优于标准 OPD。同架构 Qwen3-4B 蒸馏中，OPDVR 在 AIME24 为 36.9，超过 teacher 的 36.0 和 sampled-token OPD 的 34.2；跨架构 1.7B student 中，AMC 为 30.3，对比 sampled-token OPD 的 24.8。结果采用 avg@16。

## 证据质量与局限

证据质量中高：代码、数据与多 benchmark 已公开，并含同/跨架构对照。局限是主要在可自动判定的数学推理上验证；二元 correctness 无法表达部分进展、可恢复性和多条等价成功路径，avg@16 也不能替代 pass@K 与 sealed evaluation。

## 最接近的相关工作

最接近 RG-OPD、RWOPD、CrEST、I-SDPO 和 STAR-OPD。区别是无需另设混合权重，让 verifier 决定方向、teacher 决定幅度。

## 如何复用或推进 LLM-as-a-Verifier

将二元 gate 扩展为校准后的序数/分布式 verifier：硬真值仍决定符号，LLM verifier 只在真值无法覆盖时调节幅度；同时记录每个 token 被保留或屏蔽的原因。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 可直接实现“环境真值定方向、teacher score 定幅度”的首个 baseline。
- **A/B/T 与序数分布：** 把二元正确性扩展为退步/持平/推进，并比较是否优于硬 ReLU。
- **真值门控：** 工具执行、状态一致性和硬安全门槛优先提供符号。
- **Student critique states：** critique 只在被 verifier 证实的失败状态上影响更新。
- **高熵探索：** 正确但非 teacher 风格的分支不会被负向压制；仍需显式保留高熵成功轨迹。
- **Sealed eval：** 训练 gate 与最终 evaluator 必须分离，报告 avg@K、pass@K 和隐藏环境结果。
