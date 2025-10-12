# src/visualize.py
"""
Visualization functions for Labor Market Segmentation project
"""

import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
from sklearn.decomposition import PCA

def create_elbow_plot(sse, k_range, save_path=None):
    """
    Create and display elbow plot for K-Means clustering
    
    Args:
        sse (list): List of SSE values for each k
        k_range (range): Range of k values tested
        save_path (str, optional): Path to save the plot
    """
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, sse, 'bo-')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Sum of Squared Errors (SSE)')
    plt.title('Elbow Method for Optimal K')
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    
    plt.show()

def create_pca_plot(X, labels, save_path=None):
    """
    Create 2D PCA visualization of clusters
    
    Args:
        X (array-like): Feature matrix
        labels (array-like): Cluster labels
        save_path (str, optional): Path to save the plot
    """
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], 
                         c=labels, cmap='viridis', alpha=0.6)
    plt.colorbar(scatter, label='Cluster')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.title('Job Clusters - PCA Visualization')
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    
    plt.show()

def create_cluster_map(df, latitude_col='latitude', longitude_col='longitude',
                      cluster_col='cluster_kmeans', title_col='title',
                      salary_col='salary_mid', center=[54.5, -3], zoom=6,
                      colors=None, save_path=None):
    """
    Create interactive Folium map with job clusters
    
    Args:
        df (DataFrame): Data containing job information
        latitude_col (str): Name of latitude column
        longitude_col (str): Name of longitude column
        cluster_col (str): Name of cluster column
        title_col (str): Name of job title column
        salary_col (str): Name of salary column
        center (list): [lat, lon] for map center
        zoom (int): Initial zoom level
        colors (list): List of colors for clusters
        save_path (str, optional): Path to save the map
    """
    if colors is None:
        colors = ["red", "blue", "green", "purple", "orange", "darkred"]
    
    # Create base map
    cluster_map = folium.Map(location=center, zoom_start=zoom)
    
    # Add cluster markers
    marker_cluster = MarkerCluster().add_to(cluster_map)
    
    for idx, row in df.iterrows():
        color = colors[row[cluster_col] % len(colors)]
        
        folium.CircleMarker(
            location=[row[latitude_col], row[longitude_col]],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"{row[title_col]}<br>Salary: £{row[salary_col]:,.0f}<br>Cluster: {row[cluster_col]}",
            tooltip=row[title_col]
        ).add_to(marker_cluster)
    
    if save_path:
        cluster_map.save(save_path)
    
    return cluster_map

def plot_cluster_profiles(cluster_profile, save_path=None):
    """
    Create visualization of cluster profiles
    
    Args:
        cluster_profile (DataFrame): Cluster summary statistics
        save_path (str, optional): Path to save the plot
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot cluster sizes
    ax1.bar(cluster_profile.index, cluster_profile['count'])
    ax1.set_xlabel('Cluster')
    ax1.set_ylabel('Number of Jobs')
    ax1.set_title('Job Distribution Across Clusters')
    
    # Plot average salaries
    ax2.bar(cluster_profile.index, cluster_profile['avg_salary'])
    ax2.set_xlabel('Cluster')
    ax2.set_ylabel('Average Salary (£)')
    ax2.set_title('Average Salary by Cluster')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    
    plt.show()