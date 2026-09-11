# OmniHallu: Unified Hallucination Detection for Cross-Modal Comprehension and Generation in Multimodal Large Language Models

- **作者**：Jianjiang Yang、Peihang Li、Shanqing Xu、Mengchen Qian、Lu Zhang、Meng Luo
- **首次公开日期**：2026-09-10
- **当前版本日期**：2026-09-10（v1）
- **原始论文**：https://arxiv.org/abs/2609.11244
- **DOI**：https://doi.org/10.48550/arXiv.2609.11244
- **代码**：截至记录时未发现公开代码
- **状态**：EMNLP 2026 Findings 接收

## 一句话结论

OmniHallu 用偏好优化 student verifier 逼近昂贵的多专家验证边界，并以 66% 专家调用削减展示了跨模态 verifier 蒸馏的可行性。

## 真正新增的内容

**论文原文结论**：构建 10,000 条 claim-level 人工标注的 OmniHallu-Bench，覆盖 I2T、V2T、A2T、T2I、T2V、T2A；再以原子主张分解、模态专家和结构化聚合形成 teacher，训练偏好优化 verifier 近似其决策边界。  
**分析推断**：它可视为“generative verifier panel → 单体 reward/verifier student”的蒸馏模板，尤其适合把长轨迹拆成可验证义务，但并未直接验证 Agent 决策信用分配。

## 核心方法

先将输出拆为 atomic claims，分别交给图像、视频、音频等专家核验，再聚合证据。用多专家判断构造偏好监督，并通过 GRPO 训练单体 verifier，以减少在线专家开销。

## 关键实验结果

多 Agent teacher 在六类任务上相对最强基线的 macro-F1 提升 3.4–8.1 点，10,000 次 bootstrap 检验均报告 p<0.01。移除原子主张分解下降 6.58–7.93 点，移除多专家投票下降 4.47–5.31 点。蒸馏 verifier 减少 66% 专家调用，同时仅有较小性能损失。

## 证据质量与局限

任务和模态覆盖较广，人工 claim 标签与消融增强可信度；但四类错误 taxonomy 压缩了模态特有及复合错误，验证仍以文本化主张为中心。多数投票无法解决共享盲区；视频任务的顺序、遗漏与因果归因仍是主要失败点。尚无长期交互、环境副作用或独立 sealed evaluator 证据。

## 最接近的相关工作

多 Agent Judge panel、claim decomposition、multimodal hallucination detection、preference-trained reward/verifier、SARA 的 rubric 干扰缓解、LLM Judge 遗漏盲区研究。

## 如何复用或推进 LLM-as-a-Verifier

把 Agent 轨迹拆成“已完成义务、未完成义务、环境主张、因果主张”，由专门 verifier 生成带证据判断；再蒸馏到输出序数概率与 critique 的单体模型。共享专家错误应由传感器或环境真值否决。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏多专家软分布，而非只拟合多数票硬标签。
- **A/B/T**：比较同前缀分支的 claim-level 覆盖与矛盾分布；证据重叠时允许 T。
- **真值门控**：工具返回、状态传感器和副作用日志拥有不可覆盖的硬门槛。
- **critique states**：student 先生成 atomic critique，再由专家/环境筛选后回灌。
- **高熵探索**：专家分歧大的模态状态保留分支并升级核验。
- **sealed eval**：冻结人工 claim 集、专家组合和未见模态变换，避免 student 与 teacher panel 共适应。