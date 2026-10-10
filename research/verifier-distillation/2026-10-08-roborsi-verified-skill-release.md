# RoboRSI: Stable, Efficient, and Reusable Robot Self-Evolution in Complex Real-World Environments

- **作者**：Zimo Wen；Yijin Chen；Yuxuan Cao；Wendi Chen；Yanwen Zou；Wenye Yu；Fuhang Kuang；Han Xue；Jun Lv；Chuan Wen；Cewu Lu
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12424
- **Canonical URL**：https://arxiv.org/abs/2610.12424
- **项目页**：https://lab.noematrix.ai/blog/2-roborsi-research-preview/
- **代码**：https://github.com/nssmd/RoboRSI

## 一句话结论

RoboRSI 将任务分解、失败归因、局部修复和发布前验证绑定到带契约的 skill 层级，使 Agent 经验只有在执行证据支持且通过 Reviewer 验证后才进入可复用能力库。

## 真正新增的内容

【论文原文】Top-Down Skill Refinement 将任务划分为 compound、atomic 和 base skill，为每个节点定义职责与输入输出契约；执行结果被归因到负责分支，修订也局限在该分支。Manager、Planner、Engineer、Reviewer 共同完成规划、执行、诊断与验证发布。

【分析推断】这把 student-generated critique states 的“准入”从文本质量问题转为版本化发布问题：critique、修复代码和 skill memory 必须绑定具体失败、契约、执行证据和回滚点。

## 核心方法

1. 按任务结构建立分层 skill tree，并为节点规定作用域和输入输出契约。
2. 将执行成败归因到负责的 skill 分支，避免全局无差别修改。
3. 由 Engineer 进行局部修复，Reviewer 在执行证据上验证后发布。
4. 将稳定的 skill 序列合并为可复用 compound skill，形成受控自进化循环。
5. 允许人类通过目标和纠正信号引导演化。

## 关键实验结果

【论文原文】真实移动机械臂经过 104 轮发展出多物体家庭清理能力；在 LIBERO、LIBERO-PRO、LIBERO-Plus 和 RoboTwin 上取得最高成功率，超过最强基线 2.7–11.0 个百分点。

## 证据质量与局限

【论文原文】包含真实机器人长期演化与四个模拟基准，且公开代码，证据较强。  
【局限】论文验证的是完整系统而非单一 verifier 组件，Manager/Reviewer、任务分解与修复策略的贡献可能耦合。家庭清理和现有机器人基准仍不足以证明开放世界中的安全泛化；Reviewer 也可能与 Agent 共适应。

## 最接近的相关工作

与 SkillAA、RSIAgent、Grounding Agent Memory、DENSE、RC-OPD、Agent Error Dataset 和 Co-Evolving Inspectable Graders 最接近。RoboRSI 的独特价值是把归因、局部修改、契约和验证发布整合为可运行的能力生命周期。

## 如何复用或推进 LLM-as-a-Verifier

可将轨迹 verifier 输出组织为“责任 skill、违反契约、证据指针、局部修复、验证结果”五元组。生成式 verifier 只负责提出诊断；程序检查器、环境重放和独立 Reviewer 决定是否把 critique/修复写入长期 memory。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：按 skill 节点蒸馏局部分数和责任归因，避免用整条轨迹总分污染无关步骤。
- **A/B/T 与序数分布**：对每个契约输出满足/违反/证据不足及严重度分布，而非单一 pass/fail。
- **程序化/环境真值门控**：skill 发布必须重放执行并检查 I/O 契约；语言 Reviewer 不能越过硬门控。
- **student-generated critique states**：把 critique 绑定到失败分支和可复现实验，验证失败则拒绝写入或回滚。
- **高熵分叉**：只冻结已验证 skill；对尚未覆盖的分支保留探索，避免复用库过早收缩策略空间。
- **sealed eval**：保留不参与 skill 演化的任务、硬件状态和 Reviewer，分别评估即时修复、跨任务复用与长期退化。

总体判断：【分析推断】RoboRSI 是把 verifier 从离线评分器升级为“受控能力发布门”的完整工程原型，对现有评测 Agent 的 memory/skill 准入模块尤其有用。