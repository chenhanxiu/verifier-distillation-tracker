# Agent-as-a-Judge

- **作者**：Runyang You、Hongru Cai、Caiqi Zhang、Qiancheng Xu、Meng Liu、Tiezheng Yu、Yongqi Li、Wenjie Li
- **首次公开日期**：2026-11-13
- **版本日期**：2026-11-13（v1）
- **原始论文**：https://arxiv.org/abs/2611.18067
- **配套资源**：https://github.com/ModalityDance/Awesome-Agent-as-a-Judge
- **标识符**：arXiv:2611.18067；DOI: 10.48550/arXiv.2611.18067

## 一句话结论

【论文原文】当静态轨迹缺少环境状态或外部事实时，可靠 Judge 需要主动规划检查、调用工具、使用记忆并依据新证据更新判断，而不能只对给定上下文打分。

## 真正新增的内容

【论文原文】本文把分散的 active evaluator 工作统一到 Agent-as-a-Judge 范式，按多 Agent 协作、工具、记忆与规划组织设计空间，并以“evaluation-directed checks 及其结果如何进入 verdict”界定范围；还汇总已发表结果并复现若干缺失比较项。

【分析推断】它不是新的蒸馏算法，而是为 generative verifier teacher 明确了接口：teacher 不只输出 score，还应输出检查计划、证据获取轨迹和停止/弃权条件。对长时程 Agent，蒸馏对象应从单次 verdict 扩展为可审计的检查策略。

## 核心方法

1. 区分固定上下文 LLM-as-a-Judge 与能主动补证的 Agent-as-a-Judge。
2. 以 evaluation-directed checking 为核心，整理结构化工作流与观察驱动控制两类方案。
3. 从多 Agent、工具、记忆、规划四个机制比较现有系统，并统一关键已发表指标。

## 关键实验结果

【论文原文】论文报告“agentic gain 并不均匀”，并为关键 agentic judge 复现缺失结果；摘要没有给出统一的绝对提升数字。主要贡献是综述、分类与比较，而非单一新模型的 SOTA 实验。

## 证据质量与局限

【论文原文】证据覆盖多种主动评估系统，并公开配套资源；作者同时把成本、可靠性、安全和治理列为尚未解决的部署条件。

【分析推断】跨论文指标与环境不可完全等价，主动取证还可能扩大攻击面、引入工具错误或让 evaluator 与被评策略共适应。该综述不能替代冻结环境上的前瞻对照实验，尤其不能证明主动 Judge 的解释天然忠实。

## 最接近的相关工作

最接近的是 FLARE 的生成式错误链、PaperDoctor 的证据指针与修复、TwinCheck 的负孪生检查，以及 Reality Is the Final Verifier 对现实结算的强调。本文的区别是把这些能力视为 Judge 的主动控制循环，而非一次生成的 critique。

## 如何复用或推进 LLM-as-a-Verifier

把 teacher 输出拆成 `check plan → tool/evidence trace → verdict distribution → abstention`，并分别蒸馏；student 只有在检查结果可复现时才继承 verdict。对于昂贵外部检查，可训练轻量 router 预测何时升级到 agentic judge，但 router 必须接受 sealed false-negative 审计。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：除了最终 score，再蒸馏“需要哪些检查”的策略分数；静态证据足够时才用低成本 student。
- **pairwise A/B/T 与序数分布**：主动检查前后分别保留分布；证据不足或冲突时输出 T，不强制排序。
- **环境真值门控**：工具与环境检查结果负责定方向，Judge 的语言解释只调节信用幅度。
- **student-generated critique states**：把 critique 视为待验证假设，允许 student 主动请求证据后再进入训练缓存。
- **高熵探索**：在高分歧分叉上分配检查预算，而不是用单一 Judge 过早裁剪。
- **sealed eval**：冻结检查工具、权限、外部数据快照和终局 evaluator，单独测量取证增益与取证诱发错误。

