# RSI-Anything: Unlocking Recursive Self-Improvement with World Models

- **作者**：Taoyong Cui；Pinxian Zeng；Wanghan Xu；Hao Xiao；Shuhan Xue；Qiang Gao；Wanli Ouyang；Pheng Ann Heng；Zhenfei Yin；Yingcheng Wu；Ling Yang
- **首次公开日期**：2026-10-09
- **版本日期**：2026-10-09（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.13912
- **Canonical URL**：https://arxiv.org/abs/2610.13912
- **代码**：未发现公开代码链接

## 一句话结论

RSI-Anything 用预测世界模型选择动作和学习数据，并通过真实反馈更新策略/工作流，再以组件与兼容性检查决定是否保留新的 policy–model pair，为“预测 verifier 辅助探索、真实环境决定提交”提供了跨领域闭环。

## 真正新增的内容

【论文原文】框架基于 JEPA-Anything，用 world model 预测指导 action selection 和 learning-data selection；观察到的外部反馈用于改进 policy/workflow，并在必要时适配 world model；更新后的 policy 与 world model 必须通过 component 和 compatibility checks 才能被保留。

【分析推断】这比单独维护 reward model 更接近长期 Agent 运维：verifier 不只评分单条轨迹，还要检查新策略、新世界模型和已有组件是否继续兼容，并支持成对版本回滚。

## 核心方法

1. 用预测 world model 估计候选动作/工作流的未来结果。
2. 按预测效用选择行动与需要纳入学习的数据。
3. 使用真实观察反馈更新 policy 或 workflow，并条件式更新 world model。
4. 对更新组件做单项检查与 policy–world-model 兼容性检查。
5. 只保留通过验证的组合，形成跨版本递归改进。

## 关键实验结果

【论文原文】代码修复中，在 coder 固定时，静态 verifier 成功率为 26.3%，预测选择提高到 29.2%，world-model adaptation 后达到 31.2%，测试用量相近。GUI 任务完成率提高且平均动作减少 39.4%；五个连续版本的实验室规划分数从 21.80% 提升到 46.01%；反应优化在同样 40 次实验预算下取得 96.15% mean best observed yield，Bayesian optimization 为 82.16%。

## 证据质量与局限

【论文原文】覆盖代码、GUI、实验室规划、化学反应与免疫科学，显示跨域适用性。  
【局限】系统组件多，难以把收益单独归因到 world model、数据选择或兼容性检查；world-model adaptation 与 policy 同步演化会增加共适应风险。不同领域指标不可直接横向比较，且真实科学发现的长期有效性仍需外部验证。

## 最接近的相关工作

与 DreamTrue、HaWMPO、FARM、RoboRSI、RSIAgent、Proof-Carrying Cognition、DENSE 和 Co-Evolving Inspectable Graders 最接近。其独特之处是把 predictive selection、反馈适配与 policy–model pair 的保留检查统一到递归改进闭环。

## 如何复用或推进 LLM-as-a-Verifier

为自动评测 Agent 建立版本化“policy–verifier–environment model”三元组：预测模型只负责候选排序，真实接口/实机结果负责结算；任何 Judge、rubric 或 world model 更新都要在固定 back case、兼容性集和 sealed set 上通过后才发布。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：用 world-model 预测选择高价值 rollout，但蒸馏方向由真实反馈确认；预测误差决定软权重。
- **A/B/T 与序数分布**：多种预测未来形成序数分布；模型版本不兼容或预测区间过宽时输出 T。
- **程序化/环境真值门控**：保留新 policy–model pair 前必须经代码测试、GUI 状态 diff 或真实实验结果硬门控。
- **student-generated critique states**：critique 与生成它的 world-model 版本绑定；只有在当前 policy 上复现改善才入库。
- **高熵分叉**：用预测不确定性与潜在价值共同分配真实试验预算，保留高价值未知分支。
- **sealed eval**：冻结独立任务、旧版本回归集和环境快照；每次联合更新都必须同时报告预测校准、真实成功和兼容性退化。

总体判断：【分析推断】这篇工作可作为现有 Agent verifier × OPD 的系统级蓝图，但需要更强的独立 sealed eval 才能证明递归提升不是 policy 与 world model 的互相迎合。