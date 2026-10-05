# Learning from Repaired Reasoning: Root-Cause-Guided On-Policy Distillation

- 作者：Chenglei Shen、Haoyang Yao、Weijie Yu、Song Jin、Xiao Zhang、Jun Xu
- 首次公开日期：2026-10-02
- 当前版本日期：2026-10-02（v1）
- arXiv：2610.03515
- 原始论文：https://arxiv.org/abs/2610.03515
- Canonical URL：https://doi.org/10.48550/arXiv.2610.03515
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】RC-OPD 不再用同一份参考解笼统监督整条 student 轨迹，而是定位最早实质错误、局部修复并让 student 从修复点继续，从而减轻 reasoning mismatch 与 distillation trap。

## 真正新增的内容

【论文原文】方法把 privileged hindsight 改造成“诊断—修复—继续—再诊断”的有限预算链：错误段由根因诊断与纠正目标监督，正确前缀由修复后的中间结果作为 anchor。它区分应保留的有效进展与必须重写的错误段，而不是把参考解强压到所有 token。

## 核心方法

【论文原文】对失败 rollout 找到最早实质错误；生成局部修正；让 student 从修正状态续写以检验修复；若仍失败则继续诊断，直至成功或耗尽预算。仅对到达正确答案的修复链实施 root-cause-guided 与 anchor-guided 两类蒸馏。

## 关键实验结果

【论文原文】论文在多个数据集与模型尺度上报告显著增益，并称同时缓解 reasoning mismatch 和 distillation trap；摘要未给出统一汇总数字，结果需按任务表格解读。

## 证据质量与局限

【论文原文】优点是监督对象来自 student 自身失败轨迹，且修复需经后续 rollout 验证。局限是根因定位与修复生成仍依赖模型判断；只有能在预算内修到正确答案的链进入训练，可能对“难以修复但信息量高”的失败产生选择偏差；尚未证明适用于含不可逆工具副作用的真实 Agent 环境。

## 最接近的相关工作

最接近 Seg-OPD 的局部重写、STRIDE 的首错定位与重启、以及 DENSE/PaperDoctor 的证据化 critique。区别是 RC-OPD 将“最早错误—局部修复—student continuation”组成可验证的迭代修复链。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把根因定位器改造成 generative verifier：输出 earliest-error span、错误类型、局部修复和可执行验证条件。只有修复后 continuation 通过程序或环境真值时，才把 critique state 纳入 teacher 数据；否则保留为不确定或反例。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level on-policy verifier distillation**：【分析推断】在每个修复节点蒸馏“错误严重度、可修复性、修复后成功概率”，而非只蒸馏整轨迹分数。
- **pairwise A/B/T 与序数评分分布**：【分析推断】原段与修复段形成 A/B；修复未被环境验证时标为 T，并保留“无错—可修—不可修”的序数分布。
- **程序化/环境真值门控**：【分析推断】用单测、求解器或环境 replay 决定修复链是否可作为正 teacher 信号，根因文本只提供解释与幅度。
- **student-generated critique states**：【分析推断】将 student 自己的诊断作为显式状态，但须附错误位置、修复补丁与验证证据。
- **高熵分叉下保留探索**：【分析推断】只修最早实质错误并保留有效前缀，可避免把参考解风格扩散到所有分叉。
- **独立 sealed eval**：【分析推断】评测集应冻结任务与验真器，并加入未参与根因生成的隐藏失败类型，防止诊断器与修复器共适应。
