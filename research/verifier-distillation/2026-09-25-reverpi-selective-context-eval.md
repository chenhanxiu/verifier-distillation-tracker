# Completed Pairs Hide Capped Failures: A ReVerPi Case Study of Selective Context Projection

- **作者**：Guangzhe Zhang
- **首次公开日期**：2026-09-25
- **版本日期**：2026-09-25（v1）
- **原始论文**：https://arxiv.org/abs/2609.31381
- **代码与复现材料**：https://github.com/timwhitez/ReVer_Pi

## 一句话结论

【论文原文】只比较“两个实验臂都完成”的 Agent 轨迹会隐藏被预算上限截断的失败；干预评测必须保留每个分配边界并独立执行两臂，同时报告完成率、交互次数和 token 成本。

## 真正新增的内容

【论文原文】该案例把 selective context projection 的表面平局拆解为停止规则、已知有界失败、未执行配对臂和资源聚合问题，并用恢复 27 个边界运行给出 projected-minus-full 成功率的区间，而非只分析 15 个完成配对。

## 核心方法

1. 对 full-context 与 projected-context continuation 做匹配分配。
2. 审计 runner 在第一臂未完成时抑制 companion arm 的机制。
3. 恢复所有 intervention boundary，将未观测配对结果作为界限而非删除。
4. 分离 selector fitting 与 evaluation，并联合报告成功、请求数、逻辑 token 与截断。

## 关键实验结果

【论文原文】86 次运行、641 次请求中，15 个完成配对两臂均为 12/15 成功；另有 12 个边界运行被停止规则截断。恢复 27 个边界后，projected-minus-full 成功差界于 -9 到 +1 个任务。11 个共同正确配对中，projection 聚合逻辑 token 降 25%，但中位配对 token 增 29%，suffix 请求从 35 增至 55；拟合集之外还多一次失败并多 8.6% token。

## 证据质量与局限

【论文原文】优点是公开源档案、分析数据与复现脚本，并谨慎限定结论只适用于记录到的 campaign。局限是单一系统、样本小且大量配对结果未实际观测；给出的区间是部分识别，不支持总体非劣或优越性结论。

## 最接近的相关工作

最接近 interface-induced trajectory censoring、Harness or Model、AutoTuneBench 的冻结测量，以及因停止/超时导致的 missing-not-at-random 评测研究。其重点是 Agent 干预实验的配对删失，而非新的 verifier 模型。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】任何 verifier-guided 分叉、critique 注入或 context compression 实验都应先记录分支分配，再独立执行 A/B；若预算阻断，输出 censoring 状态并做界限分析。否则“只在两臂完成时比较”会系统性删除最困难状态。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：对被截断轨迹不伪造低分，应保留 censoring mask 与可识别区间。
- **A/B/T 与序数分布**：未完成配对不是 T；T 表示证据平局，censored 应是独立状态。
- **真值门控**：环境成功、超时和请求上限分别记录，避免把 harness failure 当策略失败。
- **Critique states**：critique 分支与无 critique 对照必须独立执行，不能由首臂失败取消另一臂。
- **探索**：高熵分叉应预算对称，否则选择性完成会夸大某一路由器。
- **Sealed eval**：冻结停止规则、预算与 selector；报告 allocation、completion、interaction 和 token 四类指标。
