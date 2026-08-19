# Beyond the Trace：把可解释推理状态读出耦合到原生 MoE 路由

## 基本信息

- **论文标题**：Beyond the Trace: Coupling an Interpretable Reasoning-State Readout to Native MoE Routing
- **作者**：Kang Chen、Sihan Zhao、Yixin Cao、Yugang Jiang
- **首次公开日期**：2026-08-18（arXiv v1；提交时间 10:56:31 UTC）
- **版本日期**：2026-08-18（v1）
- **arXiv ID**：2608.17638
- **DOI**：10.48550/arXiv.2608.17638（arXiv/DataCite DOI，论文页标记为待注册）
- **原始论文**：https://arxiv.org/abs/2608.17638
- **HTML 全文**：https://arxiv.org/html/2608.17638v1
- **代码链接**：截至本记录日期未发现公开代码仓库；论文列出的项目页 https://cckfdu.com/jar/ 当前未能访问，不能视为已验证代码链接。
- **记录类型**：新发现；与长轨迹过程 verifier、高熵分支选择和在线算力分配高度相关，但不是传统 reward model / verifier distillation 论文。

## 一句话结论

论文把模型隐藏状态中的词表尺度 Jacobian-lens 读出蒸馏为 64 维可解释过程状态（J64），再把 J64 蒸馏到 MoE 原生路由统计（R64）；R64 可在几乎不增加推理开销的情况下帮助选择分支、加权投票并提前停止失败轨迹，为 Agent verifier 提供了一条“读取 student 内部过程状态，而不只评文本轨迹”的新路线。

## 真正新增的内容

### 论文原文结论

1. **从文本轨迹之外读取过程状态**：J64 是从模型自身推理隐藏状态构造的 64 轴语义坐标系，区分“被要求投入多少推理 effort”与“问题实际造成多少 strain”；它不是正确性分类器，也不是输出 token 的简单回声。
2. **把昂贵隐藏状态读出蒸馏到廉价路由信号**：用岭回归从 MoE expert 使用谱重建 J64，得到 R64。该映射只以 J64 为目标，不使用结果标签；服务时只需读取生成本来就产生的路由统计。
3. **把读出用于两种时间尺度的决策**：对已完成的 64 条 sibling rollouts 做单分支选择与加权投票；对生成中的 256-token 窗口估计失败风险，用 CUSUM 累积证据后停止并重采样。
4. **有限的机制干预证据**：作者编辑 router logits，观察到目标轴所指向的失败形态按预测改变，提供小规模因果案例，而不只是相关性分析。

### 分析推断

- 这不是现成的 LLM-as-a-Verifier 或 score-level OPD 方法，但它把“可蒸馏的 verifier 输入”从可见文本扩展到了 student-generated latent/routing states。
- 对长时程 Agent，R64 的价值可能更像一个**过程遥测通道**：辅助发现停滞、反复、约束丢失或分支耗散，再与环境真值和文本 critique verifier 融合；论文尚未在工具调用 Agent 环境验证这一推断。
- J64→R64 是一种 representation/readout distillation，不等于把 teacher 的偏好或奖励分布蒸馏给 student，不能直接声称解决 verifier distillation。

## 核心方法

1. **J64 语义框架**
   - 从 Jacobian lens 的词表尺度 J-space 中寻找在推理状态里稳定高激活的方向；
   - 合并近重复方向为 64 个语义族，使用每族加权平均方向作为一轴；
   - 通过伪逆把隐藏状态投影为 64 维读数；轴在构造完成后才命名，构造本身不使用 outcome、effort 或 difficulty 标签；
   - 对轨迹或滑动窗口聚合这些读数，形成“caution、arithmetic、constraint、optionality”等可读过程坐标。

2. **R64 路由代理**
   - 对三个 MoE 层统计每个 expert 的累计 gate 权重、token 数归一化使用率及 gate entropy；
   - 以岭回归学习 routing statistics → J64 的映射；
   - 映射校准阶段需要成对的 J64 与路由数据，但部署阶段不需回放隐藏状态或第二次前向。

3. **离线选择与投票**
   - 用 source benchmark 的正确/失败标签训练 selector，再冻结到其他 benchmark；
   - 既可选择单条 rollout，也可将预测正确率作为 majority vote 的分支权重。

4. **在线停止与重采样**
   - 每 256 token 计算一次窗口失败分数；
   - CUSUM 累积风险，越阈值即停止当前分支并从独立采样池重启；
   - 阈值和预算操作点只在训练问题上选择，并冻结到 held-out 问题。

## 关键实验结果

### 论文原文结果

