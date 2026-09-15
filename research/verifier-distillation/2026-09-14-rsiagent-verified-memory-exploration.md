# RSIAgent: Autonomous Exploration for Recursive Self-improvement in New Environments

## 基本信息

- **作者**：Sibo Zhu；Shicheng Fan；Xinyue Wang；Wenyi Wu；Kun Zhou；Biwei Huang
- **首次公开日期**：2026-09-14
- **版本日期**：2026-09-14（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.15364
- **代码**：未发现公开代码链接

## 一句话结论

【论文原文】RSIAgent 在无训练更新下让 curriculum、actor 与 verifier 协作探索新环境，验证执行结果并沉淀“行动—条件—后果”因果记忆，再冻结记忆用于后续任务。

## 真正新增的内容

【论文原文】系统采用先广后深的自主探索：课程模块提出覆盖环境机制的任务，actor 执行，verifier 检查结果，只有通过验证的经验才写入因果记忆；探索完成后冻结记忆，减少测试期持续改写。

【分析推断】它把 verifier 从“终局评分器”提升为长期经验准入器，直接关联 student-generated critique/memory state，但尚不是参数级 verifier distillation。

## 核心方法

1. curriculum agent 生成针对新环境机制的探索任务。
2. actor 执行动作并观察环境反馈。
3. verifier 验证结果与因果关系。
4. 将通过验证的 action–condition–consequence 经验写入记忆。
5. 从广覆盖转向关键机制深挖，随后冻结记忆并在下游任务复用。

## 关键实验结果

【论文原文】在 OSWorld-v2 与 Agent’s Last Exam 上评估；摘要报告基于 Kimi-K3 和 GLM-5.3 的系统超过若干前沿闭源模型，包括 GPT-6。

【证据边界】这是摘要层面的总体结果，未提供这里可核验的完整分项、方差和成本。跨模型比较还可能受到 harness、工具延迟、提示预算与环境版本影响，不能单凭总分归因于 verifier 记忆机制。

## 证据质量与局限

- **质量**：覆盖真实交互式基准，并明确设置探索、验证、记忆冻结三个阶段。
- **局限**：curriculum、actor 和 verifier 可能共享模型族或提示偏差；验证过的经验不一定具有可迁移因果性。
- **风险**：若 verifier 把偶然成功写成规则，记忆会在后续长轨迹中累积放大错误；摘要未证明存在完全独立的 sealed evaluator。

## 最接近的相关工作

Grounding Agent Memory 的环境探测准入、APEx 的程序化经验蒸馏、LongWoF-Bench 的验证经验、MemGuard 的置信元数据、S3Gym 的自评与严格评测分离。RSIAgent 的差异是自主 curriculum 驱动的新环境探索与因果记忆冻结。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 verifier 的通过/拒绝升级为序数后验：已证实、部分证据、仅相关、被反例推翻、环境依赖。每条记忆绑定可重放证据、作用域和过期条件；轻量 student verifier 可从这些分布标签和生成式 critique 中蒸馏。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- score-level OPD 可在记忆写入前执行：硬环境结果决定更新符号，verifier 置信分布决定幅度。
- 同一初始状态下不同探索动作形成 A/B/T；多个成功机制保留为 Tie/非支配分支。
- 程序化状态、事务日志和只读 probe 应优先于语言自证。
- student-generated critique 必须附带可重放环境证据与适用作用域，失败反例触发降权或删除。
- broad-first 阶段保持高熵，只有反复验证后才收缩探索；冻结记忆可降低在线共适应。
- sealed eval 使用未参与探索的任务、独立 harness 和冻结 evaluator，并分开报告“记忆内任务”与“机制外推任务”。