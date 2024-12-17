import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pc



def plot_heatmap_perc(s, cohort_size):

  heatmap_data = s.pivot(index=f'FIRST_ORDER_{cohort_size.upper()}', columns=f'ORDER_SEQ', values='n_customers')
  heatmap_data = heatmap_data.fillna(0)  # Set to 0 for better visibility in heatmap

  heatmap_data.index = heatmap_data.index.astype(str)
  heatmap_data.columns = heatmap_data.columns.astype(str)

  # Normalize each row so the first order month is 100%
  heatmap_percentages = heatmap_data.div(heatmap_data.max(axis=1), axis=0) * 100

  # Replace NaN with 0 for cleaner visualization
  heatmap_percentages = heatmap_percentages.fillna(0)
                                                  
  x_labels = [f"+{i}" for i in range(len(heatmap_percentages.columns))]

  # Format text for percentages
  text_values = [[f"{value:.1f}%" if value != 0 else "" for value in row] for row in heatmap_percentages.values]

  # Create the heatmap
  fig = go.Figure(
      data=go.Heatmap(
          z=heatmap_percentages.values,  # Use percentage values
          x=x_labels,  # Order months
          y=heatmap_percentages.index,  # First-order months
          colorscale='Blues',  # Color scale for percentages
          colorbar=dict(title="Retention %"),
          text=text_values,  # Add text labels for percentages
          texttemplate="%{text}",  # Format text as percentages
          showscale=True,  # Display color scale
          zmin=0,  # Minimum value for percentage scale
          zmax=100  # Maximum value for percentage scale
      )
  )

  # Update layout for better visualization
  fig.update_layout(
      title="Cohort Activity Heatmap (Percentages)",
      xaxis_title=f"{cohort_size}s since First Order",
      yaxis_title=f"First Order {cohort_size}",
      xaxis=dict(type='category'),
      yaxis=dict(type='category', autorange="reversed"),
      plot_bgcolor="white"  # Set empty background to white
  )

  # Show the heatmap
  return fig

def plot_heatmap(s, cohort_size):

  heatmap_data = s.pivot(index=f'FIRST_ORDER_{cohort_size.upper()}', columns=f'ORDER_SEQ', values='n_customers')
  heatmap_data = heatmap_data.fillna(0)  # Set to 0 for better visibility in heatmap

  heatmap_data.index = heatmap_data.index.astype(str)
  heatmap_data.columns = heatmap_data.columns.astype(str)

  z_values = heatmap_data.values
  text_values = [[f"{int(value)}" if value != 0 else "" for value in row] for row in z_values]

  # Create the heatmap
  fig = go.Figure(
      data=go.Heatmap(
          z=heatmap_data.values, 
          x=heatmap_data.columns, 
          y=heatmap_data.index,
          colorscale='Blues',  # You can change the colorscale if needed
          text=text_values,  # Pass the data as text labels
          texttemplate="%{text}",
          zmin=1,
          colorbar=dict(title="Customers")
      )
  )

  # Update layout for better visualization
  fig.update_layout(
      title="Cohort Activity Heatmap",
      xaxis_title=f"{cohort_size}s since First Order",
      yaxis_title=f"First Order {cohort_size}",
      xaxis=dict(type='category'),  # Ensure months are treated as categories
      yaxis=dict(type='category',autorange="reversed"),  # Reverse the order of the y-axis
  )

  # Show the heatmap
  return fig

def lines_chart(s, cohort_size):

  heatmap_data = s.pivot(index=f'FIRST_ORDER_{cohort_size.upper()}', columns=f'ORDER_SEQ', values='n_customers')
  heatmap_data = heatmap_data.fillna(0)  # Set to 0 for better visibility in heatmap

  heatmap_data.index = heatmap_data.index.astype(str)
  heatmap_data.columns = heatmap_data.columns.astype(str)

  # Normalize each row so the first order month is 100%
  heatmap_percentages = heatmap_data.div(heatmap_data.max(axis=1), axis=0) * 100

  # Replace NaN with 0 for cleaner visualization
  heatmap_percentages = heatmap_percentages.fillna(0)

  df = pd.DataFrame(heatmap_percentages.reset_index())
  # Melt the DataFrame to long format for easier plotting
  df_melted = df.melt(id_vars=f"FIRST_ORDER_{cohort_size.upper()}", var_name="ORDER_SEQ", value_name="n_customers")
  # Convert ORDER_SEQ to integer for correct sorting
  df_melted['ORDER_SEQ'] = df_melted['ORDER_SEQ'].astype(int)


  unique_months = df_melted[f"FIRST_ORDER_{cohort_size.upper()}"].unique()
  colors = pc.qualitative.Plotly + pc.qualitative.Bold
  color_map = {month: colors[i] for i, month in enumerate(unique_months)}
  x_labels = [f"+{i}" for i in df_melted['ORDER_SEQ'].unique()]

  # Create the line graph
  fig = go.Figure()

  # Add a trace (line) for each FIRST_ORDER_MONTH
  for cohort in df_melted[f"FIRST_ORDER_{cohort_size.upper()}"].unique():
      cohort_data = df_melted[df_melted[f"FIRST_ORDER_{cohort_size.upper()}"] == cohort]
      cohort_data = cohort_data[cohort_data['n_customers'] != 0]

      fig.add_trace(go.Scatter(
          x=x_labels,
          y=cohort_data['n_customers'],
          mode='lines+markers',
          name=cohort,  # Legend label
          line=dict(color=color_map[cohort])
      ))

  # Customize layout
  fig.update_layout(
      title=f"Customer Retention by First Order {cohort_size} (Percentage)",
      xaxis_title=f"{cohort_size}s after First Order",
      yaxis_title="% of Customers",
      plot_bgcolor='white',  # Set empty background to white
      yaxis=dict(
        type='log',  # Set y-axis to logarithmic scale
        showgrid=True,      # Show grid for y-axis
        gridcolor='lightgrey',  # Set grid color
        gridwidth=1),
      xaxis=dict(
        dtick=1,  # Ensure x-axis ticks are integers
        showgrid=True,      # Show grid for x-axis
        gridcolor='lightgrey',  # Set grid color
        gridwidth=1),         # Set grid line width
      legend_title=f"First Order {cohort_size}",
      template="plotly",  # Clean default theme
  )

  return fig