# Shuffled OPSD：语义一致性何时反而伤害 On-Policy Self-Distillation？

## 基本信息

- **论文标题**：Shuffled OPSD: When Semantic Consistency Hurts On-Policy Self-Distillation?
- **作者**：Qingyuan Zheng, Zhihao Dou
- **首次公开日期**：2026-11-03
- **版本日期**：2026-11-03（v1）
- **原始论文**：https://arxiv.org/abs/2611.04958
- **DOI**：https://doi.org/10.48550/arXiv.2611.04958
- **代码**：未见公开代码链接

## 一句话结论

在 teacher-only 完整解答保持不变时，打乱 student 与 teacher 共享题面的词序，反而能让 OPSD 在三个数学基准、三个 Qwen3 规模上优于标准 OPSD，说明共享输入的语义连贯性可能制造有害的 teacher–student 共适应。

## 真正新增的内容

**论文原文结论**：作者首次系统分离 OPSD 中共享题面、词序与 teacher-only worked example 的作用，并提出极简的 Shuffled OPSD。共享题面逐词打乱有益，但打乱 teacher-only 解答在所有规模上都降低准确率。

**分析推断**：这不是“语义越乱越好”，而是提示 score-level/token-level OPD 可能受共享前缀捷径影响。对 verifier 蒸馏而言，teacher 与 student 看见相同表述时的低分歧，未必代表可靠监督。

## 核心方法

- student 在被打乱词序的题面上生成 on-policy 推理轨迹。
- teacher 接收同一打乱题面，并额外获得保持完整的 worked example，沿 student 轨迹提供 token-level 监督。
- 通过 intact-target、不同词块粒度、打乱 teacher-only 解答、跨题混合和移除目标等控制实验，拆分内容、顺序与 privileged context 的贡献。

## 关键实验结果

- 覆盖 3 个数学推理基准与 3 个 Qwen3 模型规模。
- 在匹配训练配置下，平均准确率高于 intact-target control 与标准 OPSD。
- 相对标准 OPSD 的最大提升为 **3.52 个百分点**（Qwen3-1.7B）。
- 保留更大词块没有优于逐词打乱；打乱 teacher-only worked example 在每个规模都伤害准确率。

## 证据质量与局限

优点是控制变量清晰、跨模型规模复现，并包含多种机制消融。局限是只验证数学推理与 Qwen3 系列；没有长时程 Agent、reward/verifier 分数蒸馏或 sealed eval。效果是否来自去捷径、正则化还是输入噪声尚未被因果区分。

## 最接近的相关工作

最接近标准 OPSD、输入扰动式蒸馏、privileged-context distillation，以及通过 teacher–student 差分隔离能力位移的方法。与对比式自蒸馏不同，本工作不构造正负 teacher，而是直接扰动共享输入通道。

## 如何复用或推进 LLM-as-a-Verifier

可把“语义保持但表述去耦”加入 verifier teacher 训练：同一 Agent 状态生成多种规范化或打乱后的表示，只有跨表示稳定的 score/ordinal distribution 才用于蒸馏。也可将 teacher–student 在原始与扰动视图下的分歧作为可靠性权重。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：增加 shared-state de-correlation 对照，比较原始状态、字段重排、语义改写与 canonical state。
- **A/B/T 与序数分布**：若排序在等义视图间翻转，应转为 T 或提高分布熵，而非强制 A/B。
- **程序/环境真值**：扰动只能作用于表述，硬真值与环境状态必须保持不变。
- **student-generated critique states**：同时验证 critique 在多种状态表述下是否稳定，防止复制共享措辞捷径。
- **高熵分叉**：不要用共享输入导致的伪低熵过早收缩探索。
- **sealed eval**：评测集应包含未参与训练的状态序列化方式，以检测 evaluator 共适应。
