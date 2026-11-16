# Co-Sight Harness: Externalized Control Assets and Deterministic Enforcement for Long-Horizon Business Agents

- **作者**：Luyao Wang、Xijun Zhu、Zhaohui Hao、Xiwen Zhang、Xingyu Wen、Weishan Li、Yuyang Liao、Yanqin Gao、Yongsheng Du、Lingjun Huang、Shaowei Zhao、Gang Li、Qifan Yu、Baoli Wang
- **首次公开日期**：2026-11-13
- **版本日期**：2026-11-13（v1）
- **原始论文**：https://arxiv.org/abs/2611.17696
- **代码**：https://github.com/ZTE-AICloud/Co-Sight/tree/master/Co-Sight%20Harness
- **标识符**：arXiv:2611.17696；DOI: 10.48550/arXiv.2611.17696

## 一句话结论

【论文原文】把工作流、状态和领域知识外置成版本化控制资产，再以状态机、机器可检查验收门和独立 auditor 约束执行，可在 200 步以上业务轨迹中显著提高无人完成率并降低延迟。

## 真正新增的内容

【论文原文】Co-Sight 不改 backbone，而把长轨迹可靠性问题拆成可版本管理的 workflow/state/knowledge 资产；执行时由确定性验收门强制约束，资产更新只有通过 regression check 和人工批准后才生效，结果轨迹由独立 auditor 评分。

【分析推断】这是一种“硬真值层在外、软 verifier 层在后”的部署模板。对 verifier 蒸馏最有价值的不是性能数字本身，而是明确隔离了 teacher 信号、控制资产、执行状态和独立审计，可减少 evaluator 共适应。

## 核心方法

1. 将业务工作流、显式状态和领域知识维护为版本化外部控制资产。
2. 由状态机推进执行，每个阶段通过机器可检查 acceptance gate。
3. 变更先做回归检查和人工审批；独立 auditor 对最终 trace 评分。

## 关键实验结果

【论文原文】覆盖 3 个已部署、每个超过 200 步的工作流。Domain A 的 120 个端到端案例中，无人完成率从 50% 升至 100%，检索 recall 从 56% 升至 91.67%，延迟从 440 分钟降至 159 分钟，场景分析 recall 从 45% 升至 93%。另两个领域由非资产作者团队分别在 4 天和 7 天完成接管；受控消融分离了链式错误与词汇错配两类失败。

## 证据质量与局限

【论文原文】优势是长轨迹、真实部署、三领域、受控消融和可接管性证据，并已公开代码。

【分析推断】业务领域与指标可能有组织特定性；Domain A 的大幅提升未必能迁移到开放世界 Agent。人工审批参与资产更新，成本未完全量化；独立 auditor 的模型、盲测程度和抗操纵性仍需更细审计。

## 最接近的相关工作

最接近 GCAC 的可执行工作流契约、ContrAgent 的 LTLf/DFA 约束、MAGS 的冻结形式安全层和 AutoTuneBench 的 sealed measurement。Co-Sight 的新增侧重点是版本化控制资产、回归批准与独立 auditor 贯穿真实超长业务工作流。

## 如何复用或推进 LLM-as-a-Verifier

把 acceptance gate 输出作为不可覆盖的 teacher anchor，把 auditor 的序数评分与 critique 蒸馏给轻量 verifier；只允许经 regression check 的 rubric/knowledge 更新进入 teacher。对无法程序化的判断，要求 auditor 引用具体 gate、状态版本和事件证据。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：硬 gate 定义更新方向，auditor score 只在 gate 通过的可行集合内细化幅度。
- **pairwise A/B/T 与序数分布**：同一状态下比较通过不同 gate 的分支；缺失必要状态或资产版本不一致时标 T。
- **环境真值门控**：直接复用状态机与 acceptance gate 作为程序化 teacher 信号。
- **student-generated critique states**：critique 必须绑定资产版本、状态节点和失败 gate 才准入。
- **高熵探索**：在所有硬约束满足时保留多个可行分支，避免把控制流程误变成单一路径模仿。
- **sealed eval**：冻结控制资产、隐藏案例和独立 auditor；训练期任何资产更新不得回写 sealed 集。

