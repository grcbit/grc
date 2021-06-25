# -*- coding: utf-8 -*-
dev = False
prod = True
demo = False

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################
response.title = request.application.replace('_',' ').title()
response.subtitle = ''
## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Rodolfo Lopez'
response.meta.description = 'GRC'
response.meta.keywords = 'Riesgo, Risk'
response.meta.generator = 'Riesgo, Risk'
## your http://google.com/analytics id
response.google_analytics_id = None

response.menu = [
    (T('Dashboard'), False, URL('default', 'index'), [])
]

def inventario_menu():
    response.menu += [
        (T('Inventory'), False, '#', [
            (T('Objetive Type'), False, URL('default', 'TipoObjetivo')),
            LI(_class="divider"),
            (T('Risk Clasification'), False, URL('default', 'ClasificacionRiesgo')),
            (T('Risk Treatment Type'), False, URL('default', 'TipoTratamientoRiesgo')),
            (T('Risk Factor Group'), False, URL('default', 'GrupoFactorRiesgo')),
            LI(_class="divider"),
            (T('Control Clasification'), False, URL('default', 'ClasificacionControl')),
            (T('Control Type'), False, URL('default', 'TipoControl')),
            (T('Control Group'), False, URL('default', 'GrupoControl')),
            LI(_class="divider"),
            (T('Maturity Level'), False, URL('default', 'NivelMadurez')),
            LI(_class="divider"),
            #(T('Region'), False, URL('default', 'Region')),
            #(T('Department'), False, URL('default', 'Direccion')),
            (T('Policy Catalog'), False, URL('default', 'CatalogoPolitica')),
            (T('Policy Statement'), False, URL('default', 'DetallePolitica')),
        ]),
    ]

def definicionContexto_menu():
    response.menu += [
        (T('Context'), False, '#', [
            (T('Impact Level'), False, URL('default', 'CriterioImpacto')),
            (T('Probability Level'), False, URL('default', 'CriterioProbabilidad')),
            (T('Risk Level'), False, URL('default', 'CriterioRiesgo')),
            LI(_class="divider"),
            (T('Organisation'), False, URL('default', 'Organizacion')),
            (T('Organisational Objective'), False, URL('default', 'ObjetivoOrganizacion')),
            LI(_class="divider"),
            (T('Role & Responsibility'), False, URL('default', 'RolResponsabilidad')),
            #LI(_class="divider"),
            #(T('Policy Catalog'), False, URL('default', 'CatalogoPolitica')),
            #(T('Policy Statement'), False, URL('default', 'DetallePolitica')),
        ]),
    ]

def proceso_menu():
    response.menu += [
        (T('Process'), False, '#', [
            (T('Process'), False, URL('default', 'Proceso')),
            (T('Process Type'), False, URL('default', 'TipoProceso')),
            LI(_class="divider"),
            (T('Process & Region'), False, URL('default', 'ProcesoRegion')),
            (T('Process & Information Asset'), False, URL('default', 'ProcesoActivoInformacion')),
        ]),
    ]

'''
def seguridadTi_menu():
    response.menu += [
        (T('IT'), False, '#', [
            (T('IT Asset'), False, URL('default', 'ActivoTi')),
            (T('System Layer Type'), False, URL('default', 'TipoCapaSistema')),
            LI(_class="divider"),
            (T('IT Asset & Region'), False, URL('default', 'ActivoTiRegion')),
            (T('IT Asset & Process'), False, URL('default', 'ActivoTiProceso')),
            (T('IT Asset & Information Asset'), False, URL('default', 'ActivoTiActivoInformacion')),
            LI(_class="divider"),
            (T('Incident Type'), False, URL('default', 'TipoIncidenteSeguridad')),
            (T('Incident Description'), False, URL('default', 'IncidenteSeguridad')),
            LI(_class="divider"),
            (T('Metric Group CVSS 3.1'), False, URL('cvss', 'GrupoMetrica')),
            (T('Metric Description CVSS 3.1'), False, URL('cvss', 'Metrica')),
            (T('Metric Value CVSS 3.1'), False, URL('cvss', 'ValorMetrica')),
            (T('Evaluation CVSS 3.1'), False, URL('cvss', 'ValorMetricaSeguridadTi')),
            LI(_class="divider"),
            (T('Incident Type'), False, URL('default', 'TipoIncidenteSeguridad')),
            (T('Incident Description'), False, URL('default', 'IncidenteSeguridad')),
        ]),
    ]
'''

def riesgoControl_menu():
    response.menu += [
        (T('Risks & Controls'), False, '#', [
            (T('Risk Identification'), False, URL('default', 'AnalisisRiesgo')),
            LI(_class="divider"),
            (T('Risk Analysis'), False, URL('default', 'TratamientoRiesgo')),
            (T('Risk Analysis Evidence'), False, URL('default', 'FactorEvidencia')),
            (T('Risk Analysis CVSS'), False, URL('default', 'ValorMetricaSeguridadTi')),
            LI(_class="divider"),
            (T('Risk Classification'), False, URL('default', 'AnalisisRiesgoClasificacionRiesgo')),
            (T('Objectives Impact'), False, URL('default', 'AnalisisRiesgoObjetivoOrganizacion')),
            (T('Risk Factor'), False, URL('default', 'TratamientoRiesgoAnalisisRiesgo')),
        ]),
    ]

def activoInformacion_menu():
    response.menu += [
        (T('Information'), False, '#', [
            (T('Data Classification'), False, URL('default', 'ClasificacionInformacion')),
            (T('Data Regulatory'), False, URL('default', 'RegulacionDato')),
            (T('Information Asset'), False, URL('default', 'ActivoInformacion')),
        ]),
    ]

