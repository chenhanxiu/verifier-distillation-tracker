# PivotOPD: Learning to Recover from Pivotal Mistakes in Multi-Turn Agents

- **作者**：Yinghui He, Yapei Chang, Khushi Bhardwaj, Daniele Molinari, Tugrul Konuk, Jan Kautz, Ali Hatamizadeh
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2609.40285
- **项目页**：https://research.nvidia.com/labs/lpr/pivotopd/

## 一句话结论

PivotOPD 同时蒸馏“避免关键错误”和“进入错误状态后的恢复动作”，在三个 Agent 环境及 SWE-Bench Verified 上优于 13 个基线。

## 真正新增的内容

【论文原文】多轮失败中超过一半含有较早出现、使任务距离变远的 pivotal mistake；许多错误仍可通过后续少量 teacher 引导恢复。本文把预防与恢复拆成两个蒸馏目标。

【分析推断】它补足了只学习最佳动作的 OPD：对长轨迹而言，错误后状态并非应删除的 OOD 尾部，而是应专门训练的恢复分布。

## 核心方法

在 pivotal mistake 处由 teacher 提供 gold action，并为后续数步标注 recovery action；预防分支使用 reverse KL，恢复分支用 forward KL 覆盖 student 很少采样的行为。

## 关键实验结果

【论文原文】ALFWorld、WebShop、Search QA 上，Qwen3-1.7B/8B 均取得最强平均结果；1.7B 在 ALFWorld 比最强基线高 5.5%。迁移到 Nemotron-3.5 的 SWE-Bench Verified，resolve rate 提高 3.2%。

## 证据质量与局限

跨模型、环境和软件工程域，且比较 13 个基线；但 pivotal mistake 与 recovery action 仍依赖 teacher 判定，摘要未说明人工一致性、环境重放覆盖率或安全恢复约束。

## 最接近的相关工作

STRIDE、REVERSAL-BENCH、SkillAA、GC-OPD、LLM-as-an-Improver。

## 如何复用或推进 LLM-as-a-Verifier

训练 verifier 输出“关键错误概率、可恢复性分布、建议恢复动作”，并用环境 checkpoint 重放验证恢复是否真正改善终局。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：对关键错误和恢复窗口分别赋权，不把失败后缀统一置零。
- **A/B/T 与序数分布**：原动作、gold action、多个 recovery action构成 A/B/T；相同可恢复性保留 T。
- **硬真值门控**：错误定位与恢复收益应由 checkpoint 重放及环境结果定方向。
- **student-generated critique states**：允许 student 生成恢复 critique，但须重放成功后才入库。
- **高熵分叉**：在 pivotal turn 分配分叉预算，并保留多条成功恢复路线。
- **sealed eval**：冻结未见任务、错误类型和环境版本，避免 recovery teacher 共适应。
