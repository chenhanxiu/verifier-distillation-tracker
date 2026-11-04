# When Self-Verification Hurts：面向金融问答的校准式答案修复

## 基本信息

- **作者**：Celine Guo, Weida Liang, Yujian Fu, Anqi Dang, Yanzheng Jin, Kenji Kawaguchi, Wenya Wang
- **首次公开日期**：2026-11-03
- **版本日期**：2026-11-03（v1）
- **原始论文**：https://arxiv.org/abs/2611.05166
- **DOI**：https://doi.org/10.48550/arXiv.2611.05166
- **代码**：未见公开代码链接

## 一句话结论

开放式“验证并重写”会破坏原本正确内容；CAR 先判断修复是否值得，再选择定向检查、定位证据并限制编辑范围，在三个金融 QA 数据集和三个开放模型上全面优于通用 self-verification。

## 真正新增的内容

**论文原文结论**：作者将 repair 明确建模为“可恢复信息”与“可能损伤正确内容”的权衡，并把 verifier 从总是触发的审稿人改成选择性、局部化的修复控制器。

**分析推断**：这为 student-generated critique states 提供了准入原则：critique 的价值应按预期纠错收益减去破坏风险衡量，而不是因 teacher 给出 critique 就必然执行或蒸馏。

## 核心方法

CAR 包含四步：估计草稿是否会从修复中受益；选择针对性的关系检查；定位相关证据或草稿 span；限制允许修改的局部范围。

## 关键实验结果

- 覆盖 FinRank、Fin-RATE、FinQA 与 3 个开放权重模型。
- 所有 dataset-model 组合都优于 generic verification。
- 系统恢复 **14.6%** 的初始遗漏要求，同时仅损伤 **2.1%** 的初始正确内容。
- post-draft token 成本比迭代修订替代方案低 **30% 以上**。
- 两个设置的消融显示证据定位和 bounded editing 是主要贡献因素。

## 证据质量与局限

证据跨数据集、跨模型且报告收益/损伤双向指标，设计较扎实。局限是金融 QA 属于短输出、证据静态场景；没有测试长轨迹中的延迟后果、工具副作用或对抗性策略优化。

## 最接近的相关工作

最接近 draft–verify–revise、selective prediction、LLM-as-an-Improver、证据定位与局部编辑。区别是显式校准“是否修复”并量化对正确内容的伤害。

## 如何复用或推进 LLM-as-a-Verifier

给 verifier 增加三个输出：预计纠错收益、预计破坏风险、可编辑 span/动作集合。只有净收益为正且证据充分时才执行 critique；其余标记为 abstain/T，并保留原轨迹。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏净修复价值而非裸错误分数，加入“正确轨迹被改坏率”。
- **A/B/T/序数分布**：A=修复、B=保持、T=证据不足，并校准三类概率。
- **程序真值门控**：局部修复后重新执行相关测试/只读检查，不能只靠同一 Judge 复评。
- **critique states**：强制携带证据 span、目标关系和允许修改范围。
- **高熵分叉**：低置信时保留原分支与修复分支，而非覆盖。
- **sealed eval**：独立统计 recovered、damaged 与 abstained，防止只报告净准确率掩盖破坏。
