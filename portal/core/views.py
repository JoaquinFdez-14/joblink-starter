from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import requests

# Firebase admin (verificación de idTokens)
import firebase_admin
from firebase_admin import auth as fb_auth, credentials as fb_creds
from django.contrib.auth import login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pathlib import Path

from django.contrib.admin.views.decorators import staff_member_required
API_BASE = getattr(settings, "API_BASE", "http://localhost:8080")
API_TOKEN = getattr(settings, "API_TOKEN", "secreto123")

# ===================== OPCIONES GLOBALES =====================

CARRERAS_OPCIONES = [
    # TI / Informática
    "Analista Programador",
    "Técnico en Programación",
    "Ingeniería en Informática",
    "Ingeniería en Ciberseguridad",
    "Ingeniería en Redes y Telecomunicaciones",
    "Técnico en Redes y Telecomunicaciones",
    "Ingeniería en Automatización y Control Industrial",
    "Ciencias de la Computación",
    "Desarrollo de Software",
    "Ingeniería de Software",

    # Administración / Negocios
    "Administración de Empresas",
    "Ingeniería en Administración",
    "Contabilidad",
    "Ingeniería Comercial",
    "Logística y Operaciones",
    "Marketing",
    "Recursos Humanos",

    # Diseño / Comunicación
    "Diseño Gráfico",
    "Diseño Digital",
    "Publicidad",
    "Comunicación Audiovisual",
    "Animación Digital",
    "Diseño UX/UI",

    # Salud
    "Enfermería",
    "Kinesiología",
    "Técnico en Enfermería",
    "Nutrición y Dietética",
    "Tecnologías Médicas",

    # Ingeniería y Técnico
    "Ingeniería Civil",
    "Ingeniería Industrial",
    "Ingeniería Eléctrica",
    "Ingeniería Mecánica",
    "Ingeniería en Minas",
    "Construcción Civil",

    # Ciencia y Data
    "Estadística",
    "Ciencia de Datos",
    "Analítica de Datos",

    # Servicios y Otros
    "Gastronomía Internacional",
    "Prevención de Riesgos",
    "Hotelería y Turismo",
    "Comercio Internacional",
    "Otra",
]

SEDES_OPCIONES = [
    # INACAP
    "INACAP Apoquindo",
    "INACAP Maipú",
    "INACAP Puente Alto",
    "INACAP Renca",
    "INACAP Valparaíso",
    "INACAP Concepción",
    "INACAP La Serena",
    "INACAP Temuco",
    "INACAP Antofagasta",

    # Genéricas
    "Santiago Centro",
    "Providencia",
    "Ñuñoa",
    "Puente Alto",
    "Maipú",
    "Concepción",
    "Valparaíso",
    "La Serena",
    "Temuco",

    "Remoto / Teletrabajo",
]

INSTITUCIONES_OPCIONES = [
    "INACAP",
    "DUOC UC",
    "AIEP",
    "IP Chile",
    "Santo Tomás",
    "Universidad de Chile",
    "Universidad de Santiago (USACH)",
    "Universidad Andrés Bello",
    "Universidad Diego Portales",
    "Otra institución",
]


def _api_headers():
    return {"x-auth-token": API_TOKEN, "Content-Type": "application/json"}


def _require_login(request):
    if not request.session.get("uid"):
        messages.info(request, "Inicia sesión para continuar.")
        return False
    return True


# ===================== OFERTAS =====================

