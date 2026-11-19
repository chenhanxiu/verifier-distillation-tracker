# How Complete Must an Environment Be to Train a Capable GUI Agent?

- **作者**：Jingxing Wang、Teng Wang、Xingyu Lou、Zihan Guo、Jun Wang、Weiwen Liu、Weinan Zhang、Jianghao Lin
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：https://arxiv.org/abs/2611.23946
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.23946；DOI: 10.48550/arXiv.2611.23946

## 一句话结论

【论文原文】GUI Agent 环境可以删减无关 feature，却不能牺牲 verifier 的多路径 reward coverage 或应用数据覆盖；只奖励单一参考路径会使完整环境成功率下降 10.53 点。

## 真正新增的内容

【论文原文】把环境完整性拆为三轴：reward coverage（verifier 奖励多少条目标可达轨迹）、data coverage（Agent 能看到多少应用数据）和 feature coverage（任务未用功能是否保留）；在 MobileGym 中逐轴控制后，所有 policy 都回到原始完整环境评测，从而分离训练环境删减的真实影响。

## 核心方法

1. 分别改变 verifier 可接受路径、非任务数据记录和非任务 feature。
2. 训练 Qwen3-VL-4B-Instruct，并在同一 Full environment 做外部评测。
3. 分析 episode weighting、长绕路成功与技能侵蚀。
4. 构建保留完整 reward/data coverage、仅裁剪无关 feature 的 MobileGym-Lite。

## 关键实验结果

【论文原文】只奖励一条参考路径使成功率下降 10.53 点；删除未使用数据同样降低成功率。裁剪未用 feature 则从 51.61% 提升到 56.13%，但该收益在 episode 等权时反转、平衡任务后消失。MobileGym-Lite 在完整环境达 55.48%，高于 Full 的 51.61%，同时降低构建成本。

## 证据质量与局限

【论文原文】三轴控制、完整环境外测和 weighting 分析为较强因果证据；但只覆盖一个 GUI 环境与单一 4B 模型。MobileGym-Lite 的提升部分来自样本加权效应，不能简单归因于“环境越简越好”。

## 最接近的相关工作

接近 executable GUI gym、AutoGym、CrossEnv、reward coverage、multi-path verification 与 environment design。关键新增是实证区分 reward/data/feature 三种完整性。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】Agent verifier 训练应优先扩展等价成功路径与状态数据，而非追求 UI 功能全量仿真；sealed eval 必须回到完整环境。可用多路径 oracle 产生 A/B/T：两个不同动作序列若均满足目标，应作为并列正例保留探索。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher reward 需覆盖多条合法轨迹；单参考路径不应作为唯一 score anchor。
- **pairwise A/B/T 与序数分布**：多种成功路径标 T/等价，避免把与 reference 不同误标为 B。
- **程序化/环境真值门控**：环境 checker 按最终状态和约束验真，而非路径字符串匹配。
- **student-generated critique states**：critique 不应要求回到唯一参考路径，只指出未满足的状态义务。
- **高熵分叉探索**：reward coverage 完整是保留高熵合法策略的前提；删无关 feature 可以降噪。
- **sealed eval**：所有训练环境变体必须在原始 Full environment 上冻结复测，防止 harness 简化造成虚假提升。
