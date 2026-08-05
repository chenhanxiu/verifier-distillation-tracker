# Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance

> 来源：「Verifier 蒸馏论文」scheduler 于 2026-08-03 推送、此次补录

## 论文信息

- **标题**：Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance
- **作者**：Zhuowen Han, Jinwei Xiao, Zhengxi Lu, Renren Jin, Zhiyuan Yao, Yuxin Liu, Hongyan Hao, Yueqing Sun, Yu Yang, Qi Gu, Xunliang Cai, Deyi Xiong
- **首次公开/版本**：2026-08-01
- **arXiv**：[2608.00782](https://arxiv.org/abs/2608.00782)
- **HTML 全文**：[arxiv.org/html/2608.00782](https://arxiv.org/html/2608.00782)

## 一句话结论

RSTG 把 OPD 限定在 RL 真正失去梯度的失败组，并在样本和 token 两层做自适应 teacher guidance，是目前最贴近“只在失败处蒸馏”的新结果。

## 真正新增的内容与核心方法

只对全负、零方差的 GRPO groups 启用 OPD，按 teacher confidence 加权；token 层只蒸馏 student 高熵或 teacher–student 分歧大的位置，并用 teacher 正确轨迹 SFT 补充正梯度。

## 关键实验、证据质量与局限

相对 naive GRPO+OPD，在数学和代码上分别提升 +4.02% 与 +3.05%。论文是 2026-08-01 的 arXiv v1；需进一步核对跨模型复现、teacher 调用成本、负组定义和 verifier 错误敏感性。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

可把“negative zero-variance group”映射到 Agent rollout 全失败或 verifier 无区分度的 batch，只在此调用强 teacher。建议比较 always-on OPD、失败组 OPD、confidence-weighted、entropy/divergence token gate，并单列恢复梯度率与单位 teacher 调用收益。

## 建议定位

这篇论文应作为当前研究路线的近期直接证据保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