def baseline_menu():
    response.menu += [
        (T('Test & Audit'), False, '#', [
            (T('Control Version'), False, URL('default', 'BenchVersion')),
            (T('Control Objective'), False, URL('default', 'BenchObjetivoControl')),
            (T('Control Activity'), False, URL('default', 'BenchControl')),
            LI(_class="divider"),
            #(T('Gap Analysis'), False, URL('default', 'PruebaSeguridad')),
            (T('Control Test'), False, URL('default', 'EvaluacionControl')),
            (T('Test Evidence'), False, URL('default', 'EvaluacionEvidencia')),
            (T('Test Type'), False, URL('default', 'TipoRevision')),
            #(T('Test'), False, URL('default', 'PruebaWeb')),
            #(T('Web Test'), False, URL('default', 'PruebaWeb')),
            #LI(_class="divider"),
            #(T('Web Info'), False, URL('default', 'PruebaWebInfo')),
            #(T('Web Test'), False, URL('default', 'PruebaWebTest')),
            (T('Control Test CVSS'), False, URL('default', 'ControlCvss')),
            LI(_class="divider"),
            (T('Metric Group CVSS'), False, URL('default', 'GrupoMetrica')),
            (T('Metric Description CVSS'), False, URL('default', 'Metrica')),
            (T('Metric Value CVSS'), False, URL('default', 'ValorMetrica')),
            #(T('Evaluation CVSS 3.1'), False, URL('default', 'ValorMetricaSeguridadTi')),
        ]),
    ]

def activo_menu():
    response.menu += [
        (T('Asset'), False, '#', [
            (T('Data Classification'), False, URL('default', 'ClasificacionInformacion')),
            (T('Data Regulatory'), False, URL('default', 'RegulacionDato')),
            (T('Information Asset'), False, URL('default', 'ActivoInformacion')),
            #(T('Information Asset & Data Regulatory'), False, URL('default', 'ActivoInformacionRegulacion')),
            LI(_class="divider"),
            (T('Process Type'), False, URL('default', 'TipoProceso')),
            (T('Process'), False, URL('default', 'Proceso')),
            #(T('Process & Region'), False, URL('default', 'ProcesoRegion')),
            #(T('Process & Information Asset'), False, URL('default', 'ProcesoActivoInformacion')),
            LI(_class="divider"),
            (T('Container Type'), False, URL('default', 'TipoCapaSistema')),
            (T('Container'), False, URL('default', 'ActivoTi')),
            (T('Container Documentation'), False, URL('default', 'ContenedorDocs')),
            #(T('Container Documentation'), False, URL('default', 'ContenedorDocs')),
            #(T('IT Asset & Region'), False, URL('default', 'ActivoTiRegion')),
            LI(_class="divider"),
            (T('Process & Information Asset'), False, URL('default', 'ProcesoActivoInformacion')),
            (T('Container & Information Asset'), False, URL('default', 'ActivoTiActivoInformacion')),
            (T('Container & Process'), False, URL('default', 'ActivoTiProceso')),
            #(T('Information Asset & Regulation'), False, URL('default', 'ActivoTiProceso')),
            (T('Information Asset & Data Regulatory'), False, URL('default', 'ActivoInformacionRegulacion')),
            #LI(_class="divider"),
            #(T('Incident Type'), False, URL('default', 'TipoIncidenteSeguridad')),
            #(T('Incident Description'), False, URL('default', 'IncidenteSeguridad')),
        ]),
    ]

def tool_menu():
    response.menu += [
        (T('Tools (Beta)'), False, '#', [
            (T('Project'), False, URL('project', 'Proyecto')),
            (T('Planner'), False, URL('project', 'Actividad')),
            LI(_class="divider"),
            (T('Port Scanner'), False, URL('portScanner', 'hostScan')),
            LI(_class="divider"),
            (T('Web APP'), False, URL('proxy', 'webApp')),
            (T('HTTP Proxy'), False, URL('proxy', 'httpProxy')),
            (T('HTTP Analysis'), False, URL('proxy', 'httpAnalysis')),
            LI(_class="divider"),
            (T('App Static Analysis'), False, URL('codeAnalysis', 'aplicacion')),
            (T('Result Static Analysis'), False, URL('codeAnalysis', 'resultado')),
        ]),
    ]

def ayuda_menu():
    response.menu += [
        (T('Admin'), False, '#', [
            (T('Configuration'), False, URL('default', 'Configuracion')),
            (T('Documentation'), False, URL('default', 'Documentacion')),
            LI(_class="divider"),
            (T('User'), False, URL('default', 'Usuario')),
            (T('Membership'), False, URL('default', 'Grupo')),
        ]),
    ]


def licencia_menu():
    response.menu += [
        (T('License'), False, URL('default', 'Licencia'), [])
        ]

def reporte_menu():
    response.menu += [
        (T('Reporting'), False, '#', [
            (T('All'), False, URL('default', 'index')),
            (T('Risk Overview'), False, URL('default', 'ReporteRiesgo')),
            (T('Risk Factor'), False, URL('default', 'ReporteFactorRiesgo')),
            (T('Heat Map'), False, URL('default', 'ReporteMapaCalor')),
            (T('Control Test'), False, URL('default', 'ReporteControlTest')),
        ]),
    ]

def desarrollo_menu():
    response.menu += [
        (T('License'), False, URL('default', 'Licencia'), [])
        ]

if prod == True:
    inventario_menu()
    definicionContexto_menu()
    activo_menu()
    riesgoControl_menu()
    baseline_menu()
    reporte_menu()
    if demo == False:
        ayuda_menu()
    licencia_menu()
if dev == True:
    desarrollo_menu()
