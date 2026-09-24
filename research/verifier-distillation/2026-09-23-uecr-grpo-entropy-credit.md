# UECR-GRPO：熵校准的 verifier–teacher 统一信用分配

## 基本信息

- 论文标题：When and Where to Trust the Teacher: Unifying On-Policy Distillation and GRPO through Entropy-Calibrated Credit Assignment
- 作者：Jie Zhang；Jingxiao Yang；Zhehao Huang；Yuhang Liu；Xiaolin Huang
- 首次公开日期：2026-09-23
- 版本日期：2026-09-23（v1）
- arXiv：2609.28385
- DOI：https://doi.org/10.48550/arXiv.2609.28385
- 原始论文：https://arxiv.org/abs/2609.28385
- 代码：截至 2026-09-24，论文页面未提供作者代码链接

## 一句话结论

UECR-GRPO 在组归一化之前统一 verifier 终局奖励与 teacher 路径效用，再按 teacher 全词表熵衰减并零和重分配 token 信用，避免密集蒸馏改写整条响应的真值总信用。

## 真正新增的内容

【论文原文】Path-Utility Unification（PUU）把 verifier reward 与 teacher-to-anchor 的路径 log-ratio 放进同一 KL 正则目标，并在 GRPO 组归一化前合并；Entropy-Calibrated Redistribution（ECR）用 teacher–old-policy 的有符号 token gap 分配 verifier 信用，以全词表 teacher entropy 降权不确定位置，并通过响应级零和投影保持总信用及 token 符号。

【分析推断】这是“硬真值定总方向、软 teacher 定局部幅度”的最直接新基线，尤其适合 score-level on-policy verifier distillation。

## 核心方法

1. 计算可验证终局奖励和长度归一化的 teacher 路径分数。
2. 在 group normalization 与 PPO clipping 之前合并两类 response-level utility。
3. 依据 teacher 与旧策略的 token gap 做局部信用重分配。
4. 用全词表熵衰减不确定 teacher 指导，并以零和投影保持每条响应的 verifier 总信用不变。

## 关键实验结果

【论文原文】在五个数学推理基准上，Qwen3-1.7B 与 Qwen3-4B student 的 Avg@12 分别为 17.21% 和 65.09%，较各尺度最强基线高 0.89 和 0.56 个百分点。

## 证据质量与局限

【论文原文】覆盖两个 student 规模和五个可验证数学基准，方法约束明确保证重分配前后总信用守恒。

【分析推断】绝对提升较小，且证据集中于数学终局 verifier；“teacher 熵代表可靠性”在开放式 Agent 状态上未必成立。teacher 与 verifier 若同源，仍可能共同偏置，零和约束也不能修复错误的终局奖励。

## 最接近的相关工作

最接近 γOPD、Unified Per-Token OPD Gating、Uncertainty-Calibrated MOPD、RA-OPD、TV-Regulated OPD 与 SIGNBALANCE。UECR 的区别是同时处理组归一化前的 response 排序和保持总任务信用的 token 重分配。

## 如何复用或推进 LLM-as-a-Verifier

将程序化/环境回报视为不可覆盖的 response-level budget，将 generative verifier 的序数分布或 critique-derived teacher gap 仅用于预算内重分配。对 Agent 状态可把全词表熵替换或补充为跨 Judge 分歧、环境可恢复性和 evidence coverage。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】

- score-level OPD：直接实现 `硬真值总信用 + teacher 局部重分配` 基线，并与先归一化后融合做消融。
- A/B/T：把 teacher 高熵或跨顺序不一致状态映射到 T，并令其重分配权重趋近零。
- 真值门控：程序化/环境结算决定整条轨迹的信用总量和符号，teacher 不得翻转。
- critique states：critique 只改变哪些步骤获得信用，不能凭自身文本质量增加总回报。
- 高熵探索：高熵处降低蒸馏强度、保留多个分支；另测“熵高但环境优势明确”的例外。
- sealed eval：使用独立冻结 checker，并报告 teacher 熵校准、总信用守恒和未见 Agent 任务上的迁移，审计 verifier–teacher 共适应。