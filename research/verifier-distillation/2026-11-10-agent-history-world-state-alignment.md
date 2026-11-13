# Cleaning an Agent's History Hurts When the World Still Holds the Error

- **作者**：Egor Pakhomov、Anurag Koul、Hongjun Liu、Bo Pang、Shafiq Joty、Erik Nijkamp
- **首次公开日期**：2026-11-10
- **版本日期**：2026-11-10（v1）
- **原始论文**：https://arxiv.org/abs/2611.14654
- **代码与数据**：随 arXiv ancillary files 发布，入口见 https://arxiv.org/abs/2611.14654
- **标识符**：arXiv:2611.14654；DOI: 10.48550/arXiv.2611.14654

## 一句话结论

【论文原文】历史中的“正确内容”只有与真实世界状态一致才有帮助；把未执行的修复写成已完成会显著降低 Agent 恢复率，甚至比不编辑历史更差。

## 真正新增的内容

【论文原文】作者冻结 Agent 的精确中间世界状态，分别干预历史表述和环境效果，首次把“历史说了什么”与“世界实际发生了什么”正交分离。相同正确值作为真实旁注可提升恢复，而伪装成已完成动作会伤害恢复；AppWorld 中成功回执的作用随数据库效果是否真实存在而反转。

【分析推断】这直接否定了“只要 critique 文本正确即可作为 teacher state”的假设：student-generated critique、memory 或压缩摘要必须经过环境状态门控，否则 verifier 蒸馏会学习到语义正确但执行虚假的状态。

## 核心方法

1. 在错误发生后冻结完整轨迹与世界状态。
2. 保持世界不变，仅改变历史：真实旁注、已完成动作、匹配中性文本等。
3. 在 AppWorld 中交叉操纵成功/失败回执与数据库效果是否存在。
4. 让多个 receiver model 从该状态继续，并测恢复率或整任务成功率。

## 关键实验结果

【论文原文】AgentCE-Bench 中，真实旁注将恢复率从 51% 提至 66%，而“已完成正确动作”将其从 50% 降至 44%。AppWorld 中，成功回执在效果缺失时把成功率从 45% 降至 28%，效果存在时则从 38% 提至 49%；两种效果合计相差 27 个百分点。

## 证据质量与局限

【论文原文】采用精确状态冻结、成对干预、多个 receiver，并公开代码、数据和预先固定的分析材料。

【分析推断】任务仍集中在结构化错误与数据库写入；未证明所有开放式长轨迹 critique 都能被环境重放。部分指标依赖特定 benchmark 的恢复定义，推广到网页、代码仓库或现实工具时需重新定义可验证效果。

## 最接近的相关工作

最接近 Grounding Agent Memory、DENSE、PaperDoctor、SkillAA、RSIAgent 与 Folio。本文的区别是用因果干预量化 history/world 不一致本身，而不是只提出带来源记忆或恢复机制。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 输入拆成“声明的动作状态”和“环境可观察状态”，对二者的一致性单独建模。critique 生成后先执行只读探针或重放；若声明无法验证，输出 T/INCONCLUSIVE，而不是依据流畅度赋高分。可把 receipt/effect 的四格组合蒸馏为 ordinal state-consistency 分布。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher score 增加 history–world consistency 通道；不一致时禁止正向蒸馏。
- **A/B/T**：A=表述与效果一致，B=明确冲突，T=效果不可观察；避免把 T 当 B。
- **环境真值门控**：写操作必须由状态差分、事务日志或可执行断言确认。
- **critique states**：保留原错误与修复状态，禁止把“建议修复”重写为“已修复”。
- **高熵探索**：当环境证据不充分时保留多种恢复分支，不让伪成功摘要锁死策略。
- **sealed eval**：隐藏真实环境状态和回执操纵，测试 verifier 是否依赖证据而非文本表面。
