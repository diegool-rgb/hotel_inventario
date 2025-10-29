from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Reporte

@login_required
def lista_reportes(request):
	"""Lista simple de reportes disponibles con enlace al archivo si existe"""
	reportes = Reporte.objects.select_related('tipo_reporte', 'generado_por').order_by('-fecha_generacion')[:100]

	# Preparar urls de archivos: si es ruta relativa, la servimos desde MEDIA_URL
	from django.conf import settings
	def build_file_url(path: str | None) -> str | None:
		if not path:
			return None
		path = str(path)
		if path.startswith('http://') or path.startswith('https://'):
			return path
		if path.startswith('/'):
			# Ruta absoluta en el servidor; la dejamos tal cual
			return path
		# Considerar como ruta relativa a MEDIA_URL
		return f"{settings.MEDIA_URL.rstrip('/')}/{path}"

	reportes_info = []
	for r in reportes:
		reportes_info.append({
			'obj': r,
			'archivo_url': build_file_url(r.archivo_path),
			'tamano_kb': (r.tamaño_archivo / 1024) if r.tamaño_archivo else None,
		})

	return render(request, 'reportes/lista.html', {
		'reportes': reportes_info,
	})
