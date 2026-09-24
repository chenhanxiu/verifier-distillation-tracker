# CC-OPD：面向多约束指令的反事实约束条件化蒸馏

## 基本信息

- 论文标题：Counterfactual Constraint-Conditioned On-Policy Distillation for Multi-Constraint Instruction Following
- 作者：Yanzhao Zheng；Yuanqiang Yu；Tianze Xu；Chao Ma；Zhentao Zhang；Jihuai Zhu；Baohua Dong；Hangcheng Zhu；Ruohui Huang
- 首次公开日期：2026-09-23
- 版本日期：2026-09-23（v1）
- arXiv：2609.27421
- DOI：https://doi.org/10.48550/arXiv.2609.27421
- 原始论文：https://arxiv.org/abs/2609.27421
- 代码：截至 2026-09-24，论文页面未提供作者代码链接

## 一句话结论

CC-OPD 逐一从 teacher 条件中删去约束，以 leave-one-out token 概率差恢复每条约束的方向性监督，缓解多约束下 vanilla OPD 信号被稀释的问题。

## 真正新增的内容

【论文原文】与 privileged teacher 增加信息相反，CC-OPD 对每条约束做反事实消融；完整条件与删去单条约束的 teacher token log-likelihood 差形成约束级 shaping signal，再求和、裁剪并加入 vanilla OPD reward。全过程使用冻结 teacher，不依赖外部 verifier。

【分析推断】该设计可直接迁移为 Agent obligation verifier：逐一移除“必须完成/不得违反”的义务，估计各义务对 teacher 评分分布的边际贡献。

## 核心方法

1. student 在自身 on-policy prefix 上生成响应。
2. teacher 分别在完整约束和逐条删约束条件下评分。
3. 计算每条约束的逐 token leave-one-out log-likelihood shift。
4. 将差分求和并裁剪，作为 vanilla OPD 的 token-level shaping；总差分为零时退化回 vanilla OPD。

## 关键实验结果

【论文原文】在两个 Qwen teacher–student 组合和七个基准上，CC-OPD 的平均表现优于论文评测的全部 student-training 基线；1.5B student 在 MulDimIF 上超过其 7B RL teacher。

## 证据质量与局限

【论文原文】覆盖两个模型规模组合和七个多约束基准，并包含弱到强结果。

【分析推断】没有外部 verifier 意味着 teacher 对约束的误解也会被结构化放大；约束之间存在交互时，单条 leave-one-out 差分不等于独立因果贡献。当前证据是指令遵循，不是长轨迹环境执行。

## 最接近的相关工作

与 OPD-Aha 的差分 teacher、SCOPE-OPSD、Unified Per-Token OPD Gating、TV-Regulated OPD 及动态 rubric verifier 最接近。CC-OPD 的核心差别是以“删约束”而非“加 privileged 信息”构造逐约束差分。

## 如何复用或推进 LLM-as-a-Verifier

将动态 rubric 或 Agent 义务列表作为条件，逐条消融后输出义务级边际 score distribution；再用程序化 checker 验证高边际义务是否真实完成。对强交互义务可增加成对消融，识别非加性影响。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】

- score-level OPD：从单一 teacher score 改为每条义务的反事实 score shift。
- A/B/T：若删约束不改变分布或方向不稳定，则该约束标 T；只有稳定边际差分才形成 A/B。
- 真值门控：teacher 提供密集幅度，环境/程序 checker 决定约束是否真实满足及更新方向。
- critique states：student critique 应明确指向被违反的义务，并通过删义务反事实检验其因果相关性。
- 高熵探索：只压低明确违反某一义务的分支，对约束边际不确定的分支保留探索。
- sealed eval：冻结义务定义和 checker，加入约束重述、顺序交换及交互义务测试，防止只适配 teacher 措辞。