def ofertas_list(request):
    """
    Lista todas las ofertas desde la API.
    Admite filtros por carrera, sede y tipo (desde formulario GET).
    Además: si el estudiante completó el onboarding,
    se cargan "ofertas recomendadas" usando sus preferencias.
    """
    # ---------- Filtros manuales desde el formulario ----------
    params = {}
    carrera = request.GET.get("carrera")
    sede = request.GET.get("sede")
    tipo = request.GET.get("tipo")

    if carrera:
        params["carrera"] = carrera
    if sede:
        params["sede"] = sede
    if tipo:
        params["tipo"] = tipo

    # ---------- Ofertas generales ----------
    try:
        r = requests.get(f"{API_BASE}/api/ofertas", params=params, timeout=5)
        ofertas = r.json() if r.ok else []
    except Exception:
        ofertas = []
        messages.error(request, "No se pudo cargar las ofertas (API).")

    # ---------- Ofertas recomendadas según preferencias de sesión ----------
    recomendaciones = []
    tiene_preferencias = bool(request.session.get("onboarding_completo"))

    pref_carrera = request.session.get("carrera", "")
    pref_sede = request.session.get("sede", "")
    pref_tipo = request.session.get("tipo_practica", "")

    if tiene_preferencias:
        rec_params = {}
        if pref_carrera:
            rec_params["carrera"] = pref_carrera
        if pref_sede:
            rec_params["sede"] = pref_sede
        if pref_tipo:
            rec_params["tipo"] = pref_tipo  # campo tipo en la API

        if rec_params:
            try:
                rr = requests.get(
                    f"{API_BASE}/api/ofertas",
                    params=rec_params,
                    timeout=5,
                )
                if rr.ok:
                    recomendaciones = rr.json()
            except Exception:
                recomendaciones = []

    contexto = {
        "ofertas": ofertas,
        "filtro_carrera": carrera or "",
        "filtro_sede": sede or "",
        "filtro_tipo": tipo or "",

        # nuevas listas
        "carreras_opciones": CARRERAS_OPCIONES,
        "sedes_opciones": SEDES_OPCIONES,
        "instituciones_opciones": INSTITUCIONES_OPCIONES,

        # info de recomendaciones
        "recomendadas": recomendaciones,
        "tiene_preferencias": tiene_preferencias,
        "pref_carrera": pref_carrera,
        "pref_sede": pref_sede,
        "pref_tipo": pref_tipo,
    }
    return render(request, "ofertas_list.html", contexto)


def ofertas_detail(request, oferta_id):
    """
    Muestra el detalle de una oferta específica.
    """
    oferta = None
    try:
        r = requests.get(f"{API_BASE}/api/ofertas/{oferta_id}", timeout=5)
        if r.ok:
            oferta = r.json()
        else:
            messages.error(request, "No se encontró la oferta.")
    except Exception:
        messages.error(request, "No se pudo conectar con la API de ofertas.")

    if not oferta:
        return redirect("ofertas_list")

    return render(request, "ofertas_detail.html", {"oferta": oferta})


@require_http_methods(["GET", "POST"])
def ofertas_create(request):
    """
    Crear una nueva oferta (como empresa).
    Usa el UID del usuario logueado como empresaId.
    """
    if not _require_login(request):
        return redirect("login")

    uid = request.session.get("uid")  # empresaId

    if request.method == "POST":
        data = {
            "titulo": request.POST.get("titulo", ""),
            "descripcion": request.POST.get("descripcion", ""),
            "carrera_requerida": request.POST.get("carrera_requerida", ""),
            "sede": request.POST.get("sede", ""),
            "tipo": request.POST.get("tipo", ""),
            "empresaId": uid,
            "estado": request.POST.get("estado", "activa"),
        }
        try:
            r = requests.post(
                f"{API_BASE}/api/ofertas",
                json=data,
                headers=_api_headers(),
                timeout=5,
            )
            if r.ok:
                messages.success(request, "Oferta creada correctamente.")
                return redirect("ofertas_list")
            else:
                try:
                    err = r.json()
                except Exception:
                    err = {"error": "Error al crear oferta"}
                messages.error(request, f"No se pudo crear la oferta: {err}")
        except Exception:
            messages.error(request, "No se pudo conectar con la API de ofertas.")

        return render(request, "ofertas_form.html", {"modo": "nueva", "oferta": data})

    return render(request, "ofertas_form.html", {"modo": "nueva", "oferta": {}})


