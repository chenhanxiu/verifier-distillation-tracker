# Waypoint-OPD：用 RL 训练途中的方向一致性门控策略位移蒸馏

- **论文标题**：Waypoint-OPD: Transferring RL-Induced Policy Shifts via Gated On-Policy Distillation
- **作者**：Bingxi Hou, Guochao Jiang, Guofeng Quan, Weiqing Li, Wenfeng Feng, Guohua Liu, Yuewei Zhang
- **首次公开日期**：2026-10-15
- **版本日期**：2026-10-15（v1）
- **原始论文**：https://arxiv.org/abs/2610.21601
- **代码**：论文页面未提供公开代码链接

## 一句话结论

仅迁移 RL 前后 endpoint 位移会混入训练途中反复翻转的偏好；Waypoint-OPD 用中间 checkpoint 检查早期与晚期位移是否同向，再门控 student 访问状态上的 endpoint shift。

## 真正新增的内容

**论文原文**：引入同一 teacher RL 轨迹中的中间 checkpoint，把“base→waypoint”与“waypoint→endpoint”的相对动作偏好方向做比较；若两段方向冲突，则抑制最终位移，只多一次冻结 teacher 的打分 pass。

**分析推断**：这提供了比单一 teacher–student gap 更可信的 score-level OPD 可靠性指标：稳定积累的偏好应强蒸馏，训练过程中来回翻转的偏好应降权或保留探索。

## 核心方法

在 student-generated prefixes 上同时计算 teacher 基座、中间 checkpoint 与最终 checkpoint 的 log-prob；将 endpoint policy shift 乘以由早晚位移方向一致性得到的 gate，再更新 student。

## 关键实验结果

**论文原文**：使用 RL 训练的 Qwen3-4B teacher，面向 Qwen3-8B、14B 与 30B-A3B student，在数学和代码共六个 domain–student 设置中，Waypoint-OPD 的域平均分均为所比较蒸馏方法最高；8B 消融中移除或打乱 gate 会降低数学推理表现。

## 证据质量与局限

覆盖三个 student 尺度和两个领域，且有 gate 消融；但仍局限于同模型族和单条 RL 训练路径。方向一致并不等于正确，若 RL reward 被黑客化，稳定偏移也可能稳定地错误。

## 最接近的相关工作

与 RISE 的 checkpoint 位移外推、Lightning Weave 的相对能力位移组合、TV-Regulated OPD 的方向优先，以及 OPRD/CompassOPD 的门控式策略迁移最接近。

## 如何复用或推进 LLM-as-a-Verifier

可将 verifier 训练过程中的 early/mid/final checkpoints 视为三点测量：只有评分方向在 sealed truth 子集上稳定且校准不恶化时，才向 student 蒸馏该状态；同时保留 gate 值作为分布不确定性而不是二值丢弃。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：把 waypoint directional agreement 加入现有 teacher gap、student entropy 和执行真值三因素 gate。
- **A/B/T**：早晚同向映射 A/B，方向冲突映射 T；T 状态不做强制排序。
- **真值门控**：先用程序/环境真值校验 endpoint 方向，再用 waypoint 一致性调节幅度。
- **critique states**：只把跨 checkpoint 保持同向且有证据指针的 critique 写回状态。
- **高熵探索**：方向冲突是值得分叉采样的信号，而非应立即删除的数据。
- **sealed eval**：中间 checkpoint、门控阈值和 final evaluator 需分离；另测 reward hacking 下“稳定但错误”的位移。
