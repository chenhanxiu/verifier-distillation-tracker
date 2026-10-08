# Composing What Each Teacher Learned: Multi-Teacher On-Policy Distillation through Teacher-Relative Shifts

- 作者：Hejian Sang、Zhengze Zhou、Shayan Mohajer Hamidi、Xiaomin Li、Rohit Jain、Alborz Geramifard
- 首次公开日期：2026-10-07
- 版本日期：2026-10-07（v1）
- 原始论文：https://arxiv.org/abs/2610.10460
- Canonical URL：https://arxiv.org/abs/2610.10460
- 代码/模型：https://huggingface.co/pb09204048/

## 一句话结论

【论文原文】Δ-MOPD 不迁移 teacher endpoint，而迁移 teacher 相对其 base 的 logit shift，并在 student 冻结初始化上重锚定；这能剥离继承偏好，改善多 teacher 同状态组合和阶段顺序敏感性。

## 真正新增的内容

【论文原文】把 teacher selection 与 target construction 解耦，证明 inherited base pull 可大于真正的 post-training shift；删除该项后 teacher-term norm ratio 与 target–student KL 都下降。

## 核心方法

【论文原文】对每个 teacher 计算 teacher-minus-base logit shift，再加到 student 初始分布形成目标；在共同域组合、分域路由、分阶段和交错训练中与 endpoint supervision 对照。

## 关键实验结果

【论文原文】三 teacher 组合时比 endpoint 高 4.11 个 Math 点和 1.95 个五基准平均点；两 teacher 时相当。分阶段训练把顺序差从 10.50 降至 6.42 点；交错单 teacher 更新时两种目标接近。

## 证据质量与局限

【论文原文】控制 teacher selection，隔离 target 构造效应，并覆盖多种路由方式。【分析推断】需要访问每个 teacher 的 base logits；效果集中在信号合成场景，对黑盒 verifier 或 base 不可得场景适用性有限。

## 最接近的相关工作

【分析推断】接近 CompassOPD、Lightning Weave、VG-OPD、MOPD-Router 与 UP-MOPD；区别是校正 teacher 继承偏好，而非路由或优化器冲突。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】多 verifier teacher 不应直接平均 endpoint score；可蒸馏各 verifier 相对其未校准 base 的“判断位移”，再在统一 student reference 上组合，减少模型族与风格偏置。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：增加 endpoint、raw delta、student-reanchored delta 三臂。
- 【分析推断】A/B/T：比较各 teacher 的相对偏移，不把共同 base 偏好误作共识。
- 【分析推断】真值门控：硬真值仍定方向，delta 只调 soft score。
- 【分析推断】critique states：仅迁移 teacher 因额外证据产生的 critique 变化。
- 【分析推断】高熵分叉：减少多 teacher endpoint 平均导致的模式收缩。
- 【分析推断】sealed eval：跨 teacher 族与训练顺序测试，单列 order gap。