@require_http_methods(["GET", "POST"])
def ofertas_edit(request, oferta_id):
    """
    Edita una oferta existente.
    """
    if not _require_login(request):
        return redirect("login")

    oferta = {}
    try:
        r = requests.get(f"{API_BASE}/api/ofertas/{oferta_id}", timeout=5)
        if r.ok:
            oferta = r.json()
        else:
            messages.error(request, "No se encontró la oferta.")
    except Exception:
        messages.error(request, "No se pudo conectar con la API de ofertas.")

    if request.method == "POST":
        data = {
            "titulo": request.POST.get("titulo", oferta.get("titulo", "")),
            "descripcion": request.POST.get("descripcion", oferta.get("descripcion", "")),
            "carrera_requerida": request.POST.get(
                "carrera_requerida", oferta.get("carrera_requerida", "")
            ),
            "sede": request.POST.get("sede", oferta.get("sede", "")),
            "tipo": request.POST.get("tipo", oferta.get("tipo", "")),
            "estado": request.POST.get("estado", oferta.get("estado", "activa")),
        }
        try:
            r = requests.put(
                f"{API_BASE}/api/ofertas/{oferta_id}",
                json=data,
                headers=_api_headers(),
                timeout=5,
            )
            if r.ok:
                messages.success(request, "Oferta actualizada correctamente.")
                return redirect("ofertas_list")
            else:
                try:
                    err = r.json()
                except Exception:
                    err = {"error": "Error al actualizar oferta"}
                messages.error(request, f"No se pudo actualizar la oferta: {err}")
        except Exception:
            messages.error(request, "No se pudo conectar con la API de ofertas.")

        oferta.update(data)

    return render(request, "ofertas_form.html", {"modo": "editar", "oferta": oferta})


@require_http_methods(["GET", "POST"])
def ofertas_delete(request, oferta_id):
    """
    Confirmar y eliminar una oferta.
    """
    if not _require_login(request):
        return redirect("login")

    oferta = None
    try:
        r = requests.get(f"{API_BASE}/api/ofertas/{oferta_id}", timeout=5)
        if r.ok:
            oferta = r.json()
    except Exception:
        pass

    if request.method == "POST":
        try:
            r = requests.delete(
                f"{API_BASE}/api/ofertas/{oferta_id}",
                headers=_api_headers(),
                timeout=5,
            )
            if r.ok:
                messages.success(request, "Oferta eliminada.")
            else:
                try:
                    err = r.json()
                except Exception:
                    err = {"error": "Error al eliminar oferta"}
                messages.error(request, f"No se pudo eliminar la oferta: {err}")
        except Exception:
            messages.error(request, "No se pudo conectar con la API de ofertas.")

        return redirect("ofertas_list")

    return render(request, "ofertas_delete.html", {"oferta": oferta})


# ===================== LOGIN / PERFIL =====================

