# Capable Teacher, Myopic Scorer: Reward-Free Teacher Repair for Agentic On-Policy Distillation

- **作者**：Shu Zhao、Tan Yu
- **首次公开日期**：2026-10-20
- **版本日期**：2026-10-20（v1）
- **原始论文**：https://arxiv.org/abs/2610.28586
- **arXiv ID**：2610.28586
- **DOI**：https://doi.org/10.48550/arXiv.2610.28586
- **代码/项目**：https://shuzhao.me/r2s/

## 一句话结论

R2S 证明 teacher 会做不等于 teacher 会逐 token 正确评分，并把完整 takeover 的未来结果蒸馏回一个冻结 scorer，修复 Agent OPD 的短视监督。

## 真正新增的内容

定义 rollout–scorer gap：teacher 从高分歧状态接管能完成任务，但它的 next-token 分数会放过安全却拖延、最终耗尽轮次的动作。

## 核心方法

挖掘 student–teacher 高分歧状态，运行多次 teacher takeover，用共识或 LLM Judge 等无奖励检查筛选成功状态；将 takeover-informed 评分蒸馏到看不到未来的 teacher scorer，再冻结用于标准 OPD。

## 关键实验结果

三个环境、两个 teacher、四个 student 共 12 个组合全部超过三种强 Agent OPD 方法；相对每格最佳基线平均提高 12.8 个成功率点。

## 证据质量与局限

完整的跨 teacher/student/environment 矩阵且效应量大；但所谓 reward-free 仍依赖共识或 LLM Judge，若检查器偏差相关，会把未来错误压回 scorer。

## 最接近的相关工作

与 ToolOPD、The Tasteful Agent、Policy-Aligned Predictive Verification、γOPD 与 Caddie 最接近。

## 如何复用或推进 LLM-as-a-Verifier

将环境可验证 takeover 结果作为优先 teacher 信号；若只能用 Judge 共识，则保留分布与 abstention，并在 sealed reference 上单独估计 scorer repair 的真实方向。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】这是当前 score-level on-policy verifier distillation 最直接的新基线：先 repair teacher scorer，再做学生 OPD；应与“硬真值定方向、soft score 定幅度”并列比较。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
