# Beyond Aggregate Scores：Behavioral Correctness Assumptions for Assessing Reference-Based Automatic Evaluation Methods

- **作者**：Maria Mahbub、Ashley Rice、Michael R. Munroe、Amidu Kamara、Amir Sadovnik
- **首次公开日期**：2026-09-04
- **当前版本日期**：2026-09-04（v1）
- **原始论文**：[arXiv:2609.05289](https://arxiv.org/abs/2609.05289)
- **DOI**：[10.48550/arXiv.2609.05289](https://doi.org/10.48550/arXiv.2609.05289)
- **代码/测试集**：截至本次记录未发现公开仓库链接

## 一句话结论

该工作用“应保持评分不变”与“应降低评分”的受控变换审计 evaluator，证明相同 aggregate score 会掩盖完全不同的稳定性—敏感性失效模式。

## 真正新增的内容

**论文原文结论**：提出 behavioral correctness assumptions taxonomy，并将其操作化为 correctness-preserving / correctness-altering 变换，逐层报告 transformation、assumption、stability/sensitivity、重复运行和配置敏感性。

**分析推断**：这是 sealed Agent verifier eval 的测量模板。对 verifier 蒸馏，不能只比较与 teacher 的平均相关性；必须检查 student 是否继承 teacher 的不变性和单调性。

## 核心方法

- 从基准回答构造只改变表面形式的保持正确变换，以及破坏正确性的改变变换；
- 对前者期望分数差约为 0，对后者期望分数下降；
- 同时测稳定性、敏感性、重复运行方差、配置变化和测试集再生成的可复现性；
- 横向比较词汇、字符、语义、LLM 与混合 evaluator。

## 关键实验结果

**论文报告**：

- 没有任何 evaluator 满足全部行为正确性假设。
- Jaro 的稳定性最高 0.937，但敏感性最低 0.028，说明“稳定”不等于能识别真实错误。
- Factual Correctness 的（稳定性，敏感性）为（0.889，0.238），Truthfulness 为（0.895，0.195），总体权衡较好。
- 同类 LLM Judge 也呈现明显不同的行为画像；重新生成测试集后大体结构保持，但效应大小会变。

## 证据质量与局限

**证据质量：中高（作为评估方法论）。** 受控干预、跨 evaluator 对比、重复运行和再生成检验较完整。

**论文局限**：测试回答和变换由 LLM 生成；假设集合不穷尽；实验限于固定文档 QA 与单参考答案；对代码、工具轨迹和开放式多解任务的外推尚未实证。

## 最接近的相关工作

最接近 meta-evaluation、RoboRMBench 的等义不变性、Judge 排名反转校准、遗漏盲区与黑盒 Judge 稳定性审计。它比单一偏差测试更系统，但尚未直接进入训练闭环。

## 如何复用或推进 LLM-as-a-Verifier

- 为 Agent 定义保持正确变换：工具别名、等价参数顺序、无害日志、表述改写；改变正确变换：遗漏前置条件、错误对象、破坏副作用、越权动作。
- 对序数评分分布检查不变性和随机占优，而非只看均值。
- 把违反假设的 pair 作为 A/B/T 蒸馏难例；teacher 自身违规时不得作为硬标签。
- critique state 应通过“等义改写不变、真实错误敏感”的双检验。

## 对 Agent verifier × OPD 实验路线的具体影响

1. sealed eval 新增 metamorphic suite，完全独立于训练 teacher 与在线 prompt。
2. score-level OPD 报告行为假设通过率、稳定性—敏感性前沿和分布校准，不只相关系数。
3. 程序化环境真值为 correctness-altering 变换提供方向；LLM Judge 不能覆盖硬失败。
4. 高熵分叉只在 verifier 对等价变换稳定时用于剪枝，否则进入探索/复核队列。
5. 定期比较 teacher 与 student 的失效画像，检测 evaluator 共适应及偏差蒸馏。