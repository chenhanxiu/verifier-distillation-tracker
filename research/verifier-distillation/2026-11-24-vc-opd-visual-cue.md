# VC-OPD：用特权视觉线索进行在线自蒸馏

- **论文标题**：VC-OPD: Learning to See What Matters via Visual Cue On-Policy Self-Distillation
- **作者**：Qinxuan Wang, Zheyu Zhang, Yijing Yang, Han Shu, Chuang Wang, Peipei Yang, Shuo Tang, Jie Hu, Shiming Xiang
- **首次公开日期**：2026-11-24
- **版本日期**：2026-11-24（v1）
- **原始论文**：https://arxiv.org/abs/2611.32292
- **DOI**：https://doi.org/10.48550/arXiv.2611.32292
- **代码链接**：未见公开代码

## 一句话结论

VC-OPD 让 teacher 在 student 自生成轨迹上访问问题相关、经筛选的视觉线索，再把其 token 级信号蒸馏回不依赖线索的 student，展示了 privileged verifier teacher 的实用路径。

## 真正新增的内容

**论文原文结论**：方法从强 MLLM 生成 question-conditioned visual cues，经多阶段过滤后仅提供给 teacher；student 在推理和部署时不需要额外信息。**分析推断**：其结构可直接迁移到 Agent：teacher 访问隐藏环境状态、执行日志或未来结果，student 只看在线可用状态，从而形成 privileged verifier distillation。

## 核心方法

先生成与问题相关的视觉提示并执行质量筛选；在 student on-policy 轨迹上，带特权线索的 teacher 提供信息性 token-level 监督；student 通过自蒸馏学习关注关键证据，推理阶段移除 cues，避免额外成本和信息泄漏。

## 关键实验结果

**论文报告**：4B 模型超过多种 8B 及更大基线，并相对 RL 与标准 OPD 获得稳定提升。摘要未给出完整逐基准数值，也未隔离 cue 生成器、过滤器与蒸馏目标各自贡献，需等待完整消融和代码。

## 证据质量与局限

小模型对强基线的结果支持 privileged cue 有效，但视觉任务与长时程 Agent 的状态/行动信用不同。cue 由强模型生成，可能放大共同幻觉；过滤器若与 teacher 同源会产生 evaluator 共适应。特权信息还可能包含部署时不可恢复的捷径。

## 最接近的相关工作

与 OPD-Aha 的视觉偏好重构、SCOPE-OPSD 的 privileged representations、The Tasteful Agent 的 hindsight distillation、AC-OPD 的 teacher continuation，以及 DENSE 的证据化轨迹蒸馏相关。

## 如何复用或推进 LLM-as-a-Verifier

把 visual cues 替换为只在训练期可见的环境快照、未来结果、隐藏测试和程序证书；teacher 输出序数评分分布、证据指针及不确定性，student 只接收可在线推断的状态。cue 必须由独立 oracle 或回放检查，而不是仅由另一 LLM 自证。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：在 score-level OPD 中增加 privileged teacher 通道，比较“无特权、原始隐藏状态、经门控隐藏状态”；只在环境证书通过时强化 critique states。高熵分叉可让 teacher 看未来 rollout 后给 A/B/T，但 student 训练仍保留多分支概率，避免 hindsight 过度确定。sealed eval 必须完全移除 cues、冻结 cue 过滤器，并使用独立隐藏任务检查捷径泄漏。
