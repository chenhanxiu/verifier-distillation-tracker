# Same Rule, Different Verdicts：Rubric 语言与句法结构会改变 LLM Judge 裁决

## 基本信息

- **作者**：Sangdo Han, Moonsoo Kim
- **首次公开日期**：2026-11-03
- **版本日期**：2026-11-03（v1）
- **原始论文**：https://arxiv.org/abs/2611.04091
- **DOI**：https://doi.org/10.48550/arXiv.2611.04091
- **代码与数据**：论文 ancillary files（arXiv 页面提供）

## 一句话结论

即使规则语义相同，rubric 使用韩文还是英文、采用肯定/否定/条件/例外句式，都会系统性改变 LLM Judge 裁决；等义规则下单模型仍有 11%–15% 的翻转率。

## 真正新增的内容

**论文原文结论**：作者用预先固定的分析计划，分离 rubric 语言与 clause structure 的影响，并显示 paired examples 无法消除语言差距。

**分析推断**：ordinal/pairwise reward 分布若只从一种 rubric 表述采样，会低估 evaluator 的认识不确定性；等义 rubric 扰动可以成为低成本的 teacher reliability test。

## 核心方法

- 为支持对话编写 12 个准则，每个准则有 affirmative、negated、conditional、exception 四种结构。
- 构造两组语义等价句式，并提供韩文与英文版本。
- 7 个模型（3 个 provider 的 6 个低成本模型和 1 个 reference model）评价 60 个翻译 ESConv 对话与 144 个边界案例。
- 共执行 51,744 次请求。

## 关键实验结果

- 韩文 rubric 的跨 provider 一致性低于英文：Cohen's κ **0.687 vs 0.745**，差值 -0.058，95% CI [-0.072, -0.045]。
- 否定、条件、例外条款的分歧 odds ratio 为 **5.6**（相对肯定句）。
- 单模型对语义相同条款的 verdict 翻转率为 **11%–15%**。
- 同 provider 模型并未更一致；paired examples 也未缩小语言差距。

## 证据质量与局限

大规模、多模型、边界案例与预先固定分析增强可信度。关键局限是只测一致性、没有人类真值；材料由 LLM 起草，领域限于韩语支持对话。因此不能把高一致性解释为高正确率。

## 最接近的相关工作

与 Judge prompt sensitivity、rubric robustness、metamorphic evaluator audit、MAWILE 及语义不变性加权蒸馏最接近。

## 如何复用或推进 LLM-as-a-Verifier

对每个准则生成等义多语言/多句式变体，恢复 verdict distribution 而非单点分数。跨变体稳定性可作为蒸馏权重；敏感样本输出高熵 ordinal distribution 或 T。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher score 应对 rubric 变体做 ensemble，并按不变性降权。
- **A/B/T/序数分布**：保留变体间分歧，不用多数票抹平。
- **程序真值门控**：语义等价应由可执行契约或人工审核固定，避免变体本身改变规则。
- **critique states**：critique 必须引用具体 clause，且对否定/例外结构做解析检查。
- **高熵分叉**：rubric 敏感状态不应用强蒸馏压缩。
- **sealed eval**：冻结未见过的 rubric 语言与句式变体，检查 evaluator 是否只适配训练模板。
