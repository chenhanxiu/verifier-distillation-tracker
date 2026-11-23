# WEIR: Watershed Exploration and Drift-Aware Prefix Shrinkage for Multi-Turn Agent Reinforcement Learning

- **作者**：Pixel Nomand、Elena Voss、Marcus Hale、Sofia Reyes
- **首次公开日期**：2026-11-20
- **当前版本日期**：2026-11-20（v1）
- **原始论文**：https://arxiv.org/abs/2611.27570
- **代码**：截至本记录未发现作者公开代码链接
- **标识符**：arXiv:2611.27570；DOI: 10.48550/arXiv.2611.27570

## 一句话结论

WEIR 不在所有高熵节点盲目分叉，而在“仍有生存空间且价值陡降”的 watershed fork 集中 rollout，并用漂移感知收缩处理跨轮次旧数据；这直接细化了“高熵分叉下保留探索”的预算原则。

## 真正新增的内容

**论文原文**：基于 Doob turn-variance conservation，WEIR 维护跨迭代 canonical action-prefix tree；critic 目标在稀有节点的单轨迹回报与密集节点的经验均值之间自适应收缩，并同时做任务级 Neyman 分配与状态级 watershed 分叉。

**分析推断**：新增点是把不确定性与价值悬崖结合。纯策略熵高但结局已确定的死路不值得继续；对 verifier × OPD，应把分叉预算投向 score 分布高熵且替代行动可能改变终局的状态。

## 核心方法

- 跨训练迭代维护动作前缀树，访问计数指数衰减以处理策略漂移。
- 训练 prefix-conditioned critic，使用 minimax drift-aware shrinkage target。
- 按任务成功概率的 Neyman 分层分配 rollout 预算。
- 在任务内选择 survival-headroom uncertainty 高且 value cliff 陡的 watershed fork。

## 关键实验结果

**论文原文**：

- 在四个多跳 QA、ALFWorld、WebShop 上评估 Qwen2.5-3B/7B-Instruct。
- 平均 QA EM 分别为 32.18% 和 37.85%。
- ALFWorld 成功率分别为 84.83% 和 87.81%。
- 相比 CAPO 提升 1.50–3.74 点，同时比 chain sampling 少生成 28%–29% rollout token。

## 证据质量与局限

覆盖多任务、两种规模并同时报告性能与 token 成本，和现有长轨迹路线高度相关。局限是 actor-critic 依赖自身 critic，可能发生 evaluator 共适应；摘要未报告 sealed critic audit、分支多样性或环境不可逆性，作者与代码可验证信息也有限。

## 最接近的相关工作

最接近 CAPO、prefix-tree RL、EPIG-Tree、Belief-Shift Branching、DDO 和 REVERSAL-BENCH。相较单纯熵或梯度信息价值，WEIR显式结合剩余成功空间与价值斜率。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：用 distributional verifier 估计每个前缀的成功分布和 A/B/T 熵，再以环境回放估计局部 value cliff；只有两者同时高时生成反事实分支。定期用硬真值重估 critic，限制旧 verifier 分数在新策略上的权重。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：按 watershed 权重分配 teacher 查询和 score 蒸馏预算。
- **A/B/T 与序数分布**：分支选择应使用完整分布熵与相邻分支的序数间隔。
- **真值门控**：旧节点回报按策略版本衰减；环境终局与不可逆事件优先。
- **critique states**：只在高价值悬崖节点生成 critique，减少对 routine step 的噪声监督。
- **高熵探索**：从“所有高熵都分叉”改为“高熵 × 生存空间 × 价值陡峭度”。
- **sealed eval**：用冻结 critic/环境集复测分叉排序，避免在线 critic 与 policy 共适应后自证有效。