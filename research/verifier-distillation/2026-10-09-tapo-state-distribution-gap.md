# Trajectory-Aware Policy Optimization: Closing the State Distribution Gap in Long-Horizon LLM RL

- **作者**：Zhicheng Cai；Weinan Dai；Yuyan Zhou；Wei-Ying Ma；Ya-Qin Zhang；Hao Zhou
- **首次公开日期**：2026-10-09
- **版本日期**：2026-10-09（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.13020
- **Canonical URL**：https://arxiv.org/abs/2610.13020
- **DOI**：10.48550/arXiv.2610.13020
- **代码**：未发现公开代码链接

## 一句话结论

TAPO 指出 token/sequence 级 KL 或 clipping 无法阻止局部偏差沿长轨迹累积成状态分布漂移，并从 off-policy policy gradient 推导轨迹级校正，为 verifier 加权 OPD 的稳定性提供理论参照。

## 真正新增的内容

【论文原文】把长时程训练崩溃归因于 trajectory-induced state distribution gap，使用状态分布修正、几何均值低方差估计和长度自适应 clipping。  
【分析推断】在 Agent verifier × OPD 中，即使每一步 teacher score 看似可靠，student 被推入的新状态可能超出 verifier/teacher 覆盖；门控必须关注累计轨迹漂移而非逐 token 差异。

## 核心方法

1. 从 off-policy policy gradient 推导状态分布修正项。
2. 将修正纳入 RL 目标以补偿长轨迹访问分布差异。
3. 用几何均值估计降低轨迹乘积权重方差。
4. 依据轨迹长度动态 clipping，限制累计偏移。

## 关键实验结果

【论文原文】在八个竞赛级数学与算法 coding benchmark 上，相对 GRPO 最高提升分别为 48% 和 12%，同时显著改善训练稳定性。实验尚非工具 Agent 环境。

## 证据质量与局限

有理论推导与八 benchmark 实验，作为优化研究证据较强；但主要是语言推理/代码生成，未直接验证环境状态、工具副作用或 learned verifier。相对百分比也需结合基线绝对分数解读。

## 最接近的相关工作

与 γOPD、BATON、SHARPO、RELACE、SCAD、Gains and Collapse in OPD 和 PACT 最接近。差异是显式处理策略更新造成的轨迹访问分布变化。

## 如何复用或推进 LLM-as-a-Verifier

训练时记录每个 checkpoint 的状态访问分布、teacher 覆盖度和 verifier 校准；当累计 drift 超阈值时降低软评分权重、请求真实环境结算或重新采样 anchor state。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：把累计状态漂移加入每轨迹权重与 clipping，而非独立处理 token score。
- **A/B/T 与序数分布**：漂移大的分支即使局部分数高也应扩大不确定性或标 T。
- **程序化/环境真值门控**：在新访问状态增加真实执行检查，防止 verifier 外推。
- **student-generated critique states**：只在当前访问分布覆盖内使用；越界 critique 需重新验真。
- **高熵分叉**：动态 clipping 防止单次高分分支把策略推离探索支持。
- **sealed eval**：按轨迹长度和访问分布分层报告，检查长 horizon 上的校准与崩溃。