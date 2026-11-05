# Typed Decision Model 的展示敏感性审计

## 基本信息

- **论文标题**：Presentation Sensitivity in Typed Decision Models for Subjective Text Evaluation
- **作者**：Jatin Agrawal, Radhika Mamidi
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（v1）
- **原始论文**：https://arxiv.org/abs/2611.06384
- **DOI**：https://doi.org/10.48550/arXiv.2611.06384
- **代码**：未见公开代码链接

## 一句话结论

Jev、Clef Flash 与 Perplexity Decider 的概率、选择和评分会被位置、标识符、背书、决策 framing 与 rubric 显著改变；重复性、展示稳健性和人类对齐是三种不同属性。

## 真正新增的内容

**论文原文结论**：作者在 choice 与 score 原生接口上做受控干预，证明 typed probability output 并不天然稳健；排名有时保持不变，但分数含义已移动。

**分析推断**：distributional verifier 不能只校准 aggregate accuracy 或 ranking；A/B/T 概率必须对候选顺序与 framing 做条件化或不变性测试。

## 核心方法

- 3 类 typed decision models、6 个数据集。
- 9,000 个具有多重人工标注的幽默、有用性与摘要样本。
- 共 702,000 个 judgments。
- 保持文本不变，系统改变位置、identifier、authorship claim、endorsement、decision framing 与 rating rubric。

## 关键实验结果

- Jev 在摘要任务上的第二位置概率优势最高 **6.11 个百分点**。
- 反转读者背书使 Perplexity 在 **40.40%** 的幽默 pair 上改变选择。
- rejection framing 使 Clef 的摘要判断与人类偏好一致率下降 **23.36 点**。
- rating format 会移动 score level，即使排序经常保持。

## 证据质量与局限

受控干预、超大判断量、多模型和人工标注使证据较强。局限是主观文本任务，未覆盖长轨迹、工具证据或训练期优化压力；也未直接测试蒸馏后偏差是否放大。

## 最接近的相关工作

与 JEV 选项顺序偏差、Prompt Lottery、MAWILE、rubric 句法敏感性和 Judge position bias 最接近。

## 如何复用或推进 LLM-as-a-Verifier

对每个 verifier 样本运行双顺序、匿名 ID 与 framing 变体，恢复条件分布；将跨变体方差作为 teacher 不确定性，不稳定样本降权或标 T。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：避免蒸馏未经顺序/格式校准的裸分数。
- **A/B/T/序数分布**：双顺序概率合并；概率区间重叠时标 T。
- **程序真值门控**：展示干预不得改变环境证据或契约。
- **critique states**：匿名化来源与作者信息，防止权威线索污染。
- **高熵分叉**：展示敏感造成的高熵不应用强 teacher 更新。
- **sealed eval**：加入未见 framing 与 rubric，分别报告 repeatability、robustness、human/oracle alignment。
