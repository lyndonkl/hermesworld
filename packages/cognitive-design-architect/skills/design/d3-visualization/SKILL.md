---
name: d3-visualization
description: Builds interactive charts, networks, and maps with D3.js.
version: 1.0.0
author: Kushal D'Souza (lyndonkl)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: design
    tags: [D3.js, Data Visualization, Charts, SVG, Interactive Graphics]
    related_skills: [cognitive-design, visual-storytelling-design, cognitive-fallacies-guard]
---
# D3.js Data Visualization

Guides the construction of custom, interactive data visualizations with D3.js: bar, line, and scatter charts; force-directed networks; hierarchies; geographic maps; and real-time updates with zoom, pan, brush, and animated transitions. It covers the data-join, scale, shape, layout, and interaction layers with step-by-step workflows and copy-and-adapt templates. It does not choose the chart type for you or judge whether a chart misleads; `cognitive-design` and `cognitive-fallacies-guard` do that.

## When to Use

- The user mentions D3, d3.js, custom visualization, force-directed graph, or data-driven SVG.
- Chart libraries (Highcharts, Chart.js) lack the customization needed and low-level control over scales, shapes, and layouts is required.
- Building bar, line, or scatter charts, network diagrams, geographic maps, or hierarchies (tree, treemap, pack, partition).
- Adding zoom, pan, brush, or drag interactions, animated transitions, or real-time data updates to an existing visualization.
- Not for picking an encoding (`cognitive-design`), wrapping a chart in narrative (`visual-storytelling-design`), or checking chart honesty (`cognitive-fallacies-guard`).

Load any reference file with `skill_view("d3-visualization", file_path="references/<file>.md")`; the paths below are relative to this skill.

---

## Overview

D3 provides low-level building blocks for data-driven DOM manipulation, visual encoding, layout algorithms, and interactions — enabling bespoke visualizations that chart libraries cannot provide.

**Use D3 when:** Chart libraries lack your specific design, you need full customization, you're building network graphs/hierarchies/maps, or animating data changes smoothly.

**Prefer simpler tools when:** Simple bar/line charts suffice (Chart.js, Highcharts), you need 3D (Three.js, WebGL), or datasets exceed 10K points without aggregation.

**Core concepts:** Data Joins (bind arrays to DOM elements), Scales (data values to visual values), Shapes (SVG path generation), Layouts (position calculation for networks/trees/maps), Transitions (animated state changes), Interactions (zoom/pan/drag/brush).

### Skill Structure

- **[Getting Started](references/getting-started.md)**: Setup, prerequisites, first visualization
- **[Selections & Data Joins](references/selections-datajoins.md)**: DOM manipulation, data binding
- **[Scales & Axes](references/scales-axes.md)**: Data transformation, axis generation
- **[Shapes & Layouts](references/shapes-layouts.md)**: Path generators, basic layouts
- **[Advanced Layouts](references/advanced-layouts.md)**: Force simulation, hierarchies, geographic maps
- **[Transitions & Interactions](references/transitions-interactions.md)**: Animations, zoom/pan/drag/brush
- **[Workflows](references/workflows.md)**: Step-by-step guides for common chart types
- **[Common Patterns](references/common-patterns.md)**: Reusable code templates

---

## Workflows

Choose a workflow based on your current task:

### Create Basic Chart Workflow

**Use when:** Building bar, line, or scatter charts from scratch

**Time:** 1-2 hours

**Copy this checklist and track your progress:**

```
Basic Chart Progress:
- [ ] Step 1: Set up SVG container with margins
- [ ] Step 2: Load and parse data
- [ ] Step 3: Create scales (x, y)
- [ ] Step 4: Generate axes
- [ ] Step 5: Bind data and create visual elements
- [ ] Step 6: Style and add interactivity
```

**Step 1: Set up SVG container with margins**

