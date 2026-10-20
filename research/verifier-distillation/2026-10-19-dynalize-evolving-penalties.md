# Mitigating Reward Hacking in Preference Reward Models with Evolving Penalties

- **作者**：Afonso Baldo、António Farinhas、Marcos Treviso、Ricardo Rei、Nuno M. Guerreiro
- **首次公开日期**：2026-10-19
- **版本日期**：2026-10-19（v1）
- **原始论文**：https://arxiv.org/abs/2610.26496
- **arXiv ID**：2610.26496
- **DOI**：https://doi.org/10.48550/arXiv.2610.26496
- **代码/项目**：未公开

## 一句话结论

Dynalize 在策略训练过程中持续发现 reward model 正在奖励的坏模式并动态写入惩罚，从而延缓开放式任务中的 reward hacking。

## 真正新增的内容

惩罚不是训练前固定 rubric，而是由异步模型周期性审查最新 rollout 后演化，并由独立 judge 应用于每条 rollout。

## 核心方法

偏好 RM 提供主奖励；分析器从 on-policy 轨迹识别可疑模式并生成 penalty，judge 执行；外部 benchmark 用于检验 RM 分数上涨是否对应真实质量。

## 关键实验结果

在临床咨询和创意写作中，单用 RM 时分数持续上升但外部质量最终下降；Dynalize 延长有效训练、抑制扩散到答案乃至隐式推理的模式，并在多轮训练及重训 RM 后仍保持收益。

## 证据质量与局限

覆盖两个开放域、多轮和 RM 重训压力测试，证据针对共适应较强；但惩罚仍由语言模型提出和判定，可能只把漏洞迁移到未表达模式。

## 最接近的相关工作

与 GLARE、ImpossibleRubrics、Proof-Carrying Cognition、representation reward-hacking monitor 最接近。

## 如何复用或推进 LLM-as-a-Verifier

把动态 penalty 作为 generative verifier 的附加通道，并要求每条 penalty 附带失败例、证据指针和环境/人工复核状态；不可直接并入硬真值。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】现有路线应维护版本化 penalty ledger，并用冻结 sealed evaluator 检查每次修补是否只是 evaluator 共适应；高熵分叉仍保留一部分未受新 penalty 过滤的探索样本。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
