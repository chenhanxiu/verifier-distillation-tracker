# From Probabilities to Decisions: Search and Multi-Teacher Distillation with Jev

- 作者：Mohamad Yazan Sadoun、Sarah Sharif、Yaser Mike Banad
- 首次公开日期：2026-10-06
- 版本日期：2026-10-06（v1）
- 原始论文：https://arxiv.org/abs/2610.09188
- Canonical URL：https://arxiv.org/abs/2610.09188
- 代码：未发现论文专属公开代码链接

## 一句话结论

【论文原文】将 Jev 的快速概率判断蒸馏为每个状态都可调用的轻量 evaluator，并与异质 LLM teacher 合并，比增加同一 judge 的重复回答更有效，说明 teacher 多样性比票数更重要。

## 真正新增的内容

【论文原文】同时验证“概率 judge 进入搜索”“judge 蒸馏降成本”“固定预算多 teacher 分配”三件事；在棋局与 passage reranking 中比较 Jev、Qwen 和重复同源标签。

## 核心方法

【论文原文】bullet chess 中把 Jev 评价嵌入 Stockfish 搜索，再蒸馏 pairwise judgment 为紧凑 evaluator；固定标签预算下比较单 teacher、同源重复和 Jev+Qwen 融合。reranking 直接用 Jev 概率训练排序器。

## 关键实验结果

【论文原文】棋类 bot 对其他 bot 超过 2200 Lichess bullet rating；Jev+Qwen 比全预算只用 Qwen 高 9.6 Elo（95% 区间 4.3–14.9），并在新 openings 复现；Jev 是所测模型中 Qwen 最强搭档。同一 judge 第二次回答不能替代异质 teacher。reranking 中 Jev 21 分钟 API 标签达到 Qwen 5.1 GPU 小时标签的质量。

## 证据质量与局限

【论文原文】有新开局复现、置信区间和预算对照。【分析推断】棋类有强 search/tablebase，reranking 状态空间较短；结果不能直接证明 Jev 可独立评价开放式 Agent 轨迹。

## 最接近的相关工作

【分析推断】与 JEV-as-a-Judge、JEV rubric judges、多 Judge 有效规模和 Agreeement Overstates Evidence 最接近；新增 evaluator distillation 与异质 teacher 预算证据。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将慢 generative judge 与快概率 judge 的 pairwise/ordinal 输出蒸馏进轻量 student，按状态调用；面板设计按条件错误互补选择 teacher，而非重复采样同源模型。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：缓存异质 teacher 概率并蒸馏到逐状态 evaluator。
- 【分析推断】A/B/T：保留 Jev 与 LLM 的分歧分布，分歧大时输出 T。
- 【分析推断】真值门控：程序/环境结果仍作为最终方向锚。
- 【分析推断】critique states：概率 judge 负责路由，generative judge 只处理难例并产 critique。
- 【分析推断】高熵分叉：轻量 evaluator 支持每节点评分而不压缩搜索预算。
- 【分析推断】sealed eval：跨模型族、未见状态和独立环境检验蒸馏后相关错误。