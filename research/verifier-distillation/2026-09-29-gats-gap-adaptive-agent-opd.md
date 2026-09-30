# Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL

- **作者**：Youling Huang, Tiankuo Xu, Jiaji Liu, Tong Zheng, Shuo Zhou, Shaotong Qi, Junchi Yao, Shiyang Liu, Hao Xu, Pengcheng Xu, Bo Huang, Hongyi Fu, Lin Lin
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2609.37898
- **代码**：https://github.com/Ricardo-H/guide-then-let-go

## 一句话结论

GATS 用 teacher–student 性能差动态衰减并最终撤除 OPD，在三类稀疏奖励 Agent 环境中比纯 GRPO 提高 4.37%–11.87%。

## 真正新增的内容

【论文原文】OPD 对长时程 Agent 的价值主要集中在 teacher 明显领先、环境奖励稀疏的冷启动阶段；当差距缩小或反转，继续蒸馏会妨碍学生提升。GATS 因而按性能差调节 OPD 权重，并在达到 teacher 参考水平时退出 teacher。

【分析推断】与固定混合系数相比，它为“何时停止信任 verifier/teacher”提供了可执行规则，并允许小于 student 的专门 teacher 只负责早期导航。

## 核心方法

把 token 级 OPD 项加入 Agent RL 目标；根据在线学生表现与 teacher 参考表现的差距连续缩放该项，达到参考水平后权重归零。

## 关键实验结果

【论文原文】在 ALFWorld、WebShop、ScienceWorld 的三种 Qwen2.5 teacher–student 配置中平均成功率均为比较方法最高；在相同 student rollout 预算下比 reward-only GRPO 提高 4.37%–11.87%。

## 证据质量与局限

【论文原文】覆盖三种常用 Agent 环境和多种尺寸配置，但仍是相近模型族，teacher 参考表现及环境成功率的估计误差可能影响退场时点。【分析推断】没有证明间歇性回归或分布漂移时永久退出仍最优。

## 最接近的相关工作

RetireOPD、Persistent Teacher Anchoring、OnPoKD、STRIDE，以及固定系数的 vanilla OPD+GRPO。

## 如何复用或推进 LLM-as-a-Verifier

把单一成功率差扩展为 verifier 的校准差距：只有当环境真值、Judge 置信区间和学生回报共同表明 teacher 领先时才增加蒸馏权重。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：把现有固定 λ 改为 gap-adaptive λ，并与 RetireOPD 做正面对照。
- **A/B/T 与序数分布**：用胜/负/平后验及其置信区间估计能力差，T 区域保持小权重。
- **硬真值门控**：性能差必须优先由程序或环境成功率估计，Judge 只作稠密辅助。
- **critique states**：teacher 退出后仍可保留经环境验证的 critique replay，不继续在线灌输。
- **高熵探索**：差距小时主动撤除 teacher，有利于防止探索坍缩。
- **sealed eval**：退场阈值在开发集确定，最终成功率用独立冻结任务和 grader 测量。
