# intent-counts

Use when the prompt asks for counts by category or percentages of categories.

Signals: bar chart, count, frequency, percentage labels, each cylinder count.

Primary path:

```text
intent-counts -> primitive-bar -> layer-stat-computed-labels? -> primitive-text? -> layer-labels-theme -> output-save
```

Use `geom_bar()` for counts. Use `geom_text(..., stat='count')` with `after_stat(...)` when labels are computed from counts.

## Examples

### Category Counts

```text
Create a bar chart showing the count of cars for each cylinder count.
```

### Counts With Fill

```text
Make a filled bar chart of car counts by cyl, treating cyl as a categorical variable.
```

### Percentage Labels

```text
Show counts by cylinder and add percentage labels above each bar.
```
