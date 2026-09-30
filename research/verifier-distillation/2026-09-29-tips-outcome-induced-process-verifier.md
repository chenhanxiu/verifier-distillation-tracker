# Inducing Process Supervision from Outcome-Only Reinforcement Learning

- **作者**：Shengda Fan, Xin Cong, Zhong Zhang, Haotian Chen, Yankai Lin
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2609.36641
- **代码与数据**：https://github.com/RUCBM/TIPS

## 一句话结论

TIPS 仅用终局真值奖励训练生成式 PRM，让 4B 模型用 3.2K 条 outcome-labeled 轨迹在 ProcessBench 达到 85.2 F1。

## 真正新增的内容

【论文原文】模型一次生成 CoT、逐步标签和终局标签，奖励只检查预测终局是否匹配 ground truth；group-relative advantage 优化整段输出，从而间接强化有助于正确判断终局的步骤核验能力，不需要人工步骤标签或蒙特卡洛步骤估计。

【分析推断】这是把“程序化终局真值”蒸馏成可解释、逐步 generative verifier 的低成本原型，特别适合长轨迹中稀疏真值向稠密 critique 的迁移。

## 核心方法

生成式 PRM 同时输出推理、每步判断和 outcome 判断；只以 outcome accuracy 计算组相对优势并训练全部 token，使过程判断通过其对终局判别的贡献获得信用。

## 关键实验结果

【论文原文】跨数学、Agent benchmark 和四个 backbone family 验证；TIPS-Qwen3-4B-Thinking-2507 以 3.2K 条 outcome-labeled 轨迹在 ProcessBench 达到 85.2 F1，超过所有被测训练型 PRM 及 GPT-5.4-Instruct、Claude-4.7-Opus 的 prompt-only Judge，但仍落后 o1-mini。

## 证据质量与局限

【论文原文】跨模型族与 Agent 任务，且代码数据公开；但摘要未给出长轨迹错误定位、校准或优化压力下 reward hacking 的完整结果。【分析推断】终局可预测性可能让模型学会捷径，而非真实检查每一步，需用干预式过程验证。

## 最接近的相关工作

PROSE、FLARE、MedSNIP、Beyond Solver Verdicts、传统 Process Reward Model 与 outcome-supervised RLVR。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 生成“步骤序数标签＋证据指针＋终局分布”，由可执行 outcome 决定训练方向；再用步骤删除、交换和反事实恢复测试其 critique 是否因果有效。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：把 TIPS 的逐步分布作为稠密权重，但总符号由环境 outcome 决定。
- **A/B/T 与序数分布**：从逐步生成标签构造 A/B/T；不确定步骤保留概率分布而非硬标签。
- **硬真值门控**：正是训练锚点，应优先采用执行器、测试和环境状态。
- **critique states**：student 自生成 critique 可作为输入状态，但只有改善终局核验时才获正信用。
- **高熵探索**：避免对所有“非最佳”步骤硬负标；同 outcome 的多样路径应并存。
- **sealed eval**：使用未参与 outcome-RL 的冻结环境、扰动任务和独立过程检查器。
