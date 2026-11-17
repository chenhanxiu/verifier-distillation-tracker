# SPLICE: Structured Prompt Local Iterative Combinatorial Evolution

- **作者**：Anish Acharya、Phillip Studans、Amit Dhanda、Sina Amini Niaki、Ninad Vivek Rao、Vishal Amarlal Khatri、Brian Verkhovsky
- **首次公开日期**：2026-11-13
- **版本日期**：2026-11-13（v1）
- **原始论文**：https://arxiv.org/abs/2611.18883
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.18883；DOI: 10.48550/arXiv.2611.18883

## 一句话结论

【论文原文】SPLICE 把 prompt 优化改造成分块、选择性可变的组合搜索，形式保证冻结契约不漂移、leader 不在验证集退化，并保留来自不同父代的竞争候选。

## 真正新增的内容

【论文原文】作者把全局 prompt rewrite 的三类失败——契约漂移、beam 单一谱系坍缩、无界膨胀——分别映射到可证明机制：per-block mutability、带 diversity slots 的 elitist beam，以及 ratio length regularizer；候选由双重 section-local textual gradient 提出。

【分析推断】它不是 verifier 蒸馏算法，但直接解决 evaluator/critic 驱动的 Agent 自更新如何避免共适应与探索坍缩。冻结 rubric、工具 schema 和 sealed-eval 接口可沿用同样的 protected blocks。

## 核心方法

1. 将系统提示、工具说明、契约和示例拆为结构化 block，只开放指定 block。
2. 在 edit graph 上做 elitist beam search，并为不同父代保留 diversity slot。
3. 用局部 critique gradient 提案，并以长度正则控制性能—膨胀偏差。

## 关键实验结果

【论文原文】在 5 个复现实验协议、7 个公开基准上，SPLICE 在 4 个取胜、3 个追平最强先前方法。生产式 contract stress test 中，它保留了无约束优化器为提高 proxy metric 而牺牲的契约条款；消融把收益归因于 critique 和 elitist search。

## 证据质量与局限

【论文原文】含多协议、多基准、契约压力测试、消融及多项理论界。

【分析推断】验证集 leader 不退化不代表 sealed test 不退化；形式保证也依赖 block 划分和 proposal competence。若真正关键的规范被错误放入可变 block，仍会发生 evaluator 共适应。

## 最接近的相关工作

最接近 EvoTrias 的受保护判断层、Evidence-Governed Adoption、AutoTuneBench 与 DDO/EPIG-Tree 的探索保持。SPLICE 的区别是把保护、谱系多样性和长度控制统一进 prompt edit graph。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier rubric、硬真值接口和 sealed-eval 描述设为不可变 block，只允许证据提取与解释模板演化；每轮同时保留独立父代，并要求新 verifier 在冻结回归集上不退化。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：冻结 score 定义与硬门控，只优化可解释的软评分 block。
- **pairwise A/B/T 与序数分布**：A/B/T 语义作为契约 block 不允许被优化器改写。
- **环境真值门控**：工具 schema、状态断言和验收条件全部设为 protected blocks。
- **student-generated critique states**：critique 只能提议局部修改，不能覆盖准入契约。
- **高熵探索**：diversity slots 保留不同父代，防止 verifier 优化坍缩到单一路线。
- **sealed eval**：验证集只作搜索门，最终用不可见任务与冻结 evaluator 检查真实回归。

