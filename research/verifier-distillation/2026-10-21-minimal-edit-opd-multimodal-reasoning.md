# Edit, Don't Imitate：面向多模态推理的最小编辑 On-Policy Distillation

- **论文标题**：Edit, Don't Imitate: Minimal-Edit On-Policy Distillation for Multimodal Reasoning
- **作者**：Wen Ye, Ailin Deng, Zirui Wang, Shixing Yu, Han Zhang, Tian Yun, Nikhil Mehta, Tarun Kalluri, Xuefei Cao, Xuezhe Ma, Hengduo Li
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.30231
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.30231
- **代码**：未见作者公开代码链接

## 一句话结论

论文把 teacher 从“生成完整答案”改成“只标出 student rollout 中应纠正的 token”，并用可验证任务奖励训练正确轨迹，是 score-level OPD 中“硬真值定方向、teacher 只定局部修正”的直接实现。

## 真正新增的内容

**论文原文结论**：作者提出 minimal-edit corrective OPD：参考图描述与已验证解只在训练期提供，teacher 对错误的 student rollout 做最小编辑式评分，仅 teacher 不认可的 token 进入纠正损失；正确 rollout 则接受任务奖励 RL。该设计不要求 teacher 自己生成解，冻结的同尺寸 teacher 也有效。

**分析推断**：新增点不是一般的“OPD + reward”，而是把监督支持集限制到 teacher-disfavored token，显式减少全响应模仿导致的策略坍缩，可视为 score-level verifier distillation 的稀疏掩码版本。

## 核心方法

1. student 在自身策略分布上生成视觉数学推理轨迹。
2. 用训练期参考图描述与验证解形成 privileged teacher 信号。
3. 对失败轨迹只更新 teacher 判定需要修改的 token；不复刻完整 teacher response。
4. 对通过硬验证的轨迹使用任务奖励 RL。
5. 测试时移除参考描述与额外 teacher 调用。

## 关键实验结果

**论文原文结论**：跨模型规模，训练后的模型在测试时不使用图描述，仍达到或超过“推理时提供参考图描述”的对应基座；低层几何感知改善明显，并能迁移到外部数学与感知基准。同尺寸冻结 teacher 仍有收益，但多数指标弱于更大 teacher。

## 证据质量与局限

证据覆盖多模型规模、内部与外部基准，并包含同尺寸 teacher 对照，机制检验较强。局限是任务集中于视觉数学，摘要未给出完整数值；teacher 仍依赖训练期参考描述和已验证解，不能证明在开放式长轨迹 Agent 上同样有效。

## 最接近的相关工作

最接近标准 token-level OPD、TV-regulated OPD、γOPD、AC-OPD，以及“硬真值定方向、软 teacher 定幅度”的 UECR-GRPO。与完整序列蒸馏相比，本方法更接近局部错误掩码和 selective intervention。

## 如何复用或推进 LLM-as-a-Verifier

可让 verifier 输出逐 token / 逐动作的“保留、纠正、未知”掩码，而不是单一轨迹分数；再把程序化或环境真值作为正确轨迹的硬门控。对于 critique，可只蒸馏能够定位到证据与具体动作的局部修改，未通过执行复现的 critique 不进入更新。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：新增“全分数回归 vs 最小编辑掩码”主对照，并分别报告修正 token 比例与最终成功率。
- **A/B/T 与序数分布**：把 T 映射为“不更新该位置”，A/B 只作用于可定位的分歧位置；保留原始序数不确定性作为更新幅度。
- **硬真值门控**：环境成功决定更新方向，teacher 仅决定失败轨迹中修哪里。
- **student-generated critique states**：仅接纳能被最小编辑定位且被重放验证的 critique。
- **高熵探索**：未被 teacher 明确否定的高熵 token 不做全量模仿，降低探索被抹平的风险。
- **sealed eval**：必须在未向 teacher 暴露的图型、工具和失败模式上评估，防止 privileged 描述与评测集共适应。
