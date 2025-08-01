# Markwhen

## 1. 介绍

Markwhen 是一种类似 Markdown 的日志语言 。你编写类似 Markdown 的文本，它会被转换成 JSON，然后可以渲染到时间轴或其他视图中。

## 2. 语法 Syntax

下面的示例已缩进了，但缩进并非强制。不过，如果您像以下示例一样需要缩进，则建议使用等宽字体。

```mw
---
title: Project plan
 
#Project1: #d336b1
#Danielle: yellow
timezone: America/New_York
---
 
section All Projects
  group Project 1 #Project1
    // Supports ISO8601
    2025-01/2025-03: Sub task #John
    2025-03/2025-06: Sub task 2 #Michelle
      More info about sub task 2
 
      - [ ] We need to get this done
      - [x] And this
      - [ ] This one is extra
 
    2025-07: Yearly planning
endGroup
 
group Project 2 #Project2
  2025-04/4 months: Larger sub task #Danielle
    contact: imeal@example.com
 
  // Supports American date formats
  03/2025 - 1 year: Longer ongoing task #Michelle
    assignees: [Michelle, Johnathan]
    location: "123 Main Street, Kansas City, MO"
 
    - [x] Sub task 1
    - [x] Sub task 2
    - [ ] Sub task 3
    - [ ] Sub task 4
    - [ ] so many checkboxes omg
```

### 2.1. 事件 Events

事件是一个日期范围（date range），后跟冒号，后跟事件描述（event description）：

```mw
12/2012: End of the world
 
1961: Year after 1960
Later, 1962 would happen
 
1 year: 1962, just as predicted
 
2020-02-22T12:13:14Z-now: How long the pandemic has been going on?
12/7/1941: Pearl Harbor attacked
Launched US into WWII
 
2022-02-22T16:27:08.369Z: More specific thing
2021-01-02T06:27:00Z-2022: ongoing project work until the end of 2022
 
1892/2021-08-12: Example of EDTF date range
```

### 2.2. 日期和范围 Dates and Ranges

Markwhen 支持多种日期格式和表达时间段的机制。

扩展日期时间格式 (Extended date time format, EDTF) 是用于表达日期和范围的推荐语法。解析时，EDTF 优先于此处提到的其他日期格式。如果日期范围的表达方式存在歧义，且符合 EDTF 范围格式，则会将其解析为 EDTF。

每个事件都有一个关联的日期范围，无论其是否明确写明结束日期。日期范围是指从一个日期到另一个日期的时间段。

#### 2.2.1. EDTF Date

EDTF 日期本质上是完整 ISO8601 日期的第一部分，其正则表达式可以表示为 `\d{4}(-\d{2}(-\d{2})?)?`

```text
1981
2012-05
2022-01-30
```

#### 2.2.2. EDTF Date Ranges

Markwhen 目前符合 0 级 EDTF 标准，支持的范围包括：

```text
1964/2008
2004-06 / 2006-08
2004-02-01/ 2005-02-08
2004-02-01 /2005-02
2004-02-01/2005
2005/2006-02
2005/now
2018/6 months
```

Open-ended ranges（开放式范围）不支持.

Ranges start and end with either a EDTF Date or Relative Date or the special keyword now.
范围有开始和结束，可以是 EDTF 日期或相对日期或特殊关键字 now。

> NOTE
>
> 虽然 `now` 关键字现在和将来都会得到支持，但由于其歧义性而不建议使用。`now` 既可能表示作者编写 markwhen 文档的时间，也可能表示文档被解析的时间等。请尽量使用具体日期（即 `2025-03-01` 而不仅仅是 `March` ）。

#### 2.2.3. 非 EDTF 日期 Non-EDTF Dates

除了 EDTF 之外，其他日期格式也开箱即用。支持人类可读的日期，例如 `1665` `03/2222` `09/11/2001` `18 March 2026` `Aug 30 9:45am` ，以及 IO8601 日期，例如 `2031-11-19T01:35:10Z` 。人类可读的日期格式默认为美式月/日/年，但可以通过 Header 更改为欧式格式。

#### 2.2.4. 非 EDTF 日期范围 Non-EDTF Date Ranges

非 EDTF 日期范围通常是 `Date[-Date]`；也就是说，一个日期后面可以跟着破折号 ( `-` ) 或单词 `to` 和另一个日期。

如果未指定结束日期，则范围与其粒度一样长。例如，事件

```mw
2001: A Space Odyssey
```

从 2001 年 1 月 1 日开始，持续至 2001 年 12 月 31 日。

