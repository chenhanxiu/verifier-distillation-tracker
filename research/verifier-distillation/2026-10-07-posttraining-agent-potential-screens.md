# Before They Can Solve: Predicting Post-Training Coding-Agent Performance from Base Models

- 作者：Tan Yu、Alexander Bukharin、Khushi Bhardwaj、Jennifer Williams、Zirui Liu、Jonathan Lingjie Li 等
- 首次公开日期：2026-10-07
- 版本日期：2026-10-07（v1）
- 原始论文：https://arxiv.org/abs/2610.10478
- Canonical URL：https://arxiv.org/abs/2610.10478
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】无需让 base model 从冷启动完成整条 coding trajectory，只要在成功轨迹中用测试定位“首次令仓库通过”的决定性步骤，再测 base 对该动作和可验证替代项的支持，即可预测 post-training 后的 Agent 表现。

## 真正新增的内容

【论文原文】把成功的 post-trained 轨迹作为 lookahead，构造 Decisive-Action BPB、Patch MCQ 和 prefix-conditioned pass@k 三种 screen，绕过 base model 尚不会稳定调用工具的混淆。

## 核心方法

【论文原文】逐步重放轨迹，每次代码改动后运行测试，找到失败转通过的首个步骤；测其动作概率、与 verifier 拒绝替代项的选择，以及给定前缀后所有被测试接受的 continuation。

## 关键实验结果

【论文原文】十组公开 base/post-trained 模型对上，三种 screen 对 cohort 排名都与 post-trained SWE-bench Verified pass@1 高度一致。摘要未给出具体相关系数。

## 证据质量与局限

【论文原文】使用执行测试认证决定性动作，并跨十组模型对验证预测排名。【分析推断】依赖已有成功轨迹，且“首次变绿”可能遗漏此前必要但非充分的贡献；主要证据限于 coding agent。

## 最接近的相关工作

【分析推断】接近 RECAP、RLDS、RELACE、Legibility is Not Interpretability 与 trajectory replay 评估；本文关注 post-training 潜力预测而非直接训练信用。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可将决定性步骤及测试拒绝的近邻替代项转成高质量 A/B/T 数据，用于 verifier student；同时把“必要前置贡献”和“首次充分动作”分开建模。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：在 certified decisive state 上加大权重。
- 【分析推断】A/B/T：通过测试的多种 continuation 并列 A，拒绝项为 B，未覆盖为 T。
- 【分析推断】真值门控：逐步测试重放提供不可覆盖的方向信号。
- 【分析推断】critique states：要求 critique 指向使测试状态改变的具体差异。
- 【分析推断】高熵分叉：在决定性前缀生成多 continuation，保留所有通过分支。
- 【分析推断】sealed eval：用隐藏测试重新认证，避免对公开测试共适应。