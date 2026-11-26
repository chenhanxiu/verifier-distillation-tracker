# Failure-Driven Data Flywheel：用失败地图闭环生成数据并以 sealed test 验收

- **论文标题**：A Failure-Driven Data Flywheel for Post-Training Vision-Language-Action Models
- **作者**：Yuhao Luo, Zihao Sheng, Zilin Huang, Zhengyang Wan, Boyue Wang, Ruolin Yang, Shuai Wang, Sikai Chen
- **首次公开日期**：2026-11-25
- **版本日期**：2026-11-25（v1）
- **原始论文**：https://arxiv.org/abs/2611.34698
- **DOI**：https://doi.org/10.48550/arXiv.2611.34698
- **代码链接**：未见公开代码

## 一句话结论

该工作用逐条件失败地图分配下一轮数据生成预算，并在 sealed test 与真实车辆上验收，是“失败驱动探索—程序化评价—闭环外验证”的完整原型。

## 真正新增的内容

**论文原文结论**：框架在重建场景中插入任务相关实体，按行为要求细分条件与难度，持续把数据预算投向仍失败的区域。**分析推断**：这比单按策略熵分叉更适合 Agent verifier × OPD，因为探索预算同时由失败率、条件覆盖和独立验收约束。

## 核心方法

构造训练数据未覆盖的目标场景；以细粒度行为要求形成 failure map，每轮训练后重测并提高薄弱条件的数据配额。自动驾驶实验覆盖遮挡行人和停车标志让行，并同时测配对控制场景，避免通过过度刹车刷安全分。

## 关键实验结果

五轮训练后，sealed set 的关键阶段无碰撞率从 0.261 升至 0.579（AutoVLA），从 0.390 升至 0.765（ReCogDrive），无必要刹车率不超过 0.013；真实车辆安全通过由 1/5 升至 4/5。停车线前停止率分别从 0.100/0.000 升至 0.897/0.667。

## 证据质量与局限

有配对反事实控制、sealed test、模拟和实车验证；但仅两个驾驶能力族、样本规模有限，failure map 的分区与 grader 仍可能遗漏未知失败。

## 最接近的相关工作

与 EPIG-Tree 的信息价值分叉、AutoGym 的可验证课程、REVERSAL-BENCH 的 recoverability oracle 和 SealedLoop 的独立验收互补。

## 如何复用或推进 LLM-as-a-Verifier

将 failure map 由二元失败扩展为序数风险分布，分离“任务未完成、危险、过度保守、不可判定”。LLM 生成 critique，但配额更新只采用程序/环境 truth；不确定状态保留多分支而非过早收敛。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：用“高熵 × verifier 分歧 × sealed failure density”共同决定分叉预算；score-level OPD 以硬真值门控，soft verifier 只在可判定区域内排序。保留配对控制任务，防止 student 通过统一保守策略获得虚假提升。
