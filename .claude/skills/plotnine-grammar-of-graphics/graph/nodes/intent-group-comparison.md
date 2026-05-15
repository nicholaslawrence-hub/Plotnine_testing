# intent-group-comparison

Use when the prompt asks to compare a numeric variable across categories.

Signals: boxplot, grouped by, distribution across groups, overlay individual points.

Primary path:

```text
intent-group-comparison -> primitive-boxplot -> primitive-jitter? -> layer-aesthetic-mapping -> layer-labels-theme -> output-save
```

Map the group to categorical `x`, often with `factor(...)`, and the measured value to `y`.

## Examples

### Boxplot Comparison

```text
Compare mpg across cylinder counts with a boxplot.
```

### Grouped Distribution

```text
Show the distribution of mpg grouped by cyl, treating cyl as categorical.
```

### Boxplot With Points

```text
Create a boxplot of mpg by cylinder count and overlay jittered individual points.
```
