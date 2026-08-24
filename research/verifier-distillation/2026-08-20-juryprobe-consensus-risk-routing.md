# JuryProbe：面向参考无关 Judge Panel 的共识风险诊断与有依据验证路由

- **论文标题**：JuryProbe: An Empirical Consensus-Risk Diagnostic for Routing Reference-Free Factuality Judge Panels to Grounded Verification
- **作者**：Tianxin Zhou，Ruixi Lin
- **首次公开日期**：2026-08-20
- **版本日期**：2026-08-20（v1）
- **arXiv ID**：2608.20607
- **原始论文**：https://arxiv.org/abs/2608.20607
- **DOI**：https://doi.org/10.48550/arXiv.2608.20607
- **代码链接**：论文页面未提供公开代码

## 一句话结论

多个 Judge 一致并不等于独立证据；JuryProbe 用“仅假阴性相关性”和“错误共识增益”识别共享盲点，再把高风险的接受判定路由到带可信参考的复核。

## 真正新增的内容

**论文原文结论**：作者把 Judge panel 的风险从普通一致率细化为错误条件下的依赖性，提出 FN-only correlation、false-consensus lift 和预先固定的触发规则。与单纯增加 Judge 数量不同，该方法只在校准探针显示共识高风险时获取参考证据。

**分析推断**：这为 Agent verifier 的 A/B/T 聚合增加了一个必要检查：多个 verifier 给出 A 或 Tie 前，应先估计它们是否因共享提示、训练数据或模型家族而相关犯错；否则“多数票”会伪装成置信度。

## 核心方法

在带标签的校准探针上统计 Judge 的假阴性共现，并估计一致接受相对独立假设的增益；风险超过固定阈值时，将 reference-free majority accept 送入 trusted-reference 模式。低风险时停止升级，以节省参考获取成本。

## 关键实验结果

**论文原文**：在 FEVER 扰动数据上，两个设置的 FN-only correlation 为 0.402 和 0.368，false-consensus lift 为 3.13× 和 18.13×。加入可信参考后，最小对与非最小对上的一致错误接受都降为 0。固定规则在多类数据的 10 个切分中触发 8–10 次，而在负对照中 10 次均不触发；负对照可少获取 28% 的参考，错误接受仅增加 0.004。

## 证据质量与局限

证据为 22 页预印本，包含多类切分、负对照和明确失败边界，质量中等偏上。作者明确说明它没有形式化风险保证，也未证明在自然 Judge panel 上可以可靠“无需升级”；弱 BM25 参考虽降低错误接受，却显著损失覆盖率，且阈值会随分布变化而陈旧。

## 最接近的相关工作

最接近的是多 Judge 路由与停止、reference-grounded factuality evaluation，以及仓库中的 Stopping and Routing LLM Judge Panels、Competence, Not Accuracy 和 Rubric Dropout。区别在于 JuryProbe 关注的是错误条件相关性，而非平均准确率或调用成本。

## 如何复用或推进 LLM-as-a-Verifier

可把现有 Judge bank 的输出按错误类型分层，单独估计 false-pass、false-fail 与 Tie 的相关矩阵；只有当 panel 在 sealed probe 上表现出低依赖时，才把共识当作高置信信号。对于事实、工具参数和环境终态，应优先把高风险接受路由到程序化或检索真值，而不是再加一个同源 Judge。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：蒸馏的 teacher score 应乘以“独立证据可信度”，不能直接使用 panel 平均分。
- **pairwise A/B/T 与序数分布**：保留完整投票分布，并额外记录错误相关性；Tie 不应被简单多数票压平。
- **真值门控**：在 false-consensus 高风险区域启动环境终态、参数校验或可信参考门控。
- **student-generated critique states**：多个 critique 若来自同一模型家族，需视为相关样本而非独立证据。
- **高熵探索**：对高分歧分叉允许继续探索；对“低分歧但高相关”的虚假共识仍需复核。
- **sealed eval**：阈值必须在独立冻结探针上估计，并周期性以新 sealed slice 检查漂移，不能用训练回路内数据自证安全。
