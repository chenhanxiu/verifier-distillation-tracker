# Robust Conformal Consensus: Multi-Agent LLM-as-a-Judge Interval Evaluation with Conformal Prediction

## 基本信息

- **作者**：Lihui Liu
- **首次公开日期**：2026-09-06
- **版本日期**：2026-09-06（v1）
- **原始论文**：[arXiv:2609.06367](https://arxiv.org/abs/2609.06367)
- **代码**：未发现公开代码链接

## 一句话结论

该工作将多个 LLM Judge 的序数评分先各自 conformalize，再加权聚合并二次校准为有覆盖保证的区间，为 distributional verifier 提供了“分数+不确定区间”接口。

## 真正新增的内容

**论文原文结论：** Robust Conformal Consensus（RCC）为每个 judge 构造预测区间，按历史 concordance 聚合区间，再用独立 meta-calibration 集修正最终边界；在 exchangeability 假设下给出边际覆盖保证，并显式反映 judge 间差异。

**分析推断：** 对 Agent verifier × OPD，区间比单点平均更适合映射 A/B/T：两个动作区间明显分离才给 A/B，重叠则保留 T 与探索；区间宽度可控制 teacher 调用与蒸馏强度。

## 核心方法

数据分为 40% judge-level calibration、10% 独立 meta-calibration、50% test。GPT-4o mini、DeepSeek-R1-Distill-Qwen-32B、Qwen2.5-72B-Instruct 分别通过多种 conformal regression/ordinal 方法生成区间；按预计算一致性权重聚合，再以 meta-nonconformity quantile 扩张区间恢复覆盖保证。

## 关键实验结果

在 SummEval、DialSumm 与 ROSCOE（CosmosQA、DROP、e-SNLI、GSM8K）上，30 个随机划分重复。目标约 90% 覆盖时，多 judge CQR 在示例八个维度/任务上报告 91.1%–96.7% 覆盖；论文比较 CQR、Asym-CQR、CHR、LVD、boosted 方法、R2CCP 以及 Ordinal APS/Risk Control，并报告区间宽度—覆盖权衡。

## 证据质量与局限

**证据质量：中低。** 有明确数据拆分、理论条件、30 次重复和多 conformal 基线，但只校准静态 Likert 评分，未验证训练闭环或 Agent 轨迹；覆盖保证是 exchangeability 下的边际保证，不保证分布漂移、高风险子群或逐状态条件覆盖。依赖能暴露 token logits 的 judge，且 calibration 成本不低。论文“局限”段出现与知识图谱相关、和正文方法不一致的文字，降低文稿可信度；无公开代码，尚待独立复现。

## 最接近的相关工作

最接近单 judge conformal prediction、multi-judge panel/consensus、ordinal APS、ordinal risk control 与 selective prediction。区别是对多个 judge 的区间做加权共识并用第二层校准集恢复形式覆盖。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 输出 ordinal score distribution，再对其构造校准区间；把区间宽度、跨 judge overlap 和 coverage residual 作为独立信号。生成式 critique 可与区间绑定：只有区间窄且硬真值一致的 critique 才进入可复用状态。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析建议：**

1. A/B/T 规则改为区间判定：置信区间分离为 A/B，重叠为 T；保留完整 ordinal posterior。
2. score-level OPD 的幅度按区间宽度衰减，程序化/环境真值仍拥有不可覆盖的方向否决权。
3. 高熵分叉优先保留并触发额外 rollout/judge，而非用平均分强制收敛。
4. calibration、meta-calibration、训练和 sealed eval 四套数据严格隔离；按轨迹长度、任务族和错误类型审计 conditional coverage。
5. 首轮仅作为低风险研究基线，需先复现并修正文稿一致性问题，再进入训练闭环。