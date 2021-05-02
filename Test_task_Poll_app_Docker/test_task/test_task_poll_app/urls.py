from .views import results, results_main, submit, home, vote
from django.urls import path

urlpatterns = [
    path('<int:user_id>/results/', results, name='results'),
    path('<int:user_id>/results_main', results_main, name='results_main'),
    path('<int:user_id>/vote/submit/<int:poll_id>', submit, name='submit'),
    path('<int:user_id>/', home, name='home'),
    path('<int:user_id>/vote/', vote, name='vote'),
]