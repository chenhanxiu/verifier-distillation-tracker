# VeriEvolve: Evaluator-First Evolution for Tool-Using Agents

- **作者**：Yueshen Li、Kamer Ali Yuksel、Gokhan Tur、Dilek Hakkani-Tür、João Pedro Maia
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.29005
- **arXiv ID**：2610.29005
- **DOI**：https://doi.org/10.48550/arXiv.2610.29005
- **代码/项目**：未发现公开链接

## 一句话结论

VeriEvolve 先构建并冻结 executable evaluator，再优化 Agent；只在轮次之间用强弱轨迹端状态生成反事实测试更新 evaluator，从工程上隔离了同轮共适应。

## 真正新增的内容

提出 evaluator-first 的 Agent evolution：从任务指令生成 challenge states 与可执行 evaluator，先验收评价层，再把它作为 workflow 搜索的固定 fitness。

## 核心方法

同一 evolution round 内 evaluator 冻结；轮间把强、弱执行的 end state 转成成对反事实测试，并用外部 verifier 校准修订，兼顾新失败覆盖与历史检查保留。

## 关键实验结果

在 30 个 MCPMark Filesystem 任务上生成 30 个 evaluator 和 141 个 challenge states；生成套件 141/141 一致，executor 产生的 held-out states 上为 113/122。GLM-5.2 外部验证成功从 6/30 升至 18/30，Claude 从 27/30 升至 30/30；修订消除了弱 executor 暴露的三个假阳性。

## 证据质量与局限

有 held-out 状态与外部验证，证据较好；主量化只覆盖 30 个文件系统任务，其他环境主要是能力边界分析，且 evaluator 仍受可观察状态限制。

## 最接近的相关工作

最接近 CoVer、AutoGym、Dynalize、GameLogicBench、GCAC 与 Proof-Carrying Cognition。

## 如何复用或推进 LLM-as-a-Verifier

将 challenge-state 生成器用于构造 student-generated critique 的反事实验收；只有能区分强弱端状态且不破坏历史检查的 critique/evaluator 才进入 teacher bank。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】现有实验可采用“双时间尺度”：每个 OPD epoch 内冻结 verifier，epoch 间才用新 on-policy 失败更新；更新后必须在 sealed challenge states 和程序真值上重新准入。该设计直接降低 policy–evaluator 同步共适应风险。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
