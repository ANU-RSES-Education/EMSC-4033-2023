import streamlit as st
import numpy as np
from scipy.stats import norm
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import branca
import branca.colormap as cm
import os 

st.set_page_config(layout='wide')

app_title = "Seismic Risk Index Map of Perth, Western Australia Based on Building Vulnerability"
intro_text = "Perth, which hosts 75% of Western Australia's population, is the largest city in the \
            state and the fourth most populous urban area in Australia. However, the city's rapid \
            population growth in recent years has resulted in a corresponding increase in its \
            vulnerability to natural disasters, including seismic hazards. Seismic hazard in Perth \
            is strongly influence by the south-west seismic zone (SWSZ), a region with high \
            earthquake frequency. The SWSZ is one of the most seismically active areas in Australia, \
            having experienced several earthquakes with local magnitude 5.9 or higher in the past 40 \
            years. This hazard can cause significant damage to buildings and infrastructure, as well \
            as loss of life. In order to mitigate the risk of seismic hazards, we need to understand \
            the physical vulnerability of buildings and infrastructure to these hazards through \
            seismic risk assessment. Here, M6.0 earthquake is simulated to occur in Perth Area with \
            the Darling Fault as the source of the eartquake. Buildings are assumed to be constructed \
            using unreinforced masonry, wood, or reinforced concrete. PGA and Probability of Damage map are \
            produced based on this scenario to analyze the risk."
header1 = "Hazards"
header2 = "Exposure and Physical Vulnerability"
header3 = "Perth Seismic Risk Index"
subheader1 = "Peak Ground Acceleration (PGA) Map"
subheader2 = "Probability of Damage Map"


# Current working directory
current_dir = os.getcwd()

def display_seismicity_map(base_gdf, data_gdf):    
    # Create subplots
    fig1, ax = plt.subplots(1, 1, figsize = (10, 10))

    # Plot data
    base_gdf.plot(ax = ax, color = 'bisque', edgecolor = 'dimgray')
    for idx, row in base_gdf.iterrows():
        plt.annotate(text=row['STE_NAME21'], xy=row['coords'][0], ha="center", fontsize=6)
    
    data_gdf.plot(ax = ax, marker = 'o', color = 'red', markersize = 3)

    # Set title and label
    plt.title("Seismicity Map of Australia (Jan 1990 - Mar 2023)", fontsize=15)
    plt.xlabel("Longitude", fontsize=15)
    plt.ylabel("Latitude", fontsize=15)
    
    st.pyplot(fig1)

def display_map_pga(gdf,color):
    # Create folium map
    map_pga = folium.Map(location=[gdf.lat.mean(), gdf.lon.mean()], zoom_start=9, scrollWheelZoom=False, tiles="CartoDB positron")

    # Create colormaps
    colormaps = cm.LinearColormap(colors=['green','yellow','red'], vmin=gdf[color].min(), vmax=gdf[color].max())
    colormaps.caption = 'PGA (g)'
    colormaps.add_to(map_pga)

    # Plotting
    folium.GeoJson(
        gdf,
        style_function = lambda feature: {
            "weight":0.5, 
            'color':'black',
            'fillColor':colormaps(feature['properties']["gmv_PGA"]),
            'fillOpacity':1,
        },
        tooltip=folium.GeoJsonTooltip(fields=['SAL_NAME21', 'gmv_PGA'], aliases=["Suburb ","PGA "])
    ).add_to(map_pga)

    # Add folium map to streamlit
    st_map_pga = st_folium(map_pga, width=700, height=600 )
    #st.caption("Peak Ground Acceleration (PGA) Map")
    
