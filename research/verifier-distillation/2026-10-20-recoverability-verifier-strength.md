# Recoverability and Verifier Strength: Two Measured Preconditions for Unattended Agent Self-Improvement

- **作者**：De Wang、Peng Qi
- **首次公开日期**：2026-10-20
- **版本日期**：2026-10-20（v1）
- **原始论文**：https://arxiv.org/abs/2610.27465
- **arXiv ID**：2610.27465
- **DOI**：https://doi.org/10.48550/arXiv.2610.27465
- **代码/项目**：未公开

## 一句话结论

无人值守 Agent 自改进必须同时满足 verifier strength 可测且变更可真实回滚；只看自动 Judge 通过或生成一个 undo 都不够。

## 真正新增的内容

给出 verifier strength σ 与 recoverability 两个可操作量，并把 prompt/tool/skill 改动与权重更新分成不同自动化权限。

## 核心方法

用 trusted reference verifier 测量自动 verifier 一致性；分别测试恢复保存快照与重新生成 undo 的行为恢复程度，再据两项门槛决定是否允许自动发布。

## 关键实验结果

LLM Judge 在 37 个设置中有 9 个对所有输入给相同分且不报错；保存副本可恢复原行为，生成式 undo 不行；变更部署期间有 17% 任务结果超出正常运行波动，事后回滚无法消除。

## 证据质量与局限

τ²-bench 与真实发布门控案例直接命中工程风险，但篇幅短、平台范围有限；σ 仍依赖可信 reference，不能被理解为普适安全证明。

## 最接近的相关工作

最接近 SkillAA、RoboRSI、AutoTuneBench、MC-EvoBench 与 sealed release gate。

## 如何复用或推进 LLM-as-a-Verifier

将 student-generated critique/memory/skill 的发布门槛设为“独立 verifier σ 达标 + 保存旧版本 + 可重放回滚”；权重更新默认人工批准。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】现有实验应新增 constant-output 与 input-swap 两类 verifier 健康检查，并把 rollback fidelity、影响窗口和 pass@3/pass³ 波动纳入 sealed eval。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
