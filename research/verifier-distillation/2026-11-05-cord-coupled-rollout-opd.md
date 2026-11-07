# CoRD: Coupled Rollouts Fill the Blind Spot of On-Policy Distillation

- **作者**：Guhan Chen, Bohan Li, Jun Rao, Hejin Wang, Songtao Tian, Yexin Xie, Xiaojun Meng, Peng Yuan, Jiansheng Wei, Xuebo Liu, Zixiong Yu
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.07959
- **DOI**：https://doi.org/10.48550/arXiv.2611.07959
- **代码**：论文页面未给出公开代码链接

## 一句话结论

CoRD 保留 on-policy loss，但用最大耦合的 speculative sampling 最少量地把 student rollout 推向 teacher 可达状态，补足纯 OPD 永远看不到的 teacher-only 状态。

## 真正新增的内容

它没有改蒸馏目标，而是改训练状态分布：student 与 teacher 同意时保留 student token，仅在分歧时从 student 低估的剩余 teacher 质量中替换，因此干预频率达到精确采样下的最小值并随学习递减。

## 核心方法

以 student/teacher 分布的最大耦合构造几何插值 rollout；在耦合后的状态上继续使用标准 on-policy distillation loss，从而分离“状态覆盖”与“目标函数”两件事。

## 关键实验结果

- 六个 base student、两模型族（Qwen3/Qwen3.5，0.6B–4B）、五个数学 benchmark。
- 等训练步数与数据下，平均 pass@1 比 OPD 高 **0.9–2.0 点**，pass@8 高 **1.2–3.4 点**。
- 4B student 在 teacher-reached 冻结状态上 16 步达到的 gap closure，普通 OPD 80 步仍未达到。

## 证据质量与局限

多模型、多规模且有替换方向对照，证据较强；但实验是数学推理，不含有副作用的工具环境，teacher-reached 状态也未必环境可行，且未报告独立 sealed evaluator 下的策略多样性。

## 最接近的相关工作

最接近 Frontier-OPD、AC-OPD、SOPD、ATI-OPD、SpecOPD 与 DAgger 式状态分布校正。

## 如何复用或推进 LLM-as-a-Verifier

在 Agent 环境中只对可回滚状态使用耦合干预；teacher token 替换后先让程序/环境 oracle 验证状态合法，再蒸馏 verifier 的 score 分布与 critique。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. 将“student-only on-policy”扩展为最小 teacher 干预的耦合状态采样。
2. 被替换/未替换的同状态后缀天然形成 A/B/T 数据。
3. teacher intervention 只有通过环境真值门控才进入 critique memory。
4. 分歧大时保留多条耦合分支，避免单一路径覆盖探索。
5. sealed eval 分别报告纯 student、耦合训练和无干预部署，防止训练态收益被错误外推。