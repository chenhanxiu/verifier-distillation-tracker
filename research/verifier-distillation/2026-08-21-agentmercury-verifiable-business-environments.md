# AgentMercury：从业务场景合成可执行、可验证的 Agent 世界

- **论文标题**：AgentMercury: Your Agent Can Synthesize Verifiable Environments for Business Scenarios at scale
- **作者**：Minbyul Jeong，Chanwoong Yoon
- **首次公开日期**：2026-08-21
- **版本日期**：2026-08-21（v1）
- **arXiv ID**：2608.20634
- **原始论文**：https://arxiv.org/abs/2608.20634
- **DOI**：https://doi.org/10.48550/arXiv.2608.20634
- **代码链接**：论文页面未提供公开代码

## 一句话结论

AgentMercury 先生成持久化、带实体/服务/工具/状态和跨服务不变量的可执行世界，再从世界中产生多样任务与轨迹，为 Agent 训练提供可扩展的环境真值。

## 真正新增的内容

**论文原文结论**：它从“围绕固定任务造环境”转向“先实例化世界，再让任务自然出现”，构建 4,783 个跨行业和国家的可执行业务环境，并证明环境构造本身可通过轨迹学习。

**分析推断**：对 verifier × OPD 最重要的是环境不变量可作为 teacher 的硬信号：可从 student rollout 自动生成状态转移、约束违反和终态达成标签，减少对 LLM Judge 自评的依赖。

## 核心方法

由高层业务场景生成持久世界，明确实体、服务、工具、状态和可执行跨服务 invariants；从这些世界采样任务与交互轨迹用于 RL。另以世界构造轨迹微调环境作者模型，提高新场景的可执行世界生成率。

## 关键实验结果

**论文原文**：构建 4,783 个环境，覆盖 14 个行业与 50 个国家。Qwen3.5-4B 在 EnterpriseOps-GYM 从 12.3 提升至 15.7，在 AIME26 从 45.9 提升至 56.0。Qwen3.5-35B-A3B 经构造轨迹微调后，held-out 业务场景的可执行世界作者成功率从 3.3% 升至 83.3%。

## 证据质量与局限

规模和跨域结果较强，但目前为两位作者的首次预印本，论文页未给出公开构造代码；环境由模型合成，可能存在共享模板、隐含泄漏和 verifier 错配。AIME 提升不能单独证明 Agent 长轨迹收益，且“可执行”不等于真实业务有效。

## 最接近的相关工作

最接近 SPADE、FACET、EnvHarness、WebGrader 与 Thinkingbox。AgentMercury 的区别是以持久业务世界为生成单元，而不是只围绕单任务合成测试或修补 harness。

## 如何复用或推进 LLM-as-a-Verifier

将每个环境的不变量编译成程序化 verifier bank：前置条件、状态转移、资源守恒、权限与副作用分别打分。LLM Judge 只评价未被硬规则覆盖的语义完成度，并把环境日志作为证据输入。对合成环境本身也需要独立 verifier，防止“错误世界产生自洽奖励”。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：从环境事件日志产生稠密步骤分数，在 student 自己访问的状态上蒸馏。
- **pairwise A/B/T 与序数分布**：同一世界状态展开多个动作，按终态、不变量违反、成本形成序数偏好；等价结果保留 Tie。
- **真值门控**：环境不变量应优先于 teacher 主观评分，teacher 只补充软目标。
- **student-generated critique states**：让 student 根据日志生成失败解释，再由环境重放校验 critique 是否指向真实状态差异。
- **高熵探索**：世界可产生多任务与多解，适合在合法分支间维持探索，而非只复刻单一参考轨迹。
- **sealed eval**：冻结独立世界生成器、行业组合与不变量实现；训练环境和 sealed 世界不能共享同一模板或 evaluator。
