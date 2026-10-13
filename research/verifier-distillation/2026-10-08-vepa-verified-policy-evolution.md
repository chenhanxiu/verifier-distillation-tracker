# VEPA: Verified Evolving Formal Policy for Lifelong LLM Agent Guardrails

- **作者**：Duy Nguyen；Lesly Miculicich；Bhavana Dalvi Mishra；Shuo Li；Krishnamurthy Dj Dvijotham；Mohit Bansal；Tomas Pfister；Long T. Le
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12813
- **Canonical URL**：https://arxiv.org/abs/2610.12813
- **DOI**：10.48550/arXiv.2610.12813
- **代码**：未发现公开代码链接

## 一句话结论

VEPA 让 LLM 只负责提出形式化 guardrail 补丁，再由确定性 verifier 检查结构与冲突，并由证据权限层决定是否启用，实现“生成式 teacher 提议、程序 verifier 裁决、证据门控发布”。

## 真正新增的内容

【论文原文】把持续适应与确定性执行结合：部署反馈驱动 LLM 修补 typed event 上的可执行符号规则，但不确定更新不能直接进入运行时决策。  
【分析推断】这可直接迁移到 Agent verifier/rubric 的版本治理：模型可生成新规则，只有通过静态验证、回归集和证据阈值后才进入在线评分。

## 核心方法

1. 用 typed agent events 表示形式策略。
2. 从部署失败中由 LLM 提出最小规则补丁。
3. 确定性 verifier 检查结构合法性与规则冲突。
4. evidence-aware authority layer 判断补丁是否有足够证据启用。
5. 保留旧正确行为，持续扩展 deterministic enforcement 的覆盖范围。

## 关键实验结果

【论文原文】在 ASSEBench-Safety、ASSEBench-Security 和 ATBench 上均优于所比较 baseline；在混合流、腐败反馈和更长 horizon 下仍保持收益。摘要未给出统一数值，应以全文分任务表格解读。

## 证据质量与局限

覆盖安全、安防与长时程部署扰动，方法结构清晰。局限是形式规则只保证对编码规范的确定性，不保证规范本身完备；LLM 生成补丁可能造成 coverage gap，证据权限层的阈值也需外部校准。

## 最接近的相关工作

与 ContrAgent、MAGS、GCAC、SpecGuard、Ground-truth-as-code 和 SkillAA 最接近。VEPA 的新增点是把 formal policy 从静态资产变成经验证的持续演化对象。

## 如何复用或推进 LLM-as-a-Verifier

把五维 rubric 中的硬门槛转为可执行规则层，LLM Judge 仅处理规则未覆盖的语义部分；所有新 rubric/规则经冲突检查、历史 back case 和独立 sealed set 验收后才发布。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：形式规则决定禁止/允许及梯度符号，软 verifier 只调整幅度。
- **A/B/T 与序数分布**：形式规则覆盖时给确定 verdict；未覆盖或证据不足时输出 T。
- **程序化/环境真值门控**：确定性 verifier 成为不可绕过的发布门。
- **student-generated critique states**：critique 可提出规则补丁，但不能自行启用。
- **高熵分叉**：未知规则区域保留探索，同时隔离高风险不可逆动作。
- **sealed eval**：冻结旧规则回归集、隐藏冲突集和环境事件流，防止 patch 与在线 evaluator 共适应。