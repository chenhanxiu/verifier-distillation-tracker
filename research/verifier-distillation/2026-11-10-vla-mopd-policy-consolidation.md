# VLA-MOPD: On-Policy Distillation for Multi-Task VLA Policy Consolidation

- **作者**：Yongxuan Lv、Zhen Fang、Lichen Man、Hao Li、Pu Li、Hengyi Wang、Langfeng Cao、Lin Chen、Jie Huang、Xiu Su、Shan You、Fei Wang、Feng Zhao
- **首次公开日期**：2026-11-10
- **版本日期**：2026-11-10（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.12286
- **代码**：未发现公开代码链接
- **标识符**：arXiv:2611.12286

## 一句话结论

【论文原文】VLA-MOPD 在 student 实际访问的机器人 observation 和 flow-matching 的中间 ODE 状态上查询路由后的 specialist teacher，用逐 flow-step 目标整合多任务能力，并用 reference term 控制遗忘。

## 真正新增的内容

【论文原文】离线蒸馏看不到 student 访问的状态，endpoint action distillation 又忽略动作生成的中间流状态。本文同时把 supervision 放到 on-policy observation 与中间 ODE state，并用 instruction 路由冻结 specialist teacher，从而把多任务 VLA policy consolidation 变成细粒度的 on-policy 蒸馏问题。

## 核心方法

- shared student 在真实/模拟环境中收集自己的 robot rollout。
- 按 instruction 选择对应的冻结 specialist teacher，在每个 student observation 与中间 ODE state 查询目标。
- 对有效 action chunk 使用 masked local matching loss，teacher transition target 停梯度。
- 可选 reference-policy matching 项保留未被当前 specialist 覆盖的旧任务能力。

## 关键实验结果

【论文原文】从每个 LIBERO 任务仅一条轨迹起步，mean success-once 从 **75.4% 提升到 98.9%**，endpoint action distillation 为 **98.15%**。RoboTwin 2.0 平均成功率从 **73.0% 提升到 89.3%**；Piper 真机经过两轮 consolidation 从 **70.0% 提升到 90.0%**。近似匹配的适配实验中，reference matching 将 Object suite 的下降限制在 **3.0 点**，无该项时下降 **13.2 点**。

## 证据质量与局限

【论文原文】包含两个模拟基准与真机验证，且报告了 reference term 的保持能力，证据比单一离线 benchmark 更强。但主要指标包含 success-once，样本量、置信区间及失败类型在摘要中未给出；它研究的是连续动作 flow matching，不直接证明离散语言 verifier 的 score-level OPD 有效。

## 最接近的相关工作

最接近的是 VLA-OPD、UI-MOPD、多教师 MOPD、endpoint action distillation 与 reference-policy regularization。本文的关键差异是对 student-visited observation 和动作生成中间状态同时蒸馏，而非只匹配最终动作。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把“中间 ODE state”类比为长轨迹中 verifier 的内部阶段状态：不仅在最终 verdict 上蒸馏，还在分解后的证据、critique 与修复阶段匹配 teacher 的局部分布。reference term 可变成冻结基准 verifier 的保持约束，防止新领域蒸馏损害旧 rubric。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：从终局 score 扩展为 observation/阶段级 score distribution matching，并保持 teacher 路由可追踪。
- **A/B/T 与序数分布**：在同一 observation 的 action chunk 上构造局部比较；跨 observation 不直接比较。
- **程序化/环境真值**：机器人成功与状态约束负责硬门控，teacher flow target 只做细粒度塑形。
- **student-generated critique states**：只在 student 实际访问的 observation 上生成 critique，避免离线 teacher state 的覆盖错位。
- **高熵分叉**：reference matching 提供能力保持，但仍应保留多个可行 action chunk，不能只收敛到单一 specialist。
- **sealed eval**：冻结未参与路由训练的任务套件、真机场景与成功判据，分别报告 consolidation 与 retention。