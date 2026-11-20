# Training LLMs to Follow Reasoning Instructions with Minimal Edits

- **作者**：Alexandra Yakovleva, Luat Gia Khoi Nguyen, Juho Kannala, Harri Valpola, Alexander Ilin
- **首次公开日期**：2026-11-19
- **版本日期**：2026-11-19（v1）
- **原始论文**：[arXiv:2611.26342](https://arxiv.org/abs/2611.26342)
- **DOI**：[10.48550/arXiv.2611.26342](https://doi.org/10.48550/arXiv.2611.26342)
- **代码**：论文页面未提供公开代码链接
- **发表信息**：NeurIPS 2026 Workshop on Transitioning from Pre-training to Post-training（论文页面标注）

## 一句话结论

【论文原文】让 editor 在模型自身轨迹中定位第一处失败并只监督最小替换片段，能比整轨迹模仿或轨迹级 RL 更集中地修复 reasoning instruction failure；【分析推断】这是 student-generated critique states 与局部 verifier credit 的简洁训练原型，但 editor 结论必须经环境真值门控。

## 真正新增的内容

【论文原文】edit-based training 将监督单位从整条 completion 缩到第一处失败的最小 replacement span；在线版本会随当前模型的新失败模式持续更新编辑监督。目标是修复局部错误而保留其余已有推理分布。

【分析推断】它把 verifier 的作用从“给整轨迹一个分数”转成“指出第一个可操作修复点”，与长轨迹 Agent 的首错定位、局部回滚和 critique-state 准入高度吻合。

## 核心方法

【论文原文】

1. 从当前模型采样 completion；
2. editor 按指定标准定位第一处 failure；
3. editor 生成最小替换 span；
4. 训练只在被替换 span 上计算监督损失；
5. 可离线运行，也可在线持续采样并适应 evolving failure modes；
6. 在 Qwen3-32B 与 ReasonIF 上验证 reasoning instruction following。

## 关键实验结果

【论文原文】相对 full-trajectory imitation 与 trajectory-level RL，edit-based training 显著改善 reasoning instruction compliance，同时大体保留未定向任务能力。摘要未提供具体数值，需以正文表格为准。

## 证据质量与局限

【论文原文】包含两类强基线并明确考察未定向能力保持，适合验证“局部监督减少过约束”的命题。局限是 workshop 论文、单一 32B 模型与 ReasonIF 任务，摘要缺少效应量；editor 的准确率、成本及其错误被 student 放大的风险尚不能从摘要判断。

【分析推断】在 Agent 轨迹中“第一处失败”可能不可观测或非唯一，且后续状态受环境不可逆变化影响；只修文本 span 不一定等价于修复状态转移。

## 最接近的相关工作

- STRIDE：定位多轮 Agent 首错并从薄弱正确前缀重启。
- FLARE：从环境结算后的因果错误链训练 generative reward model。
- LLM-as-an-Improver / PaperDoctor：把验证反馈转为证据化修复建议。
- process reward model：给步骤级信用，但通常不直接生成最小修复。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 editor 输出结构化为：失败状态、证据指针、最小动作/文本替换、预期恢复条件。只有当重放后的程序测试或环境回执改善时，才把编辑作为正例；无可验证改善时保留 T/INCONCLUSIVE。可蒸馏首错位置分布与局部修复分数，而非整轨迹单分数。

## 对现有 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level on-policy verifier distillation**：只在首错附近施加 verifier/teacher KL，其他 token 维持低权重或冻结。
- **pairwise A/B/T 与序数评分分布**：原片段与最小编辑构成 A/B；重放无显著差异或证据不足标 T。
- **程序化/环境真值门控**：编辑必须通过测试、状态回放或环境成功率改善才进入训练。
- **student-generated critique states**：把 editor 的证据化最小编辑直接作为 critique state，但不通过验真不得写入长期记忆。
- **高熵分叉保留探索**：若首错后验分散，保留多个候选编辑并分叉重放，而非强制唯一修复。
- **独立 sealed eval**：使用未参与 editor prompt 调整的任务与环境，分别报告 compliance、真实成功率和副作用。
