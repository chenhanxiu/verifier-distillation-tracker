# DUET：用同权重双教师分歧进行禁令遵循 OPD

## 基本信息
- **论文标题**：DUET: Dual-Teacher On-Policy Distillation via Same-Weight Disagreement for Prohibition Compliance
- **作者**：Zihan Li, Feifei Li, Wenhui Que
- **首次公开日期**：2026-07-29（本次进入 arXiv new submissions 检索窗口）
- **版本日期**：2026-07-29（v1）
- **arXiv / DOI**：https://arxiv.org/abs/2608.14644 / 10.48550/arXiv.2608.14644
- **代码**：未发现公开代码链接

## 一句话结论
DUET 让两个权重完全相同、只在“是否看到禁令”上不同的 teacher 对同一 student rollout 打分，以其逐 token 分歧隔离禁令的因果作用；这为程序化条件门控和 A/B teacher 信号提供了非常干净的 OPD 原型。

## 真正新增的内容
**论文原文**：正 teacher 看见禁令，负 teacher 不看见；两者同权重，因此差异不再混入模型能力差。方法丢弃两 teacher 一致的位置，只在高分歧 token 上把 student 拉向正 teacher、推离负 teacher，并增加正常查询上的 utility-preservation loss。

**分析推断**：将“禁令可见性”换成“环境真值/完整工具返回/隐藏 critique 可见性”，即可构造受控 teacher 对；但只有当两条件除目标变量外完全一致时，分歧才可解释为因果信号。

## 核心方法
对 student on-policy rollout，同时计算正负 teacher 分布的对称 KL；每条序列保留分歧最高的约 10% 位置并做邻域扩张。损失含正向蒸馏、对负 teacher 偏好质量的抑制、沿双 teacher 差异外推的 purified target，以及合法请求上的 top-k KD。

## 关键实验结果
**论文报告**：工业禁令基准覆盖 PII、红线、业务内容、工具定义和 SOP 五类任务。Qwen 1.5B–8B 上禁令遵循率达到 72.3%–85.2%，同时保留 88%–93% 正常效用；SysBench 外部评估改善约束遵循，GSM8K/MATH-500 退化较小。评测集 700 条，其中 200 条使用训练外禁令池；抽样人工验证通过率 98.4%。

## 证据质量与局限
优点是同权重对照消除了 teacher 容量混杂，并同时测过拒绝、改写鲁棒性和过度拒绝。局限是主评估依赖 LLM judge、数据规模有限、没有长时程环境回放；正 teacher 仍可能被错误 student prefix 污染。未报告 sealed evaluator 或多模型 judge 一致性。

## 最接近的相关工作
GKD/MiniLLM、DistiLLM-2、AlignDistil、TIP/SCOPE、RCSD，以及条件 teacher/反事实表征学习。与一般 teacher–student disagreement 不同，DUET 的差异轴是受控上下文变量。

## 如何复用或推进 LLM-as-a-Verifier
用同一 verifier 分别读取“完整证据/删减证据”或“有环境真值/无真值”，把分歧蒸馏为 token、critique 或 score 级监督。A/B/T 可由正负条件下的序数分布差定义；一致位置不必更新。

## 对 Agent verifier × OPD 路线的影响
1. **score-level OPD**：训练完整证据 teacher 与受限证据 teacher 的分数差，而非绝对分数。
2. **A/B/T 与序数分布**：保留整个差分分布，低差异设 Tie。
3. **真值门控**：两 teacher 输入必须只差一个经过程序验证的变量。
4. **student critique states**：在 student 自己触发禁令或工具边界的状态上查询双 teacher。
5. **高熵探索**：只抑制与禁令因果相关的概率质量，不应整体剪掉探索分支。
6. **sealed eval**：训练 judge 与最终合规 evaluator 分离，并用程序检查器验证泄露/工具越界。

## 结论边界
论文支持受控上下文双 teacher 能改善禁令遵循；尚不能证明同样机制能准确估计长轨迹贡献或通用 Agent 价值。
