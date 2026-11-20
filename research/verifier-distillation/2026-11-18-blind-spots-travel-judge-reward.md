# Blind Spots Travel, Knowledge Stays Home: What RL Inherits from an LLM Judge

- **作者**：Liang Yue, Eric A. Vance
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：[arXiv:2611.25191](https://arxiv.org/abs/2611.25191)
- **DOI**：[10.48550/arXiv.2611.25191](https://doi.org/10.48550/arXiv.2611.25191)
- **代码与数据**：[liyu2195/blind-spots-travel](https://github.com/liyu2195/blind-spots-travel)

## 一句话结论

【论文原文】814 次 RL 运行表明，LLM Judge 的逐题知识几乎不会泛化给 student，但其类别级盲点会被策略系统性继承；【分析推断】Verifier 蒸馏必须把“局部标签正确率”和“错误依赖结构”分开审计，并用 sealed 类别切片防止 reward 偏差被放大。

## 真正新增的内容

【论文原文】作者系统改变唯一变量——给 7–8B student 提供奖励的 grader——比较答案键、同规模 Judge、更强 Judge、人工放置错误的 grader，以及 student 自身 32 样本投票。结果区分了两种迁移：单个问题上的知识基本不迁移，而对一类问题的拒绝/接受偏见会强烈迁移。

【分析推断】这为“teacher 更强所以蒸馏更安全”的常见假设给出反例：真正危险的是相关错误和类别条件偏差，而不只是平均准确率。

## 核心方法

【论文原文】

1. 在 PopQA、TriviaQA、NQ-open 等闭卷问答上训练模型回答或拒答；
2. 使用 GRPO+LoRA，并固定 student、训练配方与数据，只替换 grader；
3. 构造可控错误 grader，改变少量类别相关 verdict；
4. 在 held-out 问题、类别探针和强制禁止“I don't know”的解码条件下区分知识丢失与读出策略改变；
5. 公开训练代码、配置、每次运行答案、Judge 分数和审计脚本。

## 关键实验结果

【论文原文】

- 814 次 RL 运行覆盖多种 student、grader 和数据集。
- 更强 Judge 对新问题的新增知识仅约每百题纠正 1 题。
- 让 Judge 错拒前国家首都类别中 12 个正确训练答案的 11 个，会让 student 在新问题上拒答 98%。
- 仅手工改变这 12 个 verdict，即可把拒答率从 5% 推至 90%。
- 即使总体接受率对齐答案键，四个 Judge 中两个仍使该类别损失 38–42%。
- 禁止拒答后，模型仍能正确回答 94%，说明能力尚在、策略读出被 reward 改写。

## 证据质量与局限

【论文原文】证据规模大、对照清晰，并公开原始运行输出与检查脚本；人工错误放置提供了强因果识别。局限是任务为闭卷 QA/拒答，训练周期、动作空间和长轨迹信用结构仍比真实 Agent 简单；结论不等于所有 Judge 知识都无法迁移。

【分析推断】Agent 场景可能更严重，因为同一偏差会沿多步轨迹影响状态访问；也可能因环境真值及时纠错而缓解，需实测。

## 最接近的相关工作

- RLAIF 与 LLM Judge reward：研究模型反馈作为 RL 奖励。
- Who Judges Matters、Agreement Overstates Evidence：研究 Judge 家族偏好与错误相关性。
- Calibration Is Not Verification：强调一致与校准均不能替代真值。
- GLARE：用当前策略负样本持续更新 reward estimator，但也面临 evaluator–policy 共适应。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】在 verifier 数据集中加入“类别保持”与“错误相关性”审计：除总体 AUC/ECE 外，报告每类任务、每类失败、每种工具调用的拒答/误奖迁移矩阵。teacher ensemble 应按误差独立性而非模型数量加权；对类别级异常由环境 oracle 或人工小样本覆盖。

## 对现有 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level on-policy verifier distillation**：teacher 分数进入 OPD 前需做类别条件残差审计，不能只看总体相关性。
- **pairwise A/B/T 与序数评分分布**：保留各 Judge 分布及分歧，避免多数票掩盖共同盲点；T/拒答率需按类别拆解。
- **程序化/环境真值门控**：少量硬真值应优先覆盖高杠杆类别，而非均匀抽样。
- **student-generated critique states**：训练 critique 前检查其错误是否集中迁移到某类状态；异常类别不进入记忆。
- **高熵分叉保留探索**：student 自身多样采样投票可作为低成本基线，避免盲目追随外部 Judge。
- **独立 sealed eval**：必须含未见类别与对抗类别切片，且 evaluator 不参与训练或阈值调节。
