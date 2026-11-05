# 排名一致不代表局部编辑一致：论文接收预测器审计

## 基本信息

- **作者**：Shaoliang Yang, Jun Wang
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（v1）
- **原始论文**：https://arxiv.org/abs/2611.06789
- **DOI**：https://doi.org/10.48550/arXiv.2611.06789
- **代码**：未见公开代码链接

## 一句话结论

两个 evaluator 即使在现有论文排名上相近，也几乎不一致于“哪种段落改写会提分”；聚合排序表现不能证明 evaluator 适合作为局部 critique 或 repair selector。

## 真正新增的内容

**论文原文结论**：作者把静态 ranking agreement 与 edit-level intervention agreement 分开测试，并发现后者接近零；低精度计算会掩盖微小 score response，但换 FP32 后结论仍不变。

**分析推断**：这直接挑战用离线 Judge 排名精度来选择 critique teacher。局部修复 supervision 必须在它实际排序的 edits 上验证，并以执行/人工真值结算。

## 核心方法

- 198 篇 ICLR 论文。
- 一个词/文档特征 classifier 与两个同源 3B text-only acceptance predictors。
- 自动筛选保持事实、主张强度和归因不变的段落改写。
- 分别比较原论文 ranking agreement 与“哪些 rewrite 提分”的 edit agreement。
- 预注册低精度分析后，再用 FP32 做明确标注的 post-hoc 检查。

## 关键实验结果

- classifier 与一个 predictor 的原论文排名高度接近、与另一个中度接近。
- 对提高分数的段落改写，classifier 与两 predictor 均无可检测一致性。
- FP32 重算后 edit agreement 仍接近零。
- predictor 每篇从 5 个改写中挑选时，平均 raw score 相对随机选择只高 **不足 2/100**。

## 证据质量与局限

对干预级行为的设计很有价值，且透明报告数值精度问题。局限是仅两个人工开放 predictor、同一模型家族、论文接收这一领域；尚未测试昂贵 frontier evaluator 或真实接收结果。

## 最接近的相关工作

与 evaluator sensitivity、counterfactual pairwise augmentation、Calibrated Answer Repair、LLM-as-an-Improver 和 metamorphic Judge audit 最接近。

## 如何复用或推进 LLM-as-a-Verifier

评估 generative verifier 时加入“局部 repair ranking”测试：同一状态生成事实保持的多种最小修改，检查 verifier 选择是否与环境净收益一致，而非只测整轨迹排序。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：静态 AUROC/排序不是局部蒸馏充分条件。
- **A/B/T/序数分布**：最小编辑 pair 应单独校准；无稳定差异时标 T。
- **程序真值门控**：改写必须保持前置事实和权限，并由环境执行验证。
- **critique states**：critique teacher 需通过 repair-level acceptance test。
- **高熵分叉**：多个近等价 repair 不应因微小分数差被过早淘汰。
- **sealed eval**：保留独立的最小反事实 edits，防止 evaluator 只适配静态 ranking。
