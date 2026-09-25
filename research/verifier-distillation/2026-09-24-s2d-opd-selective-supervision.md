# Not Every Token Is Worth Distilling: Selective Supervision for Direct-OPD

## 基本信息

- **方法简称**：S²D-OPD
- **作者**：Yibo Zhao、Zixuan Yang、Yunshi Lan、Xiang Li
- **首次公开日期**：2026-09-24
- **版本日期**：2026-09-24（v1）
- **原始论文**：https://arxiv.org/abs/2609.29142
- **DOI**：https://doi.org/10.48550/arXiv.2609.29142
- **代码**：https://anonymous.4open.science/r/S2D-OPD-8868

## 一句话结论

Direct-OPD 的 log-ratio 可能在 teacher 实际行为几乎未变时仍给出同样奖励；用 teacher/reference JSD 只保留变化最大的 10% student states，效果反而更好。

## 真正新增的内容

【论文原文】给出精确构造：当 teacher 两 checkpoint 对 student 候选 token 的共同概率质量趋近零时，Direct-OPD reward 与更新可不变，但 JSD 和双向 KL 均趋零；据此提出按 teacher-reference JSD 排序并屏蔽低分歧状态的 S²D-OPD。

【分析推断】这把 OPD 的“监督存在”与“teacher 在此状态确实学到了新东西”区分开，是 score-level verifier distillation 的直接可靠性门控。

## 核心方法

【论文原文】在 student 自己生成的状态上计算 post-RL teacher 与 pre-RL reference 的 JSD；每个响应只保留 JSD 最高的 10% 状态用于 Direct-OPD，其余 token 不施加该监督，不增加额外 forward pass。

## 关键实验结果

【论文原文】覆盖两组 teacher pair、四个 1.7B–8B student；在 AIME/HMMT held-out accuracy 的八个设置中，七个优于 dense Direct-OPD，一个持平。

## 证据质量与局限

有理论反例、多 teacher/student 和 held-out 实验，证据较完整；但只测试数学推理，固定 top-10% 是否适合长轨迹 Agent 未知。JSD 只说明 policy change 大，不保证变化正确，必须再由硬真值或可靠 verifier 判方向。

## 最接近的相关工作

与 Direct-OPD、IWD 的不变性加权、TV-Regulated OPD 的方向优先、Unified Per-Token OPD Gating 和 VG-OPD 最接近。S²D-OPD 的独点是以 teacher 学前/学后行为变化筛选 student state。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】对 verifier teacher 也保留 pre/post checkpoint：只有其序数评分分布或 A/B/T 分布在某状态产生足够 JSD，且程序真值支持变化方向时，才蒸馏给 student verifier。低 JSD 输出 T 或零权重。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- 把 teacher `post-vs-pre JSD` 加入 score-level OPD 样本门控。
- JSD 负责“是否值得学”，环境真值负责“方向是否正确”。
- 对高熵分叉保留未被选中的候选，不把 mask 等同负标签。
- 比较固定 10%、自适应阈值和 conformal 区间三种选择规则。
- sealed eval 必须使用独立 teacher 快照和未曝光轨迹，避免共适应制造虚假高 JSD。