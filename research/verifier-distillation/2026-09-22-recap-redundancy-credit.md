# RECAP：基于语义依赖传播的冗余感知信用分配

## 基本信息

- 论文标题：Giving Credit Where It's Due: Redundancy-Aware Learning for Efficient Reasoning
- 作者：Yuqing Zhou；Hong Wang；Manqing Mao；Zhuoer Wang；Samson Koelle；Jie Yuan；Yanjun Lin；James Feng；Nikki Lijing Kuang；Ziwei Zhu；Wei Niu
- 首次公开日期：2026-09-22
- 版本日期：2026-09-22（v1）
- arXiv：2609.27156
- DOI：https://doi.org/10.48550/arXiv.2609.27156
- 原始论文：https://arxiv.org/abs/2609.27156
- 代码：截至 2026-09-24，论文页面未提供作者代码链接

## 一句话结论

RECAP 用“后续步骤依赖度 × 对正确答案的增量贡献”重塑 GRPO 信用，在不训练独立过程奖励模型的情况下同时提高准确率并缩短推理。

## 真正新增的内容

【论文原文】方法把步骤信用拆为 structural responsibility 与 step efficacy：前者在 LLM 标注的语义依赖图上从终局节点反向传播，后者通过逐步加入推理时 gold answer 对数似然的变化衡量向正确答案的进展，两者共同把 rollout-level GRPO advantage 变成 step-specific update。

【分析推断】它给 student-generated critique state 一个可操作的过滤准则：步骤“被后文引用”仍不够，还需证明其提高了可验证终局的可能性。

## 核心方法

1. 将推理轨迹转成由步骤组成的语义依赖图。
2. 从答案节点反向传播信用，计算每步的结构责任。
3. 比较加入该步骤前后 gold-answer log-likelihood，估计步骤效能。
4. 合并两类信号，重加权 GRPO 的轨迹级优势，无需另训 PRM。

## 关键实验结果

【论文原文】在两个 7B 模型和四个数学推理基准上，RECAP 改善准确率—效率权衡。Qwen2.5-Math-7B 相比 GRPO 的 pass@1 提升 2.0–3.7 个百分点，同时推理 token 减少 8%–31%；分析认为节省主要来自减少推理操作和死胡同，而非仅把措辞压短。

## 证据质量与局限

【论文原文】结果跨四个数学基准，并同时测量正确率与 token 数。

【分析推断】依赖图由 LLM 标注，可能与训练策略共适应；gold-answer likelihood 在开放式 Agent 任务中通常不可得。数学短/中程推理不能直接证明对工具交互、状态变化和长轨迹恢复同样有效。

## 最接近的相关工作

最接近 RLDS、PGPO、BATON、Key-Step Supervision 和 MedTraj。RECAP 的区别是显式建模跨步骤语义依赖，并用答案似然区分“结构重要但方向错误”的步骤。

## 如何复用或推进 LLM-as-a-Verifier

可让 generative verifier 先输出带证据边的步骤依赖图，再由环境 checker 提供终局或中间里程碑 likelihood/通过率的替代量。将每步输出为序数分布：有益、中性、冗余、有害，并保留不确定性而非压成均值。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】

- score-level OPD：用责任度 × 环境效能缩放每个状态的 teacher score gap。
- A/B/T：比较删除/保留某步骤后的可重放结果；结果等价标 T，改善或恶化标 A/B。
- 真值门控：把 gold-answer likelihood 替换为程序测试、状态断言或终局成功概率。
- critique states：只有同时存在依赖边和环境增益证据的 critique 才写入 memory。
- 高熵探索：低结构责任不自动视为错误；若其形成可恢复分支，应保留为探索数据。
- sealed eval：依赖图生成器与终局评测器分离，冻结后在未见任务上检验“删去冗余”是否伤害成功率。