from django.urls import path
from . import views

urlpatterns = [
    # Home / listados de ofertas
    path("", views.home_view, name="home"),
    path("ofertas/", views.ofertas_list, name="ofertas_list"),

    # Ofertas CRUD + detalle
    path("ofertas/nueva/", views.ofertas_create, name="ofertas_create"),
    path("ofertas/<str:oferta_id>/", views.ofertas_detail, name="ofertas_detail"),
    path("ofertas/<str:oferta_id>/editar/", views.ofertas_edit, name="ofertas_edit"),
    path("ofertas/<str:oferta_id>/eliminar/", views.ofertas_delete, name="ofertas_delete"),

    # Postulaciones
    path("postulaciones/", views.postulaciones_list, name="postulaciones_list"),
    path("postular/<str:oferta_id>/", views.postular, name="postular"),

    # Login / perfil
    path("login/", views.login_view, name="login"),
    path("auth/firebase-login/", views.firebase_token_login, name="firebase_token_login"),
    path("admin_panel/", views.admin_panel, name="admin_panel"),
    path("admin/delete/oferta/<str:oferta_id>/", views.admin_delete_oferta, name="admin_delete_oferta"),
    path("admin/delete/postulacion/<str:postulacion_id>/", views.admin_delete_postulacion, name="admin_delete_postulacion"),
    path("admin/user/upsert/", views.admin_upsert_user, name="admin_upsert_user"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.perfil_view, name="perfil"),

    # Onboarding y usuarios
    path("onboarding/", views.onboarding, name="onboarding"),
    path("usuarios/", views.usuarios_list, name="usuarios_list"),
    path("usuarios/nuevo/", views.usuarios_new, name="usuarios_new"),
]
