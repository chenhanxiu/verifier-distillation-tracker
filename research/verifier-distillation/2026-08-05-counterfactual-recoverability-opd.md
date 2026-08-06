# Not Every Divergence Should Be Suppressed：OPD 中的反事实可恢复性

## 基本信息

- **论文标题**：Not Every Divergence Should Be Suppressed: Counterfactual Recoverability in On-Policy Distillation
- **作者**：De Jiang、Zhengyang Zhang、Kehong Yuan、Shaohua Ma
- **首次公开日期**：2026-08-05
- **当前版本日期**：2026-08-05（arXiv v1）
- **arXiv ID**：2608.04408
- **原始论文**：https://arxiv.org/abs/2608.04408
- **DOI**：https://doi.org/10.48550/arXiv.2608.04408（arXiv/DataCite，论文页标注为待注册）
- **代码**：截至 2026-08-06，论文页及正文未提供公开代码链接
- **记录类型**：scheduler 新发现

## 一句话结论

论文用预算匹配的“从错误处继续”与“回滚后重采样”两条反事实分支定义可恢复性，证明 teacher–student divergence 不是决定保留还是压制探索的可靠信号；这几乎正面命中了长时程 Agent OPD 中的错误修复与探索保留问题。

## 真正新增的内容

**论文原文结论：**

1. 将错误后的训练决策形式化为**反事实可恢复性**：在相同剩余环境步数、token、温度与采样预算下，teacher 从错误状态继续完成，是否比回滚该错误并重采样更容易成功。
2. 用 branch outcome 将错误状态分为三类：可恢复、不可逆但可避免、证据含混。
3. 三类状态分别触发 retain + corrective continuation、rollback/resample、fallback to ordinary SOD。
4. 使用 shared admissible action set，让 teacher 与 student 对相同合法动作候选评分，避免非法动作和跨 tokenizer 对齐问题混入诊断。
5. 将用于构造 recoverability feature 的 probe branches 与预测目标 branches 分离，降低 outcome leakage。

**分析推断：**

这项工作的关键不是一个新的 divergence weight，而是把“是否应压制分叉”从 policy disagreement 问题改写为 outcome-grounded causal decision。对 Agent verifier × OPD 而言，它提供了一个比“高 KL=坏状态”更合理的 teacher 信号生成协议，也自然保留 ambiguous 状态而不强制二分。

## 核心方法

对观测到错误的状态 (s)，在相同剩余预算 (B(s)) 下运行两组 teacher branch：

- **continue**：保留错误动作，从当前状态继续；
- **rollback**：回到错误前状态，重采样动作后继续。

估计两者成功率 (p_{cont}(s)) 与 (p_{roll}(s))，并定义：

[
Delta_{action}(s)=p_{cont}(s)-p_{roll}(s).
]

论文预注册的分类规则为：

- (p_{cont}ge 0.50)：recoverable；
- (p_{cont}le 0.25) 且 (p_{roll}ge 0.50)：irreversible-but-avoidable；
- 其他：ambiguous。

训练 backbone 在环境提供的 shared admissible action set 上，让 teacher/student 各自计算候选动作的序列平均 log-probability，再在候选集合内归一化。teacher argmax 动作作为 retained target；SOD reproduction 使用沿轨迹的近似 divergence 变化做权重。反事实标签只决定保留、回滚或回退普通 SOD，不替代 backbone loss。

## 关键实验结果

**论文报告：**

- 训练任务：AIME2024 的 30 个 manifest 任务。
- Student：Qwen3.5-9B；teacher：Qwen3.5-27B。
- 在 200 个可回放错误状态中，65 个标为 recoverable，34 个标为 irreversible-but-avoidable，101 个为 ambiguous。
- recoverable 状态的平均 continue-minus-rollback effect 为 **0.185**；irreversible-but-avoidable 状态为 **-1.000**，两类状态需要方向相反的干预。
- branch-derived recoverability proxy 的 AUC 为 **1.000**，单独使用 divergence 的 AUC 为 **0.392**。
- frozen AIME2025 held-out protocol 上，recoverability-aware control 的 success 为 **0.578**，最佳 baseline 为 **0.517**。
- AIME2024–2025 average@32 从 **0.2656** 提升到 **0.3125**。
- GPQA-Diamond average@32 从 **0.2702** 提升到 **0.3070**。
- 组件消融中，保留 teacher 可修复 prefix 是最大的单项贡献。
- 训练健康记录中，Vanilla OPD 的 30-task success 为 0.513，SOD reproduction 为 0.452，recoverability oracle 为 0.539；论文明确说明 oracle 额外使用 teacher/environment calls，不能视为等成本排行榜。

## 证据质量与局限

**证据较强之处：**

- 反事实分支严格匹配剩余环境和生成预算，问题定义可审计。
- probe-target 分离，避免用同一批 branch outcomes 同时构造特征与评估特征。
- 有 held-out AIME2025、AIME24–25 和 GPQA-D frozen evaluation，并报告三个训练 seed。
- 作者主动限定结论：oracle 是诊断上界，不宣称是廉价在线算法，也不宣称一般化恢复规划器。

**局限：**

