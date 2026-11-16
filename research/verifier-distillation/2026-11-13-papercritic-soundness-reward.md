# PaperCritic: Training AI Reviewers to Assess the Soundness of Papers

- **作者**：Hyun Ryu、Ji Yong Cho、Eunho Yang、Moontae Lee、June Yong Yang、Sean Welleck、Carolyn Rose
- **首次公开日期**：2026-11-13
- **版本日期**：2026-11-13（v1）
- **原始论文**：https://arxiv.org/abs/2611.17834
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.17834；DOI: 10.48550/arXiv.2611.17834

## 一句话结论

【论文原文】PaperCritic 把 AI reviewer 的目标收窄为可相对客观验证的 soundness，以“有效且实质的批评点 precision”和“高质量参考问题 recall”的 F1 作 RL reward，训练结果优于 frontier reviewer 并出现跨领域迁移。

## 真正新增的内容

【论文原文】论文不再模仿包含趣味性、清晰度等主观混合信号的人类总评，而先定义 soundness-only verifier 目标，再构建 PaperSound-23K：来自 1,000 篇 ICLR 投稿的 23,000 条人类与 LLM review point，并给每条 critique 做质量标签。模型用 precision/recall F1 奖励训练。

【分析推断】这为 generative verifier distillation 提供“critique set”而非单一 score 的监督单元：既惩罚无依据的批评，也惩罚遗漏。它尤其适合 student-generated critique states 的准入，但 reference review points 并非环境真值，不能直接当硬标签。

## 核心方法

1. 将 reviewer 目标限定为论文 soundness，剥离 interestingness 与 clarity 等主观维度。
2. 对 review point 的 soundness/substantiveness 和参考问题覆盖做质量标注。
3. 以 critique precision 与 recall 的 F1 为奖励进行强化学习训练。

## 关键实验结果

【论文原文】PaperSound-23K 覆盖 1,000 篇 ICLR 投稿和 23,000 条 review point。PaperCritic 在域内测试上优于 frontier 模型及其他 AI reviewer 训练方法；对 Nature 系论文以及代码审查、法律合同审查、故事反馈也有迁移。摘要未披露具体绝对分数与置信区间。

## 证据质量与局限

【论文原文】数据同时含人类和 LLM 批评点，并有域内、跨出版物与跨任务测试。

【分析推断】“高质量参考点”仍可能不完备或存在同源 Judge 偏差，F1 会继承标注器的盲区；跨领域迁移只说明 review 行为可迁移，不等于事实正确。缺少公开代码和摘要级绝对数字也降低可复核性。

## 最接近的相关工作

最接近 PaperDoctor 的证据化修复、FLARE 的因果错误链、RM-Distiller 的多能力 teacher，以及 MAWILE 对 Judge 多轴鲁棒性的审计。PaperCritic 的区别是把生成式 critique 明确拆成 precision/recall 集合目标，并以此直接训练 reviewer。

## 如何复用或推进 LLM-as-a-Verifier

把 Agent critique 拆成原子但保持依赖结构的 review points，每点附证据指针与可执行复现；分别训练“批评是否成立”和“关键失败是否遗漏”，最后输出 critique-set 分布。环境/程序 oracle 能验证的点作为硬正负样本，其余只作软 teacher。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：同时蒸馏 critique precision 与 recall 两个 score，不用单一均值掩盖“少说但准”或“多说但错”。
- **pairwise A/B/T 与序数分布**：对两组 critique 按证据正确性和覆盖分别 A/B；无法核验的点标 T。
- **环境真值门控**：测试、状态断言和现实结算决定 critique point 是否成立，参考文本只补覆盖。
- **student-generated critique states**：先过 point-level precision gate，再检查是否覆盖首错和关键义务，才进入蒸馏。
- **高熵探索**：保留多个相互独立、证据充分的失败假设，不强迫 critique 收敛为单一叙事。
- **sealed eval**：隐藏 reference issue set 与执行证据，使用独立标注/环境复核，避免 reviewer 与参考点共同适应。

