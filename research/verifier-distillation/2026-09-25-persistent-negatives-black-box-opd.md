# Persistent Negatives for Adversarial Black-Box On-Policy Distillation

- **作者**：Haixu Ma, Saad Lahrichi, Weiwei Li, Kevin Han, Weiqiang Wu, Peggy Yang, Dongzhuo Li, Ruiyi Li, Serena Li, Gedi Zhou, Mingze Gao, Abhishek Kumar, Xiangjun Fan, Lizhu Zhang
- **首次公开日期**：2026-09-25
- **版本日期**：2026-09-25（v1）
- **原始论文**：https://arxiv.org/abs/2609.30864
- **代码**：未公开

## 一句话结论

【论文原文】在只有 teacher 样本、没有 token 概率的黑盒 OPD 中，将历史 student 负样本持续注入 discriminator，可锚定不断移动的奖励分布，同时保持 GRPO 使用最新 on-policy 样本。

## 真正新增的内容

【论文原文】论文指出 adversarial distillation 的关键不稳定源不是只有 discriminator 容量，而是每次 policy 更新都会改写负样本分布；它提出 live pool，并给出 Bayes 最优奖励等于 teacher/negative 对数密度比及历史负样本降低奖励估计 MSE 的条件性分析。

## 核心方法

1. 以 prompt-matched teacher 与 student 输出训练 discriminator。
2. 每批将一部分最新负样本替换为历史 teacher–student 比较。
3. discriminator 同时学习新旧策略边界；GRPO 奖励仍仅施加在最新 student rollout 上。
4. 在匹配 discriminator 计算量下比较 fresh-only 与 persistent-negative 训练。

## 关键实验结果

【论文原文】跨两个 student 家族、三个 Judge、四个 judged-chat benchmark，在匹配 discriminator 计算量下持续优于现有方法；fresh-policy discriminator 曲线更平滑，低于随机水平的下探更少。摘要未给出统一的绝对提升值。

## 证据质量与局限

【论文原文】理论结果明确列有假设，实验覆盖多模型与多 Judge，且控制 discriminator compute。局限是任务依赖 judged-chat 分数而非可执行环境真值，历史池可能保留旧偏差或泄漏策略版本；未报告长时程 Agent 和独立 sealed evaluator，代码也未公开。

## 最接近的相关工作

最接近黑盒 adversarial distillation、GLARE 的当前策略负样本与 replay-buffer 稳定化；也与 reward-model continual learning、off-policy correction 相邻。其区别是只让奖励模型看历史，而策略更新仍保持 fresh on-policy。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把 live pool 扩展为版本化的 Agent 失败档案：保存状态、动作、critique、环境证书与当时 policy hash，让 generative verifier 学习跨版本稳定的错误边界；同时用最近策略数据校准当前部署分布。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：用历史池稳定 score teacher，但策略梯度只对当前 rollout 生效。
- **A/B/T 与序数分布**：历史比较应保留 T/不确定与完整评分分布，避免旧二元标签固化。
- **真值门控**：池中样本须附程序/环境结算；硬真值决定正负方向，discriminator 只补充稠密幅度。
- **Critique states**：版本化保存 student-generated critique，检验 verifier 是否对旧失败仍保持判别力。
- **探索**：池采样按策略距离和高熵分叉分层，不能让常见旧失败淹没新状态。
- **Sealed eval**：最终测试轨迹不得回流 live pool，并按 policy/verifier 版本审计 evaluator 共适应。
