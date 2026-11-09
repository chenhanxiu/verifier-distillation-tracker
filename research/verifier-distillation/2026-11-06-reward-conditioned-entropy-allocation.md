# Not All Entropy Is Equal: Reward-Conditioned Entropy Allocation in Reinforcement Learning with Verifiable Rewards

## 基本信息

- **作者**：Song Yu；Li Li；Zhenming Wu
- **首次公开日期**：2026-11-06
- **版本日期**：2026-11-06（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.09448
- **DOI**：https://doi.org/10.48550/arXiv.2611.09448
- **代码**：论文列表称有代码链接，但截至记录时未能从 arXiv 元数据解析出稳定独立仓库 URL

## 一句话结论

RLVR 中“总熵高低”不足以判断探索是否健康；应按 verifier 成败、过程有效性与正确解模式分账，才能区分应压缩的错误尾部与应保留的正确策略多样性。

## 真正新增的内容

**论文原文结论**：RCEA 将轨迹熵、平均 token 熵、verifier outcome、过程有效性和正确解模式覆盖统一进分层诊断，并用局部协方差近似连接到更新方向。

**分析推断**：它不是新的 verifier 或蒸馏算法，但直接给出现有“高熵分叉保留探索”路线更精确的验收指标：保留什么熵比保留多少熵更重要。

## 核心方法

1. 分离完整轨迹熵与平均 token 熵。
2. 按 verifier 成功/失败及过程有效性分层统计。
3. 独立审计正确解模式的覆盖/收缩。
4. 用 chosen-token 协方差近似预测相邻 checkpoint 的熵变化方向。

## 关键实验结果

**论文报告**：

- 六种 RLVR 目标、两个模型尺度下，总体熵轨迹不能稳定排序推理准确率。
- 失败轨迹 token 熵普遍高于成功轨迹；共同题目配对分析的 12 个展示端点中，10 个置信区间排除相等。
- 局部协方差近似对非失败转移的相邻 checkpoint 熵变方向预测准确率为 95.5%。
- 所有可报告终点都出现某种正确解模式宽度收缩；其与大 k 覆盖的正相关仍属探索性结论。

## 证据质量与局限

- 多目标、多尺度、配对分析和置信区间使诊断证据较扎实。
- 只有 8 页；任务与模型覆盖仍有限。
- 正确模式宽度与大 k 覆盖之间不是因果证据。
- verifier outcome 本身可能有误，论文没有解决 verifier 偏差或共适应。

## 最接近的相关工作

与 entropy regularization、RLVR 熵坍缩分析、EPIG/高信息分叉、以及按 reward 分层的信用分配最接近。区别在于 RCEA 把“正确模式多样性”与失败轨迹噪声显式拆开，而非只报告全局 token entropy。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 除总分外输出过程有效性、终局正确性和策略模式标签；对各条件分别估计熵与校准误差。若模式标签来自 LLM，需用程序/环境证据抽样复核，防止 verifier 把表面表达差异误当策略多样性。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：按 verifier outcome 与过程有效性对 KL/score loss 分桶，避免失败尾部的大熵主导更新。
- **A/B/T 与序数分布**：T/不确定状态的熵要与“多种正确策略”分离报告。
- **真值门控**：只有通过环境/程序 oracle 的轨迹才能计入正确模式宽度。
- **critique states**：衡量 critique 是否增加可执行正确模式，而非只降低 token entropy。
- **高熵分叉**：优先保留“通过真值门控且模式不同”的分支；高熵但 verifier-failed 的尾部可压缩。
- **sealed eval**：正确模式覆盖必须由独立冻结分类器或规则审计，不能复用训练 verifier。