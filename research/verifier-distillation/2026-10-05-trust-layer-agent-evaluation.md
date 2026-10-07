# A Trust Layer for Agent Evaluation

- 作者：Mohammadreza Sediqin、Shivali Dalmia、Srinivasa Karthikeya Reddy Kovvuri、Abhishek Mukherji
- 首次公开日期：2026-10-05
- 版本日期：2026-10-05（v1）
- 原始论文：https://arxiv.org/abs/2610.07274
- Canonical URL：https://arxiv.org/abs/2610.07274
- 代码：论文称录用后发布，当前无公开链接

## 一句话结论

【论文原文】基准得分不等于可信完成：在 Agents' Last Exam 的 84 个记录为通过的运行中，只有 22.6% 同时通过评分逻辑、可追溯计算、完成声明一致性和重复稳定性四项检查。

## 真正新增的内容

【论文原文】提出不改原分数的 post-hoc Trust Layer，在每个得分旁报告“是否值得相信”；前三项只读保存产物，第四项重跑 Agent，LLM 只做证据标签，最终 verdict 由确定性规则得出。

## 核心方法

【论文原文】四个维度分别验证 benchmark grading 支持、通过是否由可追溯计算挣得、完成声明是否符合实际、重复执行是否稳定；模型判断采用多数票，不能直接修改分数。

## 关键实验结果

【论文原文】五种 Agent 配置、108 个任务中，各模型均存在无可追溯计算却通过、虚假完成声明和不稳定结果；18%–46% 的任务在五次运行中不能保持同一分数带。84 个通过记录仅 22.6% 四项全过，95% CI 15.0%–32.6%。

## 证据质量与局限

【论文原文】把静态工件审计与重复运行结合，并给出置信区间。【分析推断】只在一个 benchmark、108 题上验证；多数票证据标签仍可能相关失误，且重复运行成本高。框架验证“此次结果”，不等于一般能力。

## 最接近的相关工作

【分析推断】接近 AutoTuneBench、Harness or Model?、Ground-truth-as-code 与 Transect；新增的是并列于原分数的四维可信性判决。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 verifier 训练标签拆成 outcome 与 trust 两套：student 可以预测分数，但只有通过 traceability、claim consistency 和 stability 的样本进入高权重蒸馏；模型 judge 只能标注证据，最终准入用规则。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：以 trust vector 调权，避免把偶然高分当 teacher。
- 【分析推断】A/B/T：未通过可信性检查的比较转 T。
- 【分析推断】真值门控：硬评分、工件证据、完成声明分账保存。
- 【分析推断】critique states：只有与工件一致且可追溯的 critique 进入状态。
- 【分析推断】高熵分叉：对不稳定任务保留重复 rollout，而非过早收敛。
- 【分析推断】sealed eval：评测端独立重跑并冻结判决规则，训练端不可访问 trust 标签生成细节。