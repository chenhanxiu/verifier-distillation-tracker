# Not Every Rollout Needs Distillation: Correctness-Filtered On-Policy Self-Distillation

- **作者**：Harrison Zhao、Lei Huang、Fei Liu、Wen Shi、Zijian Jin
- **首次公开日期**：2026-10-19
- **版本日期**：2026-10-19（v1）
- **原始论文**：https://arxiv.org/abs/2610.25842
- **arXiv ID**：2610.25842
- **DOI**：https://doi.org/10.48550/arXiv.2610.25842
- **代码/项目**：未公开

## 一句话结论

C-OPSD 只蒸馏被验证为错误的 rollout，就能保持普通 OPSD 效果，同时显著减少无用 teacher 计算。

## 真正新增的内容

论文发现错误响应约贡献三倍的相干梯度份额，而总体平均更新方向高度重合，因此可把正确 rollout 视为低边际价值。

## 核心方法

先用可验证正确性筛选 student on-policy rollout，仅对错误子集运行 privileged/self-teacher 蒸馏；正确样本不执行昂贵 teacher 通道。

## 关键实验结果

在 Qwen 1.7B、4B、8B 与 AIME/HMMT 上达到与完整 OPSD 相当的准确率；执行训练行数减少 68%，训练时间约降低 40%。

## 证据质量与局限

多尺度模型和两个数学 benchmark 支持计算结论；但依赖廉价可靠的 correctness oracle，开放式 Agent 任务中误判会漏掉校准与风格学习信号。

## 最接近的相关工作

与 TV-Regulated OPD、IWD、RoboDrop、SIGNBALANCE 和错误驱动课程学习最接近。

## 如何复用或推进 LLM-as-a-Verifier

把程序/环境真值作为第一层过滤器：明确失败才触发完整 teacher distribution 或 critique；正确但 verifier 高熵的样本保留少量校准蒸馏，不宜一刀切丢弃。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】现有路线可用“失败全蒸馏、成功冲突保护、T/高熵轻蒸馏”的三段门控，直接形成 score-level OPD 基线，并在 sealed eval 中验证省算是否损害 OOD calibration。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
