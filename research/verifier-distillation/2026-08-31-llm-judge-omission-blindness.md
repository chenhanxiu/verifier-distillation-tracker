# LLM Judges Verify Presence, Not Absence: Omission Blindness in AI Clinical Notes and What Recovers It

## 基本信息

- **作者**：Sebastian Fox, Luke Markham, Ryan Lail, Michael Karotsieris
- **首次公开日期**：2026-08-31
- **版本日期**：2026-08-31（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2608.31016
- **DOI**：https://doi.org/10.48550/arXiv.2608.31016
- **代码**：https://github.com/composo-ai/omission-bench
- **数据集**：https://huggingface.co/datasets/ComposoAI/OmissionBench

## 一句话结论

完整输入上的整体 LLM Judge 几乎不能可靠发现“本该出现但缺失”的事实；先枚举环境/记录已确立的原子事实，再逐项做 presence check，才显著恢复检测能力。

## 真正新增的内容

**论文原文结论**：作者构造 500 个单错误 note pair，其中 298 个为确定遗漏、202 个为新增或篡改对照。八种 Judge 设计对新增/篡改的 paired discrimination 达 0.79–0.94，但对遗漏仅 0.50–0.63。换措辞、投票和 GEPA prompt 优化不能形成可用分离；将任务重构为“先列出 transcript 确立的事实，再逐项检查 note 是否包含”才有效。

**分析推断**：这类 omission blindness 很可能迁移到 Agent 轨迹评估：整体 Judge 容易识别错误工具调用，却可能漏掉“没有澄清、没有检查状态、没有执行必要恢复步骤”。因此 next-action verifier 必须显式建模 expected obligations，而不能只对已发生动作做合理性评分。

## 核心方法

- 用 transcript-derived、人工审计的 fact sheet 作为事实锚点，构造 clean/flawed 配对。
- 对比八种 Judge 设计及 scope、输出格式、投票、prompt wording、GEPA 优化。
- 两种恢复路线：
  - per-fact pipeline：列出已确立事实并逐项检查；
  - 单调用 GEPA prompt：在一个调用内执行同样的事实枚举与 presence verification。
- 使用冻结 confirmation subset、完整 evaluation set 和真实 vendor notes 检查泛化与阈值迁移。

## 关键实验结果

**论文报告**：

- 新增/篡改 paired discrimination：**0.79–0.94**；遗漏：**0.50–0.63**，接近随机。
- per-fact pipeline 在 **2.7%** false alarm 下检出 **24.6%**。
- 单调用方法检出 **36.9%**，false alarm **6.2%**，约为 pipeline 每 note 成本的十分之一。
- 二者意见相反的 10 个案例中，医师对 **10/10** 支持 pipeline（`p=0.002`）。
- 独立 clinician 对 severity rubric 的盲评达到相差不超过一级。
- rubric 锚定的跨模型 severity agreement `κ=0.662`（95% CI [0.59, 0.73]），未锚定同家族配对仅 `κ=0.177`。
- benchmark 阈值不能直接迁移到真实 vendor notes，需要重新校准。

## 证据质量与局限

- **证据质量：高（针对该任务）**。有明确事实锚点、配对设计、冻结 confirmation subset、真实部署样本、统计检验和临床专家复核。
- 医疗 note 是特定领域，不能直接把检出率外推到 Agent。
- 即使重构后，绝对遗漏检出率仍有限；事实在其他位置被改写/重述时，两种方法都可能失败。
- 恢复方法仍依赖先枚举事实，若该阶段漏项，后续 verification 无法补救。
- 真实分布上 operating threshold 不迁移，说明 sealed eval 也需持续但独立地再校准。

## 最接近的相关工作

- ProofJudge、JuryProbe：Judge 随机翻转、共识误判和可信参考路由。
- SARA / Rubric Dropout：rubric 干扰与 Judge reward hacking。
- CRATE：先抽取 step-level evidence，再做整体判断。
- ExecRubrics / AutoSciRub：把隐含义务显式化为原子可验证准则。
- RecurSE：独立人工锚定检测 evaluator 共适应。

## 如何复用或推进 LLM-as-a-Verifier

- 对每个 Agent 状态先生成“必须满足/必须检查/不得违反”的 obligation set。
- 分两路评分：
  - 对已执行动作检查 commission/error；
  - 对 obligation set 逐项检查 omission/missing action。
- 输出每项 obligation 的满足概率、证据位置和未满足原因，再聚合为序数评分分布。
- 对 Judge 投票不要只看一致率；投票可能让同一 omission blind spot 更稳定。
- 需要用程序状态、工具日志和人工锚点校准漏检率与阈值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：student verifier 应蒸馏 obligation-level logits，而不是只蒸馏 holistic score。
- **pairwise A/B/T**：比较动作 A/B 时，应额外检查二者分别遗漏了哪些必要义务；当覆盖不同义务且证据不足时允许 tie。
- **程序化真值门控**：从环境状态导出必需前置条件、权限、安全检查和终态约束，作为 omission detector 的硬锚。
- **student critique states**：critique 必须列出“缺了什么”，并通过后续重放验证补上该步骤是否改善目标推进。
- **高熵分叉**：obligation 是约束而非唯一解；满足义务的多条路径都应保留，避免把表面风格差异误判为缺失。
- **sealed eval**：保留专门的 omission challenge set、不同 Judge 家族和人工锚定；同时报告 commission 与 omission 两套指标，防止总体准确率掩盖系统性漏检。
