# RM-VLM: From Natural-Language Task Descriptions to Vision-Grounded Reward Machines

- **作者**：Roko Parac, Christos Ziakas, Leo Ardon, Alessandra Russo
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.08308
- **DOI**：https://doi.org/10.48550/arXiv.2611.08308
- **代码**：论文页面未给出公开代码链接

## 一句话结论

RM-VLM 用 LLM 将自然语言任务编译成 reward-machine 自动机，再用 VLM 落地图像命题并估计转移进度，为非马尔可夫长任务提供结构化稠密奖励。

## 真正新增的内容

它把 reward machine 原本依赖人工编写的 proposition-grounding oracle 替换为 VLM，并加入 VLM value estimator，为每个自动机转移生成进度型 dense reward，从而连接自然语言规范、视觉状态与时序信用。

## 核心方法

LLM 从任务描述生成自动机；自动机状态表达尚未满足的时序义务。VLM 在图像观测上判断命题是否成立，并估计距离下一状态转移的进度；策略在 RM 引导下学习。

## 关键实验结果

论文在三类非马尔可夫任务上评估：grid-world navigation、机器人操作、3D 物体收集。作者报告 RM-VLM 在所有测试域中均取得高于既有 VLM reward 方法的任务成功率。

## 证据质量与局限

**论文原文结论**：跨三类环境验证，方法结构与非马尔可夫信用问题匹配。  
**局限**：摘要未给出具体数值；LLM 生成的自动机与 VLM 命题识别都可能系统性出错；没有独立程序 oracle 时，dense reward 仍可能被利用；未公开代码。

## 最接近的相关工作

最接近的是 reward machines、LTL/DFA 监督、ContrAgent、MAGS、VLM-as-reward，以及将自然语言规范编译为可执行 verifier 的工作。

## 如何复用或推进 LLM-as-a-Verifier

把 generative verifier 的输出从自由文本 critique 改为“自动机状态、未完成义务、触发证据、置信分布”。在可用时，用程序/环境 oracle覆盖 hard transition；VLM 只为不可直接验证的视觉命题提供软分布。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 可蒸馏每个 RM 转移的分数分布，而非只蒸馏终局 success。
2. pairwise A/B/T 可在共享自动机状态下比较候选动作；命题观测不确定时输出 T。
3. critique states 可显式携带“当前 RM state + 未完成义务 + 图像证据”，便于环境验真。
4. 高熵分叉应在多个合法转移并存时保留探索，而非强迫单一路径。
5. sealed eval 必须冻结独立命题标注器/程序状态，并测试自动机改写与视觉扰动，防止 LLM、VLM 与 policy 共同迎合同一 reward machine。