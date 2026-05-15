# intent-relationship

Use when the prompt asks how two quantitative variables relate.

Signals: scatter plot, relationship, correlation, x versus y, compare horsepower and mpg.

Primary path:

```text
intent-relationship -> primitive-point -> layer-aesthetic-mapping -> primitive-smooth? -> layer-labels-theme -> output-save
```

Usually maps `x` and `y` to numeric columns. Add `color='factor(...)'` when a categorical grouping is requested.

## Examples

### Scatter Relationship

```text
Create a scatter plot of horsepower on x and miles per gallon on y.
```

### Relationship With Grouping

```text
Show hp versus mpg and color the points by cylinder count as a category.
```

### Relationship With Trend

```text
Compare wt and mpg with points and add a linear trend line with no confidence interval.
```