def display_dataframe(df, col):
    # Create a list as a option for select box
    suburbs = [" All suburbs"] + list(df[col].unique())
    suburbs.sort()

    # Create select box to filter dataframe
    suburb_opt = st.selectbox('Select a suburb', suburbs)

    # Filtering dataframe
    if suburb_opt == " All suburbs":
        filtered_df = df.copy()
    else:
        filtered_df = df[df[col] == suburb_opt]

    # Add filtered dataframe to streamlit
    st.dataframe(filtered_df,use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download CSV', csv, 'file.csv', 'text/csv')

def display_building_map(base_gdf, data_gdf):
    # Create subplots
    fig2, ax = plt.subplots(1, 1, figsize = (4, 4))

    # Plot data
    base_gdf.plot(ax = ax, color = 'bisque', edgecolor = 'dimgray')
    data_gdf.plot(ax = ax, color = 'blue', edgecolor = 'dimgray', markersize=2)

    # Set title
    plt.title('Building Distribution in Perth, WA', fontsize=10)
    ax.set_xlim(115.25, 116.75)
    ax.tick_params(axis='both', which='major', labelsize=6)
    plt.xlabel("Longitude",  fontsize=10)
    plt.ylabel("Latitude",  fontsize=10)
    
    st.pyplot(fig2)

def display_fragility_filter(df, col):    
    frag_id = df[col].unique()
    frag_id_opt = st.selectbox('Select fragility function', frag_id)
    
    return frag_id_opt

def display_fragility_curves(df, col, id):
    # Define the range of PGA values
    pga_values = np.linspace(0.0, 3, 300) 

    frag_id_filtered = df[df[col] == id]

    # Plot the fragility curve
    fig3 = plt.figure()
    plt.plot(pga_values, norm.cdf(pga_values, frag_id_filtered["slight_mean"], frag_id_filtered["slight_stddev"]), label="slight damage")
    plt.plot(pga_values, norm.cdf(pga_values, frag_id_filtered["moderate_mean"], frag_id_filtered["moderate_stddev"]), label="moderate damage")
    plt.plot(pga_values, norm.cdf(pga_values, frag_id_filtered["extensive_mean"], frag_id_filtered["extensive_stddev"]), label="extensive damage")
    plt.plot(pga_values, norm.cdf(pga_values, frag_id_filtered["complete_mean"], frag_id_filtered["complete_stddev"]), label="complete damage")
    plt.xlabel('PGA (g)')
    plt.ylabel('Probability of Exceedance')
    plt.title('Fragility Curve - ' + id)
    plt.legend()
    plt.grid(True)

    st.pyplot(fig3)

def taxonomy_filter(df, col):
    taxonomy = ["All taxonomy"] + list(df[col].unique())
    taxonomy_opt = st.selectbox('Select taxonomy', taxonomy)

    return taxonomy_opt

def display_bar_plot(df, col,id):
    fig4, ax = plt.subplots(1, 1)

    if id == "All taxonomy":
        summ_df = df.loc[:,["structural~no_damage","structural~slight","structural~moderate","structural~extensive","structural~complete"]].sum(axis = 0)
        summ_df.plot(kind='bar', ax=ax, ylabel='Number of assets', color='sandybrown')
    else:
        taxonomy_filtered = df[df[col] == id]
        summ_df = taxonomy_filtered.loc[:,["structural~no_damage","structural~slight","structural~moderate","structural~extensive","structural~complete"]].sum(axis = 0)
        summ_df.plot(kind='bar', ax=ax, ylabel='Number of assets',color='sandybrown')
    
    st.pyplot(fig4)

def display_probability_map(gdf, dictionary):
     # Create Folium map
    probability_map = folium.Map(location=[gdf.lat.mean(), gdf.lon.mean()], zoom_start=9, scrollWheelZoom=False, tiles="CartoDB positron")
    
     # Create colormaps
    colormaps = cm.LinearColormap(colors=['white','yellow','orange','red'], vmin=0, vmax=1)
    colormaps.add_to(probability_map)

    # Plotting
    for key, value in dictionary.items():
        colormaps.caption = 'Probability of ' + value
        folium.GeoJson(
            gdf,
            style_function = lambda feature: {
                "weight":0.5, 
                'color':'black',
                'fillColor':colormaps(feature['properties'][key]),
                'fillOpacity':1,
            },
            name=value,
            tooltip=folium.GeoJsonTooltip(fields=['index_left', key], aliases=["Suburb ","Probability "])
        ).add_to(probability_map)
    folium.LayerControl().add_to(probability_map)
    
    # Add folium map to streamlit
    st_probability_map = st_folium(probability_map, width=700, height=600 )
    #st.caption("Probability of Damage Map")

@st.cache_data
def load_data():
    # Read SHP of Australia and use WGS 84 (epsg:4326) as the geographic coordinate system
    aus_gdf = gpd.read_file(os.path.join(current_dir, "SHP", "STE_2021_AUST_GDA2020" + ".shp"))
    aus_gdf.drop(aus_gdf.tail(1).index,inplace=True)
    aus_gdf['coords'] = aus_gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
    aus_gdf = aus_gdf.to_crs(epsg=4326)

    # Read SHP of Perth suburb and use WGS 84 (epsg:4326) as the geographic coordinate system
    perth_gdf = gpd.read_file(os.path.join(current_dir,"SHP","perth_suburb" + ".shp"))
    perth_gdf = perth_gdf.to_crs(epsg=4326)
    perth_buildings_gdf = gpd.read_file(os.path.join(current_dir, "SHP", "perth_suburb_buildings" + ".shp"))
    perth_buildings_gdf = perth_buildings_gdf.to_crs(epsg="4326")

    # Read csv file as dataframe, convert it to geodataframe, and use WGS 84 (epsg:4326) as the geographic coordinate system
    events = pd.read_csv(os.path.join(current_dir, "SHP", "query_earthquakes" + ".csv"), delimiter = ";")
    events_gdf = gpd.GeoDataFrame(events, geometry=gpd.points_from_xy(events.Longitude,events.Latitude))
    events_gdf.set_crs('epsg:4326',inplace = True)

    # Read csv file of PGA generated from OpenQuake as dataframe
    avg_gmf_path = os.path.join(current_dir,"samples", "output", "avg_gmf_95" + ".csv")
    avg_gmf_df = pd.read_csv(avg_gmf_path, skiprows = 1)

    # Convert dataframe to geodataframe and use WGS 84 (epsg:4326) as the geographic coordinate system
    avg_gmf_gdf = gpd.GeoDataFrame(avg_gmf_df, geometry=gpd.points_from_xy(avg_gmf_df.lon, avg_gmf_df.lat))
    avg_gmf_gdf.set_crs('epsg:4326',inplace = True)

    # Spasial join geodataframe use index from second (or perth_gdf); retain only the perth_gdf geometry column
    suburb_pga = avg_gmf_gdf.sjoin(perth_gdf, how="right")
    suburb_pga_filtered =suburb_pga[ ~suburb_pga["custom_site_id"].isna()]
    suburb_pga_gdf = suburb_pga_filtered[["custom_site_id", "lon","lat","gmv_PGA", "SAL_NAME21","geometry"]]

    # Convert geodataframe to dataframe
    suburb_pga_df = pd.DataFrame(suburb_pga_gdf.drop(columns='geometry'))
    suburb_pga_df = suburb_pga_df.rename(columns={"gmv_PGA":"PGA", "SAL_NAME21":"suburb"})
    suburb_pga_df = suburb_pga_df.reindex(columns=["custom_site_id", "lon", "lat","suburb","PGA"])
    suburb_pga_df = suburb_pga_df.reset_index(drop=True)

    # Read csv file of damage realization generated from OpenQuake as dataframe
    avg_damage_path = os.path.join(current_dir, "samples", "output", "avg_damages-rlz-000_95" + ".csv")
    avg_damage_df = pd.read_csv(avg_damage_path, skiprows=1)

    # Read csv file of fragility function used in OpenQuake calculation as datafrane
    csv_path = os.path.join(current_dir, "samples", "output", "fragility_model" + ".csv")
    frag_curves_df = pd.read_csv(csv_path)
    frag_curves_df = frag_curves_df.loc[:, ~frag_curves_df.columns.str.contains('^Unnamed')]

    # Pivot table
    avg_damage_df_piv = pd.pivot_table(avg_damage_df, index = ["suburb"], 
                        values=["lon","lat","structural~no_damage","structural~slight","structural~moderate","structural~extensive","structural~complete"], 
                        aggfunc={"structural~no_damage": np.mean,
                                "structural~slight": np.mean,
                                "structural~moderate": np.mean,
                                    "structural~extensive": np.mean,
                                    "structural~complete": np.mean,
                                    "lon": np.mean,
                                    "lat": np.mean
                                })
    # Reset index pivot table
    avg_damage_piv_df = avg_damage_df_piv.reset_index()
    avg_damage_piv_df = avg_damage_piv_df.rename(columns={"structural~no_damage":"prob_of_no_damage","structural~slight":"prob_of_slight_damage",
                        "structural~moderate":"prob_of_moderate_damage","structural~extensive":"prob_of_extensive_damage","structural~complete":"prob_of_complete_damage"})
    avg_damage_piv_df = avg_damage_piv_df.reindex(columns=["suburb","lat","lon","prob_of_no_damage","prob_of_slight_damage","prob_of_moderate_damage","prob_of_extensive_damage","prob_of_complete_damage"])
    
    # Convert pivot table to geodataframe and use WGS 84 (epsg:4326) as the geographic coordinate system
    avg_damage_gdf = gpd.GeoDataFrame(avg_damage_df_piv, geometry=gpd.points_from_xy(avg_damage_df_piv.lon,avg_damage_df_piv.lat))
    avg_damage_gdf.set_crs(epsg="4326", inplace=True)

    # Spasial join geodataframe use index from second (or perth_gdf); retain only the perth_gdf geometry column
    suburb_damage = avg_damage_gdf.sjoin(perth_gdf, how="right")
    suburb_damage_filtered =suburb_damage[ ~suburb_damage["index_left"].isna()]
    suburb_damage_gdf = suburb_damage_filtered[["index_left", "lon","lat","structural~no_damage","structural~slight","structural~moderate","structural~extensive","structural~complete","geometry"]]

    # Damage states dictionary
    damages_state = {}
    damages_state["structural~no_damage"] = "No damage"
    damages_state["structural~slight"] = "Slight damage"
    damages_state["structural~moderate"] = "Moderate damage"
    damages_state["structural~extensive"] = "Extensive damage"
    damages_state["structural~complete"] = "Complete damage"

    return aus_gdf, events_gdf, suburb_pga_gdf, suburb_pga_df, perth_gdf, perth_buildings_gdf, frag_curves_df, suburb_damage_gdf, damages_state, avg_damage_df, avg_damage_piv_df

def main():

    aus_gdf, events_gdf, suburb_pga_gdf, suburb_pga_df, perth_gdf, perth_buildings_gdf, frag_curves_df, suburb_damage_gdf, damages_state, avg_damage_df, avg_damage_piv_df = load_data()

    st.title(app_title)
    
    seismicity_map, introduction = st.columns(2)
    with seismicity_map:
        display_seismicity_map(aus_gdf, events_gdf)
    
    with introduction:
        st.write(intro_text)
    
    st.header(header1)
    st.subheader(subheader1)
    map_pga, table_pga = st.columns(2)
    with map_pga:
        display_map_pga(suburb_pga_gdf,"gmv_PGA")
    
    with table_pga:
        display_dataframe(suburb_pga_df, "suburb")
    
    st.header(header2)
    building_map, fragility_curves = st.columns(2)
    with building_map:
        display_building_map(perth_gdf, perth_buildings_gdf)
    
    with fragility_curves:
        frag_id_selected = display_fragility_filter(frag_curves_df, "frag_func_id")
        display_fragility_curves(frag_curves_df, "frag_func_id",frag_id_selected)
    
    st.header(header3)
    st.subheader(subheader2)
    probability_map, damage_bar_plot = st.columns(2)
    with probability_map:
        display_probability_map(suburb_damage_gdf, damages_state)

    with damage_bar_plot:
        taxonomy_selected = taxonomy_filter(avg_damage_df,"taxonomy")
        display_bar_plot(avg_damage_df,"taxonomy",taxonomy_selected)

    display_dataframe(avg_damage_piv_df, "suburb")


if __name__ == "__main__":
     main()


    






