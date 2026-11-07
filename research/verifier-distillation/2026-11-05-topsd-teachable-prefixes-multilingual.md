# Knowing When to Teach: Learning from Teachable Prefixes in Multilingual Reasoning Distillation

- **作者**：Jaewon Cho, Minseo Yoon, Jinyoung Park, Jinwoo Seo, Jaewon Chu, Alice Oh, Hyunwoo J. Kim
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.08179
- **DOI**：https://doi.org/10.48550/arXiv.2611.08179
- **代码**：论文页面未给出公开代码链接

## 一句话结论

TOPSD 先估计 teacher 开始随 student 错误漂移的位置，再验证 teacher 能否从该前缀恢复正确答案，只蒸馏通过恢复测试的前缀；低资源语言受益尤其明显。

## 真正新增的内容

论文发现 Teacher Drift 在低资源语言更早出现，并把“是否教、教到哪里”做成逐轨迹决策，而不是对所有 token 统一 self-distill。

## 核心方法

用 teacher–student likelihood 估计漂移起点并截取候选前缀；让 privileged teacher 从该前缀续写，只有能恢复正确终局的前缀才产生 OPSD 信号。

## 关键实验结果

在十种语言、三个模型规模的多语言数学推理上，TOPSD 一致优于 conventional OPSD，提升主要集中在低资源与中资源语言。摘要未给出逐语言绝对数值。

## 证据质量与局限

语言覆盖和模型规模较广，并以可恢复性做 gate；但“恢复正确答案”仍是终局标准，不能证明中间 critique 因果正确，也未直接覆盖交互式 Agent。

## 最接近的相关工作

最接近 Verify-Before-Distill、STRIDE、SCOPE、O²PD、TESD 与 multilingual verifier calibration。

## 如何复用或推进 LLM-as-a-Verifier

把 recoverability test 扩展为“从当前 Agent state 由 teacher 继续执行能否通过环境 oracle”；只有可恢复状态的 teacher score/critique 才用于蒸馏，并按语言、工具域、轨迹深度分别校准。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 增加逐状态 recoverability gate。
2. A/B/T 中，teacher 不能从任一候选恢复时标 T，而非选较高语言似然者。
3. critique state 必须携带恢复轨迹与环境证据。
4. 低资源语言更早触发多分支/强 verifier，避免错误前缀锁定。
5. sealed eval 按语言和轨迹深度分层，检查同一 gate 是否存在系统性覆盖差异。