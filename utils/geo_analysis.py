import folium
import geopandas as gpd
import tempfile
import os
import streamlit as st

class TerrainAnalyzer:
    def __init__(self, uploaded_file):
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.geojson') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Read the file using geopandas
        try:
            self.gdf = gpd.read_file(tmp_file_path)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            raise
        finally:
            # Clean up the temporary file
            os.unlink(tmp_file_path)

        self.center = self._calculate_center()
        
    def _calculate_center(self):
        centroid = self.gdf.geometry.centroid
        return [centroid.y.mean(), centroid.x.mean()]
        
    def generate_map(self, vegetation_threshold=0.5):
        m = folium.Map(location=self.center, zoom_start=12)
        
        # Add Stamen Terrain tiles with attribution
        folium.TileLayer(
            tiles='Stamen Terrain',
            attr='Map tiles by <a href="https://stamen.com">Stamen Design</a>, under <a href="https://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="https://openstreetmap.org">OpenStreetMap</a>, under <a href="https://www.openstreetmap.org/copyright">ODbL</a>.',
            name='Stamen Terrain'
        ).add_to(m)
        
        # Add GeoJSON layer
        folium.GeoJson(
            self.gdf,
            style_function=lambda feature: {
                'fillColor': self._color_by_vegetation(feature),
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            }
        ).add_to(m)
        
        return m
    
    def _color_by_vegetation(self, feature):
        # Mock vegetation analysis
        return '#238823' if feature.properties.get('ndvi', 0) > 0.5 else '#ffd700'
    
    def get_statistics(self):
        return {
            'area': round(self.gdf.geometry.area.sum(), 2),
            'elevation': round(self.gdf['elevation'].mean(), 1),
            'vegetation': round(len(self.gdf[self.gdf['ndvi'] > 0.5])/len(self.gdf)*100, 1)
        }