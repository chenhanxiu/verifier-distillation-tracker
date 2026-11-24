# When Video Verifier Scores Mislead: Capability Assessment and Verifier Selection

- **作者**：Charles Weng, Zixi Huang
- **首次公开日期**：2026-11-20
- **版本日期**：2026-11-20（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.28287
- **DOI**：https://doi.org/10.48550/arXiv.2611.28287
- **代码**：未见作者在 arXiv 摘要页给出独立代码链接

## 一句话结论

Verifier 的排名会随负例类型和判定接口反转；选择 verifier 时必须让评测错误分布对齐实际 generator 的错误，而不能用单一容易负例上的分数替代部署可靠性。

## 真正新增的内容

**论文原文结论**：构造具有精确真值的 endpoint-matched negatives 与 truth-switch test，将“是否看懂事件”与“是否能组合事件状态”分离，并证明负例类型足以改变 verifier 选择。  
**分析推断**：这为 Agent verifier 的 sealed eval 增加了一个必要维度：不仅任务要隔离，负例生成过程也要模拟当前 student 的 on-policy 失败分布。

## 核心方法

比较直接判定与先推理后判定两种接口；用同一候选在两段视频间交换真值的 truth-switch 设计控制表面特征；再用生成器实际错误分布检验 verifier 的重排收益。

## 关键实验结果

在事件帧已显式提供时，先推理可使 4 个模型中的 3 个从低于 10% 提升到 70–100%；但在自然视频中需要先定位事件时无显著收益，部分条件还下降。按 event-denial 负例选出的 verifier，在“事件保留但细节改变”的负例上低 8.9 点，重排生成器答案时仅恢复约一半准确率。

## 证据质量与局限

精确真值、truth-switch 和自然视频验证使因果解释较强；但领域是视频问答，尚未覆盖文本/工具 Agent 的长轨迹，也未训练蒸馏 student。

## 最接近的相关工作

最接近 MAWILE 的受控扰动审计、Agreement Overstates Evidence 的相关错误分析、AutoTuneBench 的 sealed measurement，以及 Ground-truth-as-code 的可执行真值。

## 如何复用或推进 LLM-as-a-Verifier

为每类 Agent 失败建立保持终点相同但内部状态错误、保持动作类型但细节错误、以及 outcome truth-switch 三类负例；分别报告 direct score、generative rationale score 和对真实 on-policy 错误的 rerank gain。

## 对 Agent verifier × OPD 实验路线的具体影响

训练集中的 A/B/T 负例应按当前 student 失败分布在线更新，不能只用容易拒绝的人工负例。高熵分叉的两个分支要尽量 endpoint-matched，以迫使 verifier 学内部状态差异；sealed eval 固定独立负例生成器，防止 student 与 evaluator 对同一负例模板共适应。