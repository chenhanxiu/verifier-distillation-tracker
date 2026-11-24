# Muted Distillation: Sealing Reasoning from Teacher Unlocks Token-Efficient Agents

- **作者**：Yuwei Zhang, Ian Miao, Wentao Zhang, Chen Qu, Bill Bi, Jingbo Shang, Donna Schut
- **首次公开日期**：2026-11-21
- **版本日期**：2026-11-21（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.28445
- **DOI**：https://doi.org/10.48550/arXiv.2611.28445
- **代码**：未见作者在 arXiv 摘要页给出独立代码链接

## 一句话结论

在多轮知识工作 Agent 中，向 teacher 暴露 student 的完整 reasoning 会让 teacher 分数受干扰并诱导更长轨迹；隐藏 reasoning、只让 teacher 判断行为可显著降 token 且不损准确率。

## 真正新增的内容

**论文原文结论**：提出 Muted Distillation，仅遮蔽 student reasoning、保留其行为结果供 teacher 评分；方法无需额外数据或超参数。  
**分析推断**：这是“密封 evaluator 视图”的训练时版本，显示 teacher access policy 本身就是 OPD 的关键实验变量。

## 核心方法

在标准 OPD 的 student rollout 上改变 teacher 可见信息：teacher 看见 student 做了什么，但不见其 reasoning，从而减少 student 文字对 teacher score 的 distractor effect。

## 关键实验结果

相对标准 OPD，OfficeQA Pro 和 SpreadsheetBench 每 episode 输出 token 分别减少 57% 与 53%；OfficeQA Pro 准确率持平，SpreadsheetBench pass@1 提升 4.8 点。

## 证据质量与局限

直接在多轮 Agent benchmark 上比较，指标同时覆盖质量与成本。局限是 ongoing work、任务仅两个，摘要未给统计区间；隐藏 reasoning 可能牺牲对过程性安全问题的可见性。

## 最接近的相关工作

最接近 Endpoint-Conditioned Process Value 的 evidence-access 操作、Beyond Accuracy 的轨迹披露阈值效应，以及 Harness or Model? 对 scaffold 混淆的审计。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier 输入拆成行为视图、critique 视图和完整思维视图，分别校准；默认用行为/工具证据蒸馏 outcome score，仅在程序真值触发异常时开放 critique，以避免语言风格污染分数。

## 对 Agent verifier × OPD 实验路线的具体影响

新增 access ablation：`action+observation`、`+student critique`、`+full reasoning`。只有在 sealed outcome 上确有增益的视图才进入 teacher 信号；student-generated critique 不直接作为真值，需环境门控。高熵分叉继续保留完整轨迹供独立审计，但训练 teacher 可采用 muted 视图。