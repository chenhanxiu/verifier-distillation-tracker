# 对比式自蒸馏：用正负 Privileged Teacher 抵消行为漂移

- 论文标题：On Repulsive and Attractive Teachers: Separating Correctness from Behavior in Self-Distillation
- 作者：Anton Baumann；Akmal Ashirmatov；Leo Schmidt-Traub；Frederike Lübeck；Jonas Hübotter；Thomas Kleine Buening；Andreas Krause
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.21561
- DOI：https://doi.org/10.48550/arXiv.2609.21561
- 相关实现基础：https://github.com/lasgroup/SDPO（论文使用其 sampled-token 实现；并非本论文独立代码发布）

## 一句话结论

Privileged teacher 的概率差不只携带“正确性”，还会压短或拉长推理；用正确解条件 teacher 与错误解条件 teacher 的对比 log-ratio，可抵消共同风格偏移并保留更接近正确性的 token 信号。

## 真正新增的内容

- 【论文原文】分别隔离 attractive self-distillation 和 repulsive self-distillation，证明二者会产生方向相反的行为漂移：前者压缩探索、变短且更自信，后者使响应变长、可能唤醒隐藏 thinking mode 并最终不稳定。
- 【论文原文】提出 balanced contrastive self-distillation：靠近正确解条件 teacher，同时远离错误解条件 teacher。
- 【论文原文】在 1/2 权重下 student 自身项精确相消，token advantage 化为正负 teacher 概率的 log-ratio。
- 【分析推断】这直接挑战“teacher–student gap 就等于能力差”的假设：gap 中可能混有长度、思考模式、语气和探索偏好，score-level OPD 必须先做行为去混淆。

## 核心方法

对 student 的同一 on-policy prefix，分别构造带正确解上下文的正 teacher 和带错误 rollout 上下文的负 teacher。正向 reverse-KL 提供 attraction，负向项提供 repulsion；平衡组合后，每个 token 的监督只取正负 teacher 的相对支持。实验单独优化蒸馏目标，不叠加 GRPO reward，从而隔离蒸馏信号本身。

## 关键实验结果

- 【论文原文】Qwen3-4B 非 thinking、Qwen3-4B-Instruct-2507 和已开启 thinking 的 Qwen3-4B 三种设置中，contrastive 训练均能提高训练与评测表现，同时响应长度平稳、低于 token cap。
- 【论文原文】纯 repulsive 在 instruct-only 模型上也先提升后因长度暴涨、截断而崩溃；因此不稳定不能只归因于切换到显式 thinking mode。
- 【论文原文】已开启 thinking 的 Group Anagrams 设置中，repulsive 大约在第 12 step 后因长度增长崩溃；contrastive 则持续改善。
- 【论文原文】数学评测覆盖 AIME 2024/2025/2026、AMC23、HMMT25、MATH-500；主模型规模为 4B。

## 证据质量与局限

- 【论文原文】实验有三类行为初态，并刻意不混入 GRPO，有助于识别 causal mechanism；但结果主要以训练曲线和宏平均呈现。
- 【论文原文】模型集中于 Qwen3-4B，任务集中于数学与程序化 anagram，正/负上下文质量依赖专家解或同组 rollout。
- 【分析推断】“行为漂移抵消”依赖正负 teacher 具有相似的非正确性行为；在 Agent 轨迹中，成功与失败分支往往长度、工具类型和状态可达性都不同，抵消未必成立。
- 【分析推断】没有环境级 Agent 实验，也没有独立 sealed evaluator；不能据此断言对比式蒸馏已解决 reward hacking 或 teacher 共适应。

## 最接近的相关工作

最接近 SDPO、RLCSD、CEPO、Anti-Self-Distillation、Self-Distilled RLVR 和标准 OPD。与 TV-Regulated OPD 的共同点是关注更新方向；本工作更具体地把 teacher gap 分解为正确性与行为偏移。

## 如何复用或推进 LLM-as-a-Verifier

为同一 student action/critique state 构造正 teacher（附带环境验证的成功证据）与负 teacher（附带已验证失败或反例证据），用二者的 score/logit 差训练 verifier student。除了最终准确性，还应同步监控响应长度、工具调用数、探索熵、thinking-mode 切换和拒绝率，确认性能提升不是行为模式迁移造成的假象。

## 对现有 Agent verifier × OPD 路线的具体影响

- score-level OPD：增加 positive-evidence teacher 与 negative-evidence teacher 的差分臂，并与单 teacher OPD、reward-gated OPD 做消融。
- pairwise A/B/T：正负证据不能可靠区分时输出 T；避免把风格差异当作 A/B 优劣。
- 真值门控：正负上下文必须来自程序化或环境验证，至少保证更新方向不由 teacher 自己定义。
- student-generated critique states：同一 critique 分别在成功证据和失败证据条件下评分，只保留差分稳定的事实性部分。
- 高熵探索：监控蒸馏前后 policy entropy 与分支长度；attractive 分量过强时限制权重，避免提前坍缩为短答。
- sealed eval：独立测正确率、行为长度、工具多样性与恢复率，防止“分数提高”其实只是 evaluator 偏爱更短或更显式的轨迹。
