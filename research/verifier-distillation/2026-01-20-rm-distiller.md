# RM-Distiller: Exploiting Generative LLM for Reward Model Distillation

> 来源：历史研究计划核心条目（2026-07-27 整理）

## 论文信息

- **标题**：RM-Distiller: Exploiting Generative LLM for Reward Model Distillation
- **作者**：Hongli Zhou, Hui Huang, Wei Liu, Chenglong Wang, Xingyuan Bu, Lvyuan Han, Fuhai Song, Muyun Yang, Wenhao Jiang, Hailong Cao, Tiejun Zhao
- **首次公开/版本**：2026-01-20（v2：2026-07-26；IJCAI-ECAI 2026）
- **arXiv**：[2601.14032](https://arxiv.org/abs/2601.14032)
- **HTML 全文**：[arxiv.org/html/2601.14032](https://arxiv.org/html/2601.14032)

## 一句话结论

它是 reward-model distillation 的直接基线，但主要仍是离线 teacher 能力利用，并未解决 student-state on-policy 分布迁移。

## 真正新增的内容与核心方法

同时利用生成式 teacher 的三种能力：合成细粒度对比 response pairs、给出偏好强度以训练 margin-aware objective、用生成分布正则化 reward model 的语言能力。

## 关键实验、证据质量与局限

在 reward-model benchmark 与基于 RL 的对齐实验中优于传统蒸馏，并被 IJCAI-ECAI 2026 接收。局限是 teacher 信号混合较多，尚不能证明哪部分对长 Agent 轨迹和校准最关键。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

应作为 off-policy RM distillation 基线，与 student-generated critique states 上的 score-level OPD 对比。可复用 teacher 的 pair refinement 与强度评分，但需要加入真实工具执行结果和 sealed eval，防止只模仿 teacher 偏差。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
