# Data-free On-policy Distillation

## 基本信息

- **作者**：Gengsheng Li；Mao Zheng；Mingyang Song；Jie Sun；Zeyuan Liu；Ruiqi Liu；Qiyong Zhong；Haiyun Guo；Junfeng Fang；Jinqiao Wang
- **首次公开日期**：2026-09-12
- **版本日期**：2026-09-12（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.14193
- **代码**：未发现公开代码链接

## 一句话结论

【论文原文】OPD 的关键覆盖单位更像 student 实际到达的状态而非输入 prompt；teacher 自生成极少量问题即可触发广泛能力迁移，无需外部训练集或复杂过滤。

## 真正新增的内容

【论文原文】论文首次系统展示 data-free OPD：由 teacher 自行生成问题，student 在这些问题上 on-policy 采样，再从 teacher 分布蒸馏。仅 8 个 prompt 即可匹配约 17k 条数据的训练效果；跨域编程 prompt 也能恢复超过 90% 的域内增益。

【分析推断】结果把数据选择问题从“收集多少题”改写为“是否触达关键决策状态”，与 One-Shot OPD 的状态覆盖结论形成直接呼应。

## 核心方法

1. teacher 自主生成少量任务，无需外部语料、标签或额外过滤器。
2. student 基于这些任务产生 on-policy 轨迹。
3. teacher 对 student 已访问状态给出分布监督，以 OPD 更新 student。
4. 多 teacher 设置中，各 teacher 可生成自身擅长领域的问题并共同蒸馏。

## 关键实验结果

【论文原文】8 个 prompt 匹配约 17k 条数据的效果；使用编程问题进行跨域蒸馏仍恢复超过 90% 的域内收益。在多 teacher 实验中，1k 个自生成问题关闭 98.5% 的能力差距，而 7k 个真实问题关闭 96.6%。

【证据边界】这些数字支持“状态覆盖优先”，但不等于任意 8 个任务都足够，也未证明在长时程、部分可观测 Agent 环境中同样样本高效。

## 证据质量与局限

- **质量**：包含极小数据、跨域和多 teacher 对照，能排除“只是复用大规模域内数据”的解释。
- **局限**：teacher 同时生成任务与提供监督，可能形成 teacher-centric 状态分布；没有环境真值时，错误题目或错误解释可共同自洽。
- **风险**：状态覆盖以模型内部或行为相似度度量时，可能遗漏低频但高代价的 Agent 分叉。

## 最接近的相关工作

One-Shot OPD、开放域多 teacher OPD、teacher-generated curriculum、SAGE 的高熵状态选择，以及 EnvHarness/LURE 的学生失败驱动任务生成。本文区别在于不依赖外部数据，且把极少 prompt 的广泛迁移作为主要结论。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】让 generative verifier 不仅给分，还针对当前 student 的低覆盖状态生成“最小反例任务”。随后用环境 oracle 对生成任务和终态验真，再将 verifier 的序数评分分布蒸馏到轻量 student verifier。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- 以**状态覆盖率**而非 prompt 数量作为数据预算横轴。
- 从高熵分叉、首个不可恢复错误和 critique 冲突处生成任务，优先补齐稀缺状态。
- teacher 自生成任务必须经过程序化可执行性、初始状态一致性和终态 oracle 门控。
- 对同一 state 采样多个可行行动，构造 A/B/T；Tie 与高不确定状态保留探索，不做强 KL。
- 建立完全独立的 sealed task generator 与 evaluator，避免训练 teacher 通过生成“自己会判的题”制造虚高。