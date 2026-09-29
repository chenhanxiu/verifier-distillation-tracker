# Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents

- **作者**：Yingjian Zhu, Zhenyi Wang, Jiaxin Guo, Kun Ding, Ying Wang, Shen Huang, Xunjie Zhu, Pengjun Xie, Shiming Xiang
- **首次公开日期**：2026-09-28
- **版本日期**：2026-09-28（v1）
- **原始论文**：https://arxiv.org/abs/2609.34296
- **代码**：未在 arXiv 页面提供

## 一句话结论

【论文原文】Dr.Credit 不依赖唯一答案，而以 rubric 为共同参照，衡量每次工具返回相对既有证据历史新增了多少支持，从而为 deep-research Agent 分配过程信用。

## 真正新增的内容

【论文原文】开放式研究任务缺少 canonical answer，现有过程奖励难以落地；论文新增 rubric-grounded incremental support，将重复证据与真正新增支持区分开，并识别每项 rubric 的部分完成度。

## 核心方法

1. 将任务要求拆成 rubric。\n2. 维护每个 rubric 已接受支持的历史。\n3. 评估新工具结果对每项 rubric 的边际支持。\n4. 将 process advantage 与 GRPO outcome advantage 联合训练。

## 关键实验结果

【论文原文】在四个域内与域外 benchmark 上，每个 primary metric 和 submetric 均优于所测开源 deep-research baseline；8B backbone 的平均表现可与所测前沿闭源模型竞争。摘要未给统一绝对提升值。

## 证据质量与局限

【论文原文】同时覆盖 OOD benchmark 与工具预算分析，适合开放式 Agent。局限是 rubric 本身可能不完整或可被迎合；边际支持仍由 evaluator 判断，未证明能抵御证据包装、重复改写或 evaluator 共适应。

## 最接近的相关工作

最接近 DRACO、ArenaFlow、事实核验证据—答案分账与 PaperDoctor；区别是用 rubric-specific evidence history 计算工具步的新增支持。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把最终状态五维评分与逐工具边际贡献统一到 rubric ledger：每步写入证据指针、支持的 criterion、增量与可撤销性；程序真值维度单独硬门控。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：蒸馏每个 rubric 的增量支持向量，而非单标量。\n- **A/B/T 与序数分布**：比较两步对同一 rubric 的增量，证据等价则 T。\n- **真值门控**：可执行事实和环境状态优先于文本支持。\n- **Critique states**：critique 必须指向新增证据，重复意见不给信用。\n- **探索**：对未覆盖 rubric 和高不确定项分配工具预算。\n- **Sealed eval**：冻结 final rubric，训练用过程 Judge 与最终报告 Judge 分离。
