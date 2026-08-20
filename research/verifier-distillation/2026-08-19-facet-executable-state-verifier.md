# FACET：以共享可执行状态对齐 Terminal 任务、解法与 Verifier

## 基本信息

- **论文标题**：FACET: Preserving Source Intent and Executable State in Terminal Task Synthesis
- **作者**：Kou Shi、Zun Wang、Qisheng Su、Shiting Huang、Ziao Zhang、Zhen Fang、Qingnan Ren、Jin Liu、Yu Zeng、Yiming Zhao、Lin Chen、Zehui Chen、Feng Zhao
- **首次公开日期**：2026-08-19
- **版本日期**：2026-08-19（v1）
- **arXiv ID**：2608.18580
- **DOI**：10.48550/arXiv.2608.18580
- **论文**：https://arxiv.org/abs/2608.18580
- **代码**：https://github.com/StoKou/FACET-Terminal
- **项目页**：https://stokou.github.io/FACET-Terminal/

## 一句话结论

FACET 先实现并修复容器环境，再从同一已实现状态生成 instruction、reference solution 与 executable verifier，并用定向执行修复维护跨 artifact 一致性；这为 Agent verifier 的程序化真值层提供了比“先写题目或 verifier 再补环境”更可靠的数据构造顺序。

## 真正新增的内容

### 论文原文结论

FACET 从异构 Agent skills 重建带目标、依赖和状态转换的场景，先落地容器环境，再让 instruction、solution、verifier 共享该状态。每个 artifact 失败后仅定向修复失败部分，避免重生成破坏已正确组件。生成任务带密集 executable checks。

### 分析推断

它不做 verifier distillation 或 OPD，但直接解决训练数据中 solution–verifier–environment 假设不一致的问题。对现有 Agent verifier 路线，FACET 更适合作为 teacher 信号的“真值生产层”，而不是 learned Judge 本身。

## 核心方法

1. 将相关 skills 组织为连贯 scenario，保留 source intent、依赖与过程约束。
2. 构建并执行容器环境，修复依赖、文件、工具和初始状态。
3. 基于已实现状态依次生成 instruction、reference solution 与 executable verifier。
4. 执行 solution 与 tests，按 artifact 类型定向修复。
5. 收集通过 verifier 的成功轨迹用于 SFT；任务采用 Harbor/Terminal-Bench 风格封装。

## 关键实验结果

### 论文原文

- 生成 6,078 个验证任务，平均每任务 22.77 个 executable tests，高于列出的其他 terminal 数据集。
- FACET 任务上 teacher rollout P@1 为 27、P@3 为 35，较低 pass rate 与更密集检查一致。
- 从约 6K 任务中筛出 1.2K 完整成功轨迹做 SFT。
- Terminal-Bench 2.1：Qwen3.5-4B 从 17.60 提升到 24.72（+7.12）；9B 从 27.34 到 35.58（+8.24）；27B 从 40.82 到 47.57（+6.75）。
- 顺序式、环境先行构造比 verifier 先行或 joint generation 的 solution–verifier alignment 更好。

## 证据质量与局限

- **质量**：真实容器执行、密集 tests、生成方案消融、多模型尺度 downstream SFT；代码、数据与项目页公开。
- **局限**：只训练成功轨迹，没有验证失败/可恢复轨迹的 score-level 蒸馏；测试数量多不等于覆盖无漏洞；主要外部结果为 Terminal-Bench 2.1；teacher 生成与修复仍可能引入模型偏差；v1 预印本。
- 公开 benchmark 对比中的部分模型来自不同报告/协议，不能把跨行差异完全归因于 FACET。

## 最接近的相关工作

Terminal-Bench、TerminalWorld、Terminal-Lego、SkillSynth、WebGrader，以及可执行环境/自动 verifier 生成与修复。

## 如何推进 LLM-as-a-Verifier

- 将 executable tests 的每个检查项映射为 rubric 维度，输出多维通过分布与剩余约束，而非仅 overall pass。
- 在失败轨迹中定位首次造成最终 test failure 的 state transition，生成可验证 critique。
- 用 LLM Judge 评不可程序化维度时，把容器 state diff 与 test traces 作为 evidence。

## 对 Agent verifier × OPD 路线的具体影响

以下为**分析推断**：

- **Score-level OPD**：以每项 executable check 的通过比例和关键性构成序数 score，再对 teacher dense signal 做门控。
- **A/B/T**：从同一初始容器运行两个候选 action；比较状态差与 tests，均等或互有优劣时输出 T/分布。
- **真值门控**：沿用“环境先实现、verifier 后生成”的顺序，避免 teacher 与 evaluator 共享错误假设。
- **Critique states**：让 student 读取 test failure 和 state diff 生成 critique，再验证下一步是否提高通过项。
- **高熵探索**：多个动作只要满足最终 state constraints 都应保留，不以 reference command sequence 为唯一真值。
- **Sealed eval**：sealed containers、tests 与任务来源完全隔离；训练阶段不可见隐藏 tests，最终 evaluator 不由训练期生成器修复或改写。