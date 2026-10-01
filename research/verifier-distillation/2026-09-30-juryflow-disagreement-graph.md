# JuryFlow: Disagreement-Guided Human-in-the-Loop Multi-Agent Evaluation

- **作者**：Mufeng Yang, Junwei Yu, Yepeng Ding
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2609.40103
- **代码**：未发现公开代码链接

## 一句话结论

JuryFlow 不对 Judge 分歧做多数票平均，而在 claim 级构图、按熵选择最值得澄清的争议，并把最小人工干预传播为可复用 rubric。

## 真正新增的内容

【论文原文】候选回答先拆成原子 claim，异构 Judge 给出逐 claim verdict；分歧图的节点由 verdict entropy 计分，边表示结构相似。人工只选择一个 focal disagreement 并给出最小干预，修正再传播到相似 claim 与历史案例。

【分析推断】它适合把三 Judge 投票改成“分歧定位—选择性复核—rubric 更新”，但 rubric 自我更新必须与 sealed evaluator 隔离。

## 核心方法

构建 claim disagreement graph；熵排序选 focal claim；重新评估、图传播，并把纠正固化为 Judge 共享 rubric。自动实验用熵排序代替真实人工选择。

## 关键实验结果

【论文原文】MT-Bench 和 LLMBar 上，相对单 Judge 与多数票 panel 提高 gold agreement；消融分别验证定向复评、传播和 rubric induction 的贡献。摘要未给绝对增益值，且大规模实验为自动配置。

## 证据质量与局限

有两个数据集和组件消融，但没有真实 human-in-the-loop 大规模实验，且非 Agent 长轨迹；共享 rubric 会增加 Judge 错误相关性与 evaluator 共适应风险。

## 最接近的相关工作

VStress、Agreement Overstates Evidence、Robust Conformal Consensus、JudgeProfile、MAWILE。

## 如何复用或推进 LLM-as-a-Verifier

把轨迹拆为事实、动作效果、约束和终局 claim；只把高熵且高影响节点送人工/强 verifier，并记录 rubric 版本和传播范围。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：用 claim-level entropy 和影响度决定复核与蒸馏强度。
- **A/B/T 与序数分布**：分歧节点先保留 T/后验分布，不用多数票强制 A/B。
- **硬真值门控**：可执行 claim 先由环境验证，人工处理不可程序化部分。
- **student-generated critique states**：critique 拆为 claim，并限制纠正规则的适用范围。
- **高熵分叉**：高熵不是直接负样本，而是追加证据和保留探索的触发器。
- **sealed eval**：动态 rubric 仅用于训练；最终评测用冻结、未传播的 rubric 与独立 Judge。
