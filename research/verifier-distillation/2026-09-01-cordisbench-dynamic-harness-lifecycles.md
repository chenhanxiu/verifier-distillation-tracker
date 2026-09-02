# CordisBench：动态 Agent Harness 生命周期的可执行真值评测

## 基本信息

- **论文标题**：CordisBench: Can Language Models Reason About Component Lifecycles in Dynamic Agent Harnesses?
- **作者**：Damien Sileo, Dimitri Kachler
- **首次公开日期**：2026-09-01
- **当前版本日期**：2026-09-01（v1）
- **arXiv**：[2609.01600](https://arxiv.org/abs/2609.01600)
- **DOI**：[10.48550/arXiv.2609.01600](https://doi.org/10.48550/arXiv.2609.01600)（DataCite 注册待完成）
- **代码**：[sileod/cordis-bench](https://github.com/sileod/cordis-bench)
- **数据**：论文 arXiv 页面提供 Hugging Face 数据链接

## 一句话结论

CordisBench 用独立有限语义与真实 runtime 执行一致性为动态 harness 推理提供硬真值，显示模型在依赖、清理顺序和终态上的可靠性随交互数迅速下降；这是一类适合程序门控 verifier 蒸馏的长链基准。

## 真正新增的内容

**论文原文结论**：动态 Agent harness 允许模型修改塑造自身执行的软件组件，但局部插件改动会经依赖和 cleanup 传播。CordisBench 用 1,200 道题覆盖受影响组件识别、指定 teardown 顺序后的状态、所有/某些顺序下的性质，以及能否执行成功的重配置选择。

关键新增是同时提供受控形式语义和实际 Cordis runtime，并让一个独立 finite reference semantics 与 528 道可执行题的每个观察/动作结果逐项对齐，从而不依赖 LLM Judge 产生标签。

## 核心方法

任务按相关交互数 2、4、8、16、24、32 分层。模型需要跨组件依赖、生命周期事件和销毁顺序推导终态或选择配置；评分器按任务类型确定性判分。额外实验改变推理 effort，比较准确率提升与 token 成本。reference semantics 与 runtime 双轨校验 ground truth。

## 关键实验结果

**论文报告**：三个效率取向模型在低推理 effort 下，小系统通常表现良好，但随相关交互数增加可靠性下降，终态预测和跨 teardown 顺序推理尤为明显。提高推理 effort 对部分模型有显著帮助，但成本高：GPT-5.6 Luna 在 16 交互子集的 medium effort 每题接近 3,000 reasoning tokens。对 528 道可执行题，独立有限语义在所有用于评分的观察和动作结果上与 Cordis 执行一致。

## 证据质量与局限

证据质量较高：任务规模明确、难度受控、评分确定、reference semantics 与 runtime 交叉验证，且代码/数据公开。局限是合成的 Cordis 组件生命周期不代表所有真实 Agent harness；1,200 道离散问答主要测状态推导，不直接测自主修改后的长期任务成功。可能存在模板模式或 formalism-specific 学习。

## 最接近的相关工作

接近 Thinkingbox、FACET、SBCO、EnvHarness、ExecRubrics 与程序验证/状态机 benchmark。相较只检查最终输出的 Agent 评测，它同时审计中间生命周期状态和顺序量词；相较 LLM Judge，它提供完全可执行、可重复的真值。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：把 reference semantics 作为 teacher 的硬门，训练小 verifier 输出终态的序数风险分布、受影响组件集合和可审计推导；generative verifier 先生成依赖/cleanup critique，再执行候选重配置验证。对预测与执行不一致的状态优先加入 on-policy hard set。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher 可输出每个组件生命周期状态分布，程序执行决定正确方向；比较单标量与结构化分布蒸馏。
- **A/B/T/序数**：同一初态比较两种 teardown/reconfiguration；相同终态标 T，不同风险按可执行结果排序。
- **真值门控**：reference semantics 与 runtime 双验证可直接充当高置信 teacher gate，并检测 harness 自身 bug。
- **critique states**：student 生成依赖链和 cleanup 顺序解释，再由执行器逐步核验；只蒸馏被核验的中间状态。
- **探索**：多个 teardown 顺序在尚未执行前保留概率质量，尤其对“存在某顺序/所有顺序”任务避免贪心剪枝。
- **sealed eval**：隐藏组件图、顺序族与 runtime 版本；最终评价只由独立执行/语义检查产生，避免 evaluator 共适应。