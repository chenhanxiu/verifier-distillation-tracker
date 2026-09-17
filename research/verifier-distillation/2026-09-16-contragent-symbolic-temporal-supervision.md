# ContrAgent：用契约对 LLM Agent 做符号化时序监督

## 元数据

- **论文标题**：Symbolic Temporal Supervision of LLM Agents Using Contracts
- **作者**：Yifeng Xiao、Pierluigi Nuzzo
- **首次公开日期**：2026-09-16
- **版本日期**：2026-09-16（v1）
- **原始论文**：https://arxiv.org/abs/2609.18128
- **代码链接**：未发现公开代码链接

## 一句话结论

同一套独立契约可同时在线门控动作和离线评价完整轨迹，为长时程 Agent 提供确定、可复用且不可被随机 Judge 覆盖的硬 verifier。

## 真正新增的内容

**论文原文结论**：ContrAgent 将工具调用序列转成有限迹上的可检查谓词，用 assume–guarantee LTLf 契约编译为 DFA；同一 DFA 既在线拦截动作，也离线评价记录轨迹，在四个基准上匹配强 LLM-Judge/规则 guardrail，同时在线延迟低多个数量级。

**分析推断**：契约 verdict 最适合作为混合 verifier 的硬门控层，而非替代所有软质量判断；其自动机状态也可成为比自由文本 critique 更稳定的 student state。

## 核心方法

- 将 agent tool trace 映射为固定谓词集合。
- 用有限迹线性时序逻辑表达 assume–guarantee 契约。
- 将契约编译为确定有限自动机，统一在线 action gating 与离线 trace scoring。
- 契约库独立于 Agent 模型，可跨同域多个 Agent 复用。

## 关键实验结果

**论文报告**：在覆盖在线与离线角色的四个基准上，ContrAgent 匹配 state-of-the-art LLM-Judge 和规则 guardrail 基线；在线模式每次调用延迟低多个数量级。摘要未提供逐基准绝对分数，因此不补写未核验数值。

## 证据质量与局限

- 优点：形式语义、确定性执行、在线/离线同构、与模型解耦。
- 局限：契约覆盖率依赖人工谓词和规范质量；不能自然表达开放式审美或隐含目标；“匹配基线”不等于覆盖未知风险；四个基准的域外泛化仍待验证。

## 最接近的相关工作

ExecRubrics 将 rubric 编译为程序，Ground-truth-as-code 动态重算真值，Persistent Teacher Anchoring 在副作用前验证。ContrAgent 的新增点是 LTLf 时序契约与在线/离线共用的 DFA。

## 如何复用或推进 LLM-as-a-Verifier

构建三层 verifier：DFA 契约给硬 pass/fail，序数模型给软质量分布，生成式 verifier 给证据化 critique。将 DFA 当前状态、未满足 obligation 和最短违规前缀编码为结构化 critique state，供 student 学习而不暴露 sealed 契约全集。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：硬契约决定梯度方向/是否更新，软 teacher 决定幅度。
- **A/B/T**：从同一自动机状态生成满足、违反、未决三类分支，天然对应 A/B/T。
- **真值门控**：DFA 是不可覆盖 gate，契约库置于 student 修改面之外。
- **critique states**：使用 obligation/violation state，替代易漂移的纯自然语言 critique。
- **高熵探索**：未决状态保留多个不违规分支，不因单一软评分过早剪枝。
- **sealed eval**：训练只暴露部分契约或抽象状态，完整契约集与隐藏谓词留作独立评测。