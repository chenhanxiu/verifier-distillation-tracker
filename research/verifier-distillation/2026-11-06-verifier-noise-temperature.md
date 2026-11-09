# Verifier Noise Is a Temperature: Testing Tilt Predictions in Finite-Budget LLM-Guided Search

## 基本信息

- **作者**：Xiaomeng Li
- **首次公开日期**：2026-11-06
- **版本日期**：2026-11-06（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.09699
- **DOI**：https://doi.org/10.48550/arXiv.2611.09699
- **代码与数据**：论文附录描述了代码和数据校验和；截至记录时论文页未提供可直接解析的独立仓库 URL

## 一句话结论

重复重评分时，verifier 噪声可近似视为控制搜索选择强度的“温度”，但预注册实验表明简单平稳倾斜模型的定量预测并不可靠，缓存 incumbent 分数还会系统性制造分数膨胀。

## 真正新增的内容

**论文原文结论**：在可逆 mutation 与 logistic 分差条件下，keep-if-better 搜索有解析的指数倾斜平稳分布；更一般噪声在小步扩散极限下也得到有效 β。论文随后用预注册实验主动检验并部分否证其定量预测。

**分析推断**：这为 distributional verifier 的重复采样方差提供了操作性参数，但不能把 β 当普适定律；应把它作为可审计的局部近似。

## 核心方法

1. 每次比较都重评分 candidate 与 incumbent。
2. 推导 logistic 噪声下平稳分布与 β；一般对称噪声下 β=4F'(0)。
3. 分析 minibatch 规模使 β 约按平方根增长。
4. 对程序搜索和 prompt 优化预注册预测并实测；比较重评分与缓存 incumbent。

## 关键实验结果

**论文报告**：

- 150 步后，7 个设置中 6 个的性能随 minibatch 增大。
- bin packing 上，编辑父代时只达到预测收益的 62–88%，生成新启发式时达到 109–119%。
- 未选 mutation 的父子质量相关性与“达到预测的比例”负相关；新设置只确认方向，未确认定量值。
- 好程序起步的运行在 300 步内持续掉质量，且由搜索挑中的起点掉得更多。
- frozen-score prompt optimization 中，搜索超过倾斜预测，跨域关系未迁移。

## 证据质量与局限

- 预注册、校准数据先承诺预测、附校验和，证据纪律较强。
- 多个关键预测失败，作者明确保留“平稳倾斜是否成立”的开放结论。
- 理论依赖可逆 mutation、噪声差分形式和小步近似；真实 Agent 分叉通常不满足。
- 研究搜索而非 verifier 蒸馏，没有直接训练 student。

## 最接近的相关工作

接近 noisy comparison、Metropolis/Markov-chain 搜索、Best-of-N、LLM prompt/program optimization 与 score calibration。它将 verifier 方差从“误差条”提升为影响搜索分布的机制变量。

## 如何复用或推进 LLM-as-a-Verifier

对每个状态重复采样 Judge，估计 pairwise 分差分布与局部 β；禁止把缓存 incumbent 分数与新 candidate 分数直接比较。将 β、分差方差和相关性作为 distributional verifier 的输出，供搜索与蒸馏门控。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：蒸馏的不只是均值分数，还应包含噪声尺度；幅度按局部 β 校正。
- **A/B/T 与序数分布**：当分差相对噪声过小，应输出 T；重复评分恢复概率分布。
- **真值门控**：β 只能调软 teacher 幅度，不能改变程序/环境真值方向。
- **critique states**：比较 critique 前后候选时必须成对重评，避免缓存基准引起虚假改进。
- **高熵分叉**：minibatch/重复评审会提高选择强度，可能过早压缩探索，需联合监控模式覆盖。
- **sealed eval**：最终评估冻结评分协议并重新评分所有候选，禁止沿用训练搜索缓存。