@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Login simple:
    - UID (puede ser estudiante o empresa)
    - Nombre
    - Rol (estudiante/empresa)
    Se guarda sesión + se registra/actualiza en /api/usuarios.
    """
    if request.method == "POST":
        uid = (request.POST.get("uid") or "").strip()
        nombre = (request.POST.get("nombre") or "").strip()
        rol = (request.POST.get("rol") or "estudiante").strip()

        if not uid or not nombre:
            messages.error(request, "Completa UID y Nombre.")
            return render(request, "login.html")

        # Guarda en sesión
        request.session["uid"] = uid
        request.session["nombre"] = nombre
        request.session["rol"] = rol

        # Sincroniza con la API
        try:
            payload = {"uid": uid, "nombre": nombre, "rol": rol}
            requests.post(
                f"{API_BASE}/api/usuarios",
                json=payload,
                headers=_api_headers(),
                timeout=5,
            )
        except Exception:
            messages.warning(
                request,
                "No se pudo sincronizar el usuario con la API (/api/usuarios).",
            )

        # 🔹 NUEVO: si es estudiante y aún no tiene onboarding en esta sesión,
        # lo mandamos a completar sus preferencias.
        if rol == "estudiante" and not request.session.get("onboarding_completo"):
            messages.success(request, f"Bienvenido, {nombre}. Completemos tu perfil ✨")
            return redirect("onboarding")
        if rol == "empresa" and not request.session.get("onboarding_completo"):
            messages.success(request, f"Bienvenido, {nombre}. Completa el perfil de tu empresa ✨")
            return redirect("onboarding-empresa")

        # Para empresas o estudiantes que ya tienen onboarding en sesión
        messages.success(request, f"Bienvenido, {nombre}")
        return redirect("ofertas_list")

    return render(request, "login.html")


@csrf_exempt
def firebase_token_login(request):
    """
    Endpoint que recibe POST {'idToken': '...'}.
    Verifica el token con Firebase Admin, crea/actualiza un User de Django
    y hace login() para establecer la sesión en el portal.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=405)

    try:
        data = request.body.decode("utf-8")
        import json
        payload = json.loads(data or "{}")
    except Exception:
        payload = {}

    id_token = payload.get("idToken")
    if not id_token:
        return JsonResponse({"error": "idToken requerido"}, status=400)

    # inicializar firebase admin si es necesario
    if not firebase_admin._apps:
        # ruta al proyecto padre (donde está la carpeta `api`)
        root = Path(settings.BASE_DIR).parent
        # buscar service account con dos nombres posibles (algunos repos tienen doble .json)
        service_path = root / "api" / "serviceAccountKey.json"
        service_path_alt = root / "api" / "serviceAccountKey.json.json"
        chosen = None
        if service_path.exists():
            chosen = service_path
        elif service_path_alt.exists():
            chosen = service_path_alt

        if chosen:
            cred = fb_creds.Certificate(str(chosen))
            firebase_admin.initialize_app(cred)
        else:
            # intentar inicializar sin certificado (usar GOOGLE_APPLICATION_CREDENTIALS)
            try:
                firebase_admin.initialize_app()
            except Exception:
                return JsonResponse({"error": "Servicio de autenticación no configurado"}, status=500)

    try:
        decoded = fb_auth.verify_id_token(id_token)
    except Exception as e:
        return JsonResponse({"error": "token inválido", "detail": str(e)}, status=401)

    uid = decoded.get("uid")
    email = decoded.get("email")

    email_verified = decoded.get("email_verified", False)
    name = decoded.get("name") or email or uid
    # Ya no se exige verificación de correo

    User = get_user_model()
    user, created = User.objects.get_or_create(username=uid, defaults={"email": email, "first_name": name})
    # Marcar is_staff si el correo está en la lista de administradores en settings
    admin_emails = getattr(settings, 'ADMIN_EMAILS', '') or ''
    admin_list = [e.strip().lower() for e in admin_emails.split(',') if e.strip()]
    if email and email.lower() in admin_list:
        user.is_staff = True
    user.save()

    # Consultar el backend para obtener el rol real
    import requests
    rol = 'estudiante'
    try:
        api_url = f"{API_BASE}/api/usuarios/{uid}"
        r = requests.get(api_url, timeout=5)
        if r.ok:
            perfil = r.json()
            rol = perfil.get('rol', 'estudiante')
    except Exception:
        pass

    login(request, user)
    # Guardar info en la sesión para compatibilidad con el portal
    request.session['uid'] = uid
    request.session['nombre'] = name
    request.session['rol'] = rol
    request.session['email'] = email

    # Redirección a onboarding según rol y estado
    if rol == "estudiante" and not request.session.get("onboarding_completo"):
        messages.success(request, f"Bienvenido, {name}. Completemos tu perfil ✨")
        return JsonResponse({"redirect": "/onboarding/"})
    if rol == "empresa" and not request.session.get("onboarding_completo"):
        messages.success(request, f"Bienvenido, {name}. Completa el perfil de tu empresa ✨")
        return JsonResponse({"redirect": "/onboarding-empresa/"})

    return JsonResponse({"ok": True, "uid": uid, "email": email, "rol": rol})


