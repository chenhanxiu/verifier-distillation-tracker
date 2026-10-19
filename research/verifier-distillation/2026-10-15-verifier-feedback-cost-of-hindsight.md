# Repair, Retry, and the Cost of Hindsight: Verifier Feedback in Formal Theorem Proving

## 基本信息

- 作者：Jack Li, Sophia Li
- 首次公开日期：2026-10-15
- 版本日期：2026-10-15（v1）
- arXiv：2610.22698
- 原始论文：https://arxiv.org/abs/2610.22698
- DOI：https://doi.org/10.48550/arXiv.2610.22698
- 代码：未发现公开代码链接
- 会议：NeurIPS 2026 Workshop on AI for Verifiable Coding

## 一句话结论

正确 verifier diagnostic 可以修复“看到自己失败证明”带来的损失，却未在等 token 预算下胜过独立重采样；critique state 的价值必须用 matched-budget counterfactual 验证。

## 真正新增的内容

**论文原文结论：** 论文把失败前驱、正确/错误编译器诊断、重试指令分别控制，揭示两个相反效应：失败轨迹会诱发复制并降低成功率，匹配的诊断能部分恢复，但不必然提供超过重新采样的净收益。

**分析推断：** “verifier feedback 改善 repair”与“反馈值得占用上下文/预算”是不同命题。Agent verifier × OPD 应比较 critique-conditioned rollout 与等成本 fresh branch，而不是只看相对无反馈重试。

## 核心方法

1. 固定同一个失败证明，分别控制是否展示失败文本、诊断是否匹配、是否加入 retry instruction。
2. 测试通用 Qwen3.6-27B 与专用 DeepSeek-Prover-V2-7B。
3. 在困难 MiniF2F 问题上做一步修复，并进行 11 题、最多 64 次尝试的序列实验。
4. 用独立重采样作为等 token 预算基线。

## 关键实验结果

**论文原文：** 展示失败前驱会降低成功并显著增加复制；对 Qwen 加入对应编译器错误可把损失恢复到“只给诊断”的水平。换成别题的失败证明大体消除退化；换成别题诊断则显著削弱 Qwen 的恢复。没有失败证明时，正确诊断相对错误诊断未显示明确优势。一步条件和 64 次序列修复均未证明优于等预算 instruction-only resampling。

**分析推断：** critique 的主要作用可能是解除失败轨迹造成的锚定，而非提供额外可迁移知识。

## 证据质量与局限

- 控制实验和等预算重采样基线很强，能分离多个常被混合的因素。
- 只有两个模型、Lean/MiniF2F 和少量序列题；不等同于开放工具 Agent。
- 编译器错误是高精度结构化反馈，LLM critique 的噪声通常更高。
- “未建立优势”不是证明所有多步修复无效。

## 最接近的相关工作

- LLM-as-an-Improver；
- Critique-Conditioned OPD；
- EquiReview-R 与 PaperDoctor；
- ReDiST 的 student-conditioned trace repair；
- STRIDE 的首错后重启。

## 如何复用或推进 LLM-as-a-Verifier

把 critique-state 准入做成 A/B 测试：同一失败状态分别生成 `fresh resample`、`failed trace only`、`diagnostic only`、`trace + matched diagnostic`。只有超过等预算 fresh resample 的 critique 才蒸馏或写入 memory。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD：** critique score 应基于相对 fresh-branch 的增量价值，而非修复成功本身。
- **A/B/T 与序数分布：** A=critique-conditioned，B=fresh resample，T=差异未分辨。
- **真值门控：** 优先使用编译器、测试与环境异常等匹配诊断。
- **critique states：** 避免无条件回放完整失败轨迹，减少复制和锚定。
- **高熵探索：** 预算中保留独立分支，不能全部转成连续修复链。
- **sealed eval：** 固定 token/调用预算、失败前驱和任务，使用未参与训练的证明集。
