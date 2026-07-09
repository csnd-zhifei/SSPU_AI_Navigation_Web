# 修复日志 - 2026年3月7日

## 修复的三个主要问题

### 1. 右键菜单位置问题 ✅

**问题描述：**
- 右键菜单出现在鼠标位置下方
- Dock底部的图标右键后看不到菜单
- 滚动页面后，菜单位置不正确

**原因：**
- 使用了 `e.pageX` 和 `e.pageY`，这是相对于整个文档的坐标
- 没有考虑菜单会超出视口的情况
- 没有进行菜单边界检测

**修复方案：**
- 改用 `e.clientX` 和 `e.clientY`（相对于视口）
- 添加菜单边界检测逻辑
- 当菜单超出右边界或下边界时，自动调整位置

**代码改动：**
```javascript
// 使用 clientX/clientY 相对于视口定位
let x = e.clientX;
let y = e.clientY;

// 获取菜单尺寸
const menuRect = menu.getBoundingClientRect();
const menuWidth = menuRect.width;
const menuHeight = menuRect.height;

// 检查是否超出视口并调整
if (x + menuWidth > window.innerWidth) {
    x = window.innerWidth - menuWidth - 10;
}
if (y + menuHeight > window.innerHeight) {
    y = window.innerHeight - menuHeight - 10;
}
```

### 2. 模糊背景效果问题 ✅

**问题描述：**
- 启用模糊效果后，背景"只是比例变了"，看不到毛玻璃效果

**原因：**
- 默认CSS中所有卡片都有`backdrop-filter: blur(10px)`
- 启用/禁用开关没有视觉差异

**修复方案：**
- 修改CSS策略：默认**没有** blur 效果
- 启用模糊时才添加 `with-blur` class
- 在renderCategories和renderDock时根据设置添加class

**CSS改动：**
```css
/* 默认没有穀玻璃效果 */
.category-card {
    backdrop-filter: none;
}

/* 启用模糊时添加 */
.category-card.with-blur {
    backdrop-filter: blur(10px);
}
```

**JS改动：**
- 创建category-card时检查 `settings.blur_enabled`
- 如果启用则添加 `with-blur` class
- 切换开关时通过 `applyBlurEffect()` 动态更新class

### 3. 其他改进

**右键菜单改进：**
- 菜单现在使用 `position: fixed` 确保相对视口定位
- 自动调整到合适位置，不会被遮挡

**模糊效果改进：**
- 更直观的视觉反馈
- 可以明显看到打开/关闭模糊效果的区别
- Dock和分类卡片都支持模糊效果切换

## 修改的文件

- `templates/index.html`
  - 修改了 `showContextMenu()` 函数
  - 修改了 `applyBlurEffect()` 函数
  - 修改了 `renderCategories()` 函数，添加blur class逻辑
  - 修改了CSS定义：`.category-card`, `.dock-container` 添加了 `.with-blur` class定义

## 测试建议

1. **测试右键菜单：**
   - 在Dock最右边的图标右键
   - 在页面底部的图标右键
   - 滚动页面后右键
   - 验证菜单始终在合适位置

2. **测试模糊效果：**
   - 打开设置面板
   - 关闭"启用模糊效果"开关
   - 观察卡片和Dock变清晰（no blur）
   - 再次打开开关
   - 观察卡片和Dock显示毛玻璃效果（with blur）

3. **测试删除功能：**
   - 在Dock中右键任何用户添加的图标
   - 验证"删除"选项出现
   - 在"我的收藏"中右键图标
   - 验证"删除"选项出现
   - 对于预置图标，验证"删除"选项不出现

## 浏览器兼容性

- `backdrop-filter` 支持：Chrome 76+, Edge 79+, Safari 9+, Firefox 暂不支持
- 如果浏览器不支持 `backdrop-filter`，用户将看不到毛玻璃效果
  - 这不会破坏功能，只是显示效果差异

## 已知限制

- `backdrop-filter` 需要背景图片才能看到明显效果
- 纯色背景下的模糊效果可能不明显
- 建议用户为更佳体验上传背景图片
