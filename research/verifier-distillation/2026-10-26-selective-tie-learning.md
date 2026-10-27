# Selective Tie Learning：用高影响平局削弱偏好模型伪相关

## 基本信息

- **论文标题**：Selective Tie Learning: Mitigating Spurious Correlations in Preference Optimization
- **作者**：Christian Moya, Purav Matlia, Elliott Thornley, Guang Lin
- **首次公开日期**：2026-10-26
- **版本日期**：2026-10-26（v1）
- **论文链接**：https://arxiv.org/abs/2610.35787
- **代码链接**：未发现公开代码

## 一句话结论

不是所有 T（tie）标签都同样有价值；优先加入预计最能削弱伪特征依赖的 tie，可用更少样本纠正偏好优化。

## 真正新增的内容

**论文原文结论**：对 log-linear policy 推导每个 tie 对伪相关依赖的影响，并证明在等大小子集中选择最大预测下降是一阶最优；再用隐式 reward margin 和反事实 proxy 近似难以获得的伪特征与曲率信息。

**分析推断**：现有 A/B/T 方案不应把 T 当作“Judge 不确定时的废标签”。精心选择的 T 是主动约束，可明确告诉 verifier/student 某些表面差异不应改变偏好。

## 核心方法

- 推导 tie 对 spurious reliance 的 influence。
- 使用目标曲率；在语言模型中以 generalized Gauss–Newton 近似。
- 当真实伪特征未知时，用反事实扰动测量伪依赖，并研究 implicit reward margin 何时是可用 proxy。
- 比较 influence-based、margin proxy 与均匀 tie 采样。

## 关键实验结果

**论文报告**：在 log-linear policy、神经网络和 LLM 上，选择规则都能以少于均匀采样的 tie 数量达到相近的伪相关下降。摘要未提供统一绝对提升值。

## 证据质量与局限

理论与跨模型实验相互支撑。局限是需要可构造的反事实 proxy，且论文主要研究 preference optimization，不是长轨迹 Agent；对非传递偏好与多维 rubric 的效果仍未知。

## 最接近的相关工作

distributional preference modeling、B-CARE、SCUR、Robust Conformal Consensus，以及语义保持扰动下的 IWD。本文首次把“选哪条 tie”与减少伪依赖直接联系起来。

## 如何复用或推进 LLM-as-a-Verifier

构造语义等价但改变长度、格式、工具名、措辞或呈现顺序的轨迹对，将它们标成 T；优先选择会最大幅度改变 Judge 当前预测、但环境真值相同的 pair。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：tie 对不应产生方向梯度，可作为零差异/方差收缩约束。
- **A/B/T**：从被动 abstention 升级为主动去偏数据。
- **硬真值门控**：只有环境结果等价时才能制造 T。
- **critique states**：对表述不同但修复效果相同的 critique 加 tie 约束。
- **高熵探索**：T 不等于删除两个分支，而是保留其策略多样性。
- **sealed eval**：隐藏一组新的等价变形，检测伪特征是否真正下降。