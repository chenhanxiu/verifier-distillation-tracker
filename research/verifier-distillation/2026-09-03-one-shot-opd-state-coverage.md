# Rethinking On-Policy Distillation of Large Language Models II: One Training Example

## 基本信息

- **作者**：Zixuan Fu, Bingxiang He, Yuxin Zuo, Haohuan Huang, Jinqian Zhang, Ruhang Xiao, Cheng Qian, Qinyu Luo, Huan-ang Gao, Yudong Wang, Zhiyuan Liu, Ning Ding, Chaojun Xiao
- **首次公开日期**：2026-09-03
- **版本日期**：2026-09-03（v1）
- **arXiv**：2609.04172
- **原始论文**：https://arxiv.org/abs/2609.04172
- **代码**：https://github.com/Thinking-Space/One-Shot-OPD
- **DOI**：https://doi.org/10.48550/arXiv.2609.04172

## 一句话结论

OPD 的有效监督覆盖可能主要来自 rollout 持续制造的新状态，而非大量不同题目；单题已覆盖完整训练状态的 71.5%，16 个语义多样题目达到 98.9% 并匹配全量 OPD。

## 真正新增的内容

**论文原文结论**：作者把 OPD 推到“单训练样本”极限，定义 state coverage，并将数据规模、状态覆盖和 teacher 对齐速度拆开测量；结论是 OPD “data-overfed but algorithm-starved”。

**分析推断**：对 verifier 蒸馏而言，采集预算应更多投向同一任务上的状态多样性、分叉与迭代，而不是机械增加近重复任务。这里证明的是生成模型 OPD 的状态覆盖，不等同于 verifier 的判别边界覆盖，后者仍需单独验证。

## 核心方法

- 让 student 在一个或少量 query 上持续生成 on-policy rollouts，由 teacher 提供 dense token-level 监督。
- 用 full-data OPD 曾访问状态作为参照，测量子集 rollout 的 state coverage。
- 对单 teacher、multi-teacher、真实 query、轻内容模板和域外 WildChat query 做压力测试。
- 同时测量状态覆盖速度与 student 吸收 teacher 监督的速度，避免把“看见状态”和“学会状态”混为一谈。

## 关键实验结果

- 单 query 覆盖 full-data OPD 状态的 **71.5%**，多数覆盖在前 100 步内出现。
- 16 个语义多样 query 达到 **98.9%** coverage，并匹配全量训练验证准确率。
- multi-teacher OPD 中，每域 16 个多样 query 可匹配 full-data MOPD。
- 轻内容模板与域外 WildChat query 也接近真实 query 基线，说明题目内容与诱导状态覆盖可分离。
- 即使固定状态集合，student 吸收监督仍需数百步；瓶颈更像优化/吸收效率而非数据量。

## 证据质量与局限

- **质量：中高。** 跨任务域与模型家族，并提供明确覆盖指标和多种压力测试。
- state 的相似/覆盖定义会影响结论，不能自动保证语义上关键的低频失败状态被覆盖。
- 单题产生高覆盖不代表 sealed eval 上泛化；训练 rollout 与验证状态仍可能共享生成机制。
- 论文研究生成策略的 token-level OPD，没有直接训练 score-level verifier 或长时程 Agent verifier。

## 最接近的相关工作

最接近的是该团队第一篇 *Rethinking On-Policy Distillation of Large Language Models*、SuRe/OPSA 对 OPD 梯度与低概率 token 的分析，以及 OPD × Test-Time Scaling 对“重排已有能力还是扩大能力集合”的审计。它也与 CROP、SAGE 的状态/高熵选择形成互补：本工作回答覆盖多少，后者更关心哪些状态值得监督。

## 如何复用或推进 LLM-as-a-Verifier

- 对 verifier student 定义“判别状态覆盖”：teacher/student 分歧桶、评分熵桶、错误类型、轨迹阶段与工具状态，而不只用文本 embedding。
- 用少量 seed 任务反复 on-policy 生成 A/B/T 分支；只有 coverage 新增或进入高熵桶时才调用昂贵 teacher。
- 分开记录“已覆盖状态”和“student 校准误差下降”，防止把频繁访问误当作已经学会。
- 对 generative verifier，可让同一轨迹状态生成多种 critique state，再测其对序数评分分布的新增覆盖。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level on-policy verifier distillation**：优先做 1/4/16/全量任务的 scaling ablation，同时保持 rollout 数和 teacher 调用预算可比。
- **pairwise A/B/T 与序数分布**：覆盖指标应按 A胜/B胜/Tie 及各序数桶分层，避免 98% 文本状态覆盖掩盖稀有 Tie 或严重失败桶缺失。
- **真值门控**：程序化成功/失败不应用来定义全部 coverage，但应作为硬标签分层，检查单题是否只覆盖一种终局。
- **student-generated critique states**：把 critique 的新颖性和后续纠错效果纳入 coverage，而非仅统计 critique 文本数量。
- **高熵探索**：单题成功依赖持续状态扩展，支持在高熵分叉保留多样 rollout；过早蒸馏收缩可能直接降低覆盖。
- **sealed eval**：必须保留独立任务、环境与错误类型；论文的高训练状态覆盖不能替代未见环境上的 sealed 评估。