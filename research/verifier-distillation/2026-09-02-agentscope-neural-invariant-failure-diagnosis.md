# AgentScope：用行为抽象与 Neural Invariant 诊断 Agent 失败

## 基本信息

- **论文标题**：Diagnosing with Insights: Structured Analysis of Agent Failures via Behavioral Abstractions
- **作者**：Jiayi Bi, Yanjie Gao, Yuanmin Xie, Liqun Li, Tianyin Xu, Fan Yang, Mao Yang
- **首次公开日期**：2026-09-02
- **当前版本日期**：2026-09-02（v1）
- **arXiv**：[2609.02371](https://arxiv.org/abs/2609.02371)
- **DOI**：[10.48550/arXiv.2609.02371](https://doi.org/10.48550/arXiv.2609.02371)（DataCite 注册待完成）
- **代码**：截至 v1 未在 arXiv 页面提供论文代码链接

## 一句话结论

AgentScope 先把长轨迹压成结构化行为图，再用可由神经函数判断的 invariant 约束 LLM 推理，相比直接让 Judge 阅读全轨迹，更稳定地定位失败步骤与类型。

## 真正新增的内容

**论文原文结论**：传统软件诊断难处理 LLM Agent，而纯 LLM Judge 又不可靠。AgentScope 引入行为抽象和 neural invariant：前者将轨迹转成结构表示，后者以神经函数描述 Agent 应满足或违反的行为性质；LLM 在图与 invariant 上推理，联合输出 failure step 和 failure type。

新增点不是更长的诊断 prompt，而是把轨迹语义、候选失败性质和定位推理解耦，并发布更综合的 AgentErrata 数据集。

## 核心方法

从 Agent 消息、工具调用、状态与角色关系构建结构化表示；neural invariants 检查行为性质并保留候选异常；LLM 根据结构图和 invariant 证据完成定位与归因。实验分别在提供/不提供参考 solution 时，与 Who&When 的 all-at-once 和 step-by-step 方案比较。

## 关键实验结果

**论文报告**：在 AgentErrata 上定位准确率随模型/容差设置为 28.38%–54.13%；Who&When Algorithm-Generated 为 25.40%–77.78%，Hand-Crafted 为 22.41%–34.48%。例如 GPT-4o、提供 solution、严格 T±0 时，Hand-Crafted 为 25.86%，高于 step-by-step 15.52% 和 all-at-once 5.26%。但 GPT-5.1 在部分 Who&When 设置只与最强 baseline 持平，说明提升并非普遍。

## 证据质量与局限

覆盖两个数据源、两个 backbone、不同定位容差和有无 solution 设置，且主动披露未一致提升，证据较可信。绝对严格定位准确率仍偏低；多重合理失败点与 annotation policy 会显著影响结果。neural invariant 仍依赖模型判断，不等同于程序不变量；未见公开代码也限制复现。

## 最接近的相关工作

最接近 Who&When、AgenTracer、EDGE、LongRCA、AgenticRAG-FP 与传统 invariant-based debugging。相较 EDGE 的反事实因果边，AgentScope 更强调静态结构与行为性质；两者可互补。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：把五维 rubric 编译为轨迹 invariant：例如“工具调用前具备必要参数”“失败后发生恢复动作”“状态更新与观察一致”。generative verifier 先生成行为图和 invariant 证据，score head 再输出失败位置/类型的联合概率。程序能验证的 invariant 作为硬门，其余保留概率与 abstain。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏“步骤×错误类型”分布，不只蒸馏整轨迹 fail 分数。
- **A/B/T 与序数分布**：对候选下一步比较它违反 invariant 的风险；无法区分时标 T。
- **真值门控**：schema、参数、状态和安全 invariant 程序验证；neural invariant 只补语义层。
- **critique states**：student 生成结构化失败假设，再以 invariant/后续执行检验。
- **高熵探索**：多个合理失败点均保留概率质量，避免单标签迫使 verifier 过度自信。
- **sealed eval**：按新 invariant、新 Agent 框架和人工多标注失败点评测，防止适配固定 taxonomy。