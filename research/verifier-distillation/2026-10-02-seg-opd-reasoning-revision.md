# Learning to Revise Reasoning with Segment-wise On-Policy Distillation

- 作者：Yuxiang Zhang、Ding Cao、Shuting Cui、Lei Wang、Weijieying Ren、Tianxiang Zhao
- 首次公开日期：2026-10-02
- 当前版本日期：2026-10-02（v1）
- arXiv：2610.02703
- 原始论文：https://arxiv.org/abs/2610.02703
- Canonical URL：https://doi.org/10.48550/arXiv.2610.02703
- 代码：https://anonymous.4open.science/r/Seg-OPD

## 一句话结论

【论文原文】Seg-OPD 在不确定的 student 推理段上请求 teacher 重写，并让 student 偏好重写段而非原段，同时保留 token-level OPD，使模型显式学习“如何修订当前步骤”。

## 真正新增的内容

【论文原文】常规 token-level OPD 只能在既有坏前缀上继续给分布监督；Seg-OPD 通过受控替换证明 teacher redraft 能改善后续推理，再把 redraft 转成 segment-level pairwise supervision，直接改变中间 reasoning state。

## 核心方法

【论文原文】以不确定性指标选择 student 片段，取得对应 teacher redraft；对 redraft 与原片段施加偏好目标，并与密集 token-wise OPD 联合训练。监督对象是完整语义片段而非孤立 token。

## 关键实验结果

【论文原文】在数学推理和竞赛编程任务、多个模型上，Seg-OPD 的 revision success rate 高于基线；总体推理准确率相对提升平均为 5.22%，并一致优于论文所比较的先进基线。

## 证据质量与局限

【论文原文】优点是先用干预实验验证“替换片段会改善后续推理”，再训练修订能力，并覆盖多个任务/模型。局限是不确定性未必等于错误；teacher redraft 可能改变风格而非正确性；数学/编程结果不能直接证明在有环境副作用的 Agent 轨迹中安全，匿名代码也限制长期可追溯性。

## 最接近的相关工作

最接近 RC-OPD 的根因局部修复、STRIDE 的首错重启、PaperDoctor 的证据化修复建议，以及 student-generated critique state 路线。Seg-OPD 的独特点是 segment pairwise preference 与 token OPD 联合。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】训练 generative verifier 输出“待修订段 + redraft + 后续影响预测”，再用程序或环境 replay 对原段/重写段做成对结算；只有重写带来可验证改善时才作为正样本。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level on-policy verifier distillation**：【分析推断】为每个片段蒸馏 revision gain，而非仅给绝对好坏分；可用后续成功率差校准。
- **pairwise A/B/T 与序数评分分布**：【分析推断】原片段/重写片段天然形成 A/B；两者等价或验证波动时标 T，并保存多次 replay 的序数分布。
- **程序化/环境真值门控**：【分析推断】teacher redraft 只有通过单测、约束或环境回放后才获得正偏好。
- **student-generated critique states**：【分析推断】critique state 可包含“不确定片段、修改理由、redraft、验证结果”，非常贴合现有路线。
- **高熵分叉下保留探索**：【分析推断】只在高不确定且可验证改善的片段更新；对多个有效 redraft 保留并列正样本。
- **独立 sealed eval**：【分析推断】用未见错误类型与隐藏测试测 revision gain，防止 selector、teacher 和验证器对同一题库共适应。
