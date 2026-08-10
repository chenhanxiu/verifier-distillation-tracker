# The Horizon Gap：长时程 LLM Agent 的规划、记忆、执行、训练与评估

## 基本信息

- **论文标题**：The Horizon Gap: Planning, Memory, Execution, Training, and Evaluation for Long-Horizon LLM Agents
- **作者**：Mingguang Chen、Licheng Wang、Bo Qu
- **首次公开日期**：2026-08-07
- **版本日期**：2026-08-07（arXiv v1）
- **arXiv ID**：2608.06663
- **DOI**：https://doi.org/10.48550/arXiv.2608.06663
- **原始论文**：https://arxiv.org/abs/2608.06663
- **代码/数据**：截至记录时未发现公开代码或结构化语料仓库
- **记录类型**：新综述（2026-08-10 新列表检出）

## 一句话结论

这篇系统综述的关键判断是：轨迹越长，单一终局信号越缺乏诊断力，训练和评估都在转向 step-level 过程信号；但当训练 verifier 与评估器共享“什么算中间进展”的假设时会产生相关测量偏差，这直接支持 Agent verifier × OPD 路线中的独立 sealed eval。

## 真正新增的内容

**论文原文结论：**作者系统收集 2024–2026 年 1,547 篇 arXiv 论文，并以“任务需要多少步”的 long-horizon、“模型可容纳多少 token”的 long-context、“信息跨步骤/会话持久化”的 long-term memory 三者区分为基础，将文献组织为规划、记忆、执行、训练、评估、基础/安全六类及三种 horizon carrying 位置。跨类别共同趋势是从终局 pass/fail 转向过程奖励、credit assignment 与轨迹诊断。

作者明确把“训练过程信号与评估过程信号可能共享偏差”标成**结构类比假设而非已证实发现**：现有语料没有直接证明某个训练器与 benchmark 之间存在这种相关偏差。

**分析推断：**这为 verifier distillation 提供了实验优先级，而非新算法：必须把 student on-policy 轨迹作为共同分析单位，并有意构造假设不相交的训练 teacher 与 sealed evaluator，否则 score-level 蒸馏的提升可能只是 evaluator 共适应。

## 核心方法

- 通过系统 seed harvest、26.8% bleed filter 和定向补充形成 1,547 篇语料。
- 用六阶段任务生命周期分类，并增加 horizon 位于 context 内、单任务跨 context、跨任务持久化的轴。
- 同时纳入方法论文、诊断和批判工作，而非只汇总性能提升方法。
- 综合比较规划、编排、恢复、记忆、过程奖励、credit assignment、benchmark 和安全研究的证据形态。
- 区分文献已有结果、作者跨文献综合和仍待验证的假设。

## 关键结果与观点

**论文报告/综合：**

- outcome-only 信号随 horizon 增长而变得不够 informative，长时程训练转向 PRM 与 credit assignment，评估转向 trajectory-level diagnostics。
- 训练部分文献数量中，作者报告 RL/credit-assignment 与监督粒度重设计的比例约为 **130:37**，说明更多工作选择在固定奖励下分配 credit，而不是重新设计 reward granularity。
- 论文指出执行/编排类研究在 2024–2025 年长期占最大份额（约 **41%–54%**），2026 年起记忆研究份额追平或略超；作者将原因解释明确标为假设。
- 综述认为“model 能力与 harness 补偿如何归因”“长时程可靠性是否存在通用缩放规律”“训练/评估过程信号是否相关偏置”是关键未解问题。
- 轨迹正在成为存储、评分、归因、审计和调试的共同单位。

## 证据质量与局限

- **优点**：语料规模大、分类轴清楚，并主动纳入失败诊断和反例；对事实、综合判断与假设的证据等级区分较谨慎。
- **局限**：它是综述，不提供新的 verifier distillation 算法或对照实验；文献计数反映研究供给，不等价于方法效果或真实难度。
- arXiv 抽样、关键词与补充策略可能遗漏工业报告或造成类别偏差；26.8% bleed filter 虽披露但不能消除筛选主观性。
- correlated measurement bias 是合理风险但尚未被文献中的特定 benchmark–training pair 直接验证。
- 没有对 score-level OPD、ordinal verifier 或 A/B/T 协议做统一实验比较。

## 最接近的相关工作

- AgentPRM、SWE-TRACE、Think-RM、GroundedPRM：将过程奖励推进到 Agent 长轨迹。
- GRPO 与 temporal credit assignment：从稀疏结局中产生局部更新信号。
- 严谨 Agent benchmark、trajectory evaluation 与 harness/model 分离评测。
- 长时程 Agent 的 memory、context compression、recovery 与 self-evolution 综述。
- OPRM、generative verifier 和 reward model calibration：为过程信号提供分布化、可推理的实现方向。

## 如何复用或推进 LLM-as-a-Verifier

将“轨迹为共同单位”落实为分层 verifier：步骤级判断局部合法性，分叉级 A/B/T 判断可恢复性，阶段级序数分布判断进展，终局用环境真值校正。训练 teacher 与 sealed evaluator 应分别采用不同模型、提示、证据通道和假设：例如训练侧以程序测试 + critique，评估侧以隐藏环境结果 + 独立人工抽检；二者只共享任务定义，不共享过程 rubric。

## 对 Agent verifier × OPD 实验路线的具体影响

1. **Score-level on-policy verifier distillation**：支持用 student 真实轨迹上的稠密 score 代替仅终局奖励，但需证明过程分数增加的是预测信息而非共同偏见。
2. **Pairwise A/B/T 与序数评分分布**：长轨迹高方差使强制二选一尤其危险；T 与不确定性应是正式标签，序数 posterior 应随阶段和剩余预算变化。
3. **程序化/环境真值门控**：过程 verifier 必须定期用可执行终局和隐藏状态回锚，防止“看起来有进展”取代真实完成。
4. **Student-generated critique states**：critique 可提供稠密信号，但应测其是否改善后续环境结果，不能仅由同类 LLM 判断其合理。
5. **高熵分叉保留探索**：综述中的 bursty/bimodal degradation 反对简单平滑可靠性假设；在尚未被环境证伪的分叉保留熵与多样路径。
6. **Sealed eval**：这是该综述对现有路线最直接的影响。应把 evaluator independence 视为核心实验变量，而不是实现细节，并专门测 shared-rubric 与 disjoint-rubric 的结果差。

## 建议的最小实验

构造 2×2 实验：训练 verifier 使用“程序真值”或“LLM 过程 rubric”，sealed evaluator 使用与训练同源或假设不相交的信号。四组都在同一 student on-policy 轨迹上做 ordinal score distillation，比较真实环境成功率、过程分数提升、ECE、A/B/T 一致性与两种 evaluator 间的增益差。若只有同源 evaluator 显著提升，即可直接检验论文提出但未证明的 correlated measurement bias。
