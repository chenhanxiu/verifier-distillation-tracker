# SCAD: Structured Credit Assignment and Distillation for Long-Horizon Agents

- 作者：Shangyang Wu、Shuai Zhao、Ziyue Zhu、Jinyang Wu、Anh Tuan Luu、Haoran Luo
- 首次公开日期：2026-10-02
- 当前版本日期：2026-10-02（v1）
- arXiv：2610.03372
- 原始论文：https://arxiv.org/abs/2610.03372
- Canonical URL：https://doi.org/10.48550/arXiv.2610.03372
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】SCAD 将长轨迹拆成规划与有界子任务执行，并用跨 rollout 的子任务前缀树分配规划信用、在局部上下文蒸馏执行，从而同时利用终局奖励与 teacher 指导。

## 真正新增的内容

【论文原文】它不是把同一条终局奖励广播到所有步骤，而是给规划层完整终局信用，给执行层正终局信用与局部 teacher guidance；跨 rollout 的共同子任务前缀被汇总成树，用于比较哪些规划分叉更可能通向成功。

## 核心方法

【论文原文】Agent 交互被组织为高层 planning 与 bounded subtask execution。执行蒸馏限制在局部上下文，减少长历史导致的 teacher guidance 衰减；规划信用通过跨 rollout 子任务前缀树细化。

## 关键实验结果

【论文原文】相对最强训练基线，SCAD 在文本任务的宏平均准确率提高 4.48 个百分点，在多模态任务提高 4.19 个百分点；论文覆盖长时程文本与多模态 Agent 基准。

## 证据质量与局限

【论文原文】优势是方法同时覆盖规划和执行，并以多基准汇总结果支持。局限是收益依赖子任务边界与树的可比性；正终局信用仍可能掩盖成功轨迹内部的无效步骤；摘要未证明 teacher 信号经独立真值校准，也未展示优化压力下的 reward hacking 审计。

## 最接近的相关工作

最接近 BATON/RLDS 的分层信用分配、DRACO 的轨迹到步骤责任传播、ArenaFlow 的层级轨迹排序，以及 STRIDE 的长轨迹局部监督。SCAD 的特征是“子任务前缀树 + 局部执行蒸馏”。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 verifier 输出分成 planning-node 分布与 execution-segment 分布：前者预测不同子任务前缀的终局可达性，后者判断当前局部执行是否满足子任务契约。二者分别校准后再组合，避免单个整轨迹分数承担全部信用。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level on-policy verifier distillation**：【分析推断】在规划节点蒸馏跨 rollout value，在执行段蒸馏局部 score；可直接作为双层 loss 的消融基线。
- **pairwise A/B/T 与序数评分分布**：【分析推断】同一前缀树的兄弟分叉天然形成 A/B；结果等价或证据不足时标 T，并保留每个节点的成功概率分布。
- **程序化/环境真值门控**：【分析推断】子任务完成条件应由环境断言门控，teacher 只在硬门控通过后分配软信用。
- **student-generated critique states**：【分析推断】每个子任务结束时生成 critique state，记录未满足义务与恢复建议，再决定是否进入下一规划节点。
- **高熵分叉下保留探索**：【分析推断】前缀树能保留多个成功兄弟分支；不要把较低均值但高上置信界的分支过早剪掉。
- **独立 sealed eval**：【分析推断】冻结子任务分割器、终局验真器和隐藏任务；分别报告规划树质量、执行正确性与最终成功率。