- v1 preprint、无公开代码；实验规模小，三个训练 seed 的标准差不是覆盖测试样本的置信区间。
- oracle 标签需要大量额外 teacher 与环境 rollout，且与 baseline **不等总成本**。
- AUC=1.000 来自论文记录的特定 branch diagnostic，不应外推为一般环境中的完美预测。
- 训练只使用 30 个 AIME manifest task；所谓“环境”主要是共享合法候选动作的数学推理设置，尚未覆盖真实工具调用、外部状态改变和不可逆副作用。
- 101/200 状态为 ambiguous，说明 branch 预算与样本数对标签覆盖率构成明显上限。
- student/teacher 被保守地视为 tokenizer 不对齐，SOD 信号是相同动作文本的 sequence-mean log-probability gap，而不是严格 token-level KL。
- 没有独立 sealed evaluator；formal eval 虽冻结 adapter 且使用 held-out protocol，但尚不足以排除 evaluator 共适应或 benchmark-specific selection。

## 最接近的相关工作

- **SOD / step-wise divergence weighting**：根据 teacher–student divergence 的演化调节监督强度；本文表明 divergence 无法回答“继续还是回滚”的因果问题。
- **Look Ahead Before You Distill / future trajectory validation**：同样检验 teacher guidance 的未来后果；本文更明确构造 budget-matched continue-vs-rollback 反事实。
- **ROSD / reflective OPD**：定位错误并局部修复；本文不依赖自然语言 reflection，而以可执行 branch outcome 定义修复策略。
- **SPOT**：对多个局部候选做 verifier-scored continuation，并校准目标分布；SPOT关注“哪个分叉更有价值”，本文关注“当前错误 prefix 是否值得保留”。
- **Distill Where You Fail**：把蒸馏预算集中于 RL 失败组；本文把失败进一步拆成可恢复、应回滚和含混三类。
- **Agent recovery / retry planning**：通常在推理时重试或重规划；本文将可恢复性用于训练阶段的 OPD 监督决策。

## 如何复用或推进 LLM-as-a-Verifier

1. 把昂贵 branch oracle 蒸馏为轻量 **recoverability verifier**：输入 prefix、错误动作、剩余预算和环境摘要，输出三类概率而非硬标签。
2. 训练标签应由环境/程序化结果门控；LLM verifier 可生成错误定位和 repair critique，但三类标签最终由 continue/rollback 的实际 outcome 差异校验。
3. 使用 ordinal probabilistic reward model 表达“继续优于回滚”的置信度：例如从明显应回滚、弱应回滚、含混、弱可恢复、明显可恢复五级分布，而非仅三类硬阈值。
4. 将 pairwise A/B/T 映射为 A=continue、B=rollback、T=ambiguous；用 branch sampling 构造偏好后验，再蒸馏 score-level verifier。
5. 为 student-generated critique states 增加第三个反事实分支：保留 prefix + critique/repair，然后与纯 continue、rollback 比较；这能检验 critique 是真正恢复状态还是只改善表面解释。

## 对现有 Agent verifier × OPD 实验路线的具体影响

### 1. Score-level on-policy verifier distillation

建议把 student verifier 的学习目标从“当前轨迹好不好”扩成**条件化行动效应分布**：预测在给定剩余预算下 (p_{cont})、(p_{roll}) 与 (Delta_{action})。OPD 蒸馏的是对训练动作有意义的反事实 score，而不只是 teacher/student disagreement。

### 2. Pairwise A/B/T 与序数评分分布

论文的三分类正好对应 A/B/T：continue 胜、rollback 胜、tie/ambiguous。与其用固定阈值把所有状态硬分，应保留 bootstrap posterior 或 Beta-Binomial posterior，形成可校准的序数/偏好分布。

### 3. 程序化/环境真值门控 teacher 信号

该论文是直接支持：teacher 的 corrective target 只有在 branch outcome 证明 prefix 可恢复时才被保留；不可恢复状态回滚；证据不足回退保守策略。对工具 Agent，应优先采用任务成功、数据库状态、文件 diff、UI state 等环境真值判定 branch，而非只让 LLM judge 自评。

### 4. Student-generated critique states

论文未测试 critique。最值得新增的实验是三臂分叉：继续、回滚、继续并注入 student/teacher critique。若 critique 分支仅在 LLM judge 上获胜、但环境 outcome 不提升，则可直接识别“评价语言变好而行为未恢复”。

### 5. 高熵分叉下保留探索

这篇论文说明不能看到高 divergence 就压制。recoverable 状态上保留 prefix 是最大贡献，因此高熵/高分歧分叉应先做 recoverability probe；仅当 rollback 明显优于 continue 时才剪枝。ambiguous 状态应保留一定探索质量，避免 verifier 过早收缩支持集。

### 6. 独立 sealed eval

论文已有 frozen held-out eval，是正确方向，但仍非完整 sealed eval。现有路线应使用独立任务集、独立环境 evaluator、隐藏成功判定和人工抽检；训练期间不可访问 sealed branch outcomes。重点报告 recoverability verifier 在环境/工具分布迁移后的 calibration、A/B/T 翻转率和任务成功率，而不仅是训练 oracle 的 AUC。

## 建议的最小复现实验

- 选择可 snapshot/rollback 的 Agent benchmark；
- 每个失败轨迹采样首个错误点与一个高熵分叉点；
- 在等步数、等 token、等工具调用预算下运行 continue、rollback、critique-continue 三臂；
- 用环境真值获得成功后验，同时保存 LLM verifier 的序数分布；
- 训练轻量 recoverability verifier，并与 divergence-only、entropy-only、outcome-RM 对比；
- 最终只在 sealed tasks 上评估任务成功、回滚成本、探索覆盖、ECE/Brier、A/B/T 一致率和跨 evaluator 排序稳定性。
