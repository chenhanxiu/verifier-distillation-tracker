# Verify by Doing: Co-Evolving Agent Execution and Evaluation without External Feedback

- **作者**：Yitong Lin、Jianda Chen、Yihao Hu、Pan Wang、Hang Wang、Zhihao Wen、Xiaoxue Ren、Wei Wu
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（v1）
- **原始论文**：https://arxiv.org/abs/2611.15276
- **代码**：未见公开代码仓库
- **标识符**：arXiv:2611.15276；DOI: 10.48550/arXiv.2611.15276

## 一句话结论

【论文原文】Verify by Doing 让 Evaluator 主动调用工具检查产物与环境状态，并与 Actor harness 在单任务内共同演化；在无外部反馈设置下，三个基准分别领先最强基线 3.3、4.1、2.3 个百分点。

## 真正新增的内容

【论文原文】Evaluator 不再只读轨迹，而是“通过行动验证”：检查 artifact 和 environment state，用所得证据选择输出并更新执行/验证流程；候选 Evaluator 在同一候选集上比较，Actor 更新还必须由自身新输出支持。固定候选池实验表明，仅改进验证即可找回已有成功输出。

【分析推断】该工作提供了 generative/tool-using verifier 的强原型，但 Actor 与 Evaluator 共演化意味着训练内分数不能直接视为独立证据；它尤其需要 sealed eval 才能区分真实改进与 evaluator 共适应。

## 核心方法

1. Actor 产生候选执行与结果。
2. Evaluator 调用工具读取环境和产物，形成有证据的内部成功信号。
3. 在公共候选集上比较 Evaluator；Actor 规则的更新需由新鲜输出支持。
4. 模型权重保持冻结，演化发生在执行与验证 harness。

## 关键实验结果

【论文原文】在 AutomationBench、τ³ Banking 与选定 GDPval 任务上，相比同样无外部反馈的最强基线分别提升 3.3、4.1、2.3 个百分点；消融支持主动验证与 Evaluator 演化的贡献。

## 证据质量与局限

【论文原文】覆盖自动化工作流、银行任务和专业产出，且有固定候选池与组件消融。

【分析推断】“无外部反馈”不等于“有真值保证”；工具读取到的状态可能不完整，Evaluator proposal/review 仍在同一闭环内。未见跨版本冻结 Judge、隐藏环境断言或长期多轮累积误差的完整报告。

## 最接近的相关工作

最接近 CoVer、FLARE、VeriTAS、LLM-as-an-Improver 与自改进 harness。VbD 的区别是同时演化执行和验证程序，并要求验证者主动取证，而非仅生成 critique 或依赖预先给定 verifier。

## 如何复用或推进 LLM-as-a-Verifier

可把主动工具检查生成的“证据—断言—结论”三元组蒸馏到轻量 verifier；环境可直接判定的部分提供硬标签，开放式部分保留序数分布。对 evaluator 的每次更新做 frozen-candidate paired audit，并让独立 reference evaluator 校准其乐观偏差。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher score 必须附带主动检查证据，缺证据则降权或标 T。
- **A/B/T**：同一候选集上比较新旧 Evaluator 与 Actor，分歧且无环境证据时输出 T。
- **环境真值门控**：把工具检查结果绑定到实际对象版本、事务状态和时间戳。
- **critique states**：仅接纳能触发可复现检查并定位对象的 critique。
- **高熵探索**：固定候选池分析可用于区分“更会选”与“生成更好”；在高熵分叉保留多个可验证候选。
- **sealed eval**：必须冻结隐藏任务、环境断言、Evaluator 版本和候选生成预算，独立评估 Actor/Evaluator 的组合与拆分贡献。
