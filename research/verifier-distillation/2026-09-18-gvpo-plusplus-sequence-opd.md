# GVPO++：支持跨 Tokenizer 与灵活采样的序列级 OPD

- 论文标题：GVPO++: Group Variance Policy Optimization for LLM Post-Training and On-Policy Distillation
- 作者：Kaichen Zhang；Yuzhong Hong；Junwei Bao；Hongfei Jiang；Yang Song；Dingqian Hong；Hui Xiong
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.21432
- DOI：https://doi.org/10.48550/arXiv.2609.21432
- 代码：截至 v1 未见论文提供公开实现仓库

## 一句话结论

GVPO++ 将 reverse-KL OPD 重写为具有解析最优解的 KL 正则奖励优化，在序列级摆脱共享 tokenizer 和重要性采样限制，为异构 teacher 的 score-level OPD 提供了直接优化框架。

## 真正新增的内容

- 【论文原文】这是 NeurIPS 2025 GVPO 的扩展版，新增把 GVPO 系统化扩展到 OPD、扩展 OPD 目标以及更完整的理论和实验。
- 【论文原文】把 teacher–student 序列对数似然比转成奖励，最终得到以组内中心化 log-ratio 差的平方为核心的 GVPD loss。
- 【论文原文】优化在序列级进行，因此 teacher 与 student 无需共享词表或 tokenizer；采样分布也不必严格等于当前 student，无需重要性采样修正。
- 【分析推断】它提供的是“如何稳定吸收一个给定 teacher 分布”的优化器，不自动解决 teacher 信号是否正确、是否来自环境真值或是否与 Agent 目标一致。

## 核心方法

GVPO 从 KL-constrained reward maximization 的解析解推导梯度，使学习目标对组内隐式奖励距离与真实奖励距离做平方匹配。用于 OPD 时，以 teacher 相对任意 reference policy 的 log-ratio 定义 reward，reference 最终相消。扩展目标允许为每个序列设置正权重 f(x,y)；实验用长度归一化权重，证明框架可承载标准 reverse KL 之外的启发式目标。

## 关键实验结果

- 【论文原文】Qwen2.5-Math-1.5B student、DeepSeek-R1-Distill-Llama-8B teacher（不同 tokenizer）时，五个数学 benchmark 平均 35.99；SFT、SeqKD、policy gradient 分别为 19.57、19.06、24.75。
- 【论文原文】同 tokenizer 的 DeepSeek-R1-Distill-Qwen-7B teacher 下，GVPO 平均 35.35；GKD 25.27、MiniLLM 26.22、policy gradient 27.80。
- 【论文原文】post-training 实验中 GVPO 也优于 GRPO；移除解析导出的方差/协方差正则项会不收敛或生成不连贯输出。
- 【论文原文】OPD 实验训练 2 个 epoch，每步 256 prompts、每题 4 个 response，并搜索 3 个学习率；长度权重超参数仍需调节。

## 证据质量与局限

- 【论文原文】包含理论最优性推导、异构 tokenizer 和同 tokenizer 两类 OPD 对照，以及多 benchmark 实验，属于直接 OPD 证据。
- 【论文原文】主要 OPD 实验集中在 1.5B student 与数学推理，扩展权重只用长度归一化作 proof of concept；最优 alpha 随 teacher 变化。
- 【分析推断】论文没有验证长时程工具 Agent、step-level verifier、A/B/T 或环境非平稳条件；理论保证针对给定目标的优化最优性，不保证 teacher/score 的语义正确性。
- 【分析推断】若使用历史/off-policy 轨迹，仍需检查状态分布覆盖和策略漂移，不能把“无需重要性采样”误读成任意旧数据都无偏有效。

## 最接近的相关工作

最接近 GKD、MiniLLM、sequence KD、policy-gradient OPD 以及 GVPO/GRPO。与 CompassOPD 同样处理异构模型族，但 GVPO++ 从序列级目标与优化保证切入；与 TV-Regulated OPD、RA-OPD 相比，它没有内置方向真值门控。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier 对完整 action/critique 候选的概率或序数分布转换为序列级 teacher likelihood，避免不同模型 tokenizer 对齐。扩展权重 f(x,y) 可承载环境成功、Judge 置信区间、动作可恢复性和风险等级，但必须保持为正权重并单独记录门控来源。

## 对现有 Agent verifier × OPD 路线的具体影响

- score-level OPD：优先作为跨模型族 teacher 的序列级 baseline，与 token-level reverse KL 并列比较。
- pairwise A/B/T 与序数分布：把 A/B/T posterior 转成候选序列权重；T 或高不确定样本给低权重，而不是伪造唯一赢家。
- 真值门控：环境真值决定是否允许更新及方向，GVPO 权重负责幅度和稳定优化。
- student-generated critique states：可在 student 自己生成的 critique/action 序列上比较 teacher likelihood，无需 tokenizer 一致。
- 高熵探索：灵活采样允许复用历史或多策略分支，但应保留覆盖约束、版本标签和分支来源。
- sealed eval：优化器与 teacher 一起锁定训练侧；最终效果必须由不参与 f 设计、不可见训练轨迹的独立环境评价。
