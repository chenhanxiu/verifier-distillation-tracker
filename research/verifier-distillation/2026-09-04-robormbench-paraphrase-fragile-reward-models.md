# Same Trajectory, Contradictory Rewards（RoboRMBench）：Paraphrase Fragility in Vision Language Reward Models

- **作者**：Wonje Jeung、Sangyeon Yoon、Hyesoo Hong、Yoonjun Cho、Dongjae Jeon、Bumjun Kim、Jean Oh、Youngjae Yu、Albert No
- **首次公开日期**：2026-09-04
- **当前版本日期**：2026-09-04（v1）
- **原始论文**：[arXiv:2609.05401](https://arxiv.org/abs/2609.05401)
- **DOI**：[10.48550/arXiv.2609.05401](https://doi.org/10.48550/arXiv.2609.05401)
- **代码/数据**：截至本次记录未发现公开仓库链接

## 一句话结论

RoboRMBench 证明同一机器人轨迹仅因等义目标改写就会获得相互矛盾的奖励，并给出用等义方差正则显著稳定 reward model 的直接训练方案。

## 真正新增的内容

**论文原文结论**：构建含 2,390 条真实机器人轨迹、真实进度标签和 21,673 条验证过的改写指令的基准，覆盖词汇替换、句法重组和行动—目标视角变换；大多数通用 VLM 的奖励不具备等义不变性。

**分析推断**：对 distributional verifier，改写间的 reward 方差不是噪声应被隐藏，而是可测的 epistemic uncertainty；它应进入门控、A/B/T tie/abstain 和 sealed eval。

## 核心方法

- 固定轨迹，只改变语义等价的目标描述；
- 用 SCR、failure flip rate 和误差衡量奖励稳定性；
- 比较闭源/开源通用 VLM 与轨迹监督的专用 reward model；
- 训练时在预测损失上加入同一轨迹不同改写的奖励方差惩罚。

## 关键实验结果

**论文报告**：

- 更强的 action-goal perspective shift 下，部分模型对超过一半轨迹发生 failure/success 翻转。
- GPT-5.1 的 SCR 从词汇改写 0.153 升到句法改写 0.204，再到视角改写 0.300；扩大模型规模或显式推理并未稳定解决问题。
- Qwen3-VL-4B 加方差正则后，SCR 在 LS/SR/AGPS 上由 0.076/0.168/0.200 降至 0.042/0.048/0.057；对应误差也从约 1.0 降至 0.239/0.319/0.372。
- 专用 RoboReward 模型总体明显更稳定。

## 证据质量与局限

**证据质量：高（针对终局视觉奖励的等义鲁棒性）。** 真实机器人轨迹、规模化验证改写、真实进度标签、多模型比较及训练干预构成完整证据链。

**论文局限**：仅英文；主要评估 episode-end reward，未覆盖 step-level shaping、成对比较或长时程信用分配。等义过滤依赖 LLM ensemble，仍可能有残余误差。

## 最接近的相关工作

最接近机器人轨迹 reward model、FailBench、PRM-as-a-Judge 1.5，以及 Judge 的排名反转/行为正确性校准。其独特贡献是把“同轨迹、等义指令、奖励应不变”做成可训练的 metamorphic invariant。

## 如何复用或推进 LLM-as-a-Verifier

- 对每条 Agent 轨迹生成多种等义任务表述，蒸馏完整 ordinal score distribution，并最小化跨改写 Wasserstein/JS 方差。
- 把改写方差作为置信度；方差高时输出 T/abstain，而非用均值伪装确定性。
- 环境进度、最终状态和副作用检查决定监督方向；LLM reward 只补充不可程序化维度。
- critique state 也做语义等价变换，检查 verifier 是否因措辞而改变因果归因。

## 对 Agent verifier × OPD 实验路线的具体影响

1. 将 paraphrase invariance 纳入 score-level OPD 的必做消融：无正则、均值聚合、分布方差正则。
2. A/B/T 训练同时随机改写任务描述；若 pair 排序随改写翻转，则标为 T/不确定并隔离。
3. 高熵分叉不能因单一 prompt 奖励低而被剪掉，需经多改写一致性或真实 rollout 复核。
4. sealed eval 保留未见改写策略、不同语言和隐藏同轨迹配对，专门检测 evaluator 共适应。