# Where Autonomy Belongs: A Separation of Powers for Agentic Program Evolution

- **作者**：Zhengyang Ai、Tong Liu、Jingxian Tang、Xiaobing Du、Tao Xiao、Fengshi Zhang、Zishuo Li、Xiaodong Ai、Pinyan Lu
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（v1）
- **原始论文**：https://arxiv.org/abs/2611.15309
- **代码**：未见公开代码仓库
- **标识符**：arXiv:2611.15309；DOI: 10.48550/arXiv.2611.15309

## 一句话结论

【论文原文】EvoTrias 将 govern、propose、judge 分配给独立所有者，并把 Judgment 放在私有 evaluator 后；在降低 64% token 成本和扩展到 68 万行仓库的同时，保护判断可保持 benchmark 分数对迁移的忠实性。

## 真正新增的内容

【论文原文】论文把 Agent 程序演化的三个决策权显式分离：跨轮治理、任务内开放提案、受保护判断；组件只经 typed contracts 交互，runtime hooks 强化边界。其核心主张是 evaluator 不能由负责生成或治理的 Agent 同时控制。

【分析推断】这为 Agent verifier × OPD 的 sealed eval 提供架构级而非仅数据级方案：teacher/verifier 可以参与训练和路由，但最终 judge 的规则、测试与状态必须私有、冻结且不可由策略修改。

## 核心方法

1. Structured Governance 汇总跨轮证据并决定搜索方向。
2. Open Proposal 允许 coding agent 在任务内自由构造候选。
3. Protected Judgment 由私有 evaluator 结算有效性与 fitness。
4. typed contracts 和 runtime hooks 防止权限渗透；以插件形式接入现有 coding agent。

## 关键实验结果

【论文原文】在数学、系统和算法设计 benchmark 上达到新的最佳结果；Governance/Proposal 分离降低 64% token 成本，Open Proposal 支持 680K 行工业仓库，Protected Judgment 使 benchmark score 更忠实地反映迁移表现。

## 证据质量与局限

【论文原文】58 页、26 幅图，覆盖多个程序演化域并报告组件收益。

【分析推断】摘要未给出“迁移忠实性”的全部数值、泄漏审计或对恶意策略的安全边界；私有 evaluator 只能减少共适应，无法自动修复 specification gap。代码未见公开，复现门槛较高。

## 最接近的相关工作

最接近 AutoTuneBench、MAGS、GameLogicBench、Proof-Carrying Cognition 与 Agent harness/value 分解研究。EvoTrias 的差异在于把 judge 独立权提升为系统权限边界，而不是在同一 Agent 内添加一个评分步骤。

## 如何复用或推进 LLM-as-a-Verifier

将生成式 verifier 限定为可提出证据和软分数，私有 judge 只接收 typed evidence contract 并用隐藏测试结算。verifier 的更新提案不能读取 sealed labels；若需更换 judge，必须通过桥接评测和历史任务回放。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher score 可训练 student，但发布指标由独立 protected judge 计算。
- **A/B/T 与序数分布**：软 verifier 提供分布；protected judge 只在有隐藏证据时落地硬 A/B，否则保留 T。
- **环境真值门控**：隐藏程序测试与环境断言置于 judge 权限域，生成侧不可改写。
- **critique states**：critique 只能通过 typed contract 引用证据，不能声明测试已经通过。
- **高熵探索**：Open Proposal 保留多样候选；治理层管理预算，而非让 Judge 提前塑形所有生成。
- **sealed eval**：按 govern/propose/judge 三权分离实现；记录 evaluator 版本、权限和数据访问日志，防止共适应与泄漏。
