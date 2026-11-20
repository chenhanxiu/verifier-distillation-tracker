# PAIR-MED: Policy-reward Alternation for Iterative Refinement in Multilingual Medical Reasoning

- **作者**：Fan Gao, Xiaohang Xu, Lang Huang, Nan Lu, Irene Li
- **首次公开日期**：2026-11-19
- **版本日期**：2026-11-19（v1）
- **原始论文**：[arXiv:2611.25446](https://arxiv.org/abs/2611.25446)
- **DOI**：[10.48550/arXiv.2611.25446](https://doi.org/10.48550/arXiv.2611.25446)
- **代码**：论文页面未提供公开代码链接

## 一句话结论

【论文原文】固定 PRM 会随 policy 分布变化而失配，PAIR-MED 通过“当前策略生成轨迹→更新 PRM→PRM 再训练策略”的交替循环共同适配 reward 与 policy；【分析推断】这是 long-horizon Agent on-policy reward-model distillation 的直接训练骨架，但必须用冻结真值和 sealed evaluator 约束共适应。

## 真正新增的内容

【论文原文】工作不是仅为多语言医学增加一个 PRM，而是显式把 reward model 当作随策略变化的在线组件：PRM 用当前策略生成的多语言轨迹更新，再为下一轮策略优化提供过程奖励；医学步骤监督持续作为锚点。

【分析推断】它把“teacher 分布漂移”从离线数据问题改为闭环系统问题，为 verifier × OPD 提供最直接的 alternating-update 对照组。

## 核心方法

【论文原文】

1. 先对 multilingual policy 与 medical PRM 做监督初始化；
2. 当前 policy 生成 12 种语言的推理轨迹；
3. 用这些 on-policy 轨迹与医学步骤监督更新 PAIR-PRM；
4. PRM 提供过程奖励，与 outcome reward、语言相关 reward 一起更新 policy；
5. 在 8B/9B 规模上反复交替。

## 关键实验结果

【论文原文】

- 在 Global-MMLU 与 MMLU-ProX 医学子集上，PAIR 模型相对对应 Qwen backbone 平均准确率提升 3.01–7.47%。
- 在 CUREMED-BENCH 上，PAIR-MED-9B 的“语言一致性与逻辑准确性联合指标”相对基线在域内语言提升 12.88%，域外语言提升 7.45%。
- 作者报告了 PRM 适配、多语言推理质量与组件贡献分析。

## 证据质量与局限

【论文原文】覆盖 12 种语言、两种规模和域内/域外语言，且包含组件分析。局限是摘要未给出 PRM 校准、对抗 reward hacking、真实临床执行或长期闭环稳定性的证据；医学 QA 的轨迹仍不等同于具环境交互的 Agent。

【分析推断】交替更新可能提升分布匹配，也可能让 policy 与 verifier 共同利用同一漏洞；必须通过冻结锚点与独立结算判别两者。

## 最接近的相关工作

- Process reward model / ProcessBench：提供步骤级监督。
- GLARE：使用当前策略负样本持续更新 reward estimator。
- PROSE：过程奖励自训练，并警告均值奖励被利用。
- score-level OPD 与 γOPD：分别关注 on-policy 分数迁移和时间信用。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将每轮 Agent rollout 分成：环境已结算、部分可结算、不可结算三类。PRM 只在前两类用硬锚点更新；不可结算样本仅用于保留不确定性或请求更强 teacher。对每轮记录 PRM 的 ECE、首错定位、类别漂移和 sealed 轨迹成功率。

## 对现有 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level on-policy verifier distillation**：可直接采用 alternating loop，但 student verifier 更新频率应低于 policy，并设置锚点 replay。
- **pairwise A/B/T 与序数评分分布**：PRM 输出应保留步骤级分布；证据不足样本标 T，不强行产生序。
- **程序化/环境真值门控**：硬结算样本作为不可被软 PRM 覆盖的 anchor loss 与否决层。
- **student-generated critique states**：从当前 policy 的首错附近生成 critique，再由真值或冻结 teacher 验证后入库。
- **高熵分叉保留探索**：高 PRM 熵状态进入分叉采样而非单向惩罚，以免闭环过早收缩。
- **独立 sealed eval**：每轮仅在隐藏环境与冻结 evaluator 上验收，防止 PRM 与 policy 共适应。
