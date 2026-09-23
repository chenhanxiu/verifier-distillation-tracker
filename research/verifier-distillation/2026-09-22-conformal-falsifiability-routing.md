# Calibration Is Not Verification: Falsifiability-Aware Conformal Routing for Mixture-of-Agents

- **作者**：Nada Rahali, Zijia Wang, Zhisong Liu
- **首次公开日期**：2026-09-22
- **版本日期**：2026-09-22（v1）
- **原始论文**：https://arxiv.org/abs/2609.25959
- **Canonical URL**：https://arxiv.org/abs/2609.25959
- **DOI**：10.48550/arXiv.2609.25959（arXiv DataCite，待注册）
- **代码**：未见独立公开仓库
- **arXiv ID**：2609.25959

## 一句话结论

【论文原文】多 Agent 一致性可经 conformal calibration 变成有覆盖控制的 claim-level filter，但 counterfactual verifier 只有在具备领域知识时才增加信息；把近随机的辅助信号无条件融合反而会降低可靠性。

## 真正新增的内容

【论文原文】C-MoA 将每个原子 claim 在异构 Agent 间的语义支持转为 nonconformity score，并在 held-out 样本上校准保留阈值。CONTRA-MoA 再加入 provenance-blind near-miss tournament、leave-one-agent-out stability 与 availability-aware fusion，实证区分“校准的一致”与“真正能反驳错误”的 verifier。

【分析推断】这直接对应 distributional verifier 的 teacher 选择：ensemble disagreement 只能表征群体证据，不能自动等同真值；辅助 verifier 必须先证明在目标 slice 上有独立判别力。

## 核心方法

- 将长文本分解为 atomic claims，计算 proposer 之间的语义支持。
- 用 split conformal 在 example-level heldout 集上确定阈值，控制域内 retained-claim 风险。
- 构造与原 claim 仅差一个关键槽位的 near miss，盲化来源后让 verifier 做对抗比较。
- 计算 leave-one-agent-out 稳定性，并审计不同 fusion 规则是否让噪声信号覆盖可靠的一致性信号。
- 将 verifier competence 作为路由条件：只有目标域知识足够时才启用 counterfactual 通道。

## 关键实验结果

- 长文本生成中 retained-claim precision 从 0.41 提升到 0.75。
- 医疗集上，具备领域知识的 Judge 对真假 claim 的 AUC 达 1.00；在 α=0.1 时 CONTRA-MoA 去掉 20 个错误中的 10 个，precision 0.940、retention 0.894。
- FactScore 长尾实体上 counterfactual margin AUC 0.531、stability 0.511，均接近随机；max fusion 将可靠的一致性 AUC 从 0.687 降到 0.652。
- 去掉 multi-agent signal 或 atomic decomposition，precision 分别下降 0.38 和 0.35。
- 从 FactScore 校准后不重校准迁移到医疗集，在 α=0.30 仍达 precision 0.93、retention 78%，但更宽松阈值也出现“只删真 claim”的反转。

## 证据质量与局限

【论文原文】论文包含 held-out conformal 校准、人类标注医疗集、信号分解、bootstrap 和对 tournament leakage 的显式修复，且保留了 counterfactual 分支的负结果。局限是保证仅在 exchangeable/域内条件成立；短答案的一致性信号接近随机；领域知识不足时 falsifiability 无效；医疗结果规模有限，阈值在某些 α 下会反转。

【分析推断】“有覆盖保证”不能被解释成语义真值保证，它只约束所定义 nonconformity 与校准分布。线上 Agent 策略改变后仍需重新审计。

## 最接近的相关工作

最接近 Robust Conformal Consensus、Agreement Overstates Evidence/多 Judge 有效规模、Who Judges Matters，以及 J-Zero 的可控排序偏好对。与简单 majority vote 不同，本文提供 claim-level calibration，并证明多信号融合可能比单信号更差。

## 如何复用或推进 LLM-as-a-Verifier

- 将多 Judge 输出保留为分布而非平均分，显式估计有效独立信息量。
- A/B/T 标签可由 conformal interval 生成：区间重叠或辅助信号无判别力时标 T。
- 对每个 verifier channel 维护 slice-level AUC/校准表；只有通过 competence gate 的信号才参与 teacher score。
- 用环境/程序 oracle 构造 near miss，避免依赖 Judge 自己生成并自己验证的反事实。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】score-level OPD 不应无条件融合 reward model、Judge confidence、agent agreement 和 critique consistency。建议先在独立 oracle 标注 slice 上验证每通道的增量信息，再采用 competence-gated mixture；未知域与高熵分叉保留 T/探索。sealed eval 应冻结 conformal calibration 集与融合规则，并用不同模型族及程序真值审计阈值迁移，防止 evaluator 面板共同复制同一偏差。