# Weight Classification for Home Assistant

[English](#english) | [中文](#中文)

---

## English

### Overview

**Weight Classification** is a custom Home Assistant integration that automatically classifies weight measurements from a body scale (e.g., Xiaomi Mi Body Composition Scale 2) into person-specific entities based on configurable weight ranges.

Perfect for families sharing a single scale - each member gets their own sensor with historical tracking for monitoring weight trends over time.

### Features

✅ **Automatic Classification** - Measurements are automatically assigned to family members based on weight ranges  
✅ **UI Configuration** - Easy setup through Home Assistant's UI  
✅ **Historical Tracking** - All measurements are stored with long-term statistics  
✅ **Multi-language** - Supports English and Simplified Chinese  
✅ **State Restoration** - Preserves data across Home Assistant restarts  

### Installation

#### HACS (Recommended)

1. Open **HACS** in your Home Assistant
2. Click on **Integrations**
3. Click the **⋮** menu (top right) and select **Custom repositories**
4. Add this repository URL: `https://github.com/shuis/weight-classification`
5. Select **Integration** as the category
6. Click **Add**
7. Search for "Weight Classification" and click **Download**
8. Restart Home Assistant

#### Manual Installation

1. Download the `custom_components/weight_classification` folder
2. Copy it to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

### Configuration

1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for "Weight Classification"
4. Select your source weight sensor (e.g., `sensor.xiaomi_scale_weight`)
5. Add family members with their weight ranges:
   - **Name**: Person's name (e.g., "Dad", "Mom", "Child")
   - **Min Weight**: Minimum expected weight in kg
   - **Max Weight**: Maximum expected weight in kg
   - Click "Add another person" to add more members
6. Click **Submit** when done

### Example Configuration

```yaml
Source Sensor: sensor.xiaomi_scale_weight

Persons:
  - Name: Dad
    Min Weight: 70 kg
    Max Weight: 90 kg
  
  - Name: Mom
    Min Weight: 50 kg
    Max Weight: 70 kg
  
  - Name: Child
    Min Weight: 30 kg
    Max Weight: 50 kg
```

### Usage

#### Viewing Weight Trends

Create a **History Graph** card in your dashboard:

```yaml
type: history-graph
entities:
  - entity: sensor.weight_dad
    name: Dad
  - entity: sensor.weight_mom
    name: Mom
  - entity: sensor.weight_child
    name: Child
hours_to_show: 720  # 30 days
```

#### Using ApexCharts (Optional)

For more beautiful charts, install [ApexCharts Card](https://github.com/RomRider/apexcharts-card) via HACS:

```yaml
type: custom:apexcharts-card
header:
  title: Family Weight Trends
  show: true
series:
  - entity: sensor.weight_dad
    name: Dad
    stroke_width: 2
  - entity: sensor.weight_mom
    name: Mom
    stroke_width: 2
  - entity: sensor.weight_child
    name: Child
    stroke_width: 2
```

### Attributes

Each person sensor includes the following attributes:

- `person_name`: Name of the person
- `weight_range`: Configured weight range (e.g., "70-90 kg")
- `min_weight`: Minimum weight threshold
- `max_weight`: Maximum weight threshold
- `last_measured`: Timestamp of last measurement

### Troubleshooting

**Issue: Measurements not being classified**
- Check that the source sensor is reporting values
- Verify weight ranges don't have gaps
- Check Home Assistant logs for warnings

**Issue: Multiple people have overlapping weight ranges**
- The first matching person (by configuration order) will receive the measurement
- Adjust weight ranges to avoid overlaps

**Issue: Sensor not showing in UI**
- Restart Home Assistant after installation
- Clear browser cache
- Check that the integration is properly installed in `custom_components/weight_classification`

### Support

For issues and feature requests, please visit the [GitHub Issues](https://github.com/shuis/weight-classification/issues) page.

---

## 中文

### 概述

**体重分类（Weight Classification）** 是一个 Home Assistant 自定义集成，可以根据可配置的体重范围自动将体脂秤（如小米体脂秤 2）的测量数据分类到不同的家庭成员实体中。

非常适合全家共用一台体脂秤的场景 - 每个家庭成员都有自己的传感器，并带有历史记录追踪，方便监测体重变化趋势。

### 功能特性

✅ **自动分类** - 根据体重范围自动分配测量数据给对应的家庭成员  
✅ **UI 配置** - 通过 Home Assistant 界面轻松设置  
✅ **历史追踪** - 所有测量数据都带有长期统计功能  
✅ **多语言支持** - 支持英文和简体中文  
✅ **状态恢复** - 重启 Home Assistant 后保留数据  

### 安装

#### HACS（推荐）

1. 在 Home Assistant 中打开 **HACS**
2. 点击 **集成**
3. 点击右上角的 **⋮** 菜单，选择 **自定义存储库**
4. 添加此仓库地址：`https://github.com/shuis/weight-classification`
5. 类别选择 **Integration（集成）**
6. 点击 **添加**
7. 搜索 "Weight Classification" 并点击 **下载**
8. 重启 Home Assistant

#### 手动安装

1. 下载 `custom_components/weight_classification` 文件夹
2. 复制到您的 Home Assistant 的 `custom_components` 目录
3. 重启 Home Assistant

### 配置

1. 进入 **设置 → 设备与服务**
2. 点击 **+ 添加集成**
3. 搜索 "Weight Classification"
4. 选择您的源体重传感器（例如 `sensor.xiaomi_scale_weight`）
5. 添加家庭成员及其体重范围：
   - **姓名**：成员名称（如 "爸爸"、"妈妈"、"孩子"）
   - **最小体重**：预期最小体重（千克）
   - **最大体重**：预期最大体重（千克）
   - 点击 "添加其他成员" 继续添加
6. 完成后点击 **提交**

### 配置示例

```yaml
源传感器: sensor.xiaomi_scale_weight

成员:
  - 姓名: 爸爸
    最小体重: 70 千克
    最大体重: 90 千克
  
  - 姓名: 妈妈
    最小体重: 50 千克
    最大体重: 70 千克
  
  - 姓名: 孩子
    最小体重: 30 千克
    最大体重: 50 千克
```

### 使用方法

#### 查看体重趋势

在仪表板中创建 **历史图表** 卡片：

```yaml
type: history-graph
entities:
  - entity: sensor.weight_dad
    name: 爸爸
  - entity: sensor.weight_mom
    name: 妈妈
  - entity: sensor.weight_child
    name: 孩子
hours_to_show: 720  # 30 天
```

#### 使用 ApexCharts（可选）

要获得更美观的图表，可通过 HACS 安装 [ApexCharts Card](https://github.com/RomRider/apexcharts-card)：

```yaml
type: custom:apexcharts-card
header:
  title: 家庭体重趋势
  show: true
series:
  - entity: sensor.weight_dad
    name: 爸爸
    stroke_width: 2
  - entity: sensor.weight_mom
    name: 妈妈
    stroke_width: 2
  - entity: sensor.weight_child
    name: 孩子
    stroke_width: 2
```

### 实体属性

每个成员的传感器包含以下属性：

- `person_name`：成员姓名
- `weight_range`：配置的体重范围（如 "70-90 kg"）
- `min_weight`：最小体重阈值
- `max_weight`：最大体重阈值
- `last_measured`：最后测量时间戳

### 故障排除

**问题：测量数据未被分类**
- 检查源传感器是否正常上报数值
- 确认体重范围没有缺口
- 查看 Home Assistant 日志中的警告信息

**问题：多个成员的体重范围重叠**
- 测量数据将分配给第一个匹配的成员（按配置顺序）
- 调整体重范围以避免重叠

**问题：传感器未显示在界面中**
- 安装后重启 Home Assistant
- 清除浏览器缓存
- 检查集成是否正确安装在 `custom_components/weight_classification` 目录

### 支持

如有问题或功能请求，请访问 [GitHub Issues](https://github.com/shuis/weight-classification/issues) 页面。

---

## License

MIT License

## Credits

Created for the Home Assistant community 🏠
