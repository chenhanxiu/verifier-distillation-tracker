# Self-Evolving Agents through Privileged Retrospective Distillation

- **作者**：Yuhang Zhou、Yifan Wu、Bo Peng、Mingyi Wang、Jiayi Liu、Xiangjun Fan、Lizhu Zhang、Zhuokai Zhao
- **首次公开日期**：2026-10-20
- **版本日期**：2026-10-20（v1）
- **原始论文**：https://arxiv.org/abs/2610.27495
- **arXiv ID**：2610.27495
- **DOI**：https://doi.org/10.48550/arXiv.2610.27495
- **代码/项目**：未公开

## 一句话结论

RSD 用完整未来轨迹、跨任务先例和复盘经验重新打分 student 已执行动作，把无 ground-truth 的自然 Agent 经验转成多轮 on-policy 自蒸馏信号。

## 真正新增的内容

teacher 与 student 为同一模型，但 teacher 具有 turn-level reflection、future hindsight 与经验库；同时允许更强模型只编辑 privileged context 的构造策略。

## 核心方法

每轮收集 on-policy 轨迹，刷新 precedent/lesson bank，由 privileged teacher 对实际动作重新给分并蒸馏回策略；多轮共同演化模型、经验与监督上下文。

## 关键实验结果

Qwen3-8B/14B 在 ALFWorld、ScienceWorld、SearchQA 上相对 base 最高提升 59.7%；frontier-guided context-policy evolution 相对固定上下文策略再最高提升 44.7%。

## 证据质量与局限

覆盖三个 Agent 环境、两种规模与多轮演化；但核心更新没有真值奖励，hindsight rationalization 与经验库自我强化仍是主要威胁。

## 最接近的相关工作

与 BELIEFWEAVER、The Tasteful Agent、Critique-Conditioned OPD、AtomSD 和 PaperDoctor 最接近。

## 如何复用或推进 LLM-as-a-Verifier

将 privileged teacher 输出拆为可核验事实、因果归因、建议动作；只有事实可由环境回放验证时，critique state 才进入强蒸馏，其余保留为不确定 T。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】适合作为 student-generated critique states 主基线，但必须设置冻结的环境真值抽样与独立 sealed evaluator，防止经验库、teacher 和 student 三方共适应。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
