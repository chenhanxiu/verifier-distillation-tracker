# Communicative On-Policy Distillation: Distilling Black-Box Teacher Capabilities through Communication for Long-Horizon Tasks

- **作者**：Lirui Luo、Kelong Mao、Xinwei Yang、Rongqing Li、Luyu Chen、Kieran Wong、Yudong Guo、Xinrui Wang、Jiayin Zhu、Gu Simiu、Sulong Xu、Cong Fang
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：https://arxiv.org/abs/2611.23673
- **项目页**：https://liruiluo.github.io/communicative-opsd/
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.23673；DOI: 10.48550/arXiv.2611.23673

## 一句话结论

【论文原文】COPD 让 student 在长任务中自主决定何时、如何向只提供文本的黑盒 teacher 求助，再把环境验证成功的对话作为 privileged reference 蒸馏到无 adviser 的新 rollout，绕过 teacher logits 不可得问题。

## 真正新增的内容

【论文原文】把自然语言通信本身变成 OPD 通道：没有固定提问模板或干预日程；只有使用 adviser 且通过原生任务检查的轨迹进入 reference corpus；同一模型的 privileged view 和 deployable view 在 fresh adviser-free prefix 上形成 on-policy self-distillation，并与任务奖励 RL 联训。

## 核心方法

1. Student action space同时包含环境动作与自由文本 communication action。
2. 环境成功筛选 consulted trajectories，保留请求、回复、动作和观察。
3. privileged policy 读取成功咨询记录，deployable policy 不读取，两者在 student 新前缀上做分布对齐。
4. 与 task-reward PPO 联合训练，部署时关闭 adviser。

## 关键实验结果

【论文原文】CAMG-II 上 COPD-4B adviser-free 平均 59.8，初始模型 45.3，最强黑盒 OPD 基线 ActionOPD 为 51.2；相对起点的增益为基线的 2.46 倍。去掉 OPSD 降至 47.5，SFT 替代 OPSD 为 55.4。Terminal-Bench 2.1 上 4B/9B 从 23.1 提至 28.0/33.0，SWE-Bench Pro V2 从 11.2/23.1 提至 16.5/27.5。

## 证据质量与局限

【论文原文】有多域、多个 OPD 基线、关键消融和无 adviser 评测；但成功筛选会遗漏“咨询有价值但任务仍失败”的中间状态，Visual 域使用 Judge grade 而非纯程序真值。Teacher 直接执行仍为 80.7，student 尚未逼近其上限。

## 最接近的相关工作

接近 ActionOPD、ROPD、OmniOPD、GAD、OLIVE、privileged self-distillation、DAgger 与 interactive imitation learning。区别是无需 logits，student 自主生成咨询状态并在部署前内化建议。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 verifier/teacher 的自然语言回复视为 privileged critique state：student 在高熵分叉主动提问，环境真值决定是否保留；再蒸馏 adviser-visible 与 adviser-free 的 score/策略差。可进一步要求 adviser 输出 A/B/T 和序数分布，而不只给自由文本建议。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：新增“黑盒 critique→privileged score→student fresh rollout”路径，不依赖 teacher logits。
- **pairwise A/B/T 与序数分布**：咨询可请求分支比较与评分分布；环境结果负责校正方向。
- **程序化/环境真值门控**：只有原生任务 verifier 通过的咨询轨迹进入主蒸馏池；失败咨询另存为审计数据。
- **student-generated critique states**：论文直接证明 student 自主产生何时问、问什么可成为监督单元。
- **高熵分叉探索**：把策略熵、verifier 分歧和预计咨询价值联合成触发器，避免固定干预日程。
- **sealed eval**：关闭 adviser，并使用未见任务与独立环境/Judge；训练咨询记录不得进入 sealed context。
