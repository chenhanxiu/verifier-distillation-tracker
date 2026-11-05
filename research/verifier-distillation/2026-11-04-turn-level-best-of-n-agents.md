# Turn-Level Best-of-N：长时程 Agent 的逐回合候选选择

## 基本信息

- **作者**：Jalaj Bhandari, Dhawal Gupta, Hongli Zhan, Zhenting Wang, Varad Pimpalkhute, Zhengzhong Liu, Eric Xing, Rupesh Srivastava
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（v1）
- **原始论文**：https://arxiv.org/abs/2611.06868
- **DOI**：https://doi.org/10.48550/arXiv.2611.06868
- **代码**：未见公开代码链接

## 一句话结论

在每个 Agent 回合让 generator 生成 N 个动作、由独立 selector 比较后执行，可在长时程 terminal tasks 上提升 5%–10% 准确率并改善重复尝试的一致性。

## 真正新增的内容

**论文原文结论**：现成开放权重模型无需专门 critic 训练，也能作为逐回合候选 selector；收益不仅体现在终局准确率，还改变调试、测试和遵循指令等轨迹行为。

**分析推断**：逐回合 BoN 是构造同状态 A/B/T 数据的天然在线来源；但 selector 的选择不能直接当真值，必须用执行结果回标并审计位置偏差。

## 核心方法

- 每回合 generator 采样 N 个候选动作。
- selector LLM 直接比较候选并选择一个。
- 选中动作进入环境，下一回合重复。
- 分析终局成功、重复运行一致性与轨迹行为变化。

## 关键实验结果

- 在复杂长时程 terminal tasks 上，准确率提升 **5%–10%**。
- 多次运行的一致性提升。
- 轨迹表现为更少无效尝试、更好指令遵循、调试与测试行为。

## 证据质量与局限

端到端长轨迹环境使证据高度相关，但摘要没有给出具体 benchmark、N 值、selector 成本与失败分布。尚未证明 selector 校准，也没有与程序 oracle 或专用 verifier 做充分隔离。

## 最接近的相关工作

与 best-of-N、guided search、critic routing、EPIG-Tree 和 belief-shift branching 最接近。区别是把选择放在每个真实环境回合，而非只做整条轨迹重排。

## 如何复用或推进 LLM-as-a-Verifier

保存每个状态的 N 个候选、selector 完整概率/理由与执行结算，形成 pairwise A/B/T 数据。用环境结果校准 selector，并蒸馏为低成本 distributional action verifier。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：用执行回报校准 selector score，再蒸馏到 student-generated states。
- **A/B/T/序数分布**：同状态候选直接形成 pair；差异不显著时为 T。
- **程序真值门控**：测试、环境状态变化和 recoverability 决定标签方向。
- **critique states**：将 selector 理由与失败后的反事实重放配对。
- **高熵分叉**：只在高价值/高分歧回合增加 N，避免全程压缩探索。
- **sealed eval**：冻结 selector 外的独立终局 evaluator，并报告成本—成功率曲线。
