# AutoTuneBench：Agent 自动调优的可信测量协议

## 元数据

- **论文标题**：AutoTuneBench: Trustworthy Measurement for Agent Auto-Tuning of LLM Serving Engines
- **作者**：Li Chen
- **首次公开日期**：2026-09-16
- **版本日期**：2026-09-16（v1）
- **原始论文**：https://arxiv.org/abs/2609.18123
- **代码与测量语料**：https://github.com/li-ch/autotunebench （v1.0.0）

## 一句话结论

Agent 闭环中的“奖励”必须由修改面之外、冻结且带 provenance 的测量协议产生；否则基线、机器差异和基础设施缺陷足以制造虚假改进。

## 真正新增的内容

**论文原文结论**：AutoTuneBench 将测量协议冻结为代码，以数据库 validator、外置 anti-cheat、预注册 readout、外部锚点、配对随机种子统计和完整审计账本约束 Agent 的 propose–measure–keep 闭环。

**分析推断**：它是 Agent verifier × OPD 的 sealed eval 工程模板：teacher 信号不只是一个函数，还包括不可由 student 修改的执行边界、版本 pin、证据账本和事前注册的比较规则。

## 核心方法

- 协议字段冻结并带来源；测试阻止 provenance 丢失。
- 数据库层拒绝越界结果，参考实现和 anti-cheat 位于 Agent 修改面之外。
- A/B 比较预注册，并验证 treatment 确实到达运行。
- 配对 seed、跨运行变异系数上限 5%，结果锚定外部公开测量。
- 每次迭代保存 JSONL evidence ledger 和 append-only gate log。

## 关键实验结果

**论文报告**：四天、619 次模型调用揭示四类测量失真。最佳 kernel 相对天真基线为 10.6×，相对诚实基线仅 2.03×；同一配置跨机器从 1.174× 变为 1.0049×；一次预注册对照在 shared wall 上无效（2.4840 vs 2.4957 ms）；KernelBench Level-1 仅 51% 任务被协议接纳，中位 speedup 为 1.0001×。

## 证据质量与局限

- 优点：代码、语料、329 个测试和 claim-to-evidence 指针公开；测量失真有具体反例。
- 局限：单作者、集中于 serving/kernel 调优；对语义质量与主观目标的迁移仍需额外 Judge；论文未直接训练 verifier 或 OPD student。

## 最接近的相关工作

Harness-of-Harness 强调实现期测试与独立评价分离，Ground-truth-as-code 强调动态可执行真值，Cheap Verifiers, Large Blind Spots 强调闭环仪表盘失真。AutoTuneBench 给出更完整的协议即代码与审计账本实现。

## 如何复用或推进 LLM-as-a-Verifier

把每次 verifier 标签绑定到环境镜像 digest、任务版本、随机种子、调用记录和证据指针；强制执行“student 不可改 verifier/hidden tests/reference”的隔离。对软 Judge 也预注册 prompt、模型快照与聚合规则，并用外部硬测量做 sanity anchor。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：仅蒸馏通过协议 validator 的分数；异常大增益触发隔离复核。
- **A/B/T**：预注册同前缀配对运行；未实际施加 treatment 或跨机不稳定时标 T。
- **真值门控**：把程序化 gate 放在数据库入口，LLM Judge 无权覆盖。
- **critique states**：critique 必须引用 evidence ledger 中可复现事件。
- **高熵探索**：探索可在 sandbox 内继续，但不得污染正式奖励流。
- **sealed eval**：采用 digest-pinned 环境、隐藏 anti-cheat、外部基线和 append-only 审计。