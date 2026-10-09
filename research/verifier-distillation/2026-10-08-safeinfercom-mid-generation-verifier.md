# SafeInferCom: Safe Inference-Time Compute via Verifier-Guided Mid-Generation Intervention for Robotic Task Planning

- **作者**：Weizhe Xu；Jialiang Fan；Mengyu Liu；Fanxin Kong
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.11223
- **Canonical URL**：https://arxiv.org/abs/2610.11223
- **代码**：未发现公开代码链接

## 一句话结论

SafeInferCom 在计划尚未生成完时暴露中间计划给 verifier，验证通过则保持原解，发现违规则定向纠正，说明长轨迹 verifier 的价值在于“及时、最小化干预”，而不只是终局打分。

## 真正新增的内容

【论文原文】框架在不破坏长推理模型解码流程的前提下检查中间计划，并给出 verifier-guided intervention：有效计划保持不变，错误计划接受定向修复；还支持多轮迭代 refinement。

【分析推断】它提供 score-level OPD 的控制接口：序数风险分布不仅训练一个分数，还可决定何时暂停、检查、修复和继续生成。

## 核心方法

1. 在长计划生成过程中按检查点暴露中间状态。
2. verifier 判断计划约束与安全性，而不是等待完整输出后再评分。
3. 对合法前缀采取保守承诺，避免无谓改写；对违规前缀生成定向 correction。
4. 重复验证—修复循环，在推理时分配额外算力。

## 关键实验结果

【论文原文】在多个长推理模型与规划域中提高任务成功率，并更快完成错误纠正；迭代 refinement 进一步提高成功率且使用更少 token。验证覆盖 VirtualHome 与真实机械臂。摘要未给出统一绝对数字，故不补造数值。

## 证据质量与局限

【论文原文】同时包含模拟环境和真实机器人验证，比纯文本规划证据更强。  
【局限】真实机器人任务范围通常较窄；verifier 的误报可能打断本可成功的计划，漏报则可能造成物理风险。论文摘要未说明 verifier 是否独立训练、是否存在同源模型偏差及 sealed 安全评测。

## 最接近的相关工作

与 Persistent Teacher Anchoring、STI-OPD、ContrAgent、MAGS、BLINDSPOT、REVERSAL-BENCH 和 LLM-as-an-Improver 最接近。其特点是把 verifier 放在生成中途，并强调不破坏有效前缀。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier 输出设计成“继续 / 修复 / 停止 / 人工复核”的序数动作分布，并附可执行约束证据。将修复前后计划及环境结果组成 A/B/T 数据；蒸馏 student 时学习选择性干预，而非让 student 模仿所有 verifier 文本。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：从静态 reward head 扩展到 intervention policy，比较终局评分与中途门控的收益/成本。
- **A/B/T 与序数分布**：A=允许继续，B=需要定向修复，T=证据不足/人工复核；保留完整概率用于风险阈值。
- **程序化/环境真值门控**：碰撞、权限、时序约束等由形式/环境检查器硬门控，语言 verifier 负责解释和补充。
- **student-generated critique states**：每次干预产生“违规证据—最小修复—执行结果”状态，成功重放后才用于训练。
- **高熵分叉**：高不确定但可恢复的分支可继续小步探索；不可逆高风险动作在执行前必须停下。
- **sealed eval**：用训练外场景、冻结安全规则和真实执行结果评测，同时报告过度干预率与漏检率。

总体判断：【分析推断】SafeInferCom 适合作为“verifier 不只评分、还控制推理时算力与动作提交”的系统基线，尤其适合验证风险分布到干预策略的映射。