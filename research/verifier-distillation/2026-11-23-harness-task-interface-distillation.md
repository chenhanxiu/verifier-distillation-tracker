# Learning What vs. Learning How：拆分 Agent 的任务能力与接口能力

- **论文标题**：Learning What vs. Learning How: Decomposing Task and Interface Competence in Agentic Training
- **作者**：Chaeeun Lee, Hossein A. Rahmani, Aryo Pradipta Gema, Kexin Xu, Emine Yilmaz, Pasquale Minervini, T. Ian Simpson, Chen Jin, Amrutha Saseendran
- **首次公开日期**：2026-11-23
- **版本日期**：2026-11-23（v1）
- **原始论文**：https://arxiv.org/abs/2611.31427
- **DOI**：https://doi.org/10.48550/arXiv.2611.31427
- **代码**：https://github.com/chaeeunlee-io/harness-competence
- **数据**：https://huggingface.co/datasets/chaeeunlee/harness-competence

## 一句话结论

Agent 蒸馏若只在单一 harness 上训练，会把任务能力与接口熟练度混在一起；多 harness 蒸馏和接口 rehearsal 才能让能力在不同执行框架间迁移。

## 真正新增的内容

**论文原文结论**：作者将“知道做什么”的 task competence 与“知道怎样通过特定接口做”的 interface competence 分离，并显示单 harness 蒸馏会显著损害未见 harness。**分析推断**：Agent verifier 也必须做同样分账，否则评分提升可能只是学会某个 scaffold、消息格式或超时机制，不能证明 verifier 理解了轨迹质量。

## 核心方法

用多种 agent harness 交叉训练与评测，将任务示范蒸馏、harness rehearsal 和 on-policy RL 分别控制；通过 held-out harness 检查能力是否跨接口保持，从而识别任务知识、接口适配及两者交互。

## 关键实验结果

**论文报告**：在 BFCL V3 multi-turn 设置中，任务监督单独为 8.5%，harness rehearsal 单独为 32.5%，二者结合达到 58.8%；多 harness 蒸馏优于单 harness，on-policy RL 更稳健并能保留已获得的接口能力。

## 证据质量与局限

公开代码和数据提高可复现性，交叉 harness 设计能直接定位混淆因素。局限是 harness 集合仍有限，结果可能依赖 BFCL 工具调用形式；尚未单独训练 verifier 或 reward model，也未证明在更长、多模态或真实权限环境中成立。

## 最接近的相关工作

与 Harness or Model?、How Do Agent Harnesses Create Value?、AutoTuneBench 的隔离测量高度相关；也与 STRIDE 的多轮 on-policy distillation 和 DynSTEER 的阶段化轨迹评价互补。

## 如何复用或推进 LLM-as-a-Verifier

训练 verifier 时把任务状态与 harness 元数据分离编码；同一底层任务生成多 harness 轨迹，要求 verdict 与序数分布在语义等价接口间保持不变。对接口特定故障另设诊断头，而不是把它混入“任务是否完成”的总分。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：将 score-level OPD 扩展为双通道目标：任务质量分布与接口执行分布；pairwise A/B/T 尽量比较跨 harness 的语义等价分支。student-generated critique 需注明错误属于任务推理还是接口调用。保留未见 harness 的独立 sealed eval，并在训练/评测间更换 scaffold、工具序列化与超时策略，防止 evaluator 与单一执行框架共适应。
