from django.urls import path
from measurement.views import SensorRetrieveUpdateView, SensorListCreateView, MeasurementCreateView

urlpatterns = [
    path('sensors/', SensorListCreateView.as_view()),
    path('sensors/<int:pk>/', SensorRetrieveUpdateView.as_view()),
    path('measurements/', MeasurementCreateView.as_view()),
]
