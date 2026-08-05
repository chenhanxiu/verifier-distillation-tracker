# Entropy-Aware On-Policy Distillation of Language Models

> 来源：历史研究计划 OPD 条目（2026-07-27 整理）

## 论文信息

- **标题**：Entropy-Aware On-Policy Distillation of Language Models
- **作者**：Woogyeol Jin, Taywon Min, Yongjin Yang, Dennis Wei, Yi Zhou, Swanand Ravindra Kadhe, Nathalie Baracaldo, Kimin Lee
- **首次公开/版本**：2026-03-07（v3：2026-06-12；ICML 2026）
- **arXiv**：[2603.07079](https://arxiv.org/abs/2603.07079)
- **HTML 全文**：[arxiv.org/html/2603.07079](https://arxiv.org/html/2603.07079)

## 一句话结论

它把 teacher 高熵分叉视为需要 mode covering 的位置，直接支撑“高熵处保留探索”的设计。

## 真正新增的内容与核心方法

指出标准 reverse KL 的 mode-seeking 会在 teacher 高熵位置损害多样性，因而在高熵 token 加入 forward KL，在确定位置继续精确模仿。

## 关键实验、证据质量与局限

六个数学 benchmark 上，相对基线的 Pass@8 分别提升 +1.37、+2.39、+5.05（Qwen3 0.6B/1.7B/4B），并保持 token entropy。已被 ICML 2026 接收；验证集中于数学，未覆盖真实多工具分叉。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

在评分空间可把高 entropy 解释为“多个评分/解释仍合理”，动态切换散度或降低更新强度。应同时测 pass@k、多样性、校准和 fork survival，避免平均准确率掩盖探索坍缩。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
