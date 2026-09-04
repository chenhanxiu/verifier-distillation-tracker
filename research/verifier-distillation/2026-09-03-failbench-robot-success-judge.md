# FailBench: How Reliable are VLMs at Judging Robot Task Success?

## 基本信息

- **作者**：Zaruhi Navasardyan, Tatul Danielyan, Hrant Davtyan
- **首次公开日期**：2026-09-03
- **版本日期**：2026-09-03（v1）
- **原始论文**：https://arxiv.org/abs/2609.03611
- **代码/数据**：公开页未给出与本文明确绑定的代码链接
- **arXiv**：2609.03611
- **DOI**：https://doi.org/10.48550/arXiv.2609.03611

## 一句话结论

跨 14 个来源的 2,197 次机器人操作中，最佳 VLM verifier 的平均 balanced accuracy 仅 0.77，接触密集装配低于 0.60 且普遍偏向误判成功，说明视觉终局 Judge 不能替代环境/传感器真值。

## 真正新增的内容

**论文原文结论**：FailBench 用多数自然发生的失败和跨来源数据检验 robot success Judge 的域外可靠性，并按所需视觉证据类型定位失败边界。

**分析推断**：这是长时程 embodied Agent 的 sealed verifier 测试集原型。其成功偏置尤其危险：若用于 reward model distillation，会系统性接纳未完成轨迹和虚假恢复。

## 核心方法

- 汇集 14 个公开来源的 2,197 次 manipulation attempts，其中 12 个真实、2 个模拟。
- 75% 失败为自然发生；六个真实来源原本并非 failure-detection 数据集。
- 比较 13 个 VLM detector，并按对象运动可见性、接触/装配证据等因素分组。
- 通过空间定位和裁剪任务相关区域做无需额外训练的输入干预。

## 关键实验结果

- 最佳模型平均 balanced accuracy **0.77**。
- failure-detection 专门微调模型持续落后于通用 VLM 及其自身预训练基线。
- 可直接观察对象运动的任务接近饱和；接触密集装配任务降至近随机，balanced accuracy **<0.60**。
- 模糊证据下普遍偏向预测成功，提高 reasoning effort 未消除该偏置。
- 空间定位并裁剪关键区域使最佳 detector 提升 **2.4 个百分点**。

## 证据质量与局限

- **质量：高（作为评测审计）。** 跨 14 来源、真实失败占主导、13 模型和证据类型分层。
- balanced accuracy 不能完整表达校准、代价不对称和序数失败严重度。
- 终局视觉帧可能天然缺乏接触力、历史动作与隐藏状态；低分不完全等于模型推理弱。
- 论文评估检测器，没有直接展示用这些信号训练 Agent 后的收益或危害。

## 最接近的相关工作

与 PRM-as-a-Judge 1.5 的机器人过程评分、Robo-Dopamine 2.0 的恢复建模、CRATE 的移动 Agent 轨迹评估和 Thinkingbox 的终态副作用检查最接近。

## 如何复用或推进 LLM-as-a-Verifier

- 将 FailBench 按证据可观测性构建 verifier routing：视觉明显则 VLM，接触/装配则传感器或程序状态。
- 把二元 verdict 扩展为成功/部分完成/可恢复失败/不可恢复失败/证据不足的序数分布。
- 用空间 crop 作为 privileged teacher view，将局部证据判断蒸馏到看全局帧的 student。
- 在 student-generated critique 中要求引用区域和预期物理状态，未定位证据时返回不确定。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher 分数需按任务证据类型校准；接触密集任务不应使用同一温度和置信门槛。
- **A/B/T 与序数分布**：同终态多视角/传感器构造 A/B/T，视觉证据不足时使用 Tie/INCONCLUSIVE。
- **真值门控**：力传感器、装配状态和环境事件对视觉 Judge 拥有否决权。
- **critique states**：训练 student 先定位相关区域，再生成失败原因和分布评分。
- **高熵探索**：视觉不确定时保留恢复分支，不把“疑似成功”直接终止 rollout。
- **sealed eval**：按未见来源、真实/模拟和证据类型分层，避免只在同一视频风格上验证。