# 世界动作模型的 Test-Time Search：候选可选性与模拟器完整性审计

- **论文标题**：When Does Test-Time Search Help World Action Models? An Empirical Audit of Candidate Selection and Simulator Integrity
- **作者**：Jun Liu, Dajie Sun, Zhenglun Kong, Zhenjiang Fan, Peiyan Dong, Fan Yang, Wenbin Zhangg, Geng Yuan, Xue Lin, Yanzhi Wang, Dong Huang
- **首次公开日期**：2026-10-30
- **版本日期**：2026-10-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.41970
- **DOI**：https://doi.org/10.48550/arXiv.2610.41970
- **代码链接**：摘要称已发布 detector、fix 与 scripts，但 arXiv 页面未列出明确仓库 URL

## 一句话结论

在 Cosmos Policy / RoboCasa 的受测配置中，候选大多没有 outcome 差异、learned selector 甚至略差于随机，同时计算密集路径触发静默渲染损坏，说明 test-time verifier 的收益必须拆成“可选信号、真实效率、评测完整性”三段审计。

## 真正新增的内容

**论文原文结论**：更多候选并不自动产生可利用的选择信号；selector、算力优化和 simulator integrity 是相互独立的必要前提，应以预注册 premise-first 方式逐项检验。

**分析推断**：这给“高熵分叉 + verifier 选优”设置了重要否证条件：策略分布熵高不等于分支 outcome 高熵；若 82% 状态候选结果相同，强行蒸馏排序只会学习噪声或 evaluator 偏差。

## 核心方法

在 Cosmos Policy 与 RoboCasa 上预注册三个门槛：候选是否存在可利用的 outcome 差异；标称 FLOPs 节省是否转化为端到端加速；评测路径是否保持模拟器/渲染完整。比较 learned value selector、随机选择与 hindsight oracle，并对 token pruning、adaptive allocation 和渲染异常做审计。

## 关键实验结果

**论文原文报告**：

- clean data 上 learned value selector 比随机低 1.66 个百分点。
- hindsight oracle 仅高 1.40 点，episode-level 区间跨 0。
- 82% 状态的候选 outcome 完全相同，选择余量很小。
- token pruning 最多减少 47% 每次 forward FLOPs，但部署路径端到端最多仅 1.15 倍加速（排除 decode 为 1.25 倍），未达 1.5 倍目标。
- adaptive allocation 在 power gate 下结论不充分。
- 发现静默渲染损坏，且在计算密集规划路径中显著上升；官方 direct-policy 结果不受影响。

## 证据质量与局限

预注册、负结果、oracle 上界和系统完整性检查使证据质量较高，尤其能约束过度宣称。作者明确把结论限定于所测配置；因此不能据此否定所有 WAM test-time search。模拟器损坏修复后的外部复现、其他模型和更具分支差异的任务仍需验证。

## 最接近的相关工作

接近 World-Coherent Decoding、speculative uncertainty、EPIG-Tree、belief-shift branching、AutoTuneBench、Harness or Model? 与环境级 sealed evaluation。其独特价值是把 selector 头部空间与 simulator integrity 同时作为必要前提。

## 如何复用或推进 LLM-as-a-Verifier

- 训练 verifier 前先估计 candidate outcome diversity 与 oracle headroom；低于阈值则不蒸馏排序。
- 把“候选等价”显式标为 T，而不是用微小 Judge 分差制造 A/B。
- 将环境完整性 detector 作为硬门控；异常 episode 不进入 teacher data。
- 报告 selector 相对随机、相对 hindsight oracle 的差距，以及端到端成本，而非仅报成功率。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析推断**：高熵分叉路由应从 policy entropy 升级为三重门控：动作分布熵、预测 outcome diversity、环境完整性。只有存在可验证 outcome contrast 的状态才进行 score-level OPD；结果等价时保留探索和 T 分布。sealed eval 必须把 simulator build、渲染校验、随机种子与 evaluator 全部冻结，并将异常检测日志独立保存，避免计算路径改变评测本身而造成虚假 verifier 增益。