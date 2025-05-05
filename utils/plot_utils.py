import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def plot_average_aqi_per_year(df):
  # Group by year and calculate mean AQI
  yearly_avg = df.groupby('year')['AQI'].mean().reset_index()

  fig, ax = plt.subplots(figsize=(10, 5))

  sns.pointplot(x='year', y='AQI', data=yearly_avg, color='blue', markers='o', linestyles='-', ax=ax)
  ax.set_title('Average AQI per Year')
  ax.set_ylabel('Average AQI')
  ax.set_xlabel('Year')
  plt.tight_layout()
  return fig


@st.cache_data
def plot_stationwise_aqi(df):
    yearly_avg_by_station = df.groupby(['year', 'station'])['AQI'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.pointplot(data=yearly_avg_by_station, x='year', y='AQI', hue='station', palette='husl', linestyles='-', ax=ax)
    ax.set_title('Average AQI per Year per Station (2013–2017)')
    ax.set_ylabel('Average AQI')
    ax.set_xlabel('Year')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    return fig

@st.cache_data
def plot_monthlywise_aqi_per_year(df):
  monthly_yearly_avg = df.groupby(['year', 'month'])['AQI'].mean().reset_index()

  fig, ax = plt.subplots(figsize=(10, 5))
  sns.pointplot(data=monthly_yearly_avg, x='month', y='AQI', hue='year', palette='viridis', linestyles='-')
  ax.set_title('Average Monthly AQI per Year (2013–2017)')
  ax.set_ylabel('Average AQI')
  ax.set_xlabel('Month')
  ax.tick_params(axis='x', rotation=45)
  plt.tight_layout()

  return fig

# 2
@st.cache_data
def plot_yearly_pollution_trend(df):
    yearly_avg = df.groupby(['year'])[['vehicle_pollution', 'industrial_pollution']].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=yearly_avg, x='year', y='vehicle_pollution', label='Vehicle Pollution', color='blue', marker='o')
    sns.lineplot(data=yearly_avg, x='year', y='industrial_pollution', label='Industrial Pollution', color='orange', marker='o')
    ax.set_title('Yearly Average Pollution Trend')
    ax.set_xlabel('Year')
    ax.set_ylabel('Pollution Level')
    ax.legend()
    plt.tight_layout()

    return fig

@st.cache_data
def plot_monthly_pollution_pattern(df):
    monthly_seasonal = df.groupby('month')[['vehicle_pollution', 'industrial_pollution']].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=monthly_seasonal, x='month', y='vehicle_pollution', label='Vehicle Pollution', color='blue', marker='o')
    sns.lineplot(data=monthly_seasonal, x='month', y='industrial_pollution', label='Industrial Pollution', color='orange', marker='o')
    ax.set_title('Seasonal Pollution Pattern (Monthly Average)')
    ax.set_xlabel('Month')
    ax.set_ylabel('Pollution Level')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.legend()
    plt.tight_layout()

    return fig

@st.cache_data
def plot_yearly_pollution_contribution(df):
    yearly_pollution = df.groupby('year')[['vehicle_pollution', 'industrial_pollution']].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(yearly_pollution['year'], yearly_pollution['vehicle_pollution'], label='Vehicle Pollution', color='skyblue')
    ax.bar(yearly_pollution['year'], yearly_pollution['industrial_pollution'],
           bottom=yearly_pollution['vehicle_pollution'], label='Industrial Pollution', color='orange')

    ax.set_title('Vehicle vs Industrial Pollution Contribution by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Pollution')
    ax.legend()
    plt.tight_layout()

    return fig

@st.cache_data
def plot_pollution_by_station_and_year(df):
    pollution_by_station_year = df.groupby(['station', 'year'])[['vehicle_pollution', 'industrial_pollution']].sum().reset_index()

    df_melted = pollution_by_station_year.melt(
        id_vars=['station', 'year'],
        value_vars=['vehicle_pollution', 'industrial_pollution'],
        var_name='Pollution_Type',
        value_name='Pollution_Level'
    )

    g = sns.catplot(
        data=df_melted,
        x='year', y='Pollution_Level',
        hue='Pollution_Type',
        col='station',
        kind='bar',
        col_wrap=2,
        height=4,
        aspect=1.2,
        palette='Set2'
    )

    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle('Pollution Type Contribution by Station and Year')
    plt.tight_layout()

    return g.fig

# 3
@st.cache_data
def plot_rainfall_vs_aqi(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x='RAIN', y='AQI', alpha=0.6, ax=ax)
    sns.regplot(data=df, x='RAIN', y='AQI', scatter=False, color='red', label='Trend Line', ax=ax)
    ax.set_title('Rainfall vs AQI')
    ax.set_xlabel('Rainfall (mm)')
    ax.set_ylabel('AQI')
    ax.legend()
    plt.tight_layout()

    return fig

@st.cache_data
def plot_rain_vs_pollution(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Rain vs Vehicle Pollution
    sns.scatterplot(data=df, x='RAIN', y='vehicle_pollution', color='blue', ax=axes[0])
    axes[0].set_title('Rain vs Vehicle Pollution')
    axes[0].set_xlabel('Rainfall (mm)')
    axes[0].set_ylabel('Vehicle Pollution')

    # Rain vs Industrial Pollution
    sns.scatterplot(data=df, x='RAIN', y='industrial_pollution', color='orange', ax=axes[1])
    axes[1].set_title('Rain vs Industrial Pollution')
    axes[1].set_xlabel('Rainfall (mm)')
    axes[1].set_ylabel('Industrial Pollution')

    plt.tight_layout()
    return fig

@st.cache_data
def plot_seasonal_temp_dewp(df):
    monthly_seasonal = df.groupby('month')[['TEMP', 'DEWP']].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=monthly_seasonal, x='month', y='TEMP', marker='o', label='Temperature (°C)', color='red', ax=ax)
    sns.lineplot(data=monthly_seasonal, x='month', y='DEWP', marker='o', label='Dewpoint (°C)', color='green', ax=ax)

    ax.set_title('Seasonal Patterns of Temperature and Dewpoint')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Value')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    return fig

# 4
@st.cache_data
def plot_correlation_heatmap(df):
    num_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM', 'AQI', 'vehicle_pollution', 'industrial_pollution']
    corr_matrix = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title('Correlation Heatmap')
    plt.tight_layout()

    return fig

@st.cache_data
def plot_top_feature_importance(top_features_df):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Importance', y='Feature', data=top_features_df, hue='Feature', palette='viridis', ax=ax)
    ax.set_title("Top Feature Importances")
    ax.set_xlabel('Importance Score')
    ax.set_ylabel('Feature')
    plt.tight_layout()

    return fig