## Overview

这个程序是通过加载`{score}.json`的信息来演奏的，其字段包括

- `version`: **Nikki Auto Player** 的版本
- `instrument`: **乐器名**（目前只写了 violin）
- `music_name`: **乐谱名**
- `bpm`: 不用多解释了吧
- `melody`: **旋律数据**

e.g. (先别太关注melody是什么鬼，其编写格式稍后会介绍到)
```json
{
    "version": "1.0",
    "instrument": "violin",
    "music_name": "千本樱",
    "bpm": 154,
    "melody": [
        [
            "5",
            "b",
        ],
        [
            "6",
            "b",
        ],
        [
            "2#",
            "b",
        ]
    ]
}
```
## 编写你的谱子

### 基本格式
此项目提供了一个简单的，能将任意可读的二进制文本文件转换为`{score}.json`的工具，你可以先在任意文本编辑器中编写你的谱子，然后使用本程序的`导入乐谱`来转换。

> P.S. Dev请用`./test/trans.py`来测试

*Nikki Auto Player 演奏谱子是先将melody的数据转换为 **tuple**，按顺序执行，每个tuple的第一个元素是音符，第二个元素是音符的时值。
格式为：`('notes', 'duration')`，比如：
```python
melody = [
    ("5", "b"), # 按下so音符对应的键，时值为b(一拍)
    ("6", "b_"), # 按下la音符对应的键，时值为b/2(半拍)
    ("2#", "b__"), # 按下do#音符对应的键，时值为b/4(四分之一拍)
]
```
启动后，程序会按这个顺序依次按下对应的键值来演奏，

`notes`支持如下音符：
```text
# 中音
1 2 3 4 5 6 7
do re mi fa so la ti

# 升号
1# 2# 4# 5# 6# 7#
do# re# fa# so# la# ti#

# 升号（半音，默认是shift键）
sharp
s

# 降号
flat
f

# 休止符
0
```

`duration`以`b`为单位，支持如下格式的编写:

- **0, b, b/2, b/4, b/8** ( 0 在duration中同等于b，即一拍 )
- **b2**  (二全音符)
- **b_**  (八分音符)
- **b__** (十六分音符)
- **b.** (附点四分)
- **b._**  (附点八分)

`duration`还支持以`b*{float}`的形式来表示，比如`b*1.5`表示时值为1.5拍

### 编写格式

你可以在任意文本编辑器中编写你的谱子，格式如下(可完全空，但建议写上bpm)

```python
version 1.0 #为空则默认为1.0
instrument violin #为空则默认为 violin
music_name Example #为空则默认为 unnamed score
bpm 120 #为空则默认为 120
5 b
6 b_
2# b_
3# b._
2# b._
3# b._
```
以上内容将被解析为:
```python
melodyData.version: float = 1.0
melodyData.instrument: str = "violin"
melodyData.music_name: str = "Example"
melodyData.bpm: int = 120
melody: tuple = [
    ("5", "b"),
    ("6", "b_"),
    ("2#", "b_"),
    ("3#", "b._"),
    ("2#", "b._"),
    ("3#", "b._"),
]
```
此项目还支持简写格式:
- `duration`为空时默认为`0`即`b`
- 可以简写为`{notes}_` 和 `{notes}__`，解析时会自动转换为`{notes} b_` 和 `{notes} b__`
e.g.
```text
5
5#
5#_
5#__
```
以上内容将被解析为:
```python
melody = [
    ('5', '0'),
    ("5#", '0'),
    ('5#', 'b_'),
    ('5#', 'b__'),
]
```
### 分割Bar
为了方便检查乐谱的节奏，可以在乐谱中添加`@@`符号来分割小节，如：
```text
@@ bar1
5 b
6 b_
...
@@ bar2
2 b
3 b_
```
其中`bar1`和`bar2`为小节的名称(可自定义名称)，在演奏时会在控制台输出