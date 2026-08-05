# Contrastive On-Policy Distillation

> 来源：历史研究计划 OPD 条目（2026-07-27 整理）

## 论文信息

- **标题**：Contrastive On-Policy Distillation
- **作者**：Jiacheng Ruan, Jun Tang, Wenzhen Yuan, Ting Liu, Shuai Bai, Dayiheng Liu, Zhibo Yang, Yuzhuo Fu
- **首次公开/版本**：2026-07-21
- **arXiv**：[2607.19046](https://arxiv.org/abs/2607.19046)
- **HTML 全文**：[arxiv.org/html/2607.19046](https://arxiv.org/html/2607.19046)

## 一句话结论

COPD 用两个对比上下文下的 teacher log-prob 差构造 token advantage，说明 OPD 可以学习“偏好差”而非复制单一分布。

## 真正新增的内容与核心方法

对同一 student state 分别用 light/heavy reasoning 指令查询 teacher，以 token log-prob 差作为优势，显式偏向更简洁的推理模式；还可做无额外 teacher 的 self-contrast。

## 关键实验、证据质量与局限

九个多模态 benchmark 上显著缩短推理长度且不损性能，跨任务和规模保持效率收益。论文仍标注 work in progress，结论主要围绕 reasoning length，不代表 verifier correctness 改善。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

可把对比上下文换成“有/无环境证据”“正确/错误 rubric”“强/弱 critique”，蒸馏评分差。但要用 sealed eval 检查模型是否只学会迎合提示差异。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
