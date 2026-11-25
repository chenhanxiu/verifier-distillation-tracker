# Can LLM Judges Catch Unsafe Clinical Actions?：以故障注入审计长轨迹 Judge

- **论文标题**：Can LLM Judges Catch Unsafe Clinical Actions? A Fault-Injection Study
- **作者**：Neda Ghafouri
- **首次公开日期**：2026-11-24
- **版本日期**：2026-11-24（v1）
- **原始论文**：https://arxiv.org/abs/2611.33012
- **DOI**：https://doi.org/10.48550/arXiv.2611.33012
- **代码链接**：未见公开代码

## 一句话结论

仅看最终答案的 LLM Judge 会漏掉“结果看似正确、过程却不安全”的长轨迹故障；真实环境响应与规则检查器结合，才显著提高可检测性。

## 真正新增的内容

**论文原文结论**：作者构造 416 条故障轨迹、覆盖 8 类错误，比较 6 个开放 Judge，系统测量完整轨迹、推理文本、真实 EHR 响应和最终答案对安全检测的影响。**分析推断**：这是 Agent verifier 的强 sealed-audit 模板：通过可控故障注入测灵敏度，而不是只在自然数据上报告 Judge 与人类的一致率。

## 核心方法

在临床 Agent 轨迹中注入跳过检查、错误数值等安全故障，并控制终点是否保持；向 Judge 分别提供最终答案、推理、完整工具轨迹和真实 EHR 返回，比较检测率。另将 LLM Judge 与 EHR-informed rule checker 组合，测试语言评价与程序规则的互补性。

## 关键实验结果

**论文报告**：完整轨迹上的区分率为 0.75；加入真实 EHR 响应提高 0.39。推理文本整体无增益，并使错误临床数值的检测下降 0.18。final-answer-only 会把 56% 的正确轨迹误报，且无法识别终点保持型故障；原 grader 接受全部 38 条跳过化验轨迹，而 LLM 加 EHR 规则检查器检测到 97%。

## 证据质量与局限

故障类别、输入可见性和 Judge 模型均有控制，能直接测因果贡献；但领域仅为临床任务，自动注入故障与真实分布仍有差距。6 个开放模型的结论不能外推到所有闭源 Judge；高检测率也不等于低误报或正确严重度排序。

## 最接近的相关工作

与 GameLogicBench 的逐 Tick oracle、Ground-truth-as-code、ContrAgent 的时序契约、MAWILE 的受控扰动审计及 Monitoring Reward Hacking 互补。它尤其补足了“终点正确不代表过程安全”的证据。

## 如何复用或推进 LLM-as-a-Verifier

将 Agent 轨迹按故障类型标注为序数风险分布，而非单一 pass/fail；真实工具返回与程序规则作为不可覆盖的硬门控，LLM 负责解释、归因和未知故障发现。A/B/T 比较时，若环境证据缺失应输出 T/INCONCLUSIVE，而非依据推理文本自信裁决。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：建立故障注入 sealed eval：在不改变最终答案的情况下插入跳步、陈旧状态、权限越界和错误数值，单独测 verifier 灵敏度与误报率。score-level OPD 只在规则或环境证据确认后强化；student-generated critique 若与工具返回冲突应被拒收。高熵分叉应保留“终点相同但风险不同”的路径，避免 outcome reward 抹平过程安全差异。
