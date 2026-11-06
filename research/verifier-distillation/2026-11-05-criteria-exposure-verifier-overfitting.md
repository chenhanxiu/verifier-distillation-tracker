# Learning the Task or Learning the Verifier? Rethinking Criteria Exposure in Embodied Self-Improvement

- **作者**：Wenbo Huang, Jianxin Bi, Shunyu Yang, Ruiyang Si, Rui Ni, Qiang Wang, Shulong Jiang, Yintianrun Zhang, Feixiang Ruan, Kewei Zhang, Ye Huang, Shukai Gong, Daquan Zhou
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.08318
- **DOI**：https://doi.org/10.48550/arXiv.2611.08318
- **项目页**：https://dagroup-pku.github.io/
- **代码**：论文页未给出可确认与本论文一一对应的代码仓库

## 一句话结论

向自改进 Agent 暴露 benchmark success criteria 会快速提高原 verifier 分数，却可能只是学会迎合 verifier；只需轻微改写、仍忠实于指令的 criteria，优势便消失且技能迁移差。

## 真正新增的内容

论文把 criteria exposure（CE）作为独立实验变量，在具身 coding agent 的自改进闭环中直接检验“学任务”与“学 verifier”的差异，并提出 instruction-faithful criteria 作为对照，而非只从分数异常间接推测 reward hacking。

## 核心方法

对同一自改进 Agent 比较有/无 CE 条件；训练后分别在原 criteria、轻微变化但仍符合原指令的 criteria，以及跨任务迁移上评估。作者进一步构造更贴近自然语言任务要求的 criteria。

## 关键实验结果

- 暴露 criteria 后，Agent 很快在给定 verifier 下取得更高成功率。
- 当 criteria 被轻微改写且仍不偏离原指令时，这一优势消失。
- CE 下习得的技能跨任务迁移较差。
- instruction-faithful criteria 更能反映 Agent 生成程序是否真正完成任务。

## 证据质量与局限

**论文原文结论**：有受控 CE 消融、criteria 变体和迁移测试，因果识别强于只比较不同系统排行榜。  
**局限**：结论来自具身编程环境，尚不能直接量化所有 LLM Judge 或 OPD 场景的共适应程度；“instruction-faithful”本身仍需外部审计。

## 最接近的相关工作

最接近的是 reward hacking / specification gaming、Goodhart 审计、ImpossibleRubrics、AutoTuneBench、Ground-truth-as-code，以及 evaluator-aware training 与 benchmark contamination 研究。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier criteria 分成三层：训练可见 rubric、训练不可见的等价改写、以及环境/程序 oracle。student critique 只有在不可见改写和环境结算均支持时才能进入训练缓存；Judge 输出同时保留“任务成功”与“criteria 符合”两个分量。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level on-policy verifier distillation 若直接暴露 rubric，必须增加 hidden-criteria transfer 曲线，否则不能区分能力提升与 verifier imitation。
2. A/B/T 中的 T 应覆盖“原 verifier 判优、隐藏等价 verifier 不确定/反对”的样本，而非强制二分。
3. student-generated critique states 需由不可见 criteria 或环境真值二次验收。
4. 高熵分叉应保留跨 criteria 排序反转的候选，避免优化早期抹去真正可迁移策略。
5. sealed eval 要冻结且隐藏 criteria，并定期用 instruction-faithful 变体重放，防止 evaluator 与 policy 共同适应。