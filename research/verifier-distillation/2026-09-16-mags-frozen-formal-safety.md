# MAGS：冻结规范下的多 Agent 自动形式化验证

## 元数据
- **论文标题**：MAGS: Multi-agent Auto-formalization Guarantees Safety for Agentic Outputs
- **作者**：Albert Wu、Nicholas Roberts、Tzu-Heng Huang、Haoran Lin、Gil Friedman、Sungjun Cho、Gabriel Orlanski、Frederic Sala
- **首次公开日期**：2026-09-16
- **版本日期**：2026-09-16（v1）
- **原始论文**：https://arxiv.org/abs/2609.19391
- **代码链接**：未发现公开代码链接

## 一句话结论
形式 verifier 能对冻结规范给出机器可检保证，但不能证明自动形式化的语义覆盖了真实目标；硬门控仍需独立功能评测补齐 specification gap。

## 真正新增的内容
**论文原文结论**：MAGS 将人工审计的 API 与安全要求冻结，把生成程序翻译到 Dafny，利用 verifier 反馈修复，再编译回可执行代码；所有测试样例都获得对冻结规范的非平凡安全保证。

**分析推断**：最适合用作“硬真值定方向”的一层，而非完整 reward。形式证明通过但真实功能失败的样本应标为 T/规格缺口，而不是正样本。

## 核心方法
- 冻结人工审计 API 与安全属性。
- 以 Dafny 为 verification-aware 中间表示。
- 多 Agent 完成形式化、验证反馈修复和可执行代码回编译。
- 另设独立安全与功能评价。

## 关键实验结果
**论文报告**：100 个 CUDA kernel、100 个 terminal script、20 个机械臂任务，共 220 例均生成了对冻结规范满足非平凡安全保证的程序；独立评价揭示自动形式语义未覆盖目标行为时仍会失败。

## 证据质量与局限
覆盖三种差异较大的可执行域并有独立评价。局限是 100% 只针对给定冻结规范，不代表现实安全或任务成功；自动形式化语义是主要瓶颈；摘要未给独立功能评测的完整数值。

## 最接近的相关工作
ContrAgent 用 LTLf/DFA 监督工具轨迹，ExecRubrics 编译 rubric，Ground-truth-as-code 动态执行真值。MAGS 更进一步生成形式证明，但暴露 specification gap。

## 如何复用或推进 LLM-as-a-Verifier
构建“形式属性通过 + 环境功能通过 + 软质量评分”的三层 verifier。将证明失败的 counterexample 作为结构化 critique state；将语义覆盖不全作为独立不确定性头。

## 对 Agent verifier × OPD 实验路线的具体影响
- **score-level OPD**：形式失败可硬否决；形式通过只解除安全门槛，不直接给满分。
- **A/B/T**：证明通过且功能通过=A，证明失败=B，规格覆盖不确定=T。
- **真值门控**：冻结规范置于 student 修改面之外。
- **critique states**：使用 verifier counterexample 驱动修复。
- **高熵探索**：只在满足硬属性的分支间继续探索。
- **sealed eval**：用隐藏功能测试与独立规格审计检测 specification gaming。