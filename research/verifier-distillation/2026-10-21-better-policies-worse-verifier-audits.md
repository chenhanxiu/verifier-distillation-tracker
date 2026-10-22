# Better Policies, Worse Verifier Audits

- **作者**：Daniel Cieślak、Jacek Łubiński
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.29029
- **arXiv ID**：2610.29029
- **DOI**：https://doi.org/10.48550/arXiv.2610.29029
- **代码/项目**：未发现公开链接

## 一句话结论

策略变强会改变 on-policy 失败混合，从而让 verifier 审计偏好更差的 component verifier；审计数据分布本身会随训练共适应并坍缩。

## 真正新增的内容

形式化 on-policy audit collapse：对合取目标，component verifier 的 on-policy AUC 是自身失败与交叉失败判别能力的混合；策略掌握一个子目标后，相关失败样本消失，审计权重转移。

## 核心方法

论文推导 identified set、完全擦除阈值和审计反转条件，并用精确 oracle、文本多标签控制及预注册 ECG 实验验证；修复方式是在 verifier 自身失败分布上审计，并保留这些失败的支持集。

## 关键实验结果

理论与控制实验均出现审计坍缩；预注册 ECG 研究中，按 on-policy 审计刷新 verifier 会降低 off-policy component AUC、把损害迁移到未见生成器，并增加下游约束违反；保持 own-failure support 可阻止损害。

## 证据质量与局限

理论条件清晰并含预注册实证，证据质量高；但公开摘要未给出 ECG 效应量，且合取目标假设未必覆盖开放式多维 Judge。

## 最接近的相关工作

最接近 GLARE、Dynalize、Recoverability and Verifier Strength、Reward Score 残差化审计与 When Can You Trust an Agent's Own Verifier?。

## 如何复用或推进 LLM-as-a-Verifier

维护一个按 verifier 组件与失败类型分层的 replay bank；每次刷新均在固定 off-policy failure support 上重测，而不是只评当前 student rollout。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】score-level on-policy verifier distillation 必须把“策略采样分布”和“verifier 审计分布”解耦：训练可 on-policy，验收必须混入冻结失败库。A/B/T 中的 T 也应保留历史难例，不因当前策略不再访问而被清除；否则 sealed eval 仍会被分布漂移间接污染。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
