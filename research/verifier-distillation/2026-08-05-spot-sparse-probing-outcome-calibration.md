# SPOT：Sparse Probing and Outcome Calibration for On-Policy Distillation

## 基本信息

- **论文标题**：SPOT: Sparse Probing and Outcome Calibration for On-Policy Distillation
- **作者**：Zikun Qu、Min Zhang、Mingze Kong、Zhiwei Shang、Yikun Ban、Shuang Qiu、Zhongxiang Dai
- **首次公开日期**：2026-08-05
- **当前版本日期**：2026-08-05（arXiv v1）
- **arXiv ID**：2608.04419
- **原始论文**：https://arxiv.org/abs/2608.04419
- **DOI**：https://doi.org/10.48550/arXiv.2608.04419（arXiv/DataCite，论文页标注为待注册）
- **代码**：截至 2026-08-06，论文页及正文未提供公开代码链接
- **记录类型**：scheduler 新发现

## 一句话结论

SPOT 不再把 teacher 的局部 token 分布直接当作唯一真值，而是在少量高价值分叉点上用可验证的下游结果校准 teacher 分布；它是目前与“高熵分叉保留探索 + 环境真值门控 + score-level OPD”最直接衔接的方法之一。

## 真正新增的内容

**论文原文结论：**

1. 把 OPD 中两个常被混在一起的问题拆开：**在哪里值得额外探索**，以及**探索之后应该蒸馏什么目标分布**。
2. 提出稀疏 acquisition score，同时考虑 teacher 的归一化熵、teacher top-k 候选覆盖的概率质量，以及 student 对这些候选的质量/排序缺口；因此并非“熵高就探索”。
3. 在选中的位置，对 teacher 提议的多个 next-token 候选分别运行 student continuation，再用终局 verifier 结果估计候选的可执行价值。
4. 给出闭式 KL 正则目标：以 teacher 分布为 prior，用候选的下游价值作指数倾斜，得到 outcome-calibrated target，而不是坍缩成单个胜者。
5. 明确控制探测成本：每条轨迹最多增加 (M\times k_p\times N_p) 条候选 continuation。

**分析推断：**

真正重要的增量不是又一种 entropy-aware OPD，而是把“teacher 的局部概率”降级为 proposal prior，再由环境结果修正其相对赔率。这为 verifier 蒸馏提供了一个清晰接口：teacher 给候选支持集，verifier 给 branch value，student 蒸馏校准后的分布。

## 核心方法

对 student rollout 的每个位置 (t)，SPOT 计算：

- teacher 归一化熵；
- teacher top-(k_s) 候选的累计概率质量；
- student 在同一候选集上的质量欠覆盖与 JS 形状差异。

三者相乘形成 acquisition score，只探测分数最高的 (M) 个位置。随后对每个被选位置的 teacher top-(k_p) 候选，各采样 (N_p) 条由冻结 behavior student 继续完成的轨迹，并用 verifier 奖励估计候选价值 (hat V_t(v))。

在至少存在一个正奖励候选时，目标分布为：

[
	ilde{pi}_T(vmid c_t)propto ar{pi}_T(vmid c_t)exp(gamma hat V_t(v)).
]

这等价于在 teacher prior 周围的 KL trust region 内最大化估计 branch value。最终损失由全轨迹 OPD loss 和稀疏 branch-distillation cross-entropy 组成；没有找到可行分叉时退回标准 OPD。

## 关键实验结果

**论文报告：**

- Teacher 为 Qwen3-8B（关闭 thinking）；student 为 Qwen3-0.6B、1.7B、4B。
- 训练数据为 MATH 或 DAPO-Math-14k；评估覆盖 MATH-500、AMC 2023、Minerva Math、HMMT 2025、AIME 2024、AIME 2025。
- 相比标准 OPD，三个 student 尺度上的宏平均 Avg@8 提升 **0.47–1.48 个百分点**，宏平均 Pass@8 提升 **4.55–5.28 个百分点**。
- 相比最接近的 entropy-aware OPD（EOPD），宏平均 Avg@8 提升 **0.29–0.68 个百分点**，Pass@8 提升 **2.49–3.19 个百分点**。
- Qwen3-4B 上，SPOT 的宏平均 Avg@8/Pass@8 为 **36.13/54.30**，标准 OPD 为 **35.66/49.57**。
- verifier-guided calibration 消融中，Qwen3-1.7B 的四项宏平均 Avg@8/Pass@8 相对无 verifier guidance 提升 **3.21/7.38 个百分点**。
- 在 AIME24、AIME25、AMC23 的 Pass@k 测试中，(k=64) 时相对 OPD 仍有 **12.50–16.67 个百分点**优势。
- Llama-family 复现实验保留了“Pass@8 增益大于 Avg@8 增益”的整体趋势。

## 证据质量与局限

**证据较强之处：**

- 有多尺度 student、两个模型家族、六个数学 benchmark，并与 KD、OPD、GRPO、EOPD 比较。
- 对 acquisition score、verifier 校准、采样预算和 branch loss 权重做了消融。
- 目标分布有闭式推导，并清楚区分 teacher prior 与 verifier correction。

**局限（论文事实与审慎判断）：**

