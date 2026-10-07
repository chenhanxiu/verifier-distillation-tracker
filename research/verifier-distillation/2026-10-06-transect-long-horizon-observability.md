# Transect: Retaining Observability for Long-Horizon LLM Agent Evaluations

- 作者：Toby D. Pilditch、Konstantinos Voudouris、Alexandra Abbas、Cozmin Ududec
- 首次公开日期：2026-10-06
- 版本日期：2026-10-06（v1）
- 原始论文：https://arxiv.org/abs/2610.08364
- Canonical URL：https://arxiv.org/abs/2610.08364
- 代码：https://github.com/AI-Safety-Institute/transect

## 一句话结论

【论文原文】Transect 把长达数百万 token 的 Agent 运行重建为可追溯时间线，并将 judge 标签、事件、token 与子 Agent 活动绑定到原始回合，以降低长轨迹分析的自由度并提高可审计性。

## 真正新增的内容

【论文原文】它不是再加一个总体分数，而是提供可复用 evaluation-family 配置，将任务语境和行为词表与 judge/分析设置分离；每个标签可回溯到源回合，底层表格可导出做跨运行分析。

## 核心方法

【论文原文】基于 Inspect Scout 对事件、token 使用、子 Agent 活动和模型生成行为标签做统一 turn-based 对齐，生成可导航报告；配置固定行为本体，judge 与扫描器独立插拔。

## 关键实验结果

【论文原文】示例分析一个接近 1300 万 token 的 AI R&D 评测，识别出以运营和稿件生产为主、持续假设生成证据不足的行为阶段。论文展示的是工作流可用性与个案诊断，不是 verifier 准确率提升。

## 证据质量与局限

【论文原文】开源实现、原始回合追溯和数据导出增强复现性。【分析推断】当前主要证据是单一大型示例；行为标签仍受 judge 和本体设计影响，不能把可观察性等同于真值或因果归因。

## 最接近的相关工作

【分析推断】接近 AutoTuneBench 的证据账本、Terminal-Universe 的可重放轨迹、Harness or Model? 的测量隔离；区别是专注超长 transcript 的人工—模型联合审计界面。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 verifier 输出改成“标签+证据回合+配置版本+模型快照”，并将 critique、阶段划分和异常检测都绑定原始事件；这可形成 generative verifier 的证据层，而非不可追溯的自由文本。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：每个 score 保存来源回合和配置 hash，便于定位错误监督。
- 【分析推断】A/B/T：T 可表示轨迹证据不足，并链接缺失区段。
- 【分析推断】真值门控：把工具日志/环境事件与 judge 标签并排显示，真值优先。
- 【分析推断】critique states：只接纳带源回合指针的 critique。
- 【分析推断】高熵分叉：时间线保留多 Agent 分支和资源消耗，避免只审最终胜者。
- 【分析推断】sealed eval：冻结词表、扫描器和 judge 快照，导出只读证据表供独立复核。