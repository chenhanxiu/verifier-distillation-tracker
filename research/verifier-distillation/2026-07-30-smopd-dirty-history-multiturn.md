# SMOPD：Dirty-History 多轮轨迹的选择性熵掩码蒸馏

## 基本信息
- **论文标题**：SMOPD: Selective Token-Entropy Masking for Dirty-History Multi-Turn On-Policy Self-Distillation
- **作者**：Chenyang Jiang, Changhan Huang
- **首次公开日期**：2026-07-30（本次进入 arXiv new submissions 检索窗口）
- **版本日期**：2026-07-30（v1）
- **原始论文**：https://arxiv.org/abs/2608.14647
- **DOI**：10.48550/arXiv.2608.14647
- **代码**：尚未公开；论文称清理后计划发布

## 一句话结论
多轮 student 一旦产生错误中间回复，后续都会建立在 dirty history 上；SMOPD 发现简单丢弃中间回复最低熵的 20% token，比用最终正确率缩放整段 loss 更稳定，但证据仍是小规模、单基准结果。

## 真正新增的内容
**论文原文**：只对中间轮次的蒸馏 loss 做 student-entropy 排序，屏蔽最低熵 20%；最终答案和 FULL-view preservation loss 不改。对比显示最终正确率标量有时反而有害。

**分析推断**：这支持把 verifier 蒸馏预算集中到 student 不确定的 critique/action 位置，但“高熵=值得学习”并未被因果验证，仍需环境结果门控。

## 核心方法
student 生成完整多轮轨迹，privileged self-teacher 在相同 dirty history 上给 clipped generalized JSD 信号。对每个中间回复按 student entropy 排序，只保留高熵 80% token 的 distillation loss；无新增参数和推理开销。

## 关键实验结果
LiC 与 Qwen3 1.7B/4B/8B 上，SHARDED-view accuracy 单种子提升 1.0–2.5 个百分点；4B 小型多种子检查平均 +1.7pp，双侧 p=0.022。只加最终正确率缩放在 1.7B 为 -4.0pp；与掩码结合后随规模变化（4B +1.3pp、1.7B 持平、8B -0.5pp）。

## 证据质量与局限
论文主动降低结论强度：仅 LiC、Qwen3、数学偏重评估、LoRA rank 64、固定 20% 阈值且多为 100 step；跨规模大多单种子，4B 还出现单种子误导案例。没有 raw token logs、checkpoint 或完整代码，不能确认熵与纠错价值的因果关系。

## 最接近的相关工作
OPSD、entropy-selective OPD、DASH、I-SDPO、CrEST，以及按 outcome correctness 缩放的多轮蒸馏。其特点是仅改 loss mask，不改变 rollout 或 teacher。

## 如何复用或推进 LLM-as-a-Verifier
对多轮 Agent 的 student-generated critique/action 计算 verifier/student entropy，只在高熵位置蒸馏 score 或 A/B/T 分布；同时保留低熵错误样本作为 hard-negative 对照，避免把“自信错误”完全漏掉。

## 对 Agent verifier × OPD 路线的影响
- **score-level**：先做 token/turn 熵分层，再测各层 score 蒸馏增益。
- **A/B/T**：高熵分叉保留完整分布；最终 outcome 只做门控，不直接统一缩放。
- **真值门控**：工具/环境成功可否决错误 teacher 信号。
- **critique states**：重点采样 dirty-history 后的高熵 critique。
- **探索**：不剪高熵分支；对低熵分支保留少量审计样本。
- **sealed eval**：跨模型、跨任务、跨 seed 复验；最终 evaluator 不参与 entropy mask 选择。

## 结论边界
目前只能支持“小规模 LiC 上，高熵选择优于所测 outcome-scalar 方案”，不能支持其已普遍解决长时程信用分配。
