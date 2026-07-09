# 功能更新完成 - 2026年3月7日

## ✅ 已完成的功能改进

### 1. 预置图标删除功能 ✨

**功能特性：**
- 中央导航区的预置图标现在支持右键删除
- 删除预置图标时，该图标被隐藏而不是真的删除data.json
- 隐藏的图标列表存储在localStorage中

**使用方法：**
1. 右键点击中央导航区的任何预置图标
2. 选择"删除"选项
3. 图标立即消失（隐藏）
4. 用户可以在设置中或重新登录后找回被隐藏的图标

**技术实现：**
- 新增`hidden_presets` localStorage字段存储隐藏的图标ID
- `hidePresetItem()` 和 `showPresetItem()` 函数管理隐藏状态
- `renderCategories()` 在渲染时检查并跳过隐藏的预置项

### 2. 模态框内预置项不可删除 ✨

**功能特性：**
- 点击分类标题进入的分类详情模态框中的预置图标没有删除选项
- 在模态框中的预置项只能右键"添加到主页"或"添加到分类"
- 这确保了分类库的完整性

**技术实现：**
- `showContextMenu()` 新增 `isInModal` 参数区分调用位置
- 当 `isPreset=true && isInModal=true` 时不显示删除选项
- `renderCategories()` 传入 `isInModal=false`
- `renderModalItems()` 传入 `isInModal=true`

### 3. 背景模糊效果（糖玉璃风格） 🎨

**功能特性：**
- 启用模糊效果后，背景图片或纯色背景会显示模糊效果
- 卡片和内容本身保持清晰
- 效果类似毛玻璃（frosted glass）

**实现原理：**
- 创建一個固定位置的背景层 `backgroundBlurLayer`
- 该层复制body的背景（图片或颜色）
- 对该层应用 `filter: blur(8px)`
- body本身背景设为透明，让模糊层显示在下方

**视觉效果：**
```
启用前：清晰的背景图片/颜色
启用后：背景呈现毛玻璃效果（模糊8px）
      卡片和文字保持清晰
```

**用户控制：**
1. 打开设置面板（右上角齿轮）
2. 在壁纸设置中找到"启用模糊效果"开关
3. 打开/关闭即可看到变化
4. 设置自动保存到localStorage

## 📝 技术细节

### 新增/修改的函数

#### `loadHiddenPresets()` 和 `saveHiddenPresets()`
```javascript
// 从localStorage加载隐藏的预置项ID列表
function loadHiddenPresets() {
    const saved = localStorage.getItem('hidden_presets');
    return saved ? JSON.parse(saved) : [];
}
```

#### `hidePresetItem()` 和 `showPresetItem()`
```javascript
// 隐藏某个预置项
function hidePresetItem(itemId) {
    const hidden = loadHiddenPresets();
    if (!hidden.includes(itemId)) {
        hidden.push(itemId);
        saveHiddenPresets(hidden);
    }
}
```

#### `showContextMenu(e, item, isPreset, isInModal = false)`
修改了签名，添加 `isInModal` 参数来区分删除选项的显示

#### `deleteItem(item)`
新增逻辑：
```javascript
if (state.contextMenuIsPreset) {
    hidePresetItem(item.id);  // 隐藏预置项
} else {
    // 删除用户添加的项（真的删除）
    ...
}
```

#### `applyBlurEffect(enabled)` 
完全重写，使用专门的blur layer实现背景模糊：
```javascript
if (enabled) {
    // 创建模糊层，复制背景后应用blur
    blurLayer.style.filter = 'blur(8px)';
    // body背景设为透明
} else {
    // 隐藏模糊层，恢复原背景
}
```

### localStorage数据结构

```javascript
// 隐藏的预置项ID列表
{
  "hidden_presets": ["item-id-1", "item-id-2"]
}

// 现有的用户设置
{
  "user_settings": {
    "blur_enabled": true,
    "wallpaper_url": "...",
    "background_color": "#4F46E5",
    ...
  }
}
```

## 🧪 测试清单

- [ ] 右键点击预置图标可见"删除"选项
- [ ] 点击删除后图标消失
- [ ] 刷新页面后删除的图标仍然隐藏
- [ ] 点击分类标题进入模态框
- [ ] 模态框内的预置图标右键没有删除选项
- [ ] 启用模糊效果后背景显示模糊（最好用有图片的背景）
- [ ] 关闭模糊效果后背景恢复清晰
- [ ] 模糊开关状态保存到设置
- [ ] 用户添加的图标仍然可以删除

## 浏览器支持

- `filter: blur()` 支持：所有现代浏览器（IE除外）
- 纯CSS实现，无需额外库依赖

## 已知限制

- 模糊效果最明显的是有背景图片的时候
- 纯色背景下的模糊效果较不明显（颜色会发生变化）
- 模糊层覆盖整个视口，所以模糊效果是全局的
