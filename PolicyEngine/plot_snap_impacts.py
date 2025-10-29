import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

impact_df = pd.read_csv('/home/baogorek/devl/code-snippets/calculation/snap/snap_by_congressional_district.csv')

hex_gdf = gpd.read_file('HexCDv31/HexCDv31.shp')
hex_gdf['cd_id'] = hex_gdf['GEOID'].astype(int)

nonvoting_gdf = gpd.read_file('HexDDv20/HexDDv20.shp')
dc_gdf = nonvoting_gdf[nonvoting_gdf['GEOID'] == '1198'].copy()
dc_gdf['cd_id'] = dc_gdf['GEOID'].astype(int)
dc_gdf['STATEAB'] = dc_gdf['ABBREV']
dc_gdf['STATENAME'] = dc_gdf['NAME']
dc_gdf['CDLABEL'] = dc_gdf['ABBREV']

hex_gdf = pd.concat([hex_gdf, dc_gdf], ignore_index=True)

single_district_states = {
    200: 201,
    1000: 1001,
    3800: 3801,
    4600: 4601,
    5000: 5001,
    5600: 5601,
    1198: 1101
}
hex_gdf['cd_id'] = hex_gdf['cd_id'].replace(single_district_states)

merged_gdf = hex_gdf.merge(
    impact_df[['congressional_district_geoid', 'total_weighted_snap', 'state']],
    left_on='cd_id',
    right_on='congressional_district_geoid',
    how='left'
)

merged_gdf['snap_millions'] = merged_gdf['total_weighted_snap'] / 1_000_000

fig, ax = plt.subplots(figsize=(20, 12))

merged_gdf.plot(
    column='snap_millions',
    ax=ax,
    legend=True,
    cmap='YlOrRd',
    edgecolor='black',
    linewidth=0.3,
    missing_kwds={'color': 'lightgray', 'label': 'No Data'},
    legend_kwds={'label': 'SNAP Benefits (Millions $)', 'shrink': 0.8}
)
ax.set_title('Total SNAP Benefits by Congressional District\n(Annual Weighted Totals)',
              fontsize=16, fontweight='bold')
ax.axis('off')

plt.tight_layout()
plt.savefig('snap_benefits_by_district.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n=== SNAP Benefits Summary Statistics ===")
print(f"Districts with data: {impact_df.shape[0]}")
print(f"Total districts in shapefile: {hex_gdf.shape[0]}")
print(f"\nTotal SNAP Benefits: ${impact_df['total_weighted_snap'].sum():,.0f}")
print(f"Average per district: ${impact_df['total_weighted_snap'].mean():,.0f}")
print(f"Median per district: ${impact_df['total_weighted_snap'].median():,.0f}")

print(f"\nTop 10 Districts by SNAP Benefits:")
top_10 = impact_df.nlargest(10, 'total_weighted_snap')[['congressional_district_geoid', 'state', 'total_weighted_snap']]
top_10['total_weighted_snap'] = top_10['total_weighted_snap'].apply(lambda x: f"${x:,.0f}")
print(top_10.to_string(index=False))

print(f"\nBottom 10 Districts by SNAP Benefits:")
bottom_10 = impact_df.nsmallest(10, 'total_weighted_snap')[['congressional_district_geoid', 'state', 'total_weighted_snap']]
bottom_10['total_weighted_snap'] = bottom_10['total_weighted_snap'].apply(lambda x: f"${x:,.0f}")
print(bottom_10.to_string(index=False))

state_totals = impact_df.groupby('state')['total_weighted_snap'].sum().reset_index()
state_totals = state_totals.sort_values('total_weighted_snap', ascending=False)
state_totals.columns = ['State', 'Total SNAP Benefits']

print(f"\nTop 10 States by Total SNAP Benefits:")
top_states = state_totals.head(10).copy()
top_states['Total SNAP Benefits'] = top_states['Total SNAP Benefits'].apply(lambda x: f"${x:,.0f}")
print(top_states.to_string(index=False))