# ===================== ONBOARDING EMPRESA =====================
def onboarding_empresa(request):
    """
    Formulario para que la empresa complete su perfil inicial.
    Guarda en sesión y sincroniza con la API.
    """
    if "uid" not in request.session:
        return redirect("login")
    if request.session.get("rol") != "empresa":
        return redirect("ofertas_list")
    if request.method == "POST":
        nombre_empresa = request.POST.get("nombre_empresa")
        area = request.POST.get("area")
        ubicacion = request.POST.get("ubicacion")
        tipo_practica = request.POST.get("tipo_practica")
        # Guardar en sesión
        request.session["nombre_empresa"] = nombre_empresa
        request.session["area"] = area
        request.session["ubicacion"] = ubicacion
        request.session["tipo_practica"] = tipo_practica
        request.session["onboarding_completo"] = True
        # Sincronizar con API
        try:
            payload = {
                "uid": request.session.get("uid"),
                "nombre_empresa": nombre_empresa,
                "rol": "empresa",
                "area": area,
                "ubicacion": ubicacion,
                "tipo_practica": tipo_practica,
            }
            requests.post(
                f"{API_BASE}/api/usuarios",
                json=payload,
                headers=_api_headers(),
                timeout=5,
            )
        except Exception:
            messages.warning(request, "No se pudo sincronizar tu perfil de empresa con la API.")
        messages.success(request, "¡Perfil de empresa guardado!")
        return redirect("ofertas_list")
    return render(request, "onboarding_empresa.html")


@staff_member_required
def admin_panel(request):
    """Panel simple para administradores: listar usuarios, ofertas y postulaciones."""
    users = []
    ofertas = []
    postulaciones = []
    try:
        ru = requests.get(f"{API_BASE}/api/usuarios", timeout=5)
        if ru.ok:
            users = ru.json()
    except Exception:
        users = []

    try:
        ro = requests.get(f"{API_BASE}/api/ofertas", timeout=5)
        if ro.ok:
            ofertas = ro.json()
    except Exception:
        ofertas = []

    try:
        rp = requests.get(f"{API_BASE}/api/postulaciones", timeout=5)
        if rp.ok:
            postulaciones = rp.json()
    except Exception:
        postulaciones = []

    contexto = {
        "users": users,
        "ofertas": ofertas,
        "postulaciones": postulaciones,
    }
    return render(request, "admin_panel.html", contexto)


@staff_member_required
@require_http_methods(["POST"])
def admin_delete_oferta(request, oferta_id):
    try:
        r = requests.delete(f"{API_BASE}/api/ofertas/{oferta_id}", headers=_api_headers(), timeout=5)
        if r.ok:
            messages.success(request, "Oferta eliminada.")
        else:
            messages.error(request, "No se pudo eliminar la oferta.")
    except Exception:
        messages.error(request, "Error al contactar la API para eliminar oferta.")
    return redirect("admin_panel")


@staff_member_required
@require_http_methods(["POST"])
def admin_delete_postulacion(request, postulacion_id):
    try:
        r = requests.delete(f"{API_BASE}/api/postulaciones/{postulacion_id}", headers=_api_headers(), timeout=5)
        if r.ok:
            messages.success(request, "Postulación eliminada.")
        else:
            messages.error(request, "No se pudo eliminar la postulación.")
    except Exception:
        messages.error(request, "Error al contactar la API para eliminar postulación.")
    return redirect("admin_panel")


@staff_member_required
@require_http_methods(["POST"])
def admin_upsert_user(request):
    # recibe form con uid, nombre, rol, email
    uid = request.POST.get("uid")
    nombre = request.POST.get("nombre")
    rol = request.POST.get("rol") or "estudiante"
    email = request.POST.get("email")
    if not uid:
        messages.error(request, "UID requerido")
        return redirect("admin_panel")
    payload = {"uid": uid, "nombre": nombre, "rol": rol, "email": email}
    try:
        r = requests.post(f"{API_BASE}/api/usuarios", json=payload, headers=_api_headers(), timeout=5)
        if r.ok:
            messages.success(request, "Usuario creado/actualizado.")
        else:
            messages.error(request, "No se pudo crear/actualizar usuario en la API.")
    except Exception:
        messages.error(request, "Error al contactar la API para usuarios.")
    return redirect("admin_panel")


def logout_view(request):
    request.session.flush()
    messages.info(request, "Sesión cerrada.")
    return redirect("ofertas_list")


