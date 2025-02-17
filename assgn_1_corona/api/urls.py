from django.urls import path
from .views import get_time_series_data, correlation_heatmap
from .views import geographic_data
from .views import pie_chart_data
from .views import line_chart_data
from .views import bar_chart_data
from .views import scatter_plot_data



urlpatterns = [
    path("time-series/", get_time_series_data, name="time_series"),
    path("correlation-heatmap/", correlation_heatmap, name="correlation-heatmap"),
    path("line_chart/", line_chart_data, name="line_chart_data"),
    path('geographic/', geographic_data, name='geographic-data'),
    path("pie_chart/", pie_chart_data, name="pie_chart_data"),
    path("line_chart/", line_chart_data, name="line_chart_data"),
    path("bar_chart/", bar_chart_data, name="bar_chart_data"),
    path("scatter_plot/", scatter_plot_data, name="scatter_plot_data"),

    ]

