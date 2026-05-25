## ADDED Requirements

### Requirement: 三面板布局容器

认证页面 SHALL 包含三个面板（登录、注册、忘记密码），通过平移 + 淡入淡出组合动画切换活跃状态，不使用 3D 旋转。

#### Scenario: 默认显示登录面板
- **WHEN** 用户访问认证页面（`/`）
- **THEN** 登录面板处于可见状态（`translateX(0) opacity(1)`），注册和忘记密码面板不可见（`opacity(0)`）

#### Scenario: 切换到注册面板
- **WHEN** 用户点击"没有账号？注册"链接
- **THEN** 登录面板 SHALL 向左滑出并淡出（`translateX(-60px) opacity(0)`），注册面板从右侧滑入并淡入（`translateX(60px→0) opacity(0→1)`），动画时长 600ms，使用弹性缓动曲线，同时触发液态玻璃脉冲效果

#### Scenario: 切换到忘记密码面板
- **WHEN** 用户点击"忘记密码？"链接
- **THEN** 登录面板 SHALL 向左滑出并淡出，忘记密码面板从右侧滑入并淡入，动画参数同上

#### Scenario: 面板切换中途反向切换
- **WHEN** 用户在面板切换动画进行中点击另一个面板的链接
- **THEN** 动画 SHALL 平滑过渡到新目标状态，不出现跳帧或闪烁

### Requirement: Liquid Glass 视觉风格

所有认证面板 SHALL 采用 Liquid Glass 设计语言，基于 SVG `feDisplacementMap` 滤镜实现液态玻璃折射效果，配合高透明度背景和交互式扭曲动画。

#### Scenario: 面板玻璃效果
- **WHEN** 面板渲染
- **THEN** 面板 SHALL 应用 `backdrop-filter: url(#liquid-glass)` 全局 SVG 滤镜，背景透明度在 0.15~0.25 范围内，面板边缘有 1px 半透明白色边框，面板顶部有斜向高光条（`::before` 伪元素），不支持 SVG backdrop-filter 的浏览器降级为 `blur(34px) saturate(165%)`

#### Scenario: 面板切换液态脉冲
- **WHEN** 用户触发面板切换
- **THEN** SVG 滤镜的 displacement scale SHALL 先从 1.0 冲到 1.6，再平滑回落到 1.0，产生液态涌动效果，总时长约 600ms

#### Scenario: 输入框聚焦液态扰动
- **WHEN** 用户聚焦任意输入框
- **THEN** displacement scale SHALL 微增到 1.12，失焦后平息回 1.0

#### Scenario: 按钮悬停液态效果
- **WHEN** 用户悬停在按钮上
- **THEN** displacement scale SHALL 增加到 1.2，移出后平息回 1.0

#### Scenario: 输入框样式
- **WHEN** 输入框渲染
- **THEN** 输入框背景透明度 SHALL 在 0.15~0.25 范围内，聚焦时有发光效果（`box-shadow` 带主题色散射）

#### Scenario: 非活跃面板视觉降级
- **WHEN** 面板处于非活跃状态
- **THEN** 面板 opacity SHALL 降低到 0，不可见

### Requirement: 面板切换触发方式

用户 SHALL 通过面板底部的链接文字在三个面板之间切换。

#### Scenario: 登录面板的切换链接
- **WHEN** 登录面板处于活跃状态
- **THEN** 面板底部 SHALL 显示"没有账号？注册"和"忘记密码？"两个链接

#### Scenario: 注册面板的切换链接
- **WHEN** 注册面板处于活跃状态
- **THEN** 面板底部 SHALL 显示"已有账号？登录"链接

#### Scenario: 忘记密码面板的切换链接
- **WHEN** 忘记密码面板处于活跃状态
- **THEN** 面板底部 SHALL 显示"返回登录"链接
