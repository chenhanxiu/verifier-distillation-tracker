# Scope Before You Persist: Preventing Cross-Family Interference in Agent Memory

## 基本信息

- **作者**：Yezhou Cheng、Runjia Du、Zeming Liu、Qibai Chen、Hang Lyu、Yankai Zeng、Yilan Wei、Bojun Lin
- **首次公开日期**：2026-09-24
- **版本日期**：2026-09-24（v1）
- **原始论文**：https://arxiv.org/abs/2609.29144
- **DOI**：https://doi.org/10.48550/arXiv.2609.29144
- **代码**：论文页面未给出公开仓库

## 一句话结论

即使 memory edit 在原任务族通过执行验真，把它全局检索仍会伤害其他任务；“认证范围 = 检索范围”是 critique/memory 持久化不可缺少的第二道门。

## 真正新增的内容

【论文原文】在 ProcStream-RSI 的 12 轮代码修复流中，用 execution-grounded ORC gate 认证 skill edit，并证明局部有效更新的全局部署会跨任务族干扰；提出 Scoped-ORC，仅在证据覆盖的原始 family 检索记忆。

【分析推断】这把“是否写入 memory”和“在哪些状态允许读取”明确分开，直接修正仅做 critique 准入而没有作用域约束的 Agent verifier 方案。

## 核心方法

【论文原文】ORC 用执行结果门控 persistent skill edit；Scoped-ORC 为每条通过门控的 skill 绑定认证任务族，检索时只在同族启用。干预实验固定 proposal 和 gate decision，只改变 retrieval scope。

## 关键实验结果

【论文原文】固定 proposal/gate 时，family-scoped retrieval 将隐藏轨迹效用从 0.713 提升至 0.816，8 次有害部署从 6 次降至 0。27 个随机顺序配对流中，Scoped-ORC 相对 Global-ORC 平均效用提高 0.063，区间 [0.037, 0.094]；接受 63 对 12 次更新，63 次接受中无有害项。Global-ORC 的 0.713 低于静态 Agent 的 0.775。

## 证据质量与局限

有固定 gate 的因果干预、随机顺序配对与隐藏轨迹效用，证据较强；但只覆盖一个代码修复流，task-family 标签可能由实验者提供，开放世界中如何发现作用域仍未解决。

## 最接近的相关工作

与 Grounding Agent Memory、RSIAgent、SkillAA、DENSE 和 PaperDoctor 最接近。区别是它不只验证 memory 内容，还实证检索授权范围本身会决定长期效用。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】让 verifier 为 critique 输出 `(verdict, ordinal confidence, evidence pointer, certified scope)`；环境真值只授权相应 scope。跨 scope 调用时默认 T/INCONCLUSIVE，并要求重新验证，不能继承原分数。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- student-generated critique state 增加 `scope_id` 与证据哈希。
- OPD 只在认证 scope 内蒸馏；跨族样本不视为负例，而是未授权。
- 高熵分叉可检索多个局部 skill，但必须分别保留 provenance 与冲突。
- sealed eval 使用新任务族和乱序流，单独报告错误迁移、拒绝率和长期累计效用。
- evaluator、memory gate 与最终评测器分离，避免共同接受同一种局部捷径。