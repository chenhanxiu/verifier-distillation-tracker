# B-OPSD: On-Policy Self-Distillation with Self-Generated Problem Briefs

- **作者**：Zhi Xu、Yinqi Wu、Feng Zhang、Xiaotong Zhang、Hong Yu、Han Liu
- **首次公开日期**：2026-11-14
- **版本日期**：2026-11-14（v1）
- **原始论文**：https://arxiv.org/abs/2611.19273
- **代码**：https://github.com/ZevineXu/B-OPSD
- **标识符**：arXiv:2611.19273；DOI: 10.48550/arXiv.2611.19273

## 一句话结论

【论文原文】B-OPSD 用 student 自生成的“原则、适用条件与陷阱”问题简报替代 ground-truth solution 作为 frozen teacher 的 privileged context，在三个模型规模上均优于标准 OPSD。

## 真正新增的内容

【论文原文】标准 OPSD 依赖真解条件化 teacher，限制了无解答数据的使用。B-OPSD 让初始模型或历史 student checkpoint 只根据题目生成 problem brief，不给最终答案或完整解，再用 brief 条件化 frozen teacher 对当前 student 的 on-policy rollout 做 token 分布匹配。

【分析推断】problem brief 是一种 student-generated critique state：它可扩大 teacher 的条件信息，却也可能把 student 的错误先验反馈进 teacher。因而 brief 应被视为待验证的软状态，而非新 ground truth。

## 核心方法

1. 用模板从题目生成相关原则、适用条件和常见陷阱的 brief。
2. 冻结 teacher，以 brief 为 privileged context 评分当前 student rollout。
3. 用 token-level distribution matching 做 on-policy 自蒸馏，全程不使用真解。

## 关键实验结果

【论文原文】在 AIME 2024、AIME 2025 和 HMMT 2025 上，使用初始模型或 saved checkpoint 生成 brief 的两个版本，在三个 Qwen3 模型规模上平均准确率均高于 OPSD。论文公开代码；摘要未给出逐设置绝对提升。

## 证据质量与局限

【论文原文】覆盖三个竞赛数学集、三个模型规模和两种 brief 来源，并与 OPSD 比较。

【分析推断】证据仍限于可自动判分数学；brief 的事实正确性、跨 checkpoint 漂移和开放式 Agent 任务表现未验证。teacher 看到错误 brief 时是否放大错误，是关键安全缺口。

## 最接近的相关工作

最接近 OPSD、SCOPE-OPSD、Data-free OPD、Self-Disagreement 与 AC-OPD。不同点是用 student 自生成的非答案 problem brief 替代真解 privileged context。

## 如何复用或推进 LLM-as-a-Verifier

把 brief 扩展为 Agent 状态摘要、约束清单和潜在失败假设，并让环境 verifier 逐条核验；只有已证实部分能决定更新方向，未证实部分只调 teacher 幅度或触发主动检查。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：在 teacher score 中显式区分 brief-supported 与 environment-supported 部分。
- **pairwise A/B/T 与序数分布**：比较不同 brief 条件下的分支；未核验假设标 T。
- **环境真值门控**：程序化结算覆盖 brief 中可执行的条件和陷阱。
- **student-generated critique states**：brief 可直接作为 critique state，但需逐条证据准入。
- **高熵探索**：保留多个 brief 假设，不让单份自生成摘要锁死 teacher 分布。
- **sealed eval**：冻结 brief 生成器版本，并用无 brief、错误 brief 和独立真值作压力测试。

