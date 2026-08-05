# Asymmetric On-Policy Distillation: Bridging Exploitation and Imitation at the Token Level

> 来源：历史研究计划 OPD 条目（2026-07-27 整理）

## 论文信息

- **标题**：Asymmetric On-Policy Distillation: Bridging Exploitation and Imitation at the Token Level
- **作者**：Nan Jia, Haojin Yang, Xing Ma, Jiesong Lian, Shuailiang Zhang, Weipeng Zhang, Ke Zeng, Xunliang Cai, Zequn Sun
- **首次公开/版本**：2026-05-07（v3：2026-05-13）
- **arXiv**：[2605.06387](https://arxiv.org/abs/2605.06387)
- **HTML 全文**：[arxiv.org/html/2605.06387](https://arxiv.org/html/2605.06387)

## 一句话结论

AOPD 的不对称更新说明：正优势适合强化，非正优势区域更适合局部模仿，而不是一律施加负强化。

## 真正新增的内容与核心方法

针对高方差、零优势梯度消失和探索瓶颈，在 positive-advantage token 保留 policy gradient，在 non-positive 区域改用局部 divergence minimization。

## 关键实验、证据质量与局限

数学推理中强/弱初始化平均提升 4.09/8.34，并在连续工具适配中保持更高 entropy 与能力留存。局限是 advantage 与 verifier 误差耦合，错误符号可能系统性放大。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

在 A/B/T 或序数 reward 下可按 advantage sign 选择更新：确定正例强化，模糊/负例用受限分布匹配或 abstain。必须加入 advantage calibration 与错误门控消融。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
