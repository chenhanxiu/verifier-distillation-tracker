# Verifying Agents in Rubric-Graded Environments

- **作者**：Markus Dücker、Vaibhav Kumar、Yi Liu、Ronak Chaudhary、Andreas Plesner、Francisco Guzmán、Anish Athalye
- **首次公开日期**：2026-11-17
- **版本日期**：2026-11-17（v1）
- **原始论文**：https://arxiv.org/abs/2611.22841
- **代码链接**：https://github.com/Handshake-AI-Research/gandalf-the-grader
- **标识符**：arXiv:2611.22841；DOI: 10.48550/arXiv.2611.22841

## 一句话结论

【论文原文】把 verifier 本身作为研究对象后，reactive verification、environment alignment 和 domain guidance 能在更低成本下提高 rubric 级 Agent 评分质量，并跨环境泛化。

## 真正新增的内容

【论文原文】发布 BankerVerifierBench：24 个投资银行任务上的 2,464 条人工判定 rubric；从 rubric corpus 归纳九类 verifier 能力，再压缩为三条设计原则并实现开源 Gandalf，而非只把 Judge 当作固定黑盒。

## 核心方法

1. **Reactive verification**：根据当前 rubric 与证据主动选择检查方式，而非固定一次性 prompt。
2. **Environment alignment**：让判定读取交付物和环境状态变化，不只看 Agent 最终文本。
3. **Domain guidance**：向 verifier 提供领域检查程序与解释边界；以人类 rubric 标签评估准确率、成本与泛化。

## 关键实验结果

【论文原文】在 BVB 上，Gandalf+Gemini 3 Flash 的 F1 为 0.864，强基线为 0.852，而成本约为其五分之一；使用 GPT-5.4 时 F1 提升超过 0.12 且成本更低。在结构不同的 OpenClaw 环境上，Gandalf 达 0.955，最佳基线 0.934。

## 证据质量与局限

【论文原文】有人工 rubric 标签、成本比较和跨环境验证，且代码/数据可复现；但主域集中于投资银行与个人生产力，仍依赖底层闭源模型，宏平均 F1 不能直接证明长轨迹信用定位或抗 reward hacking。早期 workshop 版本统计不同，本记录以 arXiv v1 的 2,464 条/24 任务为准。

## 最接近的相关工作

最接近 LMUnit、Agent-as-a-Judge、Prometheus、DynaGuard、rubric-graded environments 与生成式 reward model。差异在于从 rubric corpus 反推 verifier 能力，并系统比较 verifier 的质量—成本 Pareto 前沿。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可将 Gandalf 作为高成本 teacher：对 student 轨迹主动收集环境证据、输出 rubric 级 verdict 与诊断；再把这些分布/解释蒸馏到小型 criterion scorer。应把“领域指导”和“环境证据”记录为独立字段，避免 student 只模仿语言风格。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher 目标从单总分改为 rubric 级分数向量与证据充分度，再由 student 学习低成本近似。
- **pairwise A/B/T 与序数分布**：同一状态的两个分支按 rubric 分别比较；冲突 rubric 保留分布，不能过早压成单一 A/B。
- **程序化/环境真值门控**：environment-aligned 证据优先，文本 Judge 只解释无法程序化的条目。
- **student-generated critique states**：critique 需指向具体环境读数或交付物，并经过 reactive check 后才进入训练。
- **高熵分叉探索**：在 rubric 间分歧大或证据成本高的状态保留多分支，评估主动检查是否真正减少不确定性。
- **sealed eval**：BVB/OpenClaw 之外保留冻结任务、独立底层 Judge 和人类标签；不能用生成训练 rubric 的同一 pipeline 做最终验收。
