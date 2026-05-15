# example-bar-percent-labels

Rendered asset:

```text
assets/fewshots/bar_with_percent_labels.png
```

Use this as the canonical few-shot for:

```text
intent-counts -> primitive-bar -> layer-stat-computed-labels -> primitive-text -> layer-labels-theme -> output-save
```

Prompt:

```text
Create a bar chart of car counts by cyl with percentage labels and save to output.png.
```

Code:

```python
from plotnine import *
from plotnine.data import mtcars
import pandas as pd

df = pd.DataFrame(mtcars)
p = (
    ggplot(df, aes(x='factor(cyl)', fill='factor(cyl)'))
    + geom_bar()
    + geom_text(
        aes(label=after_stat('prop*100'), group=1),
        stat='count',
        nudge_y=0.5,
        format_string='{:.1f}%'
    )
    + labs(title='Cars by Cylinder Count', x='Cylinders', y='Count', fill='Cylinders')
    + theme_classic()
)
p.save('output.png', dpi=150, width=8, height=6)
```

Judge expectation:

The chart should use `geom_bar()` for counts and `geom_text()` with `after_stat(...)` and `format_string` for computed labels.

