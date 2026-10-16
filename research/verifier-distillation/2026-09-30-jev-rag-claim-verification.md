# Jev-as-a-Judge：非生成式 Verifier 的置信路由审计

- **论文标题**：Jev-as-a-Judge for RAG Claim Verification: Confidence-Gated Cascading Between a Non-Generative Verifier and a Frontier LLM
- **作者**：Alden Do Rosario, Kirollos Atef
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.20634
- **代码与数据**：https://github.com/adorosario/jev-rag-claim-verification

## 一句话结论

便宜 verifier 与 frontier Judge 的总体 balanced accuracy 可以近似相同，却在不支持声明的放行率上差异巨大；置信度 cascade 的收益甚至被等预算随机升级复现，说明“会校准”不等于“会路由”。

## 真正新增的内容

**论文原文**：在同一 495 条人工标注 claim 上做严格 paired comparison，并同时报告成本、系统间分歧、false-verification 与 cascade 对照；加入相同升级比例的随机路由，发现置信阈值本身没有带来可辨别收益。

**分析推断**：distributional verifier 的置信度必须通过 selective-risk / routing lift 验收，不能因 ECE 或总体准确率好看就直接用于 OPD 权重。

## 核心方法

比较返回枚举值与原生概率的 Jev 和 frontier LLM；在折外阈值下让 Jev 处理高置信样本、其余升级，并与等成本随机升级比较。

## 关键实验结果

**论文原文**：Jev 与 Astra 的 paired balanced-accuracy 差为 -0.56 点，成本相差 187 倍；两者在 15.2% 样本上分歧。Jev 对人工标为 unsupported 的 claim 放行率为 23.2%，Astra 为 14.1%。cascade 达 74.10、每千条 2.92 美元，对比 Astra 73.83、8.93 美元；但等预算随机升级同样有效。从 Jev 起点看，cascade 花费高 61 倍仅换 0.83 点，95% CI [-3.36, 4.86]。

## 证据质量与局限

亮点是 paired 样本、置信区间、随机路由控制、公开原始预测和固定快照；局限是仅 495 条、dev split、一个 frontier 模型，部分阈值分析为样本内。RAG claim 与长轨迹 action verification 仍有分布差距。

## 最接近的相关工作

与 Calibration Is Not Verification、Robust Conformal Consensus、JEV-as-a-Judge selective routing，以及多 Judge 有效规模审计最接近。

## 如何复用或推进 LLM-as-a-Verifier

在蒸馏前同时测总体准确率、unsupported acceptance、selective risk、coverage 与 routing lift；只有相对随机路由有显著增益的置信度才能控制 teacher 调用或 OPD 强度。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：置信权重必须通过随机路由对照；否则只用作成本预算，不用作正确性代理。
- **A/B/T 与序数分布**：高置信 unsupported 放行应单列为灾难性校准错误；T 阈值按风险而非总体准确率设定。
- **真值门控**：关键 claim/动作仍由环境或程序 oracle 结算。
- **critique states**：便宜 judge 的输出只有在证据可追溯且风险阈值通过后才能写回。
- **高熵探索**：分歧样本保留并升级，不把 cheap verifier 的高置信当成剪枝充分条件。
- **sealed eval**：锁定模型、prompt、价格与数据修订；用随机升级和独立隐藏集防止路由器—evaluator 共适应。
