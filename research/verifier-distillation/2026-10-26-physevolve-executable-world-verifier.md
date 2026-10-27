# PhysEvolve：以可执行世界和确定性 Verifier 驱动自进化

## 基本信息

- **论文标题**：PhysEvolve: Verifier-grounded Self-evolution for Physical Reasoning with Executable Worlds
- **作者**：Jinyuan Hu, Yilei Jiang, Chen Tang, Minghong Cai, Xinran Liu, Xiangyu Yue
- **首次公开日期**：2026-10-26
- **版本日期**：2026-10-26（v1）
- **论文链接**：https://arxiv.org/abs/2610.34921
- **项目页面**：https://github.com/yelonhu/physevolve-page
- **代码链接**：未发现明确的训练代码仓库

## 一句话结论

PhysEvolve 让模型提出可执行物理世界，再由确定性引擎冻结世界、生成反事实分支和精确标签，用硬 verifier 同时驱动 GRPO 与课程进化。

## 真正新增的内容

**论文原文结论**：共享 VLM 生成 world program 与 evidence schema；物理引擎验证世界后模拟 baseline 和 body-elided counterfactual，自动合成 answer-bound 视觉任务，执行反馈更新 policy 与物理意图课程。

**分析推断**：这是“程序化/环境真值门控 teacher 信号”的强原型：模型可以生成任务和解释，但不能决定真值。对长时程 Agent，可把世界程序替换为工具环境快照，把 body-elision 替换为动作/步骤消融。

## 核心方法

- 模型生成可执行场景程序和证据定义。
- 确定性模拟器拒绝无效世界并冻结通过版本。
- 对同一世界运行事实与干预分支，生成离散可验答案。
- 用 exact verifier reward 训练 Qwen3-VL-8B-Instruct，并依据成功/失败调整 curriculum。

## 关键实验结果

**论文报告**：无需人工干预数据，在 PhysBench、CausalPhys 和 ContPhy 获得定向提升；PhysBench Throwing +8.8 点，ContPhy Counterfactual Removal +7.4 点、Goal-Pit +24.4 点，并迁移到 cloth、fluid、soft-body 和真实视频。

## 证据质量与局限

硬模拟器与反事实配对提供高质量方向标签，跨 benchmark 转移增强可信度。局限是模拟器只保证其规范内部的正确性，存在 sim-to-real 与 specification gap；改进集中于若干子项，不能推断全面物理能力。

## 最接近的相关工作

GameLogicBench、Ground-truth-as-code、AutoGym、ContrAgent、CoVer。PhysEvolve 的新增点是让模型生成可执行世界，但把世界验真与结果结算留给确定性引擎。

## 如何复用或推进 LLM-as-a-Verifier

让 LLM verifier 负责提出断言、证据 schema 和反事实操作，执行器负责给出不可覆盖的结果；再蒸馏“哪些检查有效”，而不是蒸馏模型自报的最终真值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：硬结果定方向，LLM 只分配步骤/解释幅度。
- **A/B/T**：同状态动作消融可直接产生 A/B；效果等价时为 T。
- **硬真值门控**：冻结环境和程序版本，所有 teacher 信号必须引用结算记录。
- **critique states**：critique 只有在反事实重放支持时入库。
- **高熵探索**：保留多个经模拟器验证但策略不同的成功世界/动作。
- **sealed eval**：使用未见世界模板、真实环境与独立模拟器检查 specification gap。