Create SVG element with proper dimensions. Define margins for axes: `{top: 20, right: 20, bottom: 30, left: 40}`. Calculate inner width/height: `width - margin.left - margin.right`. See [Getting Started](references/getting-started.md#setup-svg-container).

**Step 2: Load and parse data**

Use `d3.csv('data.csv')` for external files or define data array directly. Parse dates with `d3.timeParse('%Y-%m-%d')` for time series. Convert strings to numbers for CSV data using conversion function. See [Getting Started](references/getting-started.md#loading-data).

**Step 3: Create scales**

Choose scale types based on data: `scaleBand` (categorical), `scaleTime` (temporal), `scaleLinear` (quantitative). Set domains from data using `d3.extent()`, `d3.max()`, or manual ranges. Set ranges from SVG dimensions. See [Scales & Axes](references/scales-axes.md#scale-types).

**Step 4: Generate axes**

Create axis generators: `d3.axisBottom(xScale)`, `d3.axisLeft(yScale)`. Append g elements positioned with transforms. Call axis generators: `.call(axis)`. Customize ticks with `.ticks()`, `.tickFormat()`. See [Scales & Axes](references/scales-axes.md#creating-axes).

**Step 5: Bind data and create visual elements**

Use data join pattern: `svg.selectAll(type).data(array).join(type)`. Set attributes using scales and accessor functions: `.attr('x', d => xScale(d.category))`. For line charts, use `d3.line()` generator. For scatter plots, create circles with `cx`, `cy`, `r` attributes. See [Selections & Data Joins](references/selections-datajoins.md#data-join-pattern) and [Shapes & Layouts](references/shapes-layouts.md).

**Step 6: Style and add interactivity**

Apply colors: `.attr('fill', ...)`, `.attr('stroke', ...)`. Add hover effects: `.on('mouseover', ...)` with tooltip. Add click handlers for drill-down. Apply transitions for initial animation (optional). See [Transitions & Interactions](references/transitions-interactions.md#tooltips) and [Common Patterns](references/common-patterns.md#tooltip-pattern).

---

### Update Visualization with New Data

**Use when:** Refreshing charts with new data (real-time, filters, user interactions)

**Time:** 30 minutes - 1 hour

**Copy this checklist:**

```
Update Progress:
- [ ] Step 1: Encapsulate visualization in update function
- [ ] Step 2: Update scale domains if needed
- [ ] Step 3: Re-bind data with key function
- [ ] Step 4: Add transitions to join
- [ ] Step 5: Update attributes with new values
- [ ] Step 6: Trigger update on data change
```

**Step 1: Encapsulate visualization in update function**

Wrap steps 3-5 from basic chart workflow in `function update(newData) { ... }`. This makes visualization reusable for any dataset. See [Workflows](references/workflows.md#update-pattern-workflow).

**Step 2: Update scale domains**

Recalculate domains when data range changes: `yScale.domain([0, d3.max(newData, d => d.value)])`. Update axes with transition: `svg.select('.y-axis').transition().duration(500).call(yAxis)`. See [Selections & Data Joins](references/selections-datajoins.md#updating-scales).

**Step 3: Re-bind data with key function**

Use key function for object constancy: `.data(newData, d => d.id)`. Ensures elements track data items, not array positions. Critical for correct transitions. See [Selections & Data Joins](references/selections-datajoins.md#key-functions-object-constancy).

**Step 4: Add transitions to join**

Insert `.transition().duration(500)` before attribute updates. Specify easing with `.ease(d3.easeCubicOut)`. For custom enter/exit effects, use enter/exit functions in `.join()`. See [Transitions & Interactions](references/transitions-interactions.md#basic-pattern).

**Step 5: Update attributes with new values**

Set positions/sizes using updated scales: `.attr('y', d => yScale(d.value))`, `.attr('height', d => height - yScale(d.value))`. Transitions animate from old to new values. See [Common Patterns](references/common-patterns.md#bar-chart-template).

**Step 6: Trigger update on data change**

Call `update(newData)` when data changes: button clicks, timers (`setInterval`), WebSocket messages, API responses. For real-time, use sliding window to limit data points. See [Workflows](references/workflows.md#real-time-updates-workflow).

---

### Create Advanced Layout Workflow

**Use when:** Building network graphs, hierarchies, or geographic maps

**Time:** 2-4 hours

**Copy this checklist:**

```
Advanced Layout Progress:
- [ ] Step 1: Choose appropriate layout type
- [ ] Step 2: Prepare and structure data
- [ ] Step 3: Create and configure layout
- [ ] Step 4: Apply layout to data
- [ ] Step 5: Bind computed properties to elements
- [ ] Step 6: Add interactions (drag, zoom)
```

**Step 1: Choose appropriate layout type**

**Force Simulation**: Network diagrams, organic clustering. **Hierarchies**: Tree, cluster (node-link), treemap, pack, partition (space-filling). **Geographic**: Maps with projections. **Chord**: Flow diagrams. See [Advanced Layouts](references/advanced-layouts.md#choosing-layouts) for decision guidance.

**Step 2: Prepare and structure data**

**Force**: `nodes = [{id, group}]`, `links = [{source, target}]`. **Hierarchy**: Nested objects with children arrays, convert with `d3.hierarchy(data)`. **Geographic**: GeoJSON features. See the Basic Setup, Creating Hierarchies, and GeoJSON sections of [Advanced Layouts](references/advanced-layouts.md).

**Step 3: Create and configure layout**

**Force**: `d3.forceSimulation(nodes).force('link', d3.forceLink(links)).force('charge', d3.forceManyBody())`. **Hierarchy**: `d3.treemap().size([width, height])`. **Geographic**: `d3.geoMercator().fitExtent([[0,0], [width,height]], geojson)`. See [Advanced Layouts](references/advanced-layouts.md) for each layout type.

**Step 4: Apply layout to data**

**Force**: Simulation runs automatically, updates node positions each tick. **Hierarchy**: Call layout on root: `treemap(root)`. **Geographic**: No application needed, projection used in path generator. See [Advanced Layouts](references/advanced-layouts.md#pitfall-3-forgetting-to-apply-layout).

**Step 5: Bind computed properties to elements**

**Force**: Update `cx`, `cy` in tick handler: `node.attr('cx', d => d.x)`. **Hierarchy**: Use `d.x0`, `d.x1`, `d.y0`, `d.y1` for rectangles. **Geographic**: Use `path(feature)` for `d` attribute. See [Workflows](references/workflows.md) for layout-specific examples.

**Step 6: Add interactions**

**Drag** for force networks: `node.call(d3.drag().on('drag', dragHandler))`. **Zoom** for maps/large networks: `svg.call(d3.zoom().on('zoom', zoomHandler))`. **Click** for hierarchy drill-down. See [Transitions & Interactions](references/transitions-interactions.md).

---

## Path Selection Menu

**What would you like to do?**

1. **[I'm new to D3](references/getting-started.md)** - Setup environment, understand prerequisites, create first visualization

2. **[Build a basic chart](references/workflows.md#bar-chart-workflow)** - Bar, line, or scatter plot step-by-step

3. **[Transform data with scales](references/scales-axes.md)** - Map data values to visual properties (positions, colors, sizes)

4. **[Bind data to elements](references/selections-datajoins.md)** - Connect arrays to DOM elements, handle dynamic updates

5. **[Create network/hierarchy/map](references/advanced-layouts.md)** - Force-directed graphs, treemaps, geographic visualizations

6. **[Add animations](references/transitions-interactions.md#transitions)** - Smooth transitions between chart states

7. **[Add interactivity](references/transitions-interactions.md#interactions)** - Zoom, pan, drag, brush selection, tooltips

8. **[Update chart with new data](references/workflows.md#update-pattern-workflow)** - Handle real-time data, filters, user interactions

9. **[Get code templates](references/common-patterns.md)** - Copy-paste-modify templates for common patterns

10. **[Understand D3 concepts](references/getting-started.md#core-concepts)** - Deep dive into data joins, scales, generators, layouts

---

## Quick Reference

### Data Join Pattern (Core D3 Workflow)

```javascript
// 1. Select container
const svg = d3.select('svg');

// 2. Bind data
svg.selectAll('circle')
  .data(dataArray)
  .join('circle')          // Create/update/remove elements automatically
    .attr('cx', d => d.x)  // Use accessor functions (d = datum, i = index)
    .attr('cy', d => d.y)
    .attr('r', 5);
```

### Scale Creation (Data → Visual Transformation)

```javascript
// For quantitative data
const xScale = d3.scaleLinear()
  .domain([0, 100])        // Data range
  .range([0, 500]);        // Pixel range

// For categorical data
const xScale = d3.scaleBand()
  .domain(['A', 'B', 'C'])
  .range([0, 500])
  .padding(0.1);

// For temporal data
const xScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2020, 11, 31)])
  .range([0, 500]);
```

### Shape Generators (SVG Path Creation)

```javascript
// Line chart
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value));

svg.append('path')
  .datum(data)           // Use .datum() for single data item
  .attr('d', line)       // Line generator creates path data
  .attr('fill', 'none')
  .attr('stroke', 'steelblue');
```

### Transitions (Animation)

```javascript
// Add transition before attribute updates
svg.selectAll('rect')
  .data(newData)
  .join('rect')
  .transition()          // Everything after this is animated
  .duration(500)         // Milliseconds
  .attr('height', d => yScale(d.value));
```

### Common Scale Types

| Data Type | Task | Scale |
|-----------|------|-------|
| Quantitative (linear) | Position, size | `scaleLinear()` |
| Quantitative (exponential) | Compress range | `scaleLog()`, `scalePow()` |
| Quantitative → Circle area | Size circles | `scaleSqrt()` |
| Categorical | Bars, groups | `scaleBand()`, `scalePoint()` |
| Categorical → Colors | Color encoding | `scaleOrdinal()` |
| Temporal | Time series | `scaleTime()` |
| Quantitative → Colors | Heatmaps | `scaleSequential()` |

### D3 Module Imports (ES6)

```javascript
// Specific functions
import { select, selectAll } from 'd3-selection';
import { scaleLinear, scaleBand } from 'd3-scale';
import { line, area } from 'd3-shape';

// Entire D3 namespace
import * as d3 from 'd3';
```

### Key References by Task

- **Setup & First Chart**: [Getting Started](references/getting-started.md)
- **Data Binding**: [Selections & Data Joins](references/selections-datajoins.md)
- **Scales & Axes**: [Scales & Axes](references/scales-axes.md)
- **Chart Types**: [Workflows](references/workflows.md) + [Common Patterns](references/common-patterns.md)
- **Networks & Trees**: [Advanced Layouts](references/advanced-layouts.md#force-simulation) + [Advanced Layouts](references/advanced-layouts.md#hierarchies)
- **Maps**: [Advanced Layouts](references/advanced-layouts.md#geographic-maps)
- **Animation**: [Transitions & Interactions](references/transitions-interactions.md#transitions)
- **Interactivity**: [Transitions & Interactions](references/transitions-interactions.md#interactions)

---

## Verification

Write the finished chart to a self-contained `.html` file with `write_file` and open it in a browser (or serve the folder through `terminal`). Then check:

- The browser console is clean; no `NaN` appears in any `d` attribute or `transform`.
- Bars start at zero, axes carry units, and ticks read without hunting through a legend.
- `.data()` uses a key function wherever the data can change, so transitions track items rather than array positions.
- Transitions run only on updates, never on the initial render.
- Hover, zoom, and brush still work after an update; calling the update function twice with the same data changes nothing.

`assets/evaluation-rubric.json` scores the guidance in this skill itself (completeness, actionability, resource quality) and is for maintainers, not for judging a chart. For chart honesty run `cognitive-fallacies-guard`.

---

## Next Steps

1. **New to D3?** Start with [Getting Started](references/getting-started.md)
2. **Know basics?** Jump to [Workflows](references/workflows.md) for specific chart types
3. **Need reference?** Use [Common Patterns](references/common-patterns.md) for templates
4. **Build custom viz?** Explore [Advanced Layouts](references/advanced-layouts.md)
