# Skill-based Agentic Evaluation for Real-time Data Science Tasks

## 基本信息
- **作者**：Aniruddha Tamhane；Raghavendra Addanki；Ayushi Aggarwal；Aditya Bansal；Rui Wang；Charles Menguy；Swati Jain
- **首次公开日期**：2026-09-15
- **版本日期**：2026-09-15（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.16487
- **代码**：未发现公开代码链接

## 一句话结论
【论文原文】把随实时数据变化的参考答案写成可执行函数，再让格式无关 Judge 比较原子事实，可比自然语言参考提高 29% MCC、减少 16% token；缺少显式真值的自导 Judge 与人工判断反相关。

## 真正新增的内容
【论文原文】论文提出 ground-truth-as-code：每次评测现场从当前数据重新计算答案，避免静态 reference 过期；随后把输出和真值都分解为 factoid，独立计 precision、recall、accuracy，不受 prose、表格或 HTML 等格式影响。

【分析推断】这与用户现有 Mock Tool/环境快照非常契合：参考答案无需固定为唯一工具路径，只需可执行地产生当前应满足事实。

## 核心方法
1. 用可执行 reference function 编码任务真值。
2. 在评测时连接当前/合成数据重新计算结果。
3. 将 Agent 输出和真值拆成原子 claims。
4. 格式无关 Judge 对齐 claims 并计算 precision、recall、accuracy。
5. 在复刻生产 schema/关系的 synthetic database 上做人类—Judge 一致性研究。

## 关键实验结果
【论文原文】相对自然语言 ground truth，MCC 提升 29%，每 case token 消耗降低 16%；没有显式真值的 self-directed baseline 与人工判断反相关。

【证据边界】验证集中于内部机器学习 skill 与合成数据库；摘要未证明对非结构化 GUI、副作用或开放式偏好任务同样有效。

## 证据质量与局限
- 有生产式 schema、人工一致性和自然语言 reference 对照，证据直接。
- executable reference 只覆盖可计算事实，无法单独评价策略质量、安全、澄清和用户体验。
- factoid 分解仍可能漏掉关系约束或把同义事实重复计分。

## 最接近的相关工作
Thinkingbox、ExecRubrics、FACET、ClaimReceipt、Harness-of-Harness、ToolGate 及 AutoSciRub。本文重点在动态数据上的 ground-truth-as-code 与格式无关 factoid Judge。

## 如何复用或推进 LLM-as-a-Verifier
【分析推断】先运行 reference function 得到动态任务卡片和义务集合，再由 LLM verifier 判断 Agent 的每个 claim 是否被当前环境证据支持；将“缺失、错误、多余、不可判”输出为序数分布与证据指针。

## 对 Agent verifier × OPD 实验路线的具体影响
【分析推断】
- score-level OPD：可执行真值决定目标推进方向，LLM Judge 仅做语义对齐。
- A/B/T：不同工具路径只要产生等价 factoid set 即标 Tie，摆脱唯一参考轨迹。
- 环境真值：每次运行绑定数据库/时间/地点快照和 reference 版本。
- critique states：critique 必须引用缺失或冲突 factoid，修复后重新执行 reference。
- 探索：允许多路径，只剪掉违反动态真值或硬约束的分支。
- sealed eval：reference code、数据快照和 Judge 分离版本管理，最终用隐藏函数与新数据验收。