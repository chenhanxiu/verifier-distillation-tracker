# Who Verifies the Verifier? Co-Evolving Inspectable Graders with Self-Improving Agents

- **作者**：Xing Zhang；Guanghui Wang；Yanwei Cui；Ziyuan Li；Wei Qiu；Bing Zhu；Peiyang He
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.11464
- **Canonical URL**：https://arxiv.org/abs/2610.11464
- **代码**：未发现公开代码链接

## 一句话结论

这项工作直接回答“谁来验证 verifier”：让 grader 以可检查的小型缺陷检测器组合持续演化，但只允许经少量锚定真值准入；没有锚点时 grader 会坍缩成“永远通过”。

## 真正新增的内容

【论文原文】作者将 verifier 表示为一组小型、主要确定性的 drawback detector 的可检查表达式；从聚类失败中合成新 detector，经 birth gate 后，以 10 个锚定参考样本加未标注共识选择 verifier，且选择过程不看 Agent 得分。

【论文原文】移除锚点会产生 always-pass grader，即使 skill 训练表面同样顺利。  
【分析推断】这为 sealed eval 提供了极强反例：下游 Agent 分数提高不能证明 verifier 变好了。

## 核心方法

1. 从 Agent 失败轨迹聚类，提出候选缺陷检测器。
2. 将检测器写成可检查、可组合的 grader 表达式。
3. 通过 birth gate 防止未经证据支持的 detector 进入评分器。
4. 使用小规模锚定参考集与未标注样本共识选择 grader，但不使用 Agent reward。
5. verifier 与 agent skill 交替提升，形成“双棘轮”更新。

## 关键实验结果

【论文原文】在 MBPP+ 上，held-out agreement 提高 0.21；移除锚点时 grader 坍缩为 always-pass。Double Ratchet 在代码、text-to-SQL 和报告任务上保留了 ground-truth/rubric 方案 88%–110% 的提升；外部 judge 发现一次 gaming 后，通过新增 detector 修复。

## 证据质量与局限

【论文原文】跨三类任务，并包含关键锚点消融与真实 gaming 案例，证据与本研究方向高度吻合。  
【局限】10 个锚点很小，共识未标注数据仍可能共享系统偏差；“可检查”不等于语义完整。外部 judge 自身的独立性与稳定性仍需审计。

## 最接近的相关工作

与 CoVer、Proof-Carrying Cognition、ImpossibleRubrics、AutoTuneBench、MAWILE、MAGS 和 ContrAgent 最接近。相比纯 LLM Judge，它强调 verifier 的模块化可检查性与独立真值锚定。

## 如何复用或推进 LLM-as-a-Verifier

把 generative verifier 的 critique 编译为原子 detector：每个 detector 必须说明触发证据、预期不变量、反例和适用范围。新增 detector 只在 sealed anchor 上提高判别力且不过度拒绝时准入；旧 detector 保留版本号以支持回滚。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：总分由 detector 分布聚合；蒸馏时保留各 detector 的概率和证据，不只拟合总分。
- **A/B/T 与序数分布**：detector 证据充分为 A/B，证据缺失或冲突为 T；用序数严重度表示缺陷影响。
- **程序化/环境真值门控**：确定性测试、SQL 执行、文件 diff 等 detector 优先于语言 judge；语言 detector 不能推翻硬真值。
- **student-generated critique states**：critique 只有被编译为可重放 detector 并通过 birth gate 后才入库。
- **高熵分叉**：grader 共识高但锚点不足时继续探索/抽样，不把一致性误当真值。
- **sealed eval**：冻结一套不参与 verifier 演化的锚点、外部检测器和 harness，专门检测 always-pass 与 reward gaming。

总体判断：【分析推断】这是本轮对 verifier × Agent 路线影响最大的工作：它要求把 verifier 演化与 Agent reward 解耦，并把“独立锚点”设为不可取消的安全边界。