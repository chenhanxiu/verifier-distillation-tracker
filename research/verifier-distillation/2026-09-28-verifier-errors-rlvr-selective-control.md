# Verifier Errors in RLVR: Reward Hacking, Limits of Feedback, and Selective Control

- **作者**：Christian Moya, Elliott Thornley, Guang Lin
- **首次公开日期**：2026-09-28
- **版本日期**：2026-09-28（v1）
- **原始论文**：https://arxiv.org/abs/2609.35677
- **代码**：未在 arXiv 页面提供

## 一句话结论

【论文原文】固定 imperfect verifier 下，RLVR 可出现奖励上升而正确率下降，且仅凭训练中可见信号一般无法识别已被错误接受的答案；必须引入独立正确性审计。

## 真正新增的内容

【论文原文】论文给出 reward hacking 的梯度条件与不可识别性结果，并构造基于部分审计反馈的 selective control，在当前策略处同时降低 accepted errors、提高正确响应概率。

## 核心方法

1. 用固定 verifier 的梯度流刻画错误奖励压力。\n2. 证明 RLVR 内部观察不足以普遍检测 accepted error。\n3. 从独立 audit 获取额外 correctness feedback。\n4. 当纠正强度超过错误奖励压力时，选择性压低错误并提升正确。

## 关键实验结果

【论文原文】在线性/神经 contextual bandit 与语言模型实验中，部分审计的 selective control 同时减少 accepted errors、提高 correctness；摘要未给统一绝对提升值。

## 证据质量与局限

【论文原文】理论清楚区分可观测奖励与真实正确性，并以多级模型验证。局限是语言模型实验规模和任务细节在摘要中有限；结论是局部 current-policy 控制，不代表训练全程或分布外保证。

## 最接近的相关工作

最接近 Proof-Carrying Cognition、GLARE、Monitoring Reward Hacking 与 AutoTuneBench；区别是给出仅靠 RLVR 反馈无法保证纠错的理论边界。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】为线上 verifier 训练保留一小部分独立人工/程序 audit 流，专门估计 false acceptance；audit 只用于校正和监控，不回流主 Judge 的自举标签。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：主 score 必须附 false-acceptance 校正项。\n- **A/B/T 与序数分布**：无法识别的 accepted error 应增加 T/审计路由概率。\n- **真值门控**：独立 correctness audit 是必要信号。\n- **Critique states**：被 verifier 接受的 critique 仍需抽样验真。\n- **探索**：纠错需避免同时压制正确的异质路径。\n- **Sealed eval**：保留从未用于控制器训练的错误接受测试集。
