# Interleaved OPD 中 Teacher Bridge 的受控负结果

## 基本信息

- **论文标题**：How Much Do Teacher Bridges Matter in Interleaved On-Policy Distillation?
- **作者**：Leran Chen, Zhiyuan Yao, Lingnan Kong
- **首次公开日期**：2026-10-28
- **版本日期**：2026-10-28（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.38383
- **DOI**：https://doi.org/10.48550/arXiv.2610.38383
- **代码**：未见作者公开代码链接

## 一句话结论

在严格控制相同轨迹后，一个只占 2.7% token 的 teacher bridge 对 BF16 准确率没有可检出的额外收益；这不是“教师片段无用”的普遍结论，而是提醒必须同时核查干预覆盖率、梯度方向、数值精度和在线稳定性。

## 真正新增的内容

**论文原文结论**：

1. 在完全相同轨迹上比较 teacher token 不加 loss、forward KL 和 reverse KL，隔离“教师文本作为上下文”与“教师文本作为训练目标”。
2. 预注册主比较中三种处理的 BF16 准确率在 ±5 个百分点等价区间内无显著差异。
3. 探索性高分歧位置干预曾出现收益，但预注册复现实验未确认；四倍加权同样无显著准确率收益。
4. 在线训练变体没有同时满足稳定停止和准确率提升；FP32 下模型常触达长度上限。

**分析推断**：

- 对 Agent verifier × OPD，teacher bridge 是否有效不能只看最终均值；应把干预 token 覆盖、teacher/student 梯度夹角、停止行为与恢复率列为一级指标。
- 该负结果与 PIVOT 并不直接矛盾：PIVOT 同时改变成功轨迹可达性与片段监督，而本研究强调小比例 bridge 在特定短训练/BF16设置下可能不足。

## 核心方法

1. Qwen3-1.7B 学生、Qwen3-4B-Instruct-2507 教师。
2. 在学生第一段后插入一段教师 bridge，固定其余轨迹。
3. 对 bridge 分别使用 no loss、FKL、RKL；按 token 作者分解梯度。
4. 使用预注册等价性边界、探索性试验与独立复现，并检查 BF16/FP32 行为。

## 关键实验结果

**论文报告**：bridge 仅占全部 token 的 2.7%，其梯度较小且近乎与 student-token 梯度正交；主比较没有发现教师文本作为上下文或训练目标的额外准确率收益。训练收益在固定 response 上约四次更新后达到峰值，随后停止生成恶化。

## 证据质量与局限

- **优点**：负结果透明；有预注册主比较、复现失败披露、等价性边界和梯度分解。
- **局限**：短训练、小 student、单 teacher、bridge 覆盖低，外推范围有限。
- BF16 会舍入掉小权重变化，而 FP32 又暴露长度失控；因此论文明确没有证明 teacher-token supervision 普遍无用。
- 未覆盖真实工具环境、硬真值门控或长轨迹可恢复性。

## 最接近的相关工作

- **PIVOT / ATI-OPD**：也插入教师片段，但强调干预位置、重新续写与选择性 loss。
- **AC-OPD**：在高分歧状态使用有限 teacher continuation。
- **FKL/RKL gating**：讨论 KL 方向与逐 token 门控。

## 如何复用或推进 LLM-as-a-Verifier

对每次教师插入记录：触发证据、覆盖 token 比例、KL 方向、梯度范数/夹角、后续环境恢复率和停止行为。只有 bridge 让环境状态可恢复且 student 在无 teacher 条件下重现改进，才判为有效 verifier supervision。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：新增 no-loss bridge、FKL bridge、RKL bridge 和不插入四臂控制，保持轨迹与预算一致。
- **pairwise A/B/T 与序数分布**：对桥接前后后缀做盲评；差异落在等价区间时标 T。
- **程序化/环境真值门控**：先证明 bridge 修复可执行状态，再允许蒸馏，避免只学习教师文风。
- **student-generated critique states**：评价 critique 是否改变可重放结果，而非只看文本相似。
- **高熵分叉与探索**：近正交小梯度不应被误作强监督；保留原学生分支作为探索对照。
- **sealed eval**：用 BF16/FP32、长度上限和独立终止检测做敏感性分析，避免数值设置掩盖结论。