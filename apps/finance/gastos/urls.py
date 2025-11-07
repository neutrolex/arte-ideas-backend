from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importa las vistas desde el mismo directorio
from .views import (
    ExpenseCategoryViewSet,
    BudgetViewSet,
    PersonalExpenseViewSet,
    ServiceExpenseViewSet,
    FinancialSummaryView  
)


router = DefaultRouter()


router.register(r'categories', ExpenseCategoryViewSet, basename='expense-category')


router.register(r'budgets', BudgetViewSet, basename='budget')


router.register(r'personal', PersonalExpenseViewSet, basename='personal-expense')

router.register(r'services', ServiceExpenseViewSet, basename='service-expense')



urlpatterns = [

 
    path('', include(router.urls)),
    
    
    path(
        'summary/', 
        FinancialSummaryView.as_view(), 
        name='financial-summary'
    ),
]