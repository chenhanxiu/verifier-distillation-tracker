# How to Speculate about Uncertainty in Agentic Coding? A Draft-Model Gate Method

- **作者**：Konstantin Grotov、Valentin Malykh
- **首次公开日期**：2026-09-04
- **当前版本日期**：2026-09-04（v1）
- **原始论文**：[arXiv:2609.05274](https://arxiv.org/abs/2609.05274)
- **DOI**：[10.48550/arXiv.2609.05274](https://doi.org/10.48550/arXiv.2609.05274)
- **发表信息**：EMNLP 2026 Industry Track
- **代码**：截至本次记录未发现作者公开代码

## 一句话结论

Speculative Uncertainty 用小型 draft model 单次复评黑盒 Agent 已生成的轨迹，在执行前给出失败风险；它降低执行错误和 token 成本，但硬 veto 会牺牲部分任务成功率。

## 真正新增的内容

**论文原文结论**：反向借用 speculative decoding，让开放权重 draft model 对黑盒 Agent 的输出 token 打分；分开聚合 reasoning/action 阶段特征，并用可验证执行结果训练线性校准器。

**分析推断**：这是长时程 Agent 的低成本 distributional verifier 雏形。最适合做路由和不确定性门控，而不是取代环境真值或作为不可申诉的二元 Judge。

## 核心方法

- 不访问目标 Agent 的 logits、权重或激活，也不重复采样；
- 小 draft model 对现有轨迹做一次 teacher-forced forward pass，提取跨模型似然/熵特征；
- reasoning 与 action span 分开建模；
- 用外部二元执行 oracle 校准下一动作成功概率；
- 阈值 gate 决定执行或触发较便宜的 replan。

## 关键实验结果

**论文报告**：

- Qwen3-Coder-480B + Qwen3-4B draft：SWE-Bench Verified 执行错误率 21%→15%，DA-Code 14%→6%；每题 token 成本分别下降 14% 和 19%。
- 代价是任务成功率 SWE-Bench 49%→44%，DA-Code 64%→63%；true-veto recall 为 0.72/0.69，false-veto rate 为 0.14/0.16。
- 蒸馏使 Brier score 从 0.1265 降至 0.1012，Brier skill score 从 0.019 升至 0.215。
- DA-Code 为不再微调的 OOD 转移；方法也在 Claude 3.5 Sonnet 上验证跨 Agent 可用性。

## 证据质量与局限

**证据质量：中高。** 有在线干预结果、成本—错误—成功率三方权衡和 OOD/跨模型实验；EMNLP Industry 接收。

**论文局限**：定量证据只覆盖代码执行这一目标；组件组合未系统寻优；原始分数仍有校准缺口，作者明确只称 failure-likelihood score。

**关键提醒（分析）**：降低“每次执行错误”不等于提高任务完成率。若将其直接用于 OPD，可能蒸馏出过度保守策略。

## 最接近的相关工作

最接近小模型 speculative verifier、uncertainty routing、FailBench，以及 SAGE 的高熵 teacher 调用。不同点是它从黑盒 Agent 的完整输出反推风险，并在环境调用前干预。

## 如何复用或推进 LLM-as-a-Verifier

- student verifier 输出失败概率或序数风险分布；用执行 oracle 校准，保留 ECE/Brier 而非只报 AUROC。
- 将 A/B/T 定义为执行/重规划/不确定升级，而非简单好坏。
- 对 student-generated critique state 计算“加入 critique 前后”的风险差，只有被真实执行验证的下降才进入蒸馏。
- 高熵状态可路由到额外 teacher、沙箱测试或多分支 rollout；不可直接永久 veto。

## 对 Agent verifier × OPD 实验路线的具体影响

1. 新增 cheap verifier 基线：4B draft 特征 → ordinal risk head → score-level on-policy distillation。
2. teacher 方向由测试/执行真值决定，draft uncertainty 只控制权重与查询预算。
3. 评估同时报告 error rate、task success、false veto、token cost、Brier/ECE 和分支覆盖率。
4. sealed eval 使用新仓库、新 Agent 模型和未见故障类型，避免 calibrator 与训练轨迹共同适应。
5. 高熵分叉保留一个“允许执行的审计臂”，测量被 gate 错杀的潜在成功路径。