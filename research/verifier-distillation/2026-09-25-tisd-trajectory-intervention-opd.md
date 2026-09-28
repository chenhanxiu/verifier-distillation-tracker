# TISD: On-Policy Self-Distillation with Trajectory Intervention

- **作者**：Taeckyung Lee, Rinat Amankos, Jeonghye Kim, Hyungjun Yoon, Woogyeol Jin, Sung-Ju Lee
- **首次公开日期**：2026-09-25
- **版本日期**：2026-09-25（v1）
- **原始论文**：https://arxiv.org/abs/2609.30878
- **代码**：未公开

## 一句话结论

【论文原文】TISD 不只在 student 已访问的前缀上蒸馏 teacher，而是在最大分歧处强制采用 teacher 偏好的分支动作，再让 student 生成后缀并对整段新轨迹蒸馏，从而把监督扩展到原本不会出现的 successor states。

## 真正新增的内容

【论文原文】作者把 teacher–student 分歧从“局部 token 修复信号”重新定义为“轨迹分支提案”：受控干预显示 teacher token 能改善后续成功率，但只纠正单点不足以覆盖由该动作引出的状态。TISD 因而提出 branch–regenerate–distill 三步闭环。

## 核心方法

1. 在 student rollout 中定位 teacher–student 高分歧 token。
2. 强制执行 teacher 选中的分支 token。
3. 后缀重新交给 student 采样，保持 on-policy 风格的状态分布。
4. 使用可见 privileged context 的 teacher 对完整干预轨迹给出 dense targets。

## 关键实验结果

【论文原文】相对 SDPO，coding 模型平均 Avg@4 提升 1.2 个百分点；science 域 Avg@128 在等训练步预算下提升 0.8 点，在等时间预算下提升 0.3 点。

## 证据质量与局限

【论文原文】包含受控 token 干预诊断，并同时报告等步数与等时间预算，因而比只比较训练步数更可信。局限是改进幅度有限、仅为 v1，且摘要未证明方法在真实长时程工具 Agent、跨 tokenizer teacher 或 sealed evaluator 下仍成立；代码尚未公开。

## 最接近的相关工作

最接近 SDPO、AC-OPD 的 teacher continuation、高熵分叉方法，以及 STRIDE 的首错定位。区别是 TISD 明确把 teacher 分歧转化为新 successor-state 数据，而不只改变当前位置的 target 或 continuation 长度。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把分支触发器从 token KL 替换为 verifier 的分数分布熵、A/B/T 平局概率或 critique 分歧；在 teacher 分支后收集 student-generated critique states，再由程序/环境真值决定是否把该分支纳入蒸馏。这样 verifier 不只是打分器，也成为状态覆盖控制器。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：在高分歧状态蒸馏整段后继 score distribution，而非只拟合当前 token。
- **A/B/T 与序数分布**：把高 T 概率或高序数熵作为分支预算信号，不应把不确定性直接压成单一偏好。
- **真值门控**：分支方向可由 teacher 提议，但更新符号应由可执行/环境结算确认。
- **Critique states**：保留 teacher 分支后由 student 自己生成的 critique 与修复轨迹，避免完全 teacher-forced。
- **探索**：只在高价值分歧点干预，并保留未干预对照臂，防止探索坍缩。
- **Sealed eval**：评测需冻结分支选择器与 evaluator，并独立运行原始/干预两臂，避免选择器和 verifier 共适应。
