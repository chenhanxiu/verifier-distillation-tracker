# PromptOps: Iterative Prompt Optimization for LLM-as-a-Judge Systems

- **作者**：Sven Kleinkop, Tamás Janusko, Ricardo Bochnia, Gunnar Hempel, Steffen Tomschke, Jürgen Anke, Maik Thiele
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.07123
- **DOI**：https://doi.org/10.48550/arXiv.2611.07123
- **代码**：论文页面未给出公开代码链接

## 一句话结论

PromptOps 将 Judge 维护拆成何时优化、用什么算法、选哪些反馈、怎样更新 prompt 四个独立决策，并证明受控分布漂移后可恢复，但不存在跨场景通用的最佳更新时间或算法。

## 真正新增的内容

它把一次性静态 prompt optimization 改造成部署期闭环运维问题，并统一比较 GEPA、SIMBA、Rubric Synthesis 及两类 exemplar selection。

## 核心方法

监测交互与分数分布漂移，按策略选择反馈记录和优化器，更新 Judge prompt；在 reference-score distribution 的受控 shift 下反复校准。

## 关键实验结果

迭代优化能够恢复漂移后的 Judge 性能；但算法选择和更新时机均依赖场景，没有一种设置普遍占优。

## 证据质量与局限

受控漂移与多优化器对照适合研究运维决策；但论文没有证明 prompt 自适应后仍对真实任务构念有效，且若训练 policy 同时看到更新后的 Judge，可能形成更强共适应。

## 最接近的相关工作

最接近 GLARE、Coupled Calibration and Learning、continuous benchmark validation、MAWILE 与 Judge prompt sensitivity。

## 如何复用或推进 LLM-as-a-Verifier

将 teacher prompt、反馈窗口、校准集和更新规则全部版本化；更新只用隔离的人类/程序真值反馈，并保留旧版本做 shadow replay。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. 动态 Judge 可服务训练，但不能同时充当 sealed evaluator。
2. A/B/T 分布需保留 judge-version 维度，监测排序翻转。
3. critique memory 必须记录生成它的 Judge 版本。
4. 漂移期提高 T 和探索比例，避免错误校准快速收缩策略。
5. sealed eval 使用冻结独立 Judge；PromptOps 更新只能通过盲 holdout 晋级。