def perfil_view(request):
    if not _require_login(request):
        return redirect("login")

    uid = request.session.get("uid")
    nombre = request.session.get("nombre")
    rol = request.session.get("rol")

    # Datos extra desde la API de usuarios
    usuario_api = None
    try:
        r = requests.get(f"{API_BASE}/api/usuarios/{uid}", timeout=5)
        if r.ok:
            usuario_api = r.json()
    except Exception:
        usuario_api = None

    # Resumen de postulaciones del usuario
    postulaciones = []
    try:
        rp = requests.get(
            f"{API_BASE}/api/postulaciones",
            params={"estudianteId": uid},
            timeout=5,
        )
        if rp.ok:
            postulaciones = rp.json()
    except Exception:
        postulaciones = []

    total_postulaciones = len(postulaciones)
    ultima_postulacion = postulaciones[-1] if postulaciones else None
    ultima_oferta = None

    if ultima_postulacion:
        oferta_id = ultima_postulacion.get("ofertaId")
        if oferta_id:
            try:
                ro = requests.get(f"{API_BASE}/api/ofertas/{oferta_id}", timeout=5)
                if ro.ok:
                    ultima_oferta = ro.json()
            except Exception:
                pass

    # Merge usuario_api with session values so template always has consolidated data
    usuario = {}
    def pick(key):
        if usuario_api and key in usuario_api and usuario_api.get(key) not in (None, ""):
            return usuario_api.get(key)
        return request.session.get(key)

    usuario['uid'] = uid
    usuario['nombre'] = pick('nombre') or nombre
    usuario['rol'] = pick('rol') or rol
    usuario['email'] = pick('email')
    usuario['carrera'] = pick('carrera')
    usuario['sede'] = pick('sede')
    usuario['institucion'] = pick('institucion')
    usuario['intereses'] = pick('intereses') or []
    usuario['resumen'] = pick('resumen')

    contexto = {
        "uid": uid,
        "nombre": nombre,
        "rol": rol,
        "usuario_api": usuario_api,
        "usuario": usuario,
        "total_postulaciones": total_postulaciones,
        "ultima_postulacion": ultima_postulacion,
        "ultima_oferta": ultima_oferta,
        "postulaciones": postulaciones,
    }
    return render(request, "perfil.html", contexto)


def home_view(request):
    """
    Página principal tipo "Dashboard compacto".
    Muestra un hero corto, un buscador y dos bloques: ofertas destacadas y mis postulaciones.
    """
    # Ofertas (traemos y cortamos a 6)
    ofertas = []
    try:
        r = requests.get(f"{API_BASE}/api/ofertas", timeout=5)
        if r.ok:
            ofertas = r.json()[:6]
    except Exception:
        ofertas = []

    # Postulaciones recientes del usuario (si está logueado)
    postulaciones = []
    uid = request.session.get("uid")
    if uid:
        try:
            rp = requests.get(
                f"{API_BASE}/api/postulaciones",
                params={"estudianteId": uid},
                timeout=5,
            )
            if rp.ok:
                postulaciones = rp.json()[:3]
                # Para cada postulación intentamos resolver la oferta asociada
                for p in postulaciones:
                    oferta_id = p.get("ofertaId")
                    p["oferta"] = None
                    if oferta_id:
                        try:
                            ro = requests.get(f"{API_BASE}/api/ofertas/{oferta_id}", timeout=5)
                            if ro.ok:
                                p["oferta"] = ro.json()
                        except Exception:
                            p["oferta"] = None
        except Exception:
            postulaciones = []

    # Cálculo de empleabilidad y checklist (solo si hay usuario)
    empleabilidad = 0
    checklist = []
    perfil_completo = False
    if uid:
        try:
            r = requests.get(f"{API_BASE}/api/usuarios/{uid}", timeout=5)
            if r.ok:
                usuario_api = r.json()
                # Ejemplo de reglas simples para empleabilidad
                puntos = 0
                total = 3
                if usuario_api.get("perfil_completo"):
                    puntos += 1
                    perfil_completo = True
                else:
                    checklist.append("Completar perfil")
                if usuario_api.get("intereses"):
                    puntos += 1
                else:
                    checklist.append("Agregar intereses")
                if usuario_api.get("postulaciones_realizadas", 0) > 0:
                    puntos += 1
                else:
                    checklist.append("Postular a tu primera oferta")
                empleabilidad = int((puntos / total) * 100)
        except Exception:
            checklist.append("No se pudo obtener datos de empleabilidad")

    # Ofertas de la empresa (si el usuario es empresa)
    ofertas_empresa = []
    if request.session.get("rol") == "empresa" and uid:
        try:
            r = requests.get(f"{API_BASE}/api/ofertas", params={"empresaId": uid}, timeout=5)
            if r.ok:
                ofertas_empresa = r.json()
        except Exception:
            ofertas_empresa = []

    contexto = {
        "ofertas_destacadas": ofertas,
        "postulaciones_recientes": postulaciones,
        "usuario": {
            "nombre": request.session.get("nombre"),
            "uid": uid,
            "rol": request.session.get("rol"),
        },
        "empleabilidad": empleabilidad,
        "checklist": checklist,
        "perfil_completo": perfil_completo,
        "ofertas_empresa": ofertas_empresa,
    }
    return render(request, "home.html", contexto)


