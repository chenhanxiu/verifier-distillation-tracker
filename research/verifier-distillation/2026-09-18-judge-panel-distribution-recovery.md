# 多 Judge 面板的有效规模：多样性不等于人类分布恢复

- 论文标题：How Many Humans Is a Judge Panel Worth?
- 作者：Chao Li；Yingying Yu；Yunfeng Li
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.21277
- DOI：https://doi.org/10.48550/arXiv.2609.21277
- 代码与投票数据：https://github.com/Chao1208/chaosnli-judge-votes

## 一句话结论

同一个 32-Judge 面板按“残差多样性”只相当于约 4.24–6.50 个独立人类、按“人类标签分布恢复”只相当于约 2.30–3.75 个；Judge 数量和表面分歧不能替代对序数/类别分布误差的直接校准。

## 真正新增的内容

- 【论文原文】不再把一个 gold label 当唯一真值，而是保留 ChaosNLI 的 100 人经验标签分布，审计 Judge panel 能否恢复人类分歧。
- 【论文原文】提出两个目标相关的有效规模：基于归一化残差 Gram 矩阵参与率的 nu_H，以及匹配 distributional MSE 的 nu_MSE。
- 【论文原文】给出谱分解，说明成员误差能量、残差方向和平均方向权重共同决定分布恢复。
- 【分析推断】这为三 Judge 投票系统提供了直接警告：置信度加权或增加模型数量，可能只增加形式上的“多样”，不一定更接近真实评分分布。

## 核心方法

在 MNLI-m、SNLI、alphaNLI 上收集 32 个模型 Judge 的对齐投票，把每个 Judge 相对人类标签分布的残差组成矩阵。nu_H 用谱参与率匹配条件独立的人类抽样；nu_MSE 则直接匹配面板均值对人类分布的平方误差。作者还分析新增 Judge 对谱多样性和分布误差可能产生的相反变化，以及不同 item half 上排名是否稳定。

## 关键实验结果

- 【论文原文】32-Judge 面板的 nu_H 为 4.24–6.50，nu_MSE 为 2.30–3.75。
- 【论文原文】MNLI-m 和 SNLI 的 consensus-direction variance share 分别为 43.8% 与 33.7%，显示平均后仍保留大量共享误差。
- 【论文原文】在 alphaNLI 上，谱多样性与负分布误差的组内 Spearman 仅 0.223–0.419；按成员误差能量缩放后升至 0.937–0.960。
- 【论文原文】部分新增 Judge 会稳定地提高谱多样性却恶化分布恢复，或反之；alphaNLI 两个 item half 的 panel 排名相关性仅 0.370–0.554。

## 证据质量与局限

- 【论文原文】提供 96,000 条 baseline 与 122,000 条 presentation-order 记录、固定代码快照和可复核谱恒等式，测量证据透明。
- 【论文原文】只覆盖三个分类式 NLI 数据集和一个固定模型池；100 人分布本身有抽样误差；不是新的 panel selection/aggregation 算法。
- 【论文原文】nu_H 与 nu_MSE 都不是通用“替代多少人”的比率，equal-weight residual averaging 也不等同于多数投票错误率。
- 【分析推断】向 Agent 的 0–3 序数 rubric 和 A/B/T 偏好迁移时，需要重新估计分布目标，不能直接搬用这些数值。

## 最接近的相关工作

最接近 ChaosNLI、multi-judge ensemble、human disagreement modeling、distributional evaluation 和 LLM-as-a-Judge calibration。与 Robust Conformal Consensus 互补：后者给覆盖区间，本工作说明“面板有效样本量”必须按目标定义。

## 如何复用或推进 LLM-as-a-Verifier

人工标注不应只存最终多数票，应保留每位标注者的 0–3 分或 A/B/T 分布。对 Judge 面板同时报告：分布 MSE/EMD、校准误差、共享残差方向、成员误差能量、位置反转和同家族相关性。面板选择目标应直接对齐“恢复人类序数分布”，而不是最大化模型间差异。

## 对现有 Agent verifier × OPD 路线的具体影响

- score-level OPD：teacher target 改为校准后的序数概率分布，并按分布恢复误差降低面板权重。
- pairwise A/B/T：T 应表示真实不确定或人类分歧，不应在聚合前被强制二值化。
- 真值门控：有环境真值时让其拥有方向否决权；Judge 面板只刻画软偏好和不确定性。
- student-generated critique states：面板共享高置信结论仍可能是共模偏差，critique 准入需附证据或环境检查。
- 高熵探索：当人类/Judge 分布多峰时保留多个分支，不用平均分过早剪枝。
- sealed eval：用独立人工分布、未参与训练的 Judge 家族和冻结 endpoint 校准；同时报告单标签一致率与分布恢复质量。
