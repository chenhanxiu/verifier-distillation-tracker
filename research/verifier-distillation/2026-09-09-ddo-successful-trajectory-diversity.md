# DDO：在偏好后训练中保留多样成功轨迹

- **论文标题**：Direct Diversity Optimization for Diverse Successful Trajectories in Preference Post-Training
- **作者**：Junwon Ko, Dong-Jae Lee, Minchan Kwon, Sunghyun Baek, Junmo Kim
- **首次公开日期**：2026-09-09
- **版本日期**：2026-09-09（v1）
- **原始论文**：https://arxiv.org/abs/2609.10052
- **代码**：https://github.com/koguma00/direct_diverse_optimization

## 一句话结论

DDO 从同一决策状态构造带结果标签的分叉树，并以 reference-relative target odds 同时保留多个成功分支，缓解偏好训练把 Agent 压缩到单一路径的问题。

## 真正新增的内容

**论文原文结论**：Divergence-Tree Collection（DTC）恢复共享决策状态并收集分支集合；Reference-Relative Target-Odds（RTO）不强迫单一 winner，而是在成功备选之间匹配相对 reference 的目标赔率。作者引入 successful strategy coverage 并评估局部动作替换后的恢复能力。

**分析推断**：DTC 是当前高熵 Agent 状态生成 A/B/T/多分支监督的直接数据模板；RTO 可作为 verifier 蒸馏目标，在有多个可行解时避免 winner-take-all 的探索坍缩。

## 核心方法

从轨迹的共享状态展开多个候选行动和后续 rollout，用轨迹级 success/failure 标注分支；RTO 在成功分支集合上定义相对冻结 reference 的目标分布，并同时压低失败分支。训练是离线 preference post-training。

## 关键实验结果

BabyAI/BabaIsAI/WebShop 上，DDO 的平均成功率 0.76、H-ESD 0.35、ESD 0.40，均为比较方法最高；DPO 分别为 0.68、0.26、0.31。WebShop 成功率 0.26→0.36，覆盖指标近乎翻倍。向 DDO 加入 DTC 后，BabyAI/BabaIsAI 成功率分别 +5 和 +16 个百分点，并取得最高局部动作替换恢复率。

## 证据质量与局限

同预算比较、覆盖指标、组件消融和恢复测试使证据较完整。局限是主要环境相对受控，WebShop 成功率仍低；标签是轨迹级二元结果，没有真实序数 reward 分布或在线 verifier；覆盖类别的定义依赖环境与作者设计。

## 最接近的相关工作

DPO、TieDPO、成功轨迹模仿、解码时多样化，以及 COTA、SafeBranch、ParallelWorld 等同前缀反事实分支方法最接近。DDO 的贡献是同时改造数据收集与训练目标以优化“成功且多样”。

## 如何复用或推进 LLM-as-a-Verifier

在 student 真实访问的高熵状态运行 DTC，使用环境重放给分支硬 outcome，再让 generative verifier 解释成功条件和可恢复性；蒸馏完整分支分布与 tie，而非只蒸馏最优动作。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：把单动作 advantage 改为共享状态下 reference-relative 的分支分布目标。
- **A/B/T 与序数分布**：由多分支结果自然生成 A/B/T；将成功程度、恢复成本建模为序数分布。
- **真值门控**：环境 rollout 决定成功/失败方向，LLM verifier 仅补充软排序和解释。
- **critique states**：为每个失败分支生成“为何失败、如何恢复”的 student critique，再用反事实结果验收。
- **高熵探索**：显式保留多个成功 mode，以策略覆盖和恢复率共同选择 checkpoint。
- **sealed eval**：另设未参与 DTC 的状态与任务，冻结覆盖定义和执行器，避免 collector/verifier 共适应。