# ===================== POSTULACIONES =====================

def postulaciones_list(request):
    """
    Lista las postulaciones del estudiante logueado,
    incluyendo información de la oferta (carrera, sede, etc.).
    """
    if not _require_login(request):
        return redirect("login")

    uid = request.session.get("uid")

    # 1) Traer postulaciones del estudiante
    postulaciones = []
    try:
        r = requests.get(
            f"{API_BASE}/api/postulaciones",
            params={"estudianteId": uid},
            timeout=5,
        )
        if r.ok:
            postulaciones = r.json()
    except Exception:
        messages.error(request, "No se pudo cargar tus postulaciones (API).")

    # 2) Traer todas las ofertas para armar índice
    ofertas_idx = {}
    try:
        ro = requests.get(f"{API_BASE}/api/ofertas", timeout=5)
        if ro.ok:
            for o in ro.json():
                ofertas_idx[o.get("id")] = o
    except Exception:
        pass

    # 3) Mezclar info: postulación + oferta
    postulaciones_det = []
    for p in postulaciones:
        oferta = ofertas_idx.get(p.get("ofertaId"))
        postulaciones_det.append({
            "postulacion": p,
            "oferta": oferta,
        })

    contexto = {
        "postulaciones_det": postulaciones_det,
    }
    return render(request, "postulaciones_list.html", contexto)


@require_http_methods(["POST"])
def postular(request, oferta_id):
    """
    Envía una postulación a la oferta indicada.
    """
    if not _require_login(request):
        return redirect("login")
    uid = request.session.get("uid")
    nombre = request.session.get("nombre")
    email = request.session.get("email") or f"{uid}@fake.joblink"
    # --- Validar y sincronizar usuario como estudiante en la API ---
    try:
        r = requests.get(f"{API_BASE}/api/usuarios/{uid}", timeout=5)
        usuario_api = r.json() if r.ok else None
        if not usuario_api or usuario_api.get("rol") != "estudiante":
            # Si no existe o no es estudiante, forzar registro/actualización
            payload = {
                "uid": uid,
                "nombre": nombre,
                "rol": "estudiante",
                "email": email,
                "password": "joblink_dummy_password"
            }
            r_post = requests.post(
                f"{API_BASE}/api/usuarios",
                json=payload,
                headers=_api_headers(),
                timeout=5,
            )
            try:
                resp_json = r_post.json()
            except Exception:
                resp_json = {"error": "Respuesta no JSON"}
            if not r_post.ok:
                messages.error(request, f"No se pudo registrar/actualizar usuario en la API: {resp_json}")
                return redirect("postulaciones_list")
            # Revalidar tras crear/actualizar
            r2 = requests.get(f"{API_BASE}/api/usuarios/{uid}", timeout=5)
            usuario_api = r2.json() if r2.ok else None
            if not usuario_api or usuario_api.get("rol") != "estudiante":
                messages.error(request, f"Usuario sigue sin rol estudiante tras crear: {usuario_api}")
                return redirect("postulaciones_list")
    except Exception as e:
        messages.error(request, f"Error al validar usuario en la API: {e}")
        return redirect("postulaciones_list")
    # --- Fin validación ---
    try:
        payload = {"ofertaId": oferta_id, "estudianteId": uid}
        r = requests.post(
            f"{API_BASE}/api/postulaciones",
            json=payload,
            headers=_api_headers(),
            timeout=5,
        )
        if r.ok:
            messages.success(request, "Postulación enviada ✅")
        else:
            try:
                err = r.json()
            except Exception:
                err = {"error": "Error al postular"}
            messages.error(request, f"No se pudo postular: {err}")
    except Exception:
        messages.error(request, "No se pudo conectar con la API de postulaciones.")

    return redirect("postulaciones_list")


