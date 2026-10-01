# Cheap to Draw, Expensive to Trust: Certifying Test-Time Scaling Curves

- **作者**：Sohail, Sarkar, Shakuntala Baichoo
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2609.40190
- **代码**：未发现公开代码链接

## 一句话结论

从 best-of-k 曲线事后选择预算需要同时覆盖所有 k 的置信带；朴素设计在 100 题、64 个预算点、±1/32 精度下需 192,000 个答案。

## 真正新增的内容

【论文原文】作者推导认证整条 verifier test-time scaling 曲线的 minimax 成本，并把不确定性分解为 score tail 校准、题目间差异和题内噪声；自适应 paired audit 无需 pilot。

【分析推断】对“多采样＋verifier 选优”或多 Judge 调用预算，不能在看完曲线后挑最佳 k 再用逐点误差条声称显著。

## 核心方法

构造 simultaneous confidence band；用同题独立配对抽样消除固定 benchmark 的题间方差，并学习近最优的题目级样本分配。

## 关键实验结果

【论文原文】185 个 held-out score pool 上，在 64/1,024 个预算点分别只用最便宜竞争认证审计的 0.74/0.53 倍答案；新 MMLU-Pro 研究用 79,133 个答案认证曲线，与预拟合成本定律预测相差 0.6%。方法同样适用于 pass@k 和多数票。

## 证据质量与局限

理论成本界、合成池和新实验相互支撑；但主要针对答案选择曲线，尚未直接覆盖相关 verifier、非平稳 Agent policy 或交互轨迹。

## 最接近的相关工作

VStress、Certified Selective Automation、多 Judge 有效规模、Black-Box Judge 测量不稳定性。

## 如何复用或推进 LLM-as-a-Verifier

为 best-of-k、panel size 和分叉数建立 simultaneous band；先冻结预算候选集与选择规则，再用同状态 paired rollout 认证。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：选择蒸馏采样预算时报告整条曲线置信带。
- **A/B/T 与序数分布**：预算间差异未越过 simultaneous band 时判 T。
- **硬真值门控**：最终 correctness 由独立环境 oracle 计量。
- **student-generated critique states**：critique 数量的收益同样需认证，防止事后挑 k。
- **高熵分叉**：分叉预算可自适应，但选择规则必须预注册。
- **sealed eval**：其 simultaneous audit 可直接作为 sealed budget-selection 协议。
