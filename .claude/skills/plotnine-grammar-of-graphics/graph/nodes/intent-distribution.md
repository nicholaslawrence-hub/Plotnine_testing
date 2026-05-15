# intent-distribution

Use when the prompt asks for the distribution of one numeric variable.

Signals: histogram, distribution, bins, filled by group, faceted by group.

Primary path:

```text
intent-distribution -> primitive-histogram -> layer-aesthetic-mapping -> layer-facets? -> layer-labels-theme -> output-save
```

Map the measured variable to `x`. Map comparison groups to `fill` when requested.

## Examples

### Single Distribution

```text
Create a histogram of Avg_Daily_Usage_Hours with 20 bins.
```

### Filled Distribution

```text
Show the distribution of usage hours filled by Gender.
```

### Faceted Distribution

```text
Create a histogram of Avg_Daily_Usage_Hours filled by Gender and faceted by Academic_Level.
```
