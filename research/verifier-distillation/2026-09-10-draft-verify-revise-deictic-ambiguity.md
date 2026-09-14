# Draft-Verify-Revise 流水线中的指示语漂移

## 基本信息

- **论文标题**：Can LLMs in Draft-Verify-Revise Pipelines Resolve Deictic Ambiguity?
- **作者**：Obinna I. Ekekezie
- **首次公开日期**：2026-09-10
- **版本日期**：2026-09-10（v1）
- **原始论文**：https://arxiv.org/abs/2609.12162
- **DOI**：https://doi.org/10.48550/arXiv.2609.12162
- **代码与数据**：https://github.com/oekekezie/deictic-ambiguity-companion

## 一句话结论

【论文原文】Draft→Verifier→Reviser 的上下文级联会让“previous”等指示语在阶段间换指；高推理预算可缓解但不保证，显式写出指称对象更可靠。

## 真正新增的内容

【论文原文】首次把 deictic shift 作为多阶段 LLM 评估流水线的可控失效模式，区分 drafter 是否正确、grader 是否正确及 meta-evaluator 需要多少独立推理，并对错误理由中的表面线索依赖做分析。

## 核心方法

10 个基础样例各生成 3 个条件；固定共享组件，只改变 assistant/grader 对歧义表达的解析和 meta-evaluator 的推理难度。测试 3 家供应商、6 个模型、21 个 reasoning-effort 配置，使用 e-values 做序贯检验；另做移除 grader 错误分类标签的消融。

## 关键实验结果

【论文原文】balanced accuracy 从 0.156 到接近满分。GPT-5.2 从无推理时 0.156 升至最高预算 0.942；Gemini 3 Pro 各预算均高于 0.94，低预算成绩超过 GPT-5.2 xhigh，单次试验成本约为其 5%。错误 meta-evaluator 更常依赖表面提示而非操作性推理。

## 证据质量与局限

【论文原文】报告 12,600 次主实验和 12,600 次消融结果，代码、30 个刺激及固定分析快照公开。主要局限是只有 10 个基础合成样例，任务窄且模型多为闭源快照；外推到真实长轨迹仍需验证。

## 最接近的相关工作

Generative verifier、critique-and-revise、self-refinement、LLM-as-a-Judge 位置/上下文偏差，以及 Interface-Induced Trajectory Censoring。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】让 generative verifier 输出带稳定 ID 的 claim/action span、证据引用和明确 antecedent，reviser 只消费结构化 critique state；将无法解析指称作为 T/INCONCLUSIVE，而非强制 A/B。序数评分分布应单独保存“语义歧义不确定性”。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】student-generated critique states 必须在写入前完成指称解析和环境实体绑定。高熵分叉若来自歧义，不应立即蒸馏成单一路径；可保留多个解释分支，再以程序/环境真值门控。sealed eval 应改写或随机化指示表达，检验 verifier 是否学到操作语义而非表面提示。