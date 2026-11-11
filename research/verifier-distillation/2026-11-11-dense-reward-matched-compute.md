# Are Dense Rewards Worth Their Tokens in GRPO?

- **作者**：Vikash Singh、Weicong Chen、Debargha Ganguly、Yanyan Zhang、Mohsen Hariri、Sreehari Sankar、Wang Yang、Chaoda Song、Alexander Nemecek、Osama Zafar、Yuting Shao、Kai Ye、Biyao Zhang、Xinpeng Li、Shouren Wang、Erman Ayday、Jing Ma、Sanmukh Rao Kuppannagari、Vipin Chaudhary
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.13560
- **代码**：https://github.com/vicky157/grpo-validation
- **标识符**：arXiv:2611.13560

## 一句话结论

【论文原文】稠密过程奖励按 update 看似优于 GRPO，但 continuation 占 91% 生成 token；在等 token 和等 GPU 时间下排名反转，四种 dense-reward 变体都没有超过标准 GRPO。

## 真正新增的内容

【论文原文】论文指出“每个 update 的收益”和单 batch gradient test 都忽略过程奖励的生成成本，提出以生成 token 与训练 GPU-hours 同时匹配的预注册验证协议，并加入副作用控制。它把 verifier/过程信用的价值从纯准确率问题改成资源归一化问题。

## 核心方法

- 为 Monte-Carlo process reward 从中间步骤采样 continuation。
- 对所有训练干预匹配生成 token 预算与 GPU 时间。
- 在六个模型、1,668 次运行上进行预注册比较。
- 评估四种 dense-reward 变体、单 batch per-token gradient test、标准 GRPO 与基于预测成功率的 prompt 选择。

## 关键实验结果

【论文原文】continuation 占总生成 token 的 **91%**。在 Qwen2.5-1.5B 上，Monte-Carlo reward 按 update 领先，但等 token 时比 GRPO 低 **14.3 点**、等训练时间低 **7.8 点**；四种 dense-reward 变体即使给相同训练时间也均未超过 GRPO。选择预测成功率最接近 1/2 的 prompt，在 Qwen3-0.6B 和 Qwen2.5-1.5B 上分别提升 **1.7** 与 **0.8 点**，但标准 GRPO 仅把初始学习率加倍就逼近到半点以内。

## 证据质量与局限

【论文原文】预注册、1,668 次运行、六模型和多种资源口径使负结果证据较强；但结论针对所测 GRPO/dense reward 实现和推理任务，不等于所有低成本 process verifier 都无用，也没有直接测试多轮工具 Agent 的环境复用收益。

## 最接近的相关工作

最接近 Plug-and-Play Process Verifier、BATON、FARM 与 Verifier-Based RL Beyond SFT。本文提供关键反例：更细信用并不自动在等算力下更好，选择训练状态可能比生成大量 continuation 更划算。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】所有 verifier distillation 实验应同时报告每个有效标签的 teacher token、环境步数和 GPU-hours；比较 score-level OPD、pairwise A/B/T 与 generative critique 时，以相同总预算衡量 sealed performance，而不是按 update 对齐。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：增加等 token/等 GPU 的 GRPO 与稀疏 oracle 基线。
- **A/B/T 与序数分布**：只在高信息状态请求昂贵分布，低价值状态保持 T/不查询。
- **程序化/环境真值**：优先复用便宜硬真值，避免用昂贵 continuation 重建已有信号。
- **student-generated critique states**：记录生成与验真成本，按单位成本的 sealed gain 做准入。
- **高熵分叉**：不以策略熵单独分配预算；结合预测成功率接近 1/2 和信息价值。
- **sealed eval**：冻结总 token、GPU-hours、环境步数和 evaluator 调用数后比较方法。