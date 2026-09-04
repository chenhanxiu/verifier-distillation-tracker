# Clean Engineering, Unstable Measurement: A Preregistered Reliability Failure of Black-Box LLM Observers on Shared Endpoints

## 基本信息

- **作者**：Haoyaun Zhu, Jie Zhang（arXiv 页面提交者显示 Haoyuan Zhu，作者名拼写存在页面内不一致）
- **首次公开日期**：2026-09-03
- **版本日期**：2026-09-03（v1）
- **arXiv**：2609.04198
- **原始论文**：https://arxiv.org/abs/2609.04198
- **代码/数据**：论文公开页未给出独立代码链接
- **DOI**：https://doi.org/10.48550/arXiv.2609.04198

## 一句话结论

共享 API endpoint 上“同一模型名”不是冻结的测量仪器：52,988 次审计中，同窗口排序相关仅 0.400，字节相同的次日重放相关仅 0.78，均远低于预注册门槛。

## 真正新增的内容

**论文原文结论**：以两次预注册审计直接测试黑盒 LLM Judge 的仪器稳定性，在分析任务效应前先验证重复性，并提出 snapshot-identity ladder、八条设计规则和报告清单。

**分析推断**：sealed eval 不仅要隔离数据和 evaluator，还要锁定服务快照或实测噪声下限。若 teacher/Judge 的自然漂移大于 A/B 分支差距，任何 score-level 蒸馏都会把 endpoint 噪声蒸馏进 student。

## 核心方法

- 固定请求、阈值和分析协议，重复调用共享 endpoint。
- 测量同窗口与跨日的排序一致性，并用字节相同输入隔离请求变化。
- 检查标签—含义映射、候选差距、排列读出、等待时间、provider 切换和自托管条件。
- 在机制已知的构造错误上测量 readout 对错误类型与幅度的敏感性。

## 关键实验结果

- 共审计 **52,988** 次请求。
- 同窗口 repeat ranking 的 Spearman 为 **0.400**，预注册要求为 0.90。
- 字节相同的次日 replay 为 **0.78**，预注册要求为 0.99。
- 等待在所测日期无帮助（0.805 vs 0.800）；五天复现实验支持该结论。
- 四家 provider 的中位稳定性约 **0.74–0.88**，暴露元数据不能预测差异。
- 约完整研究 **2%** 调用量的 pilot 已足以发现两个不可达 gate。

## 证据质量与局限

- **质量：高（针对共享黑盒 endpoint 的测量稳定性）。** 预注册、大调用量、跨 provider、重放与机制分解强化了证据。
- 结论限定于所测共享服务基础设施；不能直接推广到固定权重、固定 kernel、离线确定性 evaluator。
- 排序不稳定不等于所有任务判断都无用；大间隔、可执行真值任务可能仍稳定。
- 没有直接测试 verifier distillation 的下游训练损害，相关影响属于分析推断。

## 最接近的相关工作

与 Cheap Verifiers, Large Blind Spots、RecurSE、JuryProbe、Rubric Dropout 和 Harness-of-Harness 对 evaluator 共适应与独立评测的研究最接近；本工作额外把“endpoint 身份与时间稳定性”提升为评测仪器前置条件。

## 如何复用或推进 LLM-as-a-Verifier

- 每轮蒸馏前对固定 sentinel A/B/T 集做 byte-identical replay，估计当日转移矩阵与噪声下限。
- 只有 teacher 分数差显著大于仪器噪声时才生成硬 pairwise 标签；否则保留 Tie/不确定分布。
- 保存 provider、模型 route、时间窗、参数、原始响应和排列，不能只保存模型名。
- 将多次读取的经验分布蒸馏为 distributional verifier，而非把一次随机 verdict 当真值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher score 必须经重复测量校准；小于 noise floor 的 delta 不参与蒸馏。
- **A/B/T 与序数分布**：Tie 应覆盖“不可分辨”，不是只表示语义等价；报告标签条件转移。
- **真值门控**：程序/环境真值在冲突时拥有最高优先级，黑盒 Judge 不得覆盖。
- **critique states**：对相同 state 重采样 critique，区分稳定错误定位与语言表面变化。
- **高熵探索**：Judge 自身不稳定不能误判为策略高熵；两种不确定性需分别估计。
- **sealed eval**：最好使用固定本地权重与确定性栈；若必须用 API，应保存 sentinel 审计并把时间漂移计入置信区间。