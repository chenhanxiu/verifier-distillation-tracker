# ExecRubrics: Executable Tool-Augmented Rubrics for Verifiable and Efficient Long-Form Evaluation

## 基本信息

- 作者：Kaustubh D. Dhole、Charles L. A. Clarke、Eugene Y. Agichtein
- 首次公开日期：2026-08-23
- 版本日期：2026-08-23（v1）
- arXiv：2608.22559
- 原始论文：https://arxiv.org/abs/2608.22559
- DOI：https://doi.org/10.48550/arXiv.2608.22559
- 代码：论文公开页未提供
- 状态：EMNLP 2026 Findings

## 一句话结论

把自然语言 rubric 编译为可检查的 Python 评分程序，可以表达依赖、替代、惩罚和 override 条件，并在三个长文本 benchmark 上达到或超过自然语言 rubric 基线，延迟最高降低 320 倍。

## 真正新增的内容

**论文原文结论：** ExecRubrics 为 rubric 提供固定、可执行、可编辑的操作语义，突破传统加权和无法表达条件依赖的限制，并可调用 NLTK、spaCy 等外部工具。

**分析推断：** 对 Agent verifier 而言，它可承载硬门槛与环境检查，让 LLM Judge 只负责无法程序化的语义维度；这比把所有五维评分塞进同一个 prompt 更易审计。

## 核心方法

把评分准则表示为紧凑 Python 函数：各检查项可组合为依赖、分支、否决和惩罚逻辑，并调用外部文本处理资源；执行结果形成确定性或半确定性分数，用于 pairwise 排序。

## 关键实验结果

在 HealthBench、HelpSteer 和 ArgQuality 上，最佳 preference accuracy 分别为 53%、78%、92%，与自然语言 rubric 基线相当或更优；评估延迟最高降低 320 倍，外部文本工具可进一步提高准确率。

## 证据质量与局限

证据质量中高：已录用论文，覆盖三类长文本 benchmark，并报告效率与准确率。局限是尚非多轮 Agent 轨迹实验；程序 rubric 的生成/维护成本、漏洞与对输入格式漂移的鲁棒性需要额外评估，53% 的任务也表明可执行化并非自动保证高判别力。

## 最接近的相关工作

最接近 WebGrader、FACET、Thinkingbox、G-CARL 和程序化 reward/verifier；区别是重点把自然语言评分逻辑编译成可执行组合规则，而非生成完整环境或单一终态检查。

## 如何复用或推进 LLM-as-a-Verifier

把五维 Judge 拆成“可执行硬检查 + LLM 软判断”：目标达成、工具执行、副作用和安全门槛优先程序化；目标推进与不确定性处理保留 LLM 分布评分。记录每个规则触发路径供审计。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 程序规则提供低噪声门控，LLM teacher 分数只在软维度被蒸馏。
- **A/B/T 与序数分布：** 先用硬规则排除不可行分支，再对剩余分支学习 A/B/T 或序数分布。
- **真值门控：** 与现有 Mock Tool/环境状态天然衔接，可编码硬 fail 和 override。
- **Student critique states：** critique 必须引用具体失败规则与证据，减少泛化批评。
- **高熵探索：** 对硬规则均通过但软评分分歧大的分支保留探索。
- **Sealed eval：** 冻结独立规则版本与隐藏测试状态；训练期 rubric 不直接复用为最终 evaluator。