- 当前仍是未同行评审的 v1 preprint，且未公开代码，复现性暂时有限。
- 训练 verifier 实际是**二元终局 verifier**，每个候选只采一条 probe rollout；论文推导支持更一般的 (N_p)，但实验中的 branch-value 方差可能很高。
- 实验集中于可程序验证的数学答案，尚未验证包含工具副作用、不可逆动作、长反馈延迟的 Agent 环境。
- 主要收益体现为 Pass@k/coverage，而非同等幅度的单样本准确率提升；这支持“保留探索”的主张，但不等于已证明长轨迹上的 calibrated verifier 更准确。
- 论文评测与训练使用同类答案 verifier，未设置独立 sealed evaluator，因此不能排除 evaluator 共适应或 verifier-specific optimization。
- 未报告与普通 OPD严格等总算力/总 verifier 调用的 cost-normalized 对比。

## 最接近的相关工作

- **Entropy-aware On-Policy Distillation（EOPD）**：同样在 teacher 高熵位置扩展监督；SPOT 进一步区分紧凑多峰与长尾不确定性，并用下游结果校准候选。
- **Uni-OPD**：讨论 teacher 局部偏好可能不等于可完成结果；SPOT 将该问题落实为候选 continuation 探测。
- **Rethinking On-Policy Distillation**：强调 student-teacher compatibility 和 teacher 新信息量；SPOT 的 acquisition score 直接编码这种缺口。
- **Generative/Process Reward Models**：提供更细的过程判断；SPOT 当前不训练新 verifier，而是消费外部 verifier 的终局结果。
- **OPRM / distributional reward modeling**：OPRM 对响应质量建模序数概率分布；SPOT 对候选 continuation 构造 outcome-tilted 分布，二者可在不确定性表达与分布蒸馏上自然结合。

## 如何复用或推进 LLM-as-a-Verifier

1. 将二元 (Rin{0,1}) 替换为 verifier 输出的**序数评分分布**，用期望效用、下分位数或风险敏感效用计算 (hat V_t(v))，而不是先压成标量。
2. 对 pairwise A/B/T：把 top-k 分叉候选组成局部 A/B/T 比较，蒸馏 pairwise 后验或 Bradley–Terry/ordinal posterior，再与 teacher prior 合成。
3. 让 generative verifier 为各分叉生成 critique；critique 不直接当标签，而作为新的 student-generated critique state，再由环境结果验证其是否提高可恢复率。
4. 对程序化真值可用的子任务，保留 hard gate；对无真值段落使用 calibrated LLM verifier，并显式传递其不确定性。
5. 将 probe 数据反向用于训练轻量 verifier student：输入 prefix、候选 action 和 continuation 摘要，预测 branch outcome distribution；这样可把昂贵在线探测蒸馏成可部署的局部价值模型。

## 对现有 Agent verifier × OPD 实验路线的具体影响

### 1. Score-level on-policy verifier distillation

SPOT 给出一个可直接采用的目标：不是蒸馏单一 teacher score，而是蒸馏“teacher prior × verified branch value”形成的校准分布。建议把当前 score-level 路线扩展为 branch-conditioned score distribution distillation。

### 2. Pairwise A/B/T 与序数评分分布

论文当前用 top-k 多候选和二元结果，但其 log-odds 分解天然支持 A/B/T：teacher 提供先验赔率，verifier 提供下游价值差。可将 T（tie/uncertain）显式保留为序数后验重叠，而非强行决出胜负。

### 3. 程序化/环境真值门控 teacher 信号

这是 SPOT 最可复用的部分。只在至少一个候选通过 verifier 时增加 branch supervision，相当于“环境真值先门控，再蒸馏 teacher 的密集分布”，可降低错误 teacher 信号被放大的风险。

### 4. Student-generated critique states

论文没有使用 critique state。建议新增对照组：在高 acquisition score 位置生成 critique/repair proposal，把这些 proposal 也作为候选分叉，继续用相同环境 verifier 做 outcome calibration。

### 5. 高熵分叉下保留探索

论文为该设计提供直接正证据：Pass@k 的增益显著大于 Avg@k，说明保留多个 verifier-supported 分叉能扩大可行解覆盖。但应复现为长时程 Agent 的“不同计划/动作分叉”，不能仅依赖 token 级数学结果外推。

### 6. 独立 sealed eval

论文没有充分解决这一点。现有路线应坚持：训练探测使用环境 verifier A；最终评估使用隔离数据、不可见测试任务和独立 verifier B/人工审计，并报告 train-verifier 与 sealed-eval 的相关性和排序翻转率。

## 建议的最小复现实验

- 在可回放的工具 Agent 环境中，每条轨迹仅选 1–3 个高 acquisition score 决策点；
- 每点保留 3 个动作/计划候选，各做 2–4 次 continuation；
- 同时报 hard environment outcome、OPRM 序数分布、pairwise A/B/T；
- 比较 Vanilla OPD、entropy-only、SPOT-binary、SPOT-ordinal；
- 核心指标除 task success 外，加入 branch coverage、calibration error、rollback cost、不同 verifier 下的排序稳定性，以及 sealed eval success。
