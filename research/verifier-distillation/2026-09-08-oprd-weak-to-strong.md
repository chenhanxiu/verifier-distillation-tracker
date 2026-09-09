# Eliciting Weak-to-Strong Generalization with On-Policy Reverse Distillation

## 基本信息

- **作者**：Youngrok Park、Sangmin Bae、Hojung Jung、Jongwoo Ko、Yunseon Choi、Young Jin Kim、Pashmina Cameron、Aaron Courville、Se-Young Yun
- **首次公开日期**：2026-09-08
- **版本日期**：2026-09-08（v1）
- **原始论文**：[arXiv:2609.08798](https://arxiv.org/abs/2609.08798)
- **代码**：未发现公开代码链接

## 一句话结论

OPRD 不把弱 teacher 当作最终目标，而只放大 student 的 verifier 梯度中与 teacher 后训练位移同向的分量，从而保留 verifier 目标的驻点并突破 teacher 上限。

## 真正新增的内容

**论文原文结论：** 以 teacher 相对其 reference policy 的 policy shift 构造指导方向；在 student on-policy rollout 上，仅重标定 verifier-supported policy gradient 与该方向对齐的部分。由于不替换或额外加入 teacher-matching loss，logit 空间的原优化驻点保持不变。

**分析推断：** OPRD 给出了比“KL 模仿 teacher”更安全的 verifier distillation 结构：teacher 只提供方向先验，程序化/verifier reward 保留最终决定权。它尤其适合容量较弱但领域专门化的 verifier/teacher。

## 核心方法

先比较后训练 teacher 与其参考检查点在 student 访问状态上的策略差，得到 teacher direction；再将 student 的 RLVR/GRPO 梯度投影到该方向，并放大同向分量。方法不删除冲突梯度，也不直接拉近 student 与 teacher，因此 teacher 的风格与容量上限不成为优化终点。

## 关键实验结果

Qwen3-4B teacher→Qwen3-8B student 的数学任务五检查点平均为 51.91，强于最强基线 KDRL 的 43.99（+7.92）；四个 Reasoning Gym 平均 55.18，对 KDRL 44.38（+10.80）。AIME24 达 66.92，teacher 为 42.50。1,000 次响应重采样中，对最强基线仍约高 8.0（数学）与 9.9（Reasoning Gym）。论文还报告多 teacher 与 strong-to-weak 扩展。

## 证据质量与局限

**证据质量：中高（预印本内部）。** 有 successive transfer、多 teacher、强弱顺序反转、学习曲线与重采样不确定性。

**局限：** 多 seed 完整后训练因成本未做，1,000 次 bootstrap 只覆盖响应采样而非训练随机性；弱 teacher shift 可包含长度等 reward-irrelevant 偏差，reference checkpoint 选择敏感；若 rollout 组奖励相同导致 verifier gradient 消失，OPRD 无法提供修正。尚未验证长时程工具 Agent。

## 最接近的相关工作

最接近 OPD、KDRL/dGRPO 等蒸馏+RLVR、weak-to-strong generalization、policy-shift transfer 与 gradient surgery。不同点在于 OPRD 只放大 verifier 梯度的对齐分量，不让 teacher loss 改变终点。

## 如何复用或推进 LLM-as-a-Verifier

可把强而昂贵 verifier 的“训练后相对基座变化”蒸馏为指导方向，而由环境 reward 或 sealed judge 产生主梯度。对多个领域 verifier，可按任务路由各自 shift；对 critique verifier，可将建议动作作为方向先验，但只在真实回报梯度支持时放大。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析建议：**

1. 与 score-level KL OPD 并列实现 verifier-gradient × teacher-shift projection，测试是否避免 evaluator 容量上限。
2. A/B/T 或序数分布生成主 advantage；teacher shift 只调幅，不改其正负，保持硬真值门控。
3. student-generated critique state 必须通过 rollout reward 产生非零梯度后才能被 teacher 放大。
4. 高熵分叉保留原 verifier 梯度的正交部分，避免被 teacher 单一路径抹平。
5. 记录 teacher-shift 与 verifier-gradient 的 cosine、长度偏差和零梯度率；sealed eval 使用不参与 shift 构造的环境/评估器，防止共适应。