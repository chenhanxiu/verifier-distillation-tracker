# Governed AI-Agent Coordination for Dementia Care: Architecture, Safety Contracts, and Evidence-Derived Workflow Verification

- **作者**：Francesca Medda, Hui Gong
- **首次公开日期**：2026-09-22
- **版本日期**：2026-09-22（v1）
- **原始论文**：https://arxiv.org/abs/2609.25956
- **Canonical URL**：https://arxiv.org/abs/2609.25956
- **DOI**：10.48550/arXiv.2609.25956（arXiv DataCite，待注册）
- **代码/验证材料**：arXiv ancillary files（gcac_harness.py、trace_manifest.json、逐轨迹及消融 CSV），见论文摘要页
- **arXiv ID**：2609.25956

## 一句话结论

【论文原文】把长时程 Agent 的事件、记忆、决策、动作和结果写成可执行契约，并让确定性 policy gate 与 outcome oracle 拥有不可覆盖的否决权，可检测推荐准确率遗漏的重复执行、义务丢失、陈旧状态和假闭环。

## 真正新增的内容

【论文原文】GCAC 将护理协调中的政策义务转译为 18 条可执行 trace contract，明确区分 episodic、semantic、working 和 outcome memory，并把 planner 与授权、执行、结果确认隔离。它不以 LLM 的“看起来合理”作为成功，而要求终局状态、不变量、人类 hand-off、义务保留和 outcome acknowledgment 全部满足。

【分析推断】其领域虽是痴呆照护，但对 Agent verifier × OPD 最有价值的是一个“ground truth as typed state machine”的模板：teacher 的软判断只能在硬契约允许的区域内工作。

## 核心方法

1. typed event-memory-decision-action-outcome contract 保存来源、版本、权限、当前 owner、允许动作和结果状态。
2. deterministic policy enforcement 在工具调用前检查 consent、role、authority、staleness、idempotency 与 hand-off。
3. 18 条 trace 覆盖缺失记录、药物冲突、服务失败、撤回授权、重复事件、非可信文本和未确认结果。
4. 六个单组件消融分别移除不同记忆、policy gate 或 version check，定位安全/连续性职责。
5. 使用 executable oracle，而不是 LLM Judge，对最终状态与不变量逐项验收。

## 关键实验结果

- 完整 GCAC 通过 18/18 contract oracle，0 次违规工具调用；event-threshold 与 stateless-planner 对照仅通过 2/18 和 1/18。
- 去掉 episodic memory 为 17/18；去掉 semantic memory 为 16/18 且产生 2 次违规调用；去掉 working/outcome memory 均降至 12/18。
- 去掉 policy gate 为 13/18 并产生 5 次 inadmissible call；去掉版本检查为 16/18，两个 stale transition 均被接受。
- 对照即使 mock service 返回成功，也记录不到 outcome closure，说明“已发送”不能替代“已完成”。

## 证据质量与局限

【论文原文】论文提供可执行 harness、manifest、逐 trace 结果和组件消融，因果定位清楚。但样本只有 18 条需求驱动 trace，可能存在确认偏差；工具均为 mock，未模拟网络、身份、记录质量或人类响应；stateless planner 是架构代理而非商业 LLM 比较。结果仅证明架构 conformance，不证明临床效果或安全部署。

【分析推断】这是高质量工程证据但外部有效性有限。硬契约本身可能不完备，sealed eval 仍需由不同团队基于事故与未见需求扩展，防止 specification/evaluator 共适应。

## 最接近的相关工作

最接近 ContrAgent 的 LTLf/DFA 轨迹监督、MAGS 的冻结形式安全层、Ground-truth-as-code Agent Evaluation、GameLogicBench 的逐 Tick oracle，以及 Harness-of-Harness/AutoTuneBench 的独立评测隔离。

## 如何复用或推进 LLM-as-a-Verifier

- 把每条 trace contract 作为不可覆盖的 hard label；LLM verifier 只生成缺失义务、证据解释和修复建议。
- 将 contract pass vector 蒸馏为序数/多维评分分布，而不是压成单一 reward；例如“授权、状态新鲜度、结果闭环、义务保留”分别输出概率。
- student-generated critique 只有在引用具体 event/version/outcome 并通过 replay 后才进入 memory。
- 对 A/B/T 分支，任何违反契约的分支直接 B；多个均合规且结果未定时保留 T 与探索。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】实验管线应采用双层 teacher：第一层是程序化契约门控，决定更新方向与否决；第二层是 generative verifier，提供密集 score/critique。score-level OPD 只在 hard gate 未否决且证据完整时使用软分布。高熵状态可沿不同合规动作保留探索。sealed eval 应使用冻结 manifest、独立事故 trace 和版本化 oracle；训练期 verifier、planner 与评测 oracle 不共享可修改规则。