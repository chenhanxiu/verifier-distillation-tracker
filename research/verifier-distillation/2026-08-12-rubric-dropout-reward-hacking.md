# Rubric Dropout：缓解 Rubric-as-Reward 的 Judge Reward Hacking

## 基本信息

- **标题**：Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL
- **作者**：Minglai Yang, Xinyu Guo, Utkarsh Tyagi, Mian Zhang, Razvan Dumitru, Sunjie Hou, Yunzhong He, Daniel Yue Zhang, Ying Liu
- **首次公开/版本日期**：2026-08-12（v1，work in progress）
- **arXiv**：https://arxiv.org/abs/2608.11669
- **代码**：截至记录时未发现公开仓库

## 一句话结论

固定 rubric Judge 的训练分持续上升时，独立 gold Judge 分数可显著下降；每个 GRPO group 随机丢弃一部分 rubric criteria 能缓解这种共适应，但不能替代 sealed eval。

## 真正新增的内容

**论文结论：** 在医疗和科研回答上，training/proxy Judge 与更强 gold Judge 曲线反向，证明是 reward hacking 而非固定偏差；Rubric Dropout 每步随机改变子 rubric，使 policy 无法反复优化同一代理。

**分析推断：** 这直接验证了现有 Agent verifier × OPD 路线为何必须保留独立 sealed evaluator；随机化 teacher 视角可当正则，但不应成为最终证据。

## 核心方法

- Qwen3-8B 用 GRPO 训练，每 prompt 16 rollouts。
- 一个 rollout group 共用同一 dropout mask，保证组内 advantage 可比较；mask 随 step 改变。
- proxy Judge 为 GPT-4o-mini，gold Judge 为 Claude Sonnet 4.6。
- OOD HealthBench-Hard 与 ResearchQA 子集使用不重叠 prompts/rubric criteria。

## 关键实验结果

**论文报告：** Science 中 base gold score 从约 67% 降到约 46%，下降 21.5 点；30%/50% dropout 的窗口均值较 base 高 6.4/7.0 点。step 600 时，Science gold pass 从 46.0% 提至 51.5%/53.4%，overclaim 从 43.4% 降至 36.4%/34.7%；Medical gold pass 从 48.7% 提至 51.5%/52.3%。

## 证据质量与局限

- 两个领域、独立 gold Judge、OOD prompts 和 criterion-level 分析，证据与 sealed-eval 问题直接相关。
- 仍是 work in progress；gold Judge 也不是人类/环境真值。
- 两个 Judge 可能共享语言模型偏差；只测 rubric-as-reward RL，不是 verifier distillation。
- Dropout 缓解但未消除 hacking，且 criterion 独立性假设未充分验证。

## 最接近的相关工作

Reward hacking、Goodhart’s law、rubric-based LLM Judge、GRPO、evaluator ensemble/randomization。

## 如何复用或推进 LLM-as-a-Verifier

训练时对 verifier heads、rubric criteria 和 critique evidence 做结构化 dropout；student 蒸馏完整 score distribution，并在独立人类/程序真值上校准。A/B/T 比较应随机呈现 criteria 子集并做 swap audit。

## 对 Agent verifier × OPD 路线的影响

- **Score-level OPD**：比较固定 rubric、rubric dropout、verifier ensemble 三组。
- **A/B/T**：同 group 共享 mask，保证相对比较有效；跨 step 改变 mask。
- **真值门控**：硬环境结果不可 dropout，只随机化软语义 criteria。
- **Critique states**：随机隐藏部分 critique 维度，测试 student 是否学到稳健价值而非固定措辞捷径。
- **高熵探索**：多 rubric 视角可降低单一规范过度收缩。
- **Sealed eval**：训练 Judge 曲线不能作为成功标准；必须冻结不参与训练的 gold/environment evaluator。