| 例子                                        | 推断出的范围 开始时间  | 推断出的范围 结束时间  | 解释                                                                                                                                                                 |
| ------------------------------------------- | ---------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `2024`                                      | `2024-01-01T00:00:00Z` | `2025-01-01T00:00:00Z` | 从 2024 年初到 2024 年底                                                                                                                                             |
| `04/1776`                                   | `1776-04-01T00:00:00Z` | `1776-05-01T00:00:00Z` | 从 1776 年 4 月初到 1776 年 4 月底                                                                                                                                   |
| `01/01/2024`                                | `2024-01-01T00:00:00Z` | `2024-01-02T00:00:00Z` | 2024 年 1 月 1 日开始，至 2024 年 1 月 1 日结束（全天）                                                                                                              |
| `11/11/2024-12/12/2024`                     | `2024-11-11T00:00:00Z` | `2024-12-13T00:00:00Z` | 从 2024 年 11 月 11 日开始，到 2024 年 12 月 12 日结束。                                                                                                             |
| `2031-11-19T01:35:10Z-2099-08-04T18:22:48Z` | `2031-11-19T01:35:10Z` | `2099-08-04T18:22:48Z` | 与 ISO 日期所说的完全一样具体。                                                                                                                                      |
| `January 3 - Apr 6`                         | `2025-01-03T00:00:00Z` | `2025-04-07T00:00:00Z` | 由于本文档撰写于 2025 年，因此年份推断为 2025 年。请注意，该范围延伸至 4 月 6 日结束 ，因此它对应 4 月 7 日的开始 。由于缺乏明确的年份，因此不建议使用此类日期范围。 |
| `now - 10 years 6 months 3 days`            | `now`                  | 10 年 6 个月 3 天后    | `now` 是每次时间轴渲染的时间，并不是写文档的时间。`10 years 6 months 3 days` 是一个相对日期                                                                          |
| `3:30pm - 4:30pm`                           | 今天日期的 `15:30`     | 今天日期的 `16:30`     | 当时间单独出现时，它基于最后看到的日期，如果没有，则是今天                                                                                                           |
| `1 Jan 1998 to 11/11/2011 8am`              | `1998-01-01T00:00:00Z` | `2011-11-11T08:00:00Z` |
| `Nov 11 02:30`                              | `2011-11-11T02:30:00Z` | `2011-11-11T02:30:00Z` | 当指定时间（小时/分钟）时，粒度是瞬间                                                                                                                                |

> 模糊格式 Ambiguous formats
>
> Markwhen 的设计目标是易于上手并立即使用。这种简单性的一部分体现在它支持可能比预期更模糊的日期和日期范围。例如， `April 1 - June 18` 、 `Nov 11 2:30` 和 `2020 - now` 都是完全有效的 markwhen 日期范围，但由于它们可能缺少年份或范围会变化，在未来解析时可能代表不同的含义。你应该三思而后行，避免使用任何模糊的日期语法，以确保它确实是你想要的。

#### 相对日期 Relative Dates

如果你有基于其他事件或相对于其他事件的事件，你可以描述它们之间的关系以获得你想要的范围。

例如，假设你正在使用一个项目追踪器。你可以通过使用绝对日期来概述你的项目阶段，如下所示：

```mw
// To indicate we are using European date formatting
dateFormat: d/M/y
 
// 2 weeks
01/01/2023 - 14/01/2023: Phase 1 #Exploratory
 
// Another 2 weeks
15/01/2023 - 31/01/2023: Phase 2 #Implementation
 
// 1 month
02/2023: Phase 3 #Implementation
 
// 3 days, after a one week buffer
07/03/2023 - 10/03/2023: Phase 4 - kickoff! #Launch
```

![alt text](images/image.png)

然而，一旦发生变更（比如出现疏漏或估计错误），你就必须逐个检查所有事件并手动修改它们的日期。如果变更发生在早期，这将尤其麻烦。

使用相对日期，我们可以这样表达相同的时间线：

```mw
// 2 weeks
01/01/2023 - 2 weeks: Phase 1 #Exploratory
 
// Another 2 weeks
2 weeks: Phase 2 #Implementation
 
// 1 month
1 month: Phase 3 #Implementation
 
// One week after phase 3 ends, a 3 days kickoff event
1 week - 3 days: Phase 4 - kickoff! #Launch
```

相对日期基于前一个日期，这可以追溯到我们的第一个日期， `01/01/2023`。

#### 事件 ID Event IDs

这种方式对于每个日期都依赖于前一个日期的串行日期来说已经足够好，但如果我们有多个事件都依赖于同一个事件呢？我们可以使用事件 ID 来实现这一点：

```mw
01/01/2023 - 2 weeks: Phase 1 #Exploratory
id: Phase1
 
// Another 2 weeks
after !Phase1 2 weeks: Phase 2, in parallel with Phase 3 #Implementation
 
// 1 month
after !Phase1 1 month: Phase 3, in parallel with Phase 2 #Implementation
 
// 3 days, after a one week buffer
1 week - 3 days: Phase 4 - kickoff! #Launch
```

单词 `after` 是可选的，我们也可以说 `!Phase1 2 weeks: Phase 2, in parallel with Phase 3 #Implementation` 来达到同样的效果。



### 2.3. 事件描述

### 2.4. Section 定义

### 2.5. 评论

### 2.6. 事件属性
