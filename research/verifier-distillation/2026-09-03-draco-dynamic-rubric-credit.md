# DRACO: Fine-Grained Credit Assignment with Dynamic Rubrics for Long-Horizon Agent Training

## 基本信息

- **作者**：Shubham Gandhi, Saurabh Goyal, Kiran Kate, Yara Rizk
- **首次公开日期**：2026-09-03
- **版本日期**：2026-09-03（v1）
- **arXiv**：2609.04094
- **原始论文**：https://arxiv.org/abs/2609.04094
- **代码**：https://github.com/IBM/draco
- **DOI**：https://doi.org/10.48550/arXiv.2609.04094

## 一句话结论

DRACO 用随策略演化的动态 rubric 对完整轨迹只评分一次，再依据 rubric 的步骤引用把组优势重分配到责任步骤，在没有程序化 verifier 的 AppWorld 上优于稀疏真值 GRPO。

## 真正新增的内容

**论文原文结论**：动态生成 prompt-specific 与 trajectory-specific rubrics，得到逐项判断及引用步骤，再以闭式规则重新分配每条轨迹的 advantage；无需训练额外 attribution model。

**分析推断**：这是“生成式 verifier → 结构化 rubric → step-level score”的直接工程模板，但 rubric 生成器和评分 Judge 同源时会形成共适应闭环。它适合做 teacher 信号，不应直接兼任 sealed evaluator。

## 核心方法

- 每个 rollout 生成任务特定和轨迹特定 rubrics，组内合并、去重，并删除所有 rollout 都满足的无区分项。
- Judge 对完整轨迹逐 rubric 评分并引用负责步骤。
- 将 GRPO 的轨迹级优势按步骤质量权重重新分配；保持每条轨迹总梯度质量不变。
- 对 static/dynamic rubric、是否 credit redistribution、frontier/self judge 与多次一致性进行对照。

## 关键实验结果

- AppWorld：相对 base model 提升 **15.9 点**，相对使用稀疏 ground-truth reward 的 GRPO 提升 **5.3 点**。
- 域外 Tau-Bench：摘要报告相对 base model 提升 **5.3 点**；公开代码 README 当前写为 **4.6 点**，两处存在数值不一致，应以最终论文表格复核。
- 公开仓库提供训练、评测与分析代码，并列出八种控制设置。

## 证据质量与局限

- **质量：中高。** 有真实长时程 Agent 环境、域外评测、成分对照和公开实现。
- 核心 reward 来自 LLM Judge，而不是可执行真值；步骤引用是否具有因果性没有被反事实 rollout 充分证明。
- 动态 rubric 随策略变化，可能导致 reward 标尺漂移。
- 摘要与代码 README 的 Tau-Bench 增益存在 5.3/4.6 点差异，当前记录不把该差异解释为已解决。
- self-judge 设置尤其需要独立 evaluator 防止评分与策略共同适应。

## 最接近的相关工作

与 LURE、PGPO、CrEST、Key-Step Supervision 的长轨迹信用分配最接近；与 AutoSciRub、ExecRubrics、Rubric-to-Code 的 rubric 结构化方向互补。相比纯 outcome reward，DRACO强调把轨迹级判断分摊到步骤；相比反事实方法，它成本低但因果证据更弱。

## 如何复用或推进 LLM-as-a-Verifier

- 将 rubric verdict 从单一分数改为序数分布（严重失败/轻微失败/不确定/部分完成/完成）并保留不确定性。
- 对 Judge 引用步骤构造局部 A/B/T：保留前缀，只替换被引用动作，使用环境重放检验 credit 方向。
- 程序可验证 rubric 使用硬门控；主观 rubric 使用生成式 Judge，且二者分头记录。
- student 先生成 critique state，teacher 只审核 critique 是否覆盖动态 rubric，再蒸馏 critique→分布评分。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：把每步 rubric 分布而非最终总分蒸馏给 verifier student，并保留轨迹总质量守恒约束。
- **A/B/T 与序数评分**：由同一前缀、不同动作的 rubric 差异生成 A/B/T；近似相等时显式标 Tie，避免强行排序。
- **真值门控**：AppWorld 可执行成功必须拥有 override；LLM rubric 仅补足软目标和信用分配。
- **critique states**：动态 rubric 可作为 critique 的结构骨架，但应评估其是否预测后续可执行改进。
- **高熵探索**：只对高分歧 rubric 或高熵步骤加强 teacher 蒸馏，避免对整条轨迹均匀收缩。
- **sealed eval**：冻结独立 rubric 集、Judge、环境版本和终局检查器，报告训练 Judge 与 sealed Judge 的差距。