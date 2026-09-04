# Spurious Advantage Hidden in GRPO

## 基本信息

- **作者**：Jiamian Wang, Samyadeep Basu, Koustava Goswami, Tong Yu, Zhiqiang Tao
- **首次公开日期**：2026-09-03
- **版本日期**：2026-09-03（v1）
- **原始论文**：https://arxiv.org/abs/2609.04063
- **代码**：作者注明将发布，当前无链接
- **arXiv**：2609.04063
- **DOI**：https://doi.org/10.48550/arXiv.2609.04063

## 一句话结论

GRPO 的组内 reward 统计会给“猜中答案”的 rollout 高优势；SIGNBALANCE 保留 verifier 决定的正负方向，但用与组构成无关的全局幅度并做按类零均值平衡。

## 真正新增的内容

**论文原文结论**：识别 bounded-answer、开放任务中的有界子问题，以及多路径 search agent 三种 spurious advantage 场景，并提出 composition-free 的优势幅度。

**分析推断**：即使 verifier 终局标签完全正确，基于组内分布的权重也可能奖励错误机制。对 verifier × OPD，硬真值适合决定方向，但 teacher/Judge 的置信与组频率不应未经校准地决定幅度。

## 核心方法

- 分析 GRPO 组内 reward 归一化如何把“正确但靠猜测”的 rollout 赋予高 magnitude。
- SIGNBALANCE 保留 verifier reward 的符号。
- 使用全局 scale，使优势幅度不依赖当前 rollout group 的正确/错误组成。
- 通过 stop-gradient 的 per-class rescaling 恢复零均值平衡。

## 关键实验结果

- 在不同规模的数学与 search-agent benchmark 上评测。
- 在开放答案数学上与 GRPO 相当。
- 在 bounded-answer 数学和 search agent 上优于 GRPO。
- 摘要未给出各基准具体数值，代码仍标记为未来发布，因此当前不扩写定量增益。

## 证据质量与局限

- **质量：中。** 问题定义清晰且覆盖 search agent，但公开摘要缺少具体效应量，代码尚未发布。
- “guess-like”机制的识别依赖任务结构，未必能无歧义区分幸运探索与有价值捷径。
- 只修正 advantage magnitude，不解决 verifier 本身的误判或 reward hacking。
- 对长轨迹逐步 credit 和序数 reward distribution 的效果尚未直接验证。

## 最接近的相关工作

与 OPDVR/RG-OPD 的“verifier 定方向、teacher 调幅度”、CrEST 的 verifier-bounded credit、PGPO 的状态势能，以及 RA-OPD 的真值过滤最接近。它补充说明：组归一化本身也是噪声源。

## 如何复用或推进 LLM-as-a-Verifier

- 将程序真值的 sign 与 distributional verifier 的 magnitude 明确分离。
- magnitude 使用跨 batch 的校准量，如置信下界、因果 rollout 差或固定全局尺度。
- 对小答案空间、重复终局和搜索预算大的任务记录“偶然命中概率”，作为优势抑制因子。
- 让 generative verifier解释成功机制，但只有环境证据支持时才提高 magnitude。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：先用环境真值决定更新方向，再用校准后的 teacher 分布控制幅度；禁止直接用组内命中率放大。
- **A/B/T 与序数分布**：A/B 的终局相同但过程证据不足时标 Tie/机制不明，不能仅凭正确答案强排序。
- **真值门控**：真值 gate 解决方向，不自动证明幅度合理。
- **critique states**：critique 应指出可验证的中间证据，帮助区分推理成功与猜中。
- **高熵探索**：偶然命中不应导致策略骤然收缩；保留未命中但过程合理的高熵分支。
- **sealed eval**：按答案空间大小、搜索预算和多路径等价类分层报告，防止 aggregate reward 掩盖机制退化。