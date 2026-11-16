# Learn then Bet: Learning Interpretable Rules for Reliable Agent Intervention

- **作者**：You-Lin Chen、Xinyi Lisa Chen、Pedro Herrero-Vidal、Xiaojing Yu、Bingqing Song、Bin Xu
- **首次公开日期**：2026-11-13
- **版本日期**：2026-11-13（v1）
- **原始论文**：https://arxiv.org/abs/2611.17662
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.17662；DOI: 10.48550/arXiv.2611.17662

## 一句话结论

【论文原文】LeBet 从部分轨迹学习可解释的 OR-of-AND 运行时规则，并用固定 betting statistic 累积证据，在有限样本条件下控制误干预，同时节省 34.46% token。

## 真正新增的内容

【论文原文】方法不把“是否停止/升级 Agent”当普通二分类，而是从有效且有力的干预充分条件反推学习目标；同一批轨迹可同时用于规则学习与校准，并在有限类内交换性和 leave-one-out 稳定性条件下给出训练条件化的误报与检测力保证。

【分析推断】这提供了一个可落地的 distributional process verifier 原型：逐步证据不是立即压成二元失败标签，而是累积到阈值后再触发动作。其 betting statistic 可作为 score-level OPD 的校准轨迹风险，而规则则可提供可审计的 critique state。

## 核心方法

1. 从成功/失败的部分历史中学习 OR-of-AND 布尔监控器。
2. 用随机局部搜索编辑规则，优化经验分离并满足有效/有力干预条件。
3. 在线把匹配证据输入固定 betting statistic，达到预设阈值才停止、升级或辅助。

## 关键实验结果

【论文原文】在 SWE-bench Lite、Ministral 3 8B 上，LeBet 节省 34.46% 输入加输出 token，输出 precision 从 18.33% 提升到 21.59%，经验 false-positive rate 为 13.64%。理论保证依赖有限类内交换性与 leave-one-out 稳定性。

## 证据质量与局限

【论文原文】优点是把学习、校准与运行时触发连接到明确的有限样本条件，并给出真实 coding-agent 实验。

【分析推断】单模型、SWE-bench Lite 和较低的绝对 precision 限制了外推；13.64% 的经验误报是否可接受取决于升级成本。交换性与稳定性在持续更新的 Agent 策略下容易破坏，必须做时间切分和策略版本外测试。

## 最接近的相关工作

最接近的是 FARM 的逐步失败概率、AutoTuneBench 的冻结测量、Agent 轨迹可诊断性的 abstention，以及 FLARE 的长轨迹因果错误链。LeBet 的独特点是以可解释规则和 betting process 给出运行时干预保证，而非只预测一个风险分数。

## 如何复用或推进 LLM-as-a-Verifier

让 generative verifier 产生候选可解释事件，程序解析器将其转成布尔特征；LeBet 只在证据累积充分时作硬干预。可再把 betting statistic 的区间或分位数蒸馏到小 verifier，同时保留规则原文供审计。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：用累计 betting evidence 代替未经校准的单步分数；阈值附近降低更新幅度。
- **pairwise A/B/T 与序数分布**：对“继续/升级/停止”构造序数动作分布；证据未过阈值时标 T。
- **环境真值门控**：规则特征优先来自测试、退出码、状态断言等程序真值，语言特征只能作软证据。
- **student-generated critique states**：只接纳能被规则谓词或环境事件复核的 critique。
- **高熵探索**：未积累足够失败证据前继续探索，避免把短期异常当不可恢复失败。
- **sealed eval**：以新仓库、后续策略版本和时间外任务冻结阈值，分别报告误报、漏报、节省成本与终局成功率。