- 数据主要为 AIME-24、AIME-25、HMMT-25、BRUMO-25，每个 benchmark 30 题、每题最多 64 条 rollout；主模型为 gpt-oss-20b，并在 gpt-oss-120b 与 Qwen3-30B-A3B 上复制部分结果。
- J64 加到匹配的 token-occupancy 文本基线后，轨迹结果预测的 held-out AUC 增益为 **+0.096 至 +0.135**。
- R64 对 J64 的 64 轴中位相关为 **0.692–0.864**；在 gpt-oss-20b 上保留 J64 相对文本基线结果预测增益的 **95%–100%**。
- 冻结跨 benchmark 的 best-of-64 单分支选择中，J64 相对随机选取平均提升约 **+4.9 至 +5.0 个百分点**（两种 gpt-oss 规模）；R64 在四个模型组均为正增益。
- R64 加权投票在 **8 个设置中的 7 个**优于普通 majority vote；在普通投票完全失败的 223 个问题上，J64/R64 分别找回 **17.0%/14.1%**，随机选取为 8.7%。
- 在线停止/重采样相对 sibling-permuted 控制：J64 在 gpt-oss-20b High 上提升 **+1.3 至 +5.9 点**，R64 提升 **+2.2 至 +3.2 点**；Qwen 上的提升较小但仍为正。
- 捕获 gate 权重的报告开销约 **0.07 ms/token**，相比 38.4 ms/token 解码处于运行噪声范围。

### 分析判断

- 最重要的结果不是某个单一准确率，而是：**同一问题的 sibling branches 即使局部文本相同，内部过程状态仍可能区分其后续成败**。这正适合高熵分叉后的“保留、回滚、追加 critique 或继续执行”决策。
- R64 的单分支选择并非全面压倒文本或置信度基线；其更稳定的用途是与共识组合、作为在线控制传感器，而非替代最终 verifier。
- 论文的数学任务有自动答案解析器，因而其正确性标签比纯 LLM judge 可靠；但这不自动外推到开放式 Agent 轨迹。

## 证据质量与局限

### 证据质量

- **优点**：问题分组交叉验证、question-level cluster bootstrap、sibling-permutation 控制、冻结跨 benchmark 迁移、嵌套选择在线阈值、精确计费 token，并有 20B/120B 与另一模型家族的复制。
- **优点**：将 J64 与同样聚合方式的 token-occupancy 基线对照，并做 routing shuffle、同题 sibling 置换、残差化、PCA 容量匹配等控制。
- **总体判断**：作为“内部状态可用于过程选择”的机制与系统证据较强；作为通用 Agent verifier 的证据仍是间接的。

### 论文原文局限

- 核心实验集中在竞赛数学和 gpt-oss-20b；每个模型的 J64 单独构建，跨模型轴不对齐。
- 在线控制主要基于 causally masked replay，而非完整 live serving。
- 路由干预样本规模小。
- 在答案尚未确定时，读出不直接预测最终结果；反思词汇相关活动也部分存在于输出分布中。
- 更强的序列文本基线、更广领域及线上服务尚未验证。

### 额外分析局限

- 仅适用于可访问 hidden states 或 MoE routing 的开放权重/白盒模型；黑盒 teacher API 无法直接提供 R64。
- 训练 selector 和停止控制器仍使用结果标签，存在 evaluator 与策略共同适应的风险。
- 主冻结迁移协议的 J64 无标签框架构造池横跨四个 benchmark；虽有 frame-disjoint 和 source-only 检查，但对严格 sealed eval，仍应禁止任何 eval 任务状态进入表示构造和阈值选择。
- 当前只有 v1 预印本，未见同行评审与已验证代码复现。

## 最接近的相关工作

- **Jacobian lens / verbalizable representations**：直接基础；本文把词表尺度读出压缩为 64 维轨迹框架并部署到路由代理。
- **Process Reward Models（如 Let’s Verify Step by Step）**：都做过程评估，但 PRM 通常读取显式文本步骤；J64/R64 读取隐藏或路由状态。
- **DeepConf**：同为测试时早停/筛选；DeepConf 使用输出分布置信度，本文把路由视为语义过程传感器。
- **Self-consistency 与 test-time compute scaling**：本文不是替代多样化采样，而是对候选分支加权并将算力重新分配。
- **SOPD / trajectory-level OPD**：这些方法改变训练监督粒度；本文提供了可补充 token/step loss的轨迹内部状态信号，但没有进行 OPD 训练。
- **Critique-conditioned 或 trajectory-value verifier**：最接近应用目标；本文显示 verifier 可以加入不可见于文本的 process features。

## 如何复用或推进 LLM-as-a-Verifier

