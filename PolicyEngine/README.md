PolicyEngine at the Congressional Hackathon 7.0
=========================================================

This work is based on a beta version of PolicyEngine's Congressional District Level Policy Impact Estimation Framework.

Different shapefile approaches were used:

- District shapefiles are from [The Downballot's maps database](https://docs.google.com/spreadsheets/d/13XkF59JKzvw4SeSq5mbgIFrJfYjK4amg9JoQE5e9grQ/edit?gid=0#gid=0).
- KML files from https://kml.house.gov/

We investigated Abolishing the SALT Deduction and it's impacts:

![Congressional District-level Impact of Abolishing the SALT Deduction](salt_impact_by_district.png).

### SNAP Benefits Analysis

Survey-weighted estimates of total SNAP benefits by congressional district across all 50 states plus DC.

![SNAP Benefits by Congressional District](snap_benefits_by_district.png)

**Total SNAP Benefits: $94 billion**

#### Running the SNAP Analysis

1. Generate SNAP data for all districts:
```bash
cd /home/baogorek/devl/code-snippets/calculation/snap
~/envs/pe/bin/python snap_districts.py
```
Output: `snap_by_congressional_district.csv`

2. Create the map visualization:
```bash
cd /home/baogorek/devl/Congressional-Hackathon-2025/PolicyEngine
~/envs/pe/bin/python plot_snap_impacts.py
```
Output: `snap_benefits_by_district.png`

#### Top States by SNAP Benefits
- AL: $15.1B
- AZ: $14.7B
- CA: $8.6B
- AK: $5.5B
- AR: $4.6B


### Animated Transition Idea
![Animated SALT Impact](salt_impact_animation.gif)

The animation transitions from the baseline (zero impact - would be better if they were actual values of something!) to the final income impacts after abolishing the SALT deduction. Districts with yellow borders in the final frame are the most affected by the policy change. California districts experience the largest negative income impacts, with some losing over $1,600 per household annually.

It's cool to see data in motion, but there are two values so it's debateable how much value this adds

## Technical Notes

### Congressional District GEOID Mapping
When working with congressional district data, there's an important distinction in how single-district (at-large) states are encoded:

- **Shapefile convention**: At-large districts use state FIPS + "00" (e.g., Alaska = 0200) - using 0-based indexing
- **PolicyEngine data convention**: At-large districts use state FIPS + "01" (e.g., Alaska = 0201) - using 1-based indexing

This is essentially a 0-based vs 1-based indexing difference: shapefiles start counting from 0, while PolicyEngine starts from 1. Multi-district states don't show this difference since both conventions use "01" for the first district when there are multiple districts.

This affects the following states with single congressional districts:
- Alaska (02)
- Delaware (10)
- North Dakota (38)
- South Dakota (46)
- Vermont (50)
- Wyoming (56)

The visualization script (`plot_income_stats.py`) includes a mapping correction to ensure these districts display properly with their data.
