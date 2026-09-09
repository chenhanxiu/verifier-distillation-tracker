# UniRRM: Unified Reasoning Reward Models Across Languages and Evaluation Paradigms

## 基本信息

- **作者**：Peng Lai、Yichao Du、Junchao Wu、Weibo Gao、Linan Yue、Longyue Wang、Weihua Luo、Derek F. Wong、Guanhua Chen
- **首次公开日期**：2026-09-05
- **版本日期**：2026-09-05（v1）
- **原始论文**：[arXiv:2609.05910](https://arxiv.org/abs/2609.05910)
- **代码**：[sustech-nlp/UniRRM](https://github.com/sustech-nlp/UniRRM)
- **数据/模型**：论文页面提供 MixReward 与 UniRRM 的 Hugging Face 链接

## 一句话结论

UniRRM 用动态生成的通用+指令特定 rubric 统一 pointwise、pairwise、listwise 和 103 种语言，为多协议生成式 verifier 蒸馏提供了可复用 teacher。

## 真正新增的内容

**论文原文结论：** MixReward 汇集 9 个数据源、6 个领域、103 种语言，并将 pairwise 数据扩展为 listwise；UniRRM 通过分阶段推理链动态生成 task-generic 与 instruction-specific criteria，再统一完成不同评价协议。8B/14B 模型在多项 judge/reward benchmark 接近同规模 SOTA，并迁移到训练未见的 pointwise 协议。

**分析推断：** 其最大价值不是单一榜单分数，而是可从同一 teacher 同时抽取绝对分数、A/B/T/排序与 rubric/critique，使 score-level OPD 和序数分布蒸馏共享语义锚点。

## 核心方法

数据管线先按语义密度/数学难度筛选，识别并扩展语言；用 Qwen3-235B-A22B-Thinking 与 GPT-OSS-120B 检查原文及翻译后偏好顺序，保留高一致样本；再由 Gemini-2.5-Flash 生成 listwise 负例。模型采用 staged reasoning：分析任务、生成自适应标准、逐项判断并输出协议所需结果，训练结合 SFT 与 GRPO。

## 关键实验结果

pointwise 评测中，UniRRM-8B 在 RWBench、M-RMBench、MM-Eval、JudgeBench 平均准确率 0.734；14B 为 0.771，而 Qwen3-14B 与 M-Prometheus-14B 均为 0.723。论文还在 pairwise/listwise、多语言基准上报告接近同规模最优及未见协议迁移。

## 证据质量与局限

**证据质量：中高。** 覆盖多协议、多语言、多基准，开放代码、数据与模型，且有消融。

**局限：** 大量多语数据来自机器翻译，偏好与 listwise 扩展依赖强模型过滤，可能继承同源偏差；pointwise benchmark 的“真值”部分来自闭源模型伪标签，论文自己也指出全局分数缺乏跨样本统一校准。没有长时程 Agent 轨迹、环境真值或在线蒸馏实验，因此对 Agent 的作用仍是外推。

## 最接近的相关工作

最接近 JudgeLRM、RubricRM、RM-R1、RewardAnything、M-Prometheus 与多语言 judge。它把动态 rubric、生成式解释、pair/list/point 多协议与多语言训练合并到单一模型。

## 如何复用或推进 LLM-as-a-Verifier

可直接作为昂贵 teacher，在同一 student trajectory state 上同时生成：原子 rubric、pointwise 序数分布、候选动作 pair/list 排序与自然语言 critique。训练 student 时应保留协议一致性约束，并对 T/并列、遗漏义务和跨语言 paraphrase 做专门校准。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析建议：**

1. 用同一 UniRRM teacher 生成 score、A/B/T 和 listwise 标签，比较单协议与联合协议蒸馏。
2. 将动态 rubric 输出写入 student-generated critique state，但仅在程序/环境检查通过时纳入训练。
3. 用 ordinal bins 或 cumulative-link head 保留 pointwise 分布，不把生成的整数分数当精确连续值。
4. 高熵或协议间不一致状态保留多分支 rollout，并路由到更强 verifier。
5. sealed eval 必须采用独立人工/可执行真值以及未参与 MixReward 过滤的 judge，另做跨语言等义与顺序交换测试，防止 evaluator 共适应。