# CoVer：以信息增益奖励和多样性裁剪共同训练代码生成器与 Verifier

- 论文标题：Information-Gain Rewards over Diversity-Pruned Tests: GT-Anchored Verifier Co-Training for Reliable Code Generation
- 作者：Ana Nunez；Peyman Najafirad
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.21208
- DOI：https://doi.org/10.48550/arXiv.2609.21208
- 代码：截至 v1 未见论文提供公开代码仓库

## 一句话结论

CoVer 用少量 ground-truth 测试形成分级正确性锚点，再奖励能够区分候选程序的自生成测试，把“程序真值定方向、生成式 verifier 增加密集信号”落实成同一策略内的联合训练。

## 真正新增的内容

- 【论文原文】指出 coder–test-author 自博弈会发生 permissiveness collapse：生成容易通过但没有判别力的测试；同时独立采样的测试会集中于相似输入，导致信息增益估计方差偏高。
- 【论文原文】提出 covariance-gated mutual-information reward：只有与 ground-truth 分级正确性正相关的测试才得到奖励。
- 【论文原文】用 invalidity、输入字符串和执行谱三阶段裁剪去除冗余测试，在固定执行预算下提高有效样本量。
- 【分析推断】区别于“让 Judge 自己定义好坏”，CoVer 保留不可被生成式 verifier 覆盖的硬锚点，并让软 verifier 只学习在该锚点下的判别增量。

## 核心方法

同一模型以 coder 和 verifier/test-author 两种角色采样。每个候选程序先由任务自带的 ground-truth 测试得到 0–1 分级正确性向量；每个自生成测试在候选程序集合上产生通过/失败列。测试奖励等于该列与正确性向量之间的信息增益，并以协方差符号作门控。经过多样性裁剪后，coder reward 与 verifier reward 分别形成组归一化 advantage，共同更新共享策略。

## 关键实验结果

- 【论文原文】在 LiveBench、MBPP、LiveCodeBench、CodeContests、CodeForces 上，相对 Qwen2.5-Instruct，one-shot pass@1 在 7B 提升 5.8 点、14B 提升 7.1 点。
- 【论文原文】多样性裁剪使宏平均 pass@1 从 34.27 提升到 35.94，且不增加执行成本。
- 【论文原文】改用简单 pass-rate reward、二值化正确性锚点、移除 verifier 角色，宏平均分别下降 2.03、1.19、2.43 点。
- 【论文原文】作为 CodeT 的 backbone，CoVer-7B 将宏平均从 38.97 提升到 42.47（+3.50 点）；结果包含 4 个随机种子。

## 证据质量与局限

- 【论文原文】证据包含多个代码 benchmark、7B/14B 主实验、Llama-3.1-8B 补充实验、消融和跨种子波动，内部证据较完整。
- 【论文原文】训练仍要求每题至少一个 ground-truth 测试；裁剪只处理完全重复而非高度相关测试；假设 sandbox 确定性执行；GUI、分布式系统和有随机副作用的 Agent 环境不在验证范围内。
- 【论文原文】verifier 只见过当前策略的代码分布，部署时对 OOD 代码可能误判；pass@1 提升不等于正确性保证。
- 【分析推断】coder 与 verifier 共享参数，仍可能共同适应；当前结果不能替代冻结模型、冻结测试和独立任务组成的 sealed eval。

## 最接近的相关工作

最接近 CodeT、Learning to Solve and Verify、ACECoder、StepCoder，以及使用程序执行反馈的 RL。与 OPDVR、RA-OPD 的共同点是硬真值门控；区别是 CoVer 蒸馏的是“哪些测试具有判别价值”，并与生成策略联合训练。

## 如何复用或推进 LLM-as-a-Verifier

可把 Agent 状态下的候选下一步动作视为候选程序，把可重放的程序化验收、状态不变量或终局结果视为 ground-truth correctness anchor；让 generative verifier 生成探针、反事实检查或子目标测试，并按其对候选动作的实际区分信息获得奖励。评分输出应保留“硬门控是否通过、软测试的信息增益、测试冗余度”三个分量，而不是压成单一标量。

## 对现有 Agent verifier × OPD 路线的具体影响

- score-level OPD：可将 covariance-gated information gain 作为 teacher score 的幅度，环境真值继续决定更新方向。
- pairwise A/B/T 与序数分布：对同一状态的动作候选执行测试，按通过谱与真值相关性构造 A/B/T；近似等价或证据不足者保留 T，而非强制排序。
- 真值门控：至少保留一个不可学习、不可被 verifier 改写的 executable anchor。
- student-generated critique states：允许 student 生成检查项，但只有能区分真实成功/失败分支的 critique 才进入记忆或蒸馏。
- 高熵探索：先做执行谱去冗余，再保留行为上不同的分支，避免把预算浪费在表面多样、结果同质的动作上。
- sealed eval：训练期共享 coder/verifier 可以提高效率，但上线验收必须使用隐藏测试、冻结环境与独立 evaluator，专门检测两角色的协同投机。