### 可直接复用

1. 在开放权重 MoE student 上记录每个 action/推理窗口的 expert usage 与 gate entropy，构造低成本 routing telemetry。
2. 用程序化答案、环境成功条件或人工 sealed labels 训练轻量 outcome/phase head；将 R64 与文本 critique、工具返回值、动作历史拼接，而不是单独依赖 R64。
3. 在 candidate branch reranking 中采用“共识票数 × 校准成功概率”，并保留一个只读 routing 分支用于诊断。
4. 把 CUSUM 风险累计推广为 Agent 轨迹的持续停滞检测：只在多窗口持续证据下回滚或重采样，避免单点噪声剪掉可恢复分支。

### 需要新实验验证

- 将 64 维语义框架替换或补充为 Agent 特定轴：约束记忆、目标推进、工具错误恢复、证据覆盖、循环/重复、不可逆动作风险。
- 比较 R64 与文本 PRM、generative verifier、环境 phase-progress critic 的互补性。
- 研究跨模型对齐：teacher 与 student 各自框架目前不一一对应，不能直接做 latent-axis KD；可先学共享 ordinal outcome bins 或 canonical task-state probes。

## 对 Agent verifier × OPD 实验路线的具体影响

以下均为**分析推断**，不是论文已经完成的实验。

### 1. Score-level on-policy verifier distillation

- 在 student 自生成轨迹上，用 sealed teacher/verifier 产生 outcome score，同时记录 R64/J64。
- 训练 student verifier 输出“成功概率 + 可恢复性 + 阶段进展”的分布，而不是复刻 teacher token logits。
- R64 可作为辅助输入或蒸馏目标；但最终 score 应由环境真值校准，避免把 MoE 路由习惯误当正确性。

### 2. Pairwise A/B/T 与序数评分分布

- 从同题 sibling branches 构造 A/B/T：A、B 分别表示哪条分支更值得继续，T 表示证据不足或两者近似。
- 不应直接以单一 J64/R64 线性分数硬排序；建议输出有序桶分布，如“明显退化 / 可恢复 / 中性 / 有进展 / 高置信成功”。
- 将预测熵保留下来：高熵 pair 进入 T 或继续采样，而非强制二分类。

### 3. 程序化/环境真值门控 teacher 信号

- 论文已经使用 verified answer parser 训练选择和控制头，这支持“真值先门控、teacher 再提供密集解释”的结构。
- Agent 场景应以环境 success、单元测试、数据库状态或可执行约束为高优先级门控；仅在真值不可得时使用 LLM judge，并记录不确定性来源。

### 4. Student-generated critique states

- J64/R64 本质上来自 student 自己走过的状态，适合与 student-generated critique 同步采集。
- 建议做四臂消融：文本轨迹；文本+critique；文本+R64；文本+critique+R64，以验证内部状态是否提供增量，而不是只反映 critique 已写出的内容。

### 5. 高熵分叉下保留探索

- 论文支持“发现持续失败后重采样”，不支持“看到高 strain 就立即剪枝”；strain 同时与困难度相关，困难问题可能需要更多而非更少计算。
- 控制器应区分 uncertainty、difficulty 和 unrecoverable stall：高熵但可恢复的分支继续探索，只有经过累计证据且有替代分支时才停止。
- 预算比较必须像论文一样精确计费并固定操作点，防止重采样策略靠额外 token 获益。

### 6. 独立 sealed eval 防止 evaluator 共适应

- 采用严格三分：表示/路由校准集、verifier/控制器训练集、sealed eval；sealed 任务的提示、状态、路由统计均不得参与 J64/R64 构造、阈值或正则选择。
- 评估时冻结 verifier、路由映射和停止策略；同时报告随机 sibling、文本 PRM、DeepConf、普通 majority vote 与环境 oracle 上界。
- 若 policy 与 verifier 联训，增加一个完全独立、只在最终评估访问的 evaluator，并检查 R64 的校准漂移，避免 student 学会塑造路由特征以取悦 evaluator。

## 建议的下一步实验

- 在 ALFWorld/WebShop 或有可执行真值的内部 Agent 环境，先做**只读 R64 probe**，不改变 policy。
- 每个任务采样 8–16 条 sibling trajectories，记录环境结果、阶段进度、文本 critique 与 routing telemetry。
- 用 source-only 任务训练 ordinal verifier，在全新任务族 sealed 测试：比较 pairwise A/B/T、五档序数分布和单标量三种输出。
- 只有确认 R64 在文本+critique 之上仍有增量后，再把它加入 score-level on-policy verifier distillation；第一阶段不允许 verifier 梯度回传到 policy，以减少共适应。
