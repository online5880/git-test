from django.apps import AppConfig

# 애플리케이션 등록, 설정 관련 로직

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
