# AdaGround：用二元 Verifier 控制 GUI Grounding 的观察与重试

- **论文标题**：AdaGround: Token-Normalized Adaptive Zooming with Verifier-in-the-Loop Refinement for GUI Grounding
- **作者**：Bingchao Wang, Yongcheng Jing, Chengyu Wang, Jun Huang, Jie Yang, Wei Liu, Dacheng Tao
- **首次公开日期**：2026-10-27
- **版本日期**：2026-10-27（v1）
- **原始论文**：https://arxiv.org/abs/2610.36874
- **代码链接**：https://github.com/bcwang-sjtu/AdaGround
- **标识**：arXiv:2610.36874；DOI: 10.48550/arXiv.2610.36874

## 一句话结论

一个廉价 Yes/No verifier 不只给分，还可决定保留、拒绝、重定位或弃权，从而把 GUI grounding 变成受验证的闭环搜索。

## 真正新增的内容

**论文原文结论**：AdaGround 结合自适应缩放、marked-click 二元 verifier 与结构化 grounding；verifier 在每次缩放后选择是否接受、比较 zoom chain、触发重新 grounding，并通过存在性查询决定 abstain。

**分析推断**：这是“distributional verifier 路由高成本操作”的简洁原型，尤其适合迁移为长轨迹中的选择性复核与高熵分叉控制。

## 核心方法

Token-Normalized Adaptive Zooming 根据模型估计的目标尺寸设置放大率、视野和深度；Verifier-in-the-Loop Refinement 对候选点击做 Yes/No 复核并控制重试；Compositional Structure Grounding 用表头组合定位表格单元格。

## 关键实验结果

在 Qwen3-VL 上，相对 backbone 在 OSWorld-G 与 ScreenSpot-Pro 提升 7.4–20.6 个准确率点，并优于多种训练自由 zooming 和若干训练型 GUI 模型；增益迁移到 held-out UI-Vision。

## 证据质量与局限

优点是跨多个 GUI grounding 基准并公开代码。局限是 grounding 属于短局部决策，尚未证明 verifier 在长时程副作用、权限约束或不可逆动作上可靠；二元 verdict 也没有表达多种失败原因和校准不确定性。

## 最接近的相关工作

最接近 SWE-VERIFIER 的选择性验证、VeriCUA 的主动检查、Speculative Uncertainty 的低成本风险路由，以及 BLINDSPOT 的多类执行结果。

## 如何复用或推进 LLM-as-a-Verifier

把 Yes/No 扩展为 `accept / retry / alternate branch / abstain` 的概率分布；训练时保留每个动作触发的检查成本和最终环境结果，使 verifier 同时学习质量与“何时值得检查”。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：只在 verifier 拒绝或高不确定状态调用 teacher，形成选择性 on-policy 蒸馏。
- **A/B/T 与序数分布**：zoom chains 可形成 A/B；概率重叠或目标不存在时标 T。
- **程序化/环境真值门控**：最终点击必须由 UI 状态变化或任务条件验真，不能把 verifier 接受当作真值。
- **student-generated critique states**：保留“为何拒绝点击、建议观察区域、存在性证据”，验真后再蒸馏。
- **高熵分叉与探索**：在候选接近时保留多条 zoom chain，避免二元 verifier 过早坍缩。
- **sealed eval**：使用隐藏 UI、位置扰动与不可见目标，冻结独立环境检查器，审计 verifier 的选择偏差。