# ===================== USUARIOS (pantallas básicas) =====================

def usuarios_list(request):
    """
    Renderiza la tabla de usuarios.
    El JS del template puede llamar directo a /api/usuarios.
    """
    return render(request, "usuarios_list.html")


def usuarios_new(request):
    """
    Renderiza el formulario de nuevo usuario (empresa o estudiante).
    """
    # Si el usuario está logueado, intentamos traer su perfil desde la API
    usuario_api = None
    uid = request.session.get("uid")
    if uid:
        try:
            r = requests.get(f"{API_BASE}/api/usuarios/{uid}", timeout=5)
            if r.ok:
                usuario_api = r.json()
        except Exception:
            usuario_api = None

    nombre = request.session.get("nombre", "")
    rol = request.session.get("rol", "")
    contexto = {
        "usuario_api": usuario_api or {},
        "api_base": API_BASE,
        "api_token": API_TOKEN,
        "carreras_opciones": CARRERAS_OPCIONES,
        "sedes_opciones": SEDES_OPCIONES,
        "instituciones_opciones": INSTITUCIONES_OPCIONES,
        "uid": uid or "",
        "nombre": nombre,
        "rol": rol,
    }
    return render(request, "usuarios_form.html", contexto)


# ===================== ONBOARDING (preferencias de estudiante) =====================

def onboarding(request):
    """
    Formulario para que el estudiante cuente su carrera, sede, institución e intereses.
    Por ahora guardamos solo en la sesión de Django.
    Luego podemos conectar esto con la API de Node / Firestore.
    """
    if "uid" not in request.session:
        return redirect("login")

    if request.session.get("rol") != "estudiante":
        return redirect("ofertas_list")

    if request.method == "POST":
        carrera = request.POST.get("carrera")
        sede = request.POST.get("sede")
        tipo_practica = request.POST.get("tipo_practica")
        institucion = request.POST.get("institucion")
        intereses = request.POST.getlist("intereses")  # lista de checkboxes

        # Guardamos en la sesión
        request.session["carrera"] = carrera
        request.session["sede"] = sede
        request.session["tipo_practica"] = tipo_practica
        request.session["institucion"] = institucion
        request.session["intereses"] = intereses
        request.session["onboarding_completo"] = True

        # También sincronizamos estas preferencias con la API (upsert usuario)
        try:
            payload = {
                "uid": request.session.get("uid"),
                "nombre": request.session.get("nombre"),
                "rol": request.session.get("rol"),
                "carrera": carrera,
                "sede": sede,
                "tipo_practica": tipo_practica,
                "institucion": institucion,
                "intereses": intereses,
            }
            requests.post(
                f"{API_BASE}/api/usuarios",
                json=payload,
                headers=_api_headers(),
                timeout=5,
            )
        except Exception:
            messages.warning(request, "No se pudo sincronizar tus preferencias con la API.")

        messages.success(request, "¡Guardamos tus preferencias!")
        return redirect("ofertas_list")

    # GET → mostramos el formulario con las listas
    contexto = {
        "carreras_opciones": CARRERAS_OPCIONES,
        "sedes_opciones": SEDES_OPCIONES,
        "instituciones_opciones": INSTITUCIONES_OPCIONES,
    }
    return render(request, "onboarding.html", contexto)
