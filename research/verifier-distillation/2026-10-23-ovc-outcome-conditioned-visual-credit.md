# OVC：用终局结果校准多模态 Token 信用

- **论文标题**：From Visual Affinity to Learning Credit in Multimodal Reinforcement Learning
- **作者**：Yuhang Han、Dingning Liu、Yujie Chen、Yaojie Zhang、Jingwei Song、Zequn Yang、Xuanming Shang、Li Ding、Zhijiang Guo、Linfeng Zhang
- **首次公开日期**：2026-10-23
- **版本日期**：2026-10-23（v1）
- **原始论文**：https://arxiv.org/abs/2610.32324
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.32324
- **代码**：https://github.com/kawhiiiileo/OVC

## 一句话结论

OVC 表明“与视觉输入相关”不等于“应获得更多信用”，必须用正负终局结果校准视觉关联，再在保持 advantage 符号的前提下重分配 token 权重。

## 真正新增的内容

**论文原文结论**：OVC 将视觉关联测量与信用分配解耦，通过图像相对 prompt-context 的表示差、正负 advantage 组间对比和不确定性缩放，得到 outcome-discriminative evidence，再生成均值为 1 的正 token 权重。

**分析推断**：该原则可直接迁移到 Agent：工具 observation 的显著性不能直接当作步骤贡献，必须观察它是否区分最终成功与失败。

## 核心方法

1. Relative Visual Encoding 构建相对视觉坐标。
2. Outcome-conditioned Evidence Calibration 用正负结果组校准证据方向与稳定性。
3. Normalized Credit Allocation 保持响应级 advantage 的符号和总尺度。
4. 复用既有 rollout，无需额外 RM、过程标注或推理时模块。

## 关键实验结果

**论文原文结论**：在 GSPO-token 上，三种模型的六项 benchmark 平均准确率相对 GSPO 提升 1.86–2.39 个百分点。

## 证据质量与局限

跨三模型六 benchmark 且开放代码；但集中于多模态推理，不是长时程 Agent，提升幅度中等。终局 label 仍可能含噪，正负组均值对少数模式敏感；没有验证 reward hacking 或 evaluator 共适应。

## 最接近的相关工作

与 DATC、UECR-GRPO、DelTA、MRTPO、视觉 token attribution 及 outcome-conditioned credit 最接近。区别是先校准“视觉相关性是否真与结果有关”。

## 如何复用或推进 LLM-as-a-Verifier

将视觉坐标替换为“工具 observation 相对已有上下文的增量表示”，再用环境成功/失败组校准哪些 observation 与步骤真正提供 outcome evidence。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：硬真值保留总信用，soft verifier 只做组内重分配。
- **A/B/T**：结果组差异不稳定或置信区间重叠时输出 T。
- **真值门控**：环境 verdict 负责正负分组，避免 Judge 自举。
- **critique states**：只保留能跨成功/失败组区分的证据引用。
- **探索保留**：显著但未被结果证实的高熵分支不应被强压。
- **sealed eval**：在独立任务上验证 credit 与实际反事实贡献的相关性。
