# Plug-and-Play Verifier for Decoupling Process Reward in Stabilizing Long-Horizon Agentic Reasoning

- **作者**：Mingwei Xu、Jieyuan Pei、Binghao Tu、Hao Fang
- **首次公开日期**：2026-11-10
- **版本日期**：2026-11-10（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.10305
- **代码**：未发现公开代码链接
- **标识符**：arXiv:2611.10305

## 一句话结论

【论文原文】该框架把长轨迹中的中间 reasoning artifact 抽取、领域 verifier 评估和有界聚合解耦成统一接口，再以“稠密过程奖励→稀疏结果奖励”的两阶段训练稳定 Agent 推理。

## 真正新增的内容

【论文原文】actor-critic 的 step advantage 与 GRPO 的组内终局奖励都难以区分“部分有用但最终失败”的轨迹。本文不训练一个统一 critic，而是把不同领域 verifier 作为可插拔模块，对中间 artifact 显式验真并聚合成 bounded process reward，随后与 outcome reward 分阶段结合。

## 核心方法

- 从 Agent 运行轨迹抽取可独立检查的中间 reasoning artifact。
- 通过统一接口调用领域专用 verifier，避免把所有过程判断压进单一 learned critic。
- 将多项验证结果聚合为有界过程奖励，限制局部 verifier 对总更新的支配。
- 先用稠密过程奖励稳定局部推理，再用稀疏终局奖励完成第二阶段后训练。

## 关键实验结果

【论文原文】在 HotpotQA 上，以 Qwen3.5-4B 为目标模型达到 **60.18%** accuracy，超过标准 GRPO 的 **57.73%**。论文据此主张中间 artifact verification 可提高长时程 reasoning 的稳定性；摘要没有提供更多任务、模型或统计区间。

## 证据质量与局限

【论文原文】方法直接针对长时程信用分配，但当前公开摘要的核心数字只来自一个模型和一个 benchmark，提升为 **2.45 个百分点**。未报告 verifier 校准、误报/漏报、不同 verifier 相关性、奖励聚合消融或独立 sealed evaluator，因此泛化证据有限。

## 最接近的相关工作

最接近的是 process reward model、FARM 的逐步失败风险、BATON/RLDS 的分层信用分配，以及 ContrAgent/GCAC 的程序化中间约束。区别在于该工作强调统一的 plug-and-play verifier 接口与有界过程奖励，而非学习一个全局 critic。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把每个领域 verifier 的输出从单点分数升级为序数概率分布，并保留原始证据与 abstain 状态；聚合时按程序真值、环境状态、生成式 critique 的证据等级分层，而不是简单平均。训练可蒸馏聚合后的 score，但最终 sealed evaluator 必须是冻结且未参与奖励塑形的另一套实现。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：将 bounded process reward 作为逐状态 teacher score，和终局 oracle 分两阶段蒸馏。
- **A/B/T 与序数分布**：同一 artifact 上比较候选推理；verifier 不一致或证据不足时输出 T/abstain。
- **程序化/环境真值**：优先级高于 learned verifier，负责不可违背的方向门控。
- **student-generated critique states**：critique 必须指向可抽取 artifact，并经相应 domain verifier 复核。
- **高熵分叉**：有界聚合可防单个 verifier 过度压制探索，但还需显式保留多个近似等价分支。
- **sealed eval**：训练 verifier、过程奖励聚合器与最终 evaluator 三者分离，报告 evaluator 互换后的性能。