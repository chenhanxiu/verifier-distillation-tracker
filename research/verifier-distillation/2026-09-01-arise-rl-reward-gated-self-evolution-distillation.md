# ARISE-RL：以 Rubric 为中介的 Agent 自演化与奖励门控自蒸馏

## 基本信息

- **论文标题**：ARISE-RL: Agentic Rubric-Grounded Iterative Self-Evolution with Reinforcement Learning
- **作者**：Fanrui Zhang, Ruixue Ding, Qiang Zhang, Xi Chen, Boli Chen, Shihang Wang, Qiuchen Wang, Hongmin Zhan, Jinxin Bian, Xingchao Li, Peijin Zheng, Hao Cheng, Pengjun Xie, Kaipeng Zhang, Jiawei Liu, Zheng-Jun Zha
- **首次公开日期**：2026-09-01
- **当前版本日期**：2026-09-01（v1）
- **arXiv**：[2609.01058](https://arxiv.org/abs/2609.01058)
- **DOI**：[10.48550/arXiv.2609.01058](https://doi.org/10.48550/arXiv.2609.01058)（DataCite 注册待完成）
- **代码**：[Alibaba-NLP/qqr](https://github.com/Alibaba-NLP/qqr)

## 一句话结论

ARISE-RL 把真实工具观察约束的 rubric、能力边界任务生成和“只有 memory teacher 实测奖励更高才启用”的同策略反向 KL 蒸馏连成闭环，是目前与程序化门控 Agent verifier × OPD 路线最直接的公开实现之一。

## 真正新增的内容

**论文原文结论**：Generator 在真实工具观察之后生成任务及 rubric，并被奖励去寻找约半数 rollout 成功的中等难度任务；Solver 接受逐 rubric 项的稠密奖励。RG-SED 用同一策略加 coach memory 构造临时 teacher，只有其组平均奖励相对普通 rollout 的增益超过阈值时，才在普通 on-policy 轨迹上加入 token-level reverse KL。

相较普通 OPD，这里新增的关键不是另一个 teacher，而是把“是否蒸馏”绑定到同组经验收益，并让 teacher 与 student 共享参数、仅条件上下文不同，从而缩小分布差距。论文还发布 ECR-Bench：100 条专家校准深度研究任务，以及五类、每类 100 条的多工具旅行任务，同时评估最终答案和工具过程。

## 核心方法

Generator 奖励由工具观察门、格式门和难度奖励相乘；难度在 (K) 个 Solver rollout 约一半成功时最大。Solver 奖励为 rubric 满足率与全部完成奖励的加权和。Coach 从一组失败与反馈生成角色相关 memory；同一模型在 memory 条件下产生临时 teacher 分布。若组均值奖励差 (Delta_r>	au)，则按 warm-up/decay 系数加入 reverse-KL，否则不蒸馏。Generator 与 Solver 都使用这一机制。

## 关键实验结果

**论文报告**：Qwen3.5-9B 上，ARISE-RL 在 ResearchRubrics、ECR-DeepResearch、VitaBench、ECR-Travel 的聚合分数分别为 0.479、0.781、0.417、0.599；去除 RG-SED 后分别降至 0.422、0.716、0.350、0.518。取消奖励门控也低于完整方法（0.438、0.725、0.371、0.523）。三轮共演化中四个基准均单调上升。ECR-Travel 训练组里，8.3% 的 memory 使奖励显著下降，19.6% 落在模糊区，说明近三分之一组不应盲目蒸馏。论文称在同设置下 RG-SED 的 11 个评测轴均优于 OPCD 与 GKD。

## 证据质量与局限

证据较强：同 backbone、同训练数据和同 rubric judge 比较，并有组件消融、门控统计和四次独立运行。但所有核心实验仅覆盖 8B/9B；rubric scorer、coach、格式检查都由 GPT-5.2 提供，训练闭环仍可能学习该 evaluator 的偏好。ECR-Bench 虽经专家校准，论文没有证明其与训练 rubric/judge 完全独立，因此不能把“所有轴更高”直接解释为真实泛化或更强因果信用分配。

## 最接近的相关工作

最接近 OPCD、GKD、Dr. Zero、Absolute Zero、RubricEM、EvolveR，以及带程序化奖励门控的 OPDVR/RA-OPD。与后两者相比，ARISE-RL 的门控来自同组 memory 条件 rollout 的经验奖励差，且同时训练任务/rubric Generator；与 RubricEM 相比，它更明确地把 rubric、在线能力边界课程和 token 分布蒸馏合并。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：把二值 rubric 满足 (z_j) 改为每项序数分布（失败/部分满足/满足，外加置信度），同时保留硬工具门作为 override，可得到 distributional verifier teacher。对同一前缀生成 A/B/T 三个行动或 critique 分支，用真实环境回报或 sealed checker 估计组级增益，再只蒸馏获证改善的 score/critique 分布。Coach memory 可直接作为 student-generated critique state，但应与评分头分开记录，避免 explanation 与 score 互相强化。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：优先实现“同组 teacher–student 经验奖励差门控”，并与无门控、仅正向样本、连续增益加权比较。
- **A/B/T 与序数分布**：将逐 rubric 二值判定扩展为 A/B/T 排序和序数概率，而不是只蒸馏总分均值。
- **真值门控**：沿用真实工具观察门；可执行条件决定梯度方向，LLM rubric 只提供幅度或软信用。
- **critique states**：让 student 先生成 memory/critique，再用环境结果检验其是否改善后续 rollout；未改善的 critique 不进入蒸馏。
- **高熵探索**：任务生成目标直接瞄准约 50% 成功区域；在动作高熵处保留未被证伪的分叉，避免 reverse-KL 过早收缩。
- **sealed eval**：训练用 judge/coach 与最终评测必须模型、提示、rubric 和任务来源隔离，并报告环境终态与独立人工/程序检查结果。