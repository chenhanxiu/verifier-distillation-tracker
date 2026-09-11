# Beyond Solver Verdicts: Generative Reward Models for Autoformalization

- **作者**：Vikash Singh、Debargha Ganguly、Aman Goel、Ali Torkamani、Xiaoxue Han、Joseph Lilien、Ferhat Erata、Vipin Chaudhary
- **首次公开日期**：2026-09-10
- **当前版本日期**：2026-09-10（v1）
- **原始论文**：https://arxiv.org/abs/2609.11085
- **DOI**：https://doi.org/10.48550/arXiv.2609.11085
- **代码**：截至记录时未发现公开代码

## 一句话结论

GenV 将昂贵的离线 Z3 等价性 oracle 蒸馏成无参考连续 generative verifier，直接展示了“硬真值 teacher → 可部署软评分 student”的 verifier distillation 路径。

## 真正新增的内容

**论文原文结论**：形式化 Verdict-Preserving-Unfaithfulness（错误形式化仍得到相同 solver verdict），并证明仅看结构或 verdict 的验证启发式在这类样本上受限于随机水平；GenV 把 Z3 等价性 oracle 蒸馏到语言模型原生词表读出。  
**分析推断**：这是 score-level verifier distillation 的强原型：硬 oracle 负责标签方向，生成式读出负责连续置信和定位，但不能把严格参考等价直接等同于开放世界任务正确性。

## 核心方法

利用参考形式化和 Z3 离线挖掘 VPU hard negatives，训练 GenV 输出参考等价性的连续分数；GenV+HN 强化难负例。决策投影 logit lens 与 sparse autoencoder 用于分析内部表征，显示模型可在未显式定位训练时读出空间错误坐标。

## 关键实验结果

在合并的 950 条样本（含 260 条 VPU）上，GenV+HN AUROC 为 0.961；text-disjoint 为 0.955。自一致性、ORM、PRM 与 solver-only 分别约为 0.863、0.762、0.756、0.500。联合模型报告错误定位 1.00、检测 0.961，并在 agentic test-time compute 分配中带来 11.3 个点的下游准确率提升。

## 证据质量与局限

有理论论证、hard-negative 设计和下游资源分配实验，证据较强；但数据规模仍小，等价性定义依赖指定 gold reference 与 SMT 可判定边界，合成单编辑错误可能低估真实复合失败。分数在不同形式化风格下仍需重校准，且 verifier 分数本身不会替代更多有效采样。

## 最接近的相关工作

Outcome/Process Reward Models、形式化证明 verifier、solver-grounded RLVR、generative verifier、oracle distillation、hard-negative mining；与 OPDVR/RA-OPD 的硬奖励门控、AutoSciRub/ExecRubrics 的可执行 rubric 最接近。

## 如何复用或推进 LLM-as-a-Verifier

将离线昂贵 oracle 的等价性判断、反例与错误坐标联合蒸馏为“序数分布 + critique”。部署时先用小 verifier 路由疑难轨迹，再调用 oracle 校正高熵样本；把新反例持续加入但不污染 sealed 集。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：以执行 oracle 决定 teacher 信号正负，GenV 连续分数仅控制幅度。
- **A/B/T**：同前缀两个动作若执行等价则标 T；若仅一支保持语义等价则形成硬 A/B。
- **critique states**：蒸馏“错误坐标 + 反例”比单标量更适合 student-generated critique 的准入。
- **高熵探索**：将预算投向 GenV 不确定但 solver 可区分的分叉，而非直接剪掉。
- **sealed eval**：保留未参与 hard-negative mining 的 translator、形式化风格与 oracle 查询集，审计 evaluator 共适应。