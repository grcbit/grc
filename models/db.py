# -*- coding: utf-8 -*-

if not request.env.web2py_runtime_gae:
    try:
        db = DAL('sqlite://grcDemo200220.sqlite', db_codec='UTF-8')
    except:
        db = DAL('sqlite://grcDemo200220.sqlite', db_codec='UTF-8', migrate=False, fake_migrate=False)
else:
    db = DAL('google:datastore')
    session.connect(request, response, db=db)

response.generic_patterns = ['*'] if request.is_local else []

from datetime import date
import os
from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

#-----------------------------------------------------
#create all tables needed by auth if not custom tables
#-----------------------------------------------------
#auth.define_tables(username=False, signature=False)
auth.define_tables(username=True)

#---------------
#configure email
#---------------

#---------------------
#configure auth policy
#---------------------
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
#auth.settings.registration_requires_verification = False
#auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.expiration = 1800
#auth.settings.password_field = 'pass'

#---------------
#Conexion a LDAP
#---------------

#-----------------------------------------
#Desabilitar Register y solicitar password
#-----------------------------------------
auth.settings.actions_disabled.append('register')
auth.settings.actions_disabled.append('request_reset_password')
auth.settings.actions_disabled.append('retrieve_username')
auth.settings.actions_disabled.append('profile')
auth.settings.actions_disabled.append('change_password')
auth.settings.remember_me_form = False

#---------------
#Modelo de Datos
#---------------

db.define_table('Configuracion',
    Field('Lenguaje', 'string', label=T('LANGUAGE')),
    Field('Organizacion', 'string', label=T('ORGANIZATION NAME')),
    )
db.Configuracion.Lenguaje.requires=IS_IN_SET(['Espanol','English'])

db.define_table('Email',
    Field('Server', 'string', label=T('SERVER')),
    Field('Sender', 'string', label=T('SENDER')),
    Field('Login', 'string', label=T('LOGIN')),
    Field('TLS', 'boolean', label=T('TLS')),
    )

#--------------------------------------------------
#Referenciada en AnalisisRiesgoClasificacionRiesgo
#Validacion OK
#--------------------------------------------------
db.define_table('ClasificacionRiesgo',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Nombre)
    )
db.ClasificacionRiesgo.Nombre.requires=IS_NOT_IN_DB(db, db.ClasificacionRiesgo.Nombre)

db.define_table('TipoRiesgo',
    Field('Nombre', 'string', label=T('NAME')),
    Field('descripcion', 'text', label=T('DESCRIPTION')),
    format=lambda r: '%s' % (r.Nombre)
    )
db.TipoRiesgo.Nombre.requires=IS_NOT_IN_DB(db, db.TipoRiesgo.Nombre)

#----------------------------------
#Referenciada en TratamientoRiesgo
#Validacion OK
#----------------------------------
db.define_table('TipoTratamientoRiesgo',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    #Field('Color', 'string', label=T('COLOR')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Nombre)
    )
#db.TipoTratamientoRiesgo.Color.requires= IS_IN_SET(['Rosa (Pink)', 'Purpura (Purple)', 'Amarillo (Yellow)', 'Azul (Blue)', 'Naranja (Orange)', 'Gris (Gray)', 'Rojo Indio (Indian Red)', 'Salmon (Salmon)', 'Salmon Oscuro (Dark Salmon)'])
db.TipoTratamientoRiesgo.Nombre.requires=IS_NOT_IN_DB(db, db.TipoTratamientoRiesgo.Nombre)

'''
db.define_table('Region',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Responsable', 'string', label=T('RESPONSIBLE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Nombre)
    )
db.Region.Nombre.requires=IS_NOT_IN_DB(db, db.Region.Nombre)
'''

db.define_table('Direccion',
    Field('Nombre', 'string', label=T('NAME')),
    #Field('RegionId', 'reference Region', label=T('REGION'), notnull=True),
    Field('Responsable', 'string', label=T('RESPONSIBLE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s' % (r.Nombre, '|', r.RegionId.Nombre)
    )

db.define_table('TipoProceso',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Nombre)
    )
db.TipoProceso.Nombre.requires=IS_NOT_IN_DB(db, db.TipoProceso.Nombre)

db.define_table('NivelMadurez',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Valor', 'integer', label=T('VALUE')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s' % (r.Valor, ' | ', r.Nombre)
    ) 
db.NivelMadurez.Nombre.requires=IS_NOT_IN_DB(db, db.NivelMadurez.Nombre)
db.NivelMadurez.Valor.requires=IS_NOT_IN_DB(db, db.NivelMadurez.Valor)

db.define_table('Proceso',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('Objetivo', 'text', label=T('OBJECTIVE')),
    Field('Diagrama', 'upload', label=T('FILE')),
    Field('Dueno', 'string', label=T('OWNER')),
    Field('TipoProcesoId', 'reference TipoProceso', label=T('TYPE'), notnull=True),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s' % (r.id, '|', r.TipoProcesoId.Nombre, '|', r.Nombre)
    )

db.define_table('TipoSistema',
    Field('Nombre', 'string', label=T('IT ASSET TYPE')),
    Field('Descripcion', 'text', label=T('IT ASSET DESCRIPTION')),
    format=lambda r: '%s' % (r.Nombre)
    )
db.TipoSistema.Nombre.requires=IS_NOT_IN_DB(db, db.TipoSistema.Nombre)

#------------------------------------
#Referenciada en ObjetivoOrganizacion
#Validacion OK
#------------------------------------
db.define_table('TipoObjetivo',
    Field('Nombre', 'string', label=T('OBJECTIVE')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Nombre)
    )
db.TipoObjetivo.Nombre.requires=IS_NOT_IN_DB(db(db.TipoObjetivo.Nombre==request.vars.Nombre), db.TipoObjetivo.Nombre)

db.define_table('Organizacion',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('Mision', 'text', label=T('MISION')),
    Field('Vision', 'text', label=T('VISION')),
    Field('Valores', 'text', label=T('VALUES')),
    Field('Requerimiento', 'text', label=T('SECURITY REQUIREMENTS'), comment=T('Compliance, law, regulation, contractual')),
    Field('Framework', 'text', label=T('FRAMEWORKS USED'), comment=T('COSO, ISO31, CMMI, COBIT, ISO27, NIST, etc.')),
    Field('Producto', 'text', label=T('PRODUCTS/SERVICES')),
    Field('Archivo', 'upload', label=T('FILE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    )

db.define_table('CriterioImpacto',
    Field('Nombre', 'string', label=T('NAME'), comment=T('1. Insignificante (Insignificant), 2. Menor (Minor), 3. Moderado (Moderate), 4. Mayor (Major), 5.Catastrofico (Catastrophic)') ),
    Field('Valor', 'integer', label=T('VALUE')),
    Field('Descripcion', 'text', label=T(' DESCRIPTION')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s' % (r.Valor, ' | ', r.Nombre)
    )
db.CriterioImpacto.Nombre.requires=IS_NOT_IN_DB(db, db.CriterioImpacto.Nombre)
db.CriterioImpacto.Valor.requires=IS_NOT_IN_DB(db, db.CriterioImpacto.Valor)

db.define_table('CriterioProbabilidad',
    Field('Nombre','string', label=T('NAME'), comment=T('1. Remoto (Rare), 2. Poco Probable (Unlikely), 3. Factible (Possible), 4. Muy Probable (Likely), 5.Casi Cierto (Almost Certain)') ),
    Field('Valor', 'integer', label=T('VALUE')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s' % (r.Valor, ' | ', r.Nombre)
    )
db.CriterioProbabilidad.Nombre.requires=IS_NOT_IN_DB(db, db.CriterioProbabilidad.Nombre)
db.CriterioProbabilidad.Valor.requires=IS_NOT_IN_DB(db, db.CriterioProbabilidad.Valor)

db.define_table('CriterioRiesgo',
    Field('CriterioImpactoId', 'reference CriterioImpacto', label=T('IMPACT'), notnull=True),
    Field('CriterioProbabilidadId', 'reference CriterioProbabilidad', label=T('PROBABILITY'), notnull=True),
    Field('Nombre', 'string', label=T('RISK LEVEL'), comment=T('1. Bajo (Low), 3. Moderado (Moderate), 4. Alto (High), 5. Critico (Critical)')),
    Field('RiesgoValor', 'integer', label=T('VALUE')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s %s %s %s' % ('Pr:', r.CriterioProbabilidadId.Nombre, ' | ', 'Im:', r.CriterioImpacto.Nombre, ' | ', 'Ri:', r.Riesgo)
    )
db.CriterioRiesgo.Nombre.requires=IS_NOT_IN_DB(db((db.CriterioRiesgo.CriterioProbabilidadId==request.vars.CriterioProbabilidadId) & (db.CriterioRiesgo.CriterioImpactoId==request.vars.CriterioImpactoId)), db.CriterioRiesgo.Nombre)

db.define_table('ObjetivoOrganizacion',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('TipoObjetivoId', 'reference TipoObjetivo', label=T('TYPE'), notnull=True),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s' % (r.id, '|', r.Nombre, '|', r.TipoObjetivoId.Nombre)
    )
db.ObjetivoOrganizacion.Nombre.requires=IS_NOT_IN_DB(db, db.ObjetivoOrganizacion.Nombre)

db.define_table('BenchVersion',
    Field('Version', 'string', label=T('VERSION')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('Archivo', 'upload', label=T('FILE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Version)
    )
db.BenchVersion.Version.requires = IS_NOT_IN_DB(db, db.BenchVersion.Version)

db.define_table('CatalogoControl',
    Field('Nombre', 'text', label=T('CONTROL')),
    Field('Descripcion', 'text', label=T('CONTROL OBJECTIVE')),
    Field('Baseline', 'reference BenchVersion', label=T('BASELINE')),
    Field('GuiaImplementacion', 'text', label=T('DESCRIPTION')),
    Field('GuiaAuditoria', 'text', label=T('AUDIT/IMPLEMENTATION GUIDE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s ' % (r.id, '|', r.Nombre)
    )
db.CatalogoControl.Nombre.requires=IS_NOT_IN_DB(db, db.CatalogoControl.Nombre)

db.define_table('ClasificacionInformacion',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Nombre)
    )
db.ClasificacionInformacion.Nombre.requires = IS_NOT_IN_DB(db, db.ClasificacionInformacion.Nombre)

db.define_table('AnalisisRiesgo',
    Field('Riesgo', 'text', label=T('RISK')),
    Field('FechaRevision', 'date', default=request.now, label=T('REVIEW DATE'), requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('EvidenciaRiesgo', 'upload', label=T('RISK DOCUMENTATION'), uploadfolder=os.path.join(request.folder,'uploads')),
    Field('RiesgoMaterializado','text', label=T('RISK CONSEQUENCE')),
    #Field('CriterioImpactoId', 'reference CriterioImpacto', label=T('IMPACT'), notnull=True),
    Field('NivelRiesgo', 'string', label=T('RISK LEVEL'), notnull=True),
    Field('ImpactoJustificacion', 'text', label=T('RISK JUSTIFICATION')),
    Field('DuenoRiesgo', 'string', label=T('RISK OWNER')),
    Field('AnalistaRiesgo', 'string', label=T('RISK ANALYST')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('LogDuenoRiesgo', 'string', label=T('RISK OWNER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    Field('AprobacionDuenoRiesgo', 'boolean', label=T('RISK OWNER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s ' % (r.id, '|', r.Riesgo )
    )
db.AnalisisRiesgo.NivelRiesgo.requires=IS_IN_SET(['Bajo (Low)', 'Moderado (Moderate)', 'Alto (High)', 'Critico (Critical)'])

#--------------
#Validacion OK
#--------------
db.define_table('AnalisisRiesgoClasificacionRiesgo',
    Field('AnalisisRiesgoId', 'reference AnalisisRiesgo', label=T('RISK'), notnull=True),
    Field('ClasificacionRiesgoId', 'reference ClasificacionRiesgo', label=T('RISK CLASSIFICATION'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s' % (r.id, '|', r.AnalisisRiesgoId.Riesgo, '|', r.ClasificacionRiesgoId.Nombre)
    )

db.define_table('AnalisisRiesgoObjetivoOrganizacion',
    Field('AnalisisRiesgoId', 'reference AnalisisRiesgo', label=T('RISK'), notnull=True),
    Field('ObjetivoOrganizacionId', 'reference ObjetivoOrganizacion', label=T('ORGANISATIONAL OBJECTIVE'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s' % (r.id, '|', r.AnalisisRiesgoId.Riesgo, '|', r.ObjetivoOrganizacionId.Nombre)
    )

db.define_table('GrupoControl',
    Field('Nombre', 'string', label=T('CONTROL')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s' % (r.id, '|', r.Nombre)
    )
db.GrupoControl.Nombre.requires=IS_NOT_IN_DB(db, db.GrupoControl.Nombre)

db.define_table('ObjetivoControl',
    Field('ObjetivoControl', 'string', label=T('CONTROL OBJECTIVE')),
    Field('DescripcionControl', 'string', label=T('CONTROL DESCRIPTION')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s' % (r.id, '|', r.ObjetivoControl, ' | ', r.DescripcionControl)
    )

db.define_table('TipoControl',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Nombre)
    )
db.TipoControl.Nombre.requires=IS_NOT_IN_DB(db, db.TipoControl.Nombre)

#---------------------------------
#Referenciada en TratamientoRiesgo
#Validacion OK
#---------------------------------
db.define_table('ClasificacionControl',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    #Field('Color', 'string', label=T('COLOR')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Nombre)
    )
db.ClasificacionControl.Nombre.requires=IS_NOT_IN_DB(db, db.ClasificacionControl.Nombre)
#db.ClasificacionControl.Color.requires= IS_IN_SET(['Rosa (Pink)', 'Purpura (Purple)', 'Amarillo (Yellow)', 'Azul (Blue)', 'Naranja (Orange)', 'Gris (Gray)', 'Rojo Indio (Indian Red)', 'Salmon (Salmon)', 'Salmon Oscuro (Dark Salmon)'])
#RosaPink   #FF0099, Purpura    #990099, Amarillo   #FFCC00, Azul       #0000FF, Naranja    #FF9900, 
#Gris       #666666, INDIANRED  #CD5C5C, SALMON     #FA8072, DARKSALMON #E9967A

db.define_table('GrupoMetrica',
    Field('Nombre','string', label=T('NAME')),
    Field('Descripcion','text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % ( r.Nombre)
    )
db.GrupoMetrica.Nombre.requires=IS_NOT_IN_DB(db(db.GrupoMetrica.Nombre==request.vars.Nombre), db.GrupoMetrica.Nombre)

db.define_table('Metrica',
    Field('GrupoMetricaId', 'reference GrupoMetrica', label=T('METRIC GROUP'), notnull=True),
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('Codigo', 'string', label=T('CODE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s %s %s' % ( r.id, ' | ', r.GrupoMetricaId.Nombre, ' | ', r.Codigo, ' | ', r.Nombre)
    )
db.Metrica.Nombre.requires=IS_NOT_IN_DB(db(db.Metrica.Nombre==request.vars.Nombre), db.Metrica.Nombre)
db.Metrica.Codigo.requires=IS_NOT_IN_DB(db(db.Metrica.Codigo==request.vars.Codigo), db.Metrica.Codigo)

db.define_table('ValorMetrica',
    Field('MetricaId', 'reference Metrica', label=T('METRIC GROUP'), notnull=True),
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('ValorMetrica', 'string', label=T('METRIC VALUE')),
    Field('ValorNumerico', 'double', label=T('NUMERICAL VALUE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s %s %s %s %s %s %s %s %s' % ( r.MetricaId.id, ' | ', r.MetricaId.GrupoMetricaId.Nombre, ' | ', r.MetricaId.Nombre , ' | ', r.Nombre, ' | ', r.MetricaId.Codigo, ':', r.ValorMetrica, '|', r.ValorNumerico)
    )

db.define_table('TipoCapaSistema',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s ' % (r.Nombre)
    )
db.TipoCapaSistema.Nombre.requires=IS_NOT_IN_DB(db, db.TipoCapaSistema.Nombre)

db.define_table('ActivoTi',
    Field('Nombre', 'string', label=T('CONTAINER NAME')),
    Field('TipoCapaSistemaId','reference TipoCapaSistema', label=T('CONTAINER TYPE'), notnull=True),
    #Field('IpInterna', 'string', label=T('INTERNAL IP')),
    #Field('IpPublica', 'string', label=T('PUBLIC IP')),
    #Field('Descripcion', 'text', label=T('HOST DESCRIPTION')),
    Field('AdministradorInterno', 'string', label=T('CONTAINER CUSTODIAN')),
    Field('Fecha', 'date', label=T('DATE'), default=request.now, requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('AdministradorTercero', 'boolean', label=T('EXTERNAL CONTAINER'), default='F'),
    Field('Documentacion', 'upload', label=T('DOCUMENTATION') ),
    #Field('CvssConfidentiality', 'reference ValorMetrica', label=T('CVSS CONFIDENTIALITY IMPACT'), notnull=True),
    #Field('CvssIntegrity', 'reference ValorMetrica', label=T('CVSS INTEGRITY IMPACT'), notnull=True),
    #Field('CvssAvailability', 'reference ValorMetrica', label=T('CVSS AVAILABILITY IMPACT'), notnull=True),
    #Field('CvssJustificacion', 'text', label=T('CVSS JUSTIFICATION'), comment=T('Risk / Cause / Impact')),
    Field('Descripcion', 'text', label=T('DESCRIPTION'), comment=T('Security requirements, description')),

    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s' % (r.id, '|', r.Nombre, '|', r.TipoCapaSistemaId.Nombre)
    )
db.ActivoTi.Nombre.requires=IS_NOT_IN_DB(db(db.ActivoTi.TipoCapaSistemaId==request.vars.TipoCapaSistemaId), db.ActivoTi.Nombre)
#db.ActivoTi.CvssConfidentiality.requires = IS_IN_DB(db(db.ValorMetrica.MetricaId==6), db.ValorMetrica.id, '%(Nombre)s')
#db.ActivoTi.CvssIntegrity.requires = IS_IN_DB(db(db.ValorMetrica.MetricaId==7), db.ValorMetrica.id, '%(Nombre)s')
#db.ActivoTi.CvssAvailability.requires = IS_IN_DB(db(db.ValorMetrica.MetricaId==8), db.ValorMetrica.id, '%(Nombre)s')

db.define_table('ContenedorDocs',
    Field('ActivoTiId','reference ActivoTi', label=T('CONTAINER'), notnull=True),
    Field('Documentacion', 'upload', label=T('DOCUMENTATION') ),
    Field('Fecha', 'date', label=T('DATE'), requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    )

'''
db.define_table('ActivoTiRegion',
    Field('ActivoTiId','reference ActivoTi', label=T('IT ASSET'), notnull=True),
    Field('RegionId','reference Region', label=T('REGION'), notnull=True),
    Field('Descripcion', 'text', label=T('HOST DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s %s %s' % (r.id, '|', r.ActivoTiId.Nombre, '|', r.RegionId.Nombre, '|', r.ActivoTiId.TipoCapaSistemaId.Nombre)
    )
'''

#---------------------------------
#Referenciada en TratamientoRiesgo
#Validacion OK
#---------------------------------
db.define_table('TipoVulnerabilidad',
    Field('Nombre','string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s' % (r.id, '|', r.Nombre)
    )
db.TipoVulnerabilidad.Nombre.requires=IS_NOT_IN_DB(db(db.TipoVulnerabilidad.Nombre==request.vars.Nombre), db.TipoVulnerabilidad.Nombre)

db.define_table('RegulacionDato',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Version', 'string', label=T('VERSION')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('Archivo', 'upload', label=T('FILE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s' % (r.Nombre, r.Version)
    )

db.define_table('TipoDato',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Nombre)
    )
db.TipoDato.Nombre.requires = IS_NOT_IN_DB(db, db.TipoDato.Nombre)

db.define_table('ActivoInformacion',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION'), comment=T('Information/process Description. Importance of information asset to the execution of the state organization’s mission. Mission/Essential business function supported')),
    Field('RequerimientoSeguridad', 'text', label=T('SECURITY REQUIREMENT')),
    Field('DuenoInformacion', 'string', label=T('OWNER NAME'), comment=T('Proporciona el asesoramiento necesario al responsable del tratamiento.')),
    #Field('DuenoPuesto', 'string', label=T('OWNER ROLE')),
    Field('ClasificacionInformacionId', 'reference ClasificacionInformacion', label=T('CLASSIFICATION'), notnull=True),
    #Field('RegulacionDatoId', 'reference RegulacionDato', label=T('REGULATORY'), notnull=True),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('LogDuenoInformacion', 'string', label=T('INFORMATION OWNER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    Field('AprobacionDuenoInformacion', 'boolean', label=T('INFORMATION OWNER (APPROVAL)'), default='F'),
    format = lambda r: '%s %s %s' % (r.id, '|', r.Nombre)
    )

db.define_table('ActivoInformacionRegulacion',
    Field('ActivoInformacionId', 'reference ActivoInformacion', label=T('INFORMATION ASSET')),
    Field('RegulacionDatoId', 'reference RegulacionDato', label=T('DATA REGULATORY')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    )

db.define_table('RolResponsabilidad',
    Field('Rol', 'string', label=T('ROL')),
    Field('Descripcion', 'text', label=T('RESPONSIBILITY')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s %s %s' % (r.id, '|', r.Rol, '|', r.Puesto, '|', r.Responsabilidades)
    )

db.define_table('ProcesoActivoInformacion',
    Field('ProcesoId', 'reference Proceso', label=T('PROCESS'), notnull=True),
    Field('ActivoInformacionId', 'reference ActivoInformacion', label=T('INFORMATION ASSET'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    )

db.define_table('ActivoTiActivoInformacion',
    Field('ActivoTiId', 'reference ActivoTi', label=T('CONTAINER'), notnull=True),
    Field('ActivoInformacionId', 'reference ActivoInformacion', label=T('INFORMATION ASSET'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    )

db.define_table('CatalogoPolitica',
    Field('Nombre','string', label=T('NAME')),#label=T('Policy/Standard/Framework Name')),
    Field('Descripcion','text', label=T('DESCRIPTION')),
    Field('Version','string', label=T('VERSION')),
    Field('FechaCreacion','date', label=T('ISSUE DATE'), default=request.now, requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('Archivo', 'upload', label=T('FILE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s' % (r.id, '|', r.Nombre)
    )
db.CatalogoPolitica.Nombre.requires=IS_NOT_IN_DB(db, db.CatalogoPolitica.Nombre)

'''
db.define_table('ProcesoRegion',
    Field('ProcesoId', 'reference Proceso', label=T('PROCESS'), notnull=True),
    Field('RegionId', 'reference Region', label=T('REGION'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s %s %s %s %s %s %s' % (r.RegionId.Nombre, '|', r.ProcesoId.CicloNegocioId.Nombre, '|', r.ProcesoId.MacroProcesoId.Nombre, '|', r.ProcesoId.TipoProcesoId.Nombre, '|', r.id, '|', r.ProcesoId.Nombre)
    )
'''

db.define_table('DetallePolitica',
    Field('CatalogoPoliticaId', 'reference CatalogoPolitica', label=T('POLICY CATALOG'), notnull=True),
    Field('Codigo', 'string', label=T('#')),
    Field('Nombre', 'text', label=T('POLICY')),
    Field('Comentarios', 'text', label=T('COMMENT')),
    Field('Archivo', 'upload', label=T('FILE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s %s %s' % (r.id, '|', r.CatalogoPoliticaId.Nombre, '|', r.Codigo, '|', r.Nombre)
    )
db.DetallePolitica.Nombre.requires=IS_NOT_IN_DB(db(db.DetallePolitica.CatalogoPoliticaId==request.vars.CatalogoPoliticaId), db.DetallePolitica.Nombre)

db.define_table('TratamientoRiesgo',
    Field('FechaRevision', 'date', default=request.now, label=T('REVIEW DATE'), requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('ProcesoId', 'reference Proceso', label=T('PROCESS'), notnull=True),
    Field('ActivoTiId', 'reference ActivoTi', label=T('IT ASSET'), notnull=True),
    #-------------------------------------------------------------------------------
    #En base a NIST 800-60 la informacion que se procesa/almacena/transmite 
    #en el sistema de informacion se identifica en la fase de categorizacion
    #-------------------------------------------------------------------------------
    Field('FactorRiesgo', 'text', label=T('RISK FACTOR'), comment=T('Risk / Cause / Impact')),
    Field('TipoVulnerabilidadId', 'reference TipoVulnerabilidad', label=T('RISK FACTOR TYPE'), notnull=True),
    Field('RiesgoFraude', 'boolean', label=T('FRAUD RISK'), default='F'),
    Field('EscenarioAmenaza', 'text', label=T('RISK SCENARIO'), comment='Threat-Source, Motivation, Actor, Threat Actions'),
    Field('CriterioImpactoId', 'reference CriterioImpacto', label=T('IMPACT'), notnull=True),
    Field('CriterioProbabilidadId', 'reference CriterioProbabilidad', label=T('PROBABILITY'), notnull=True),
    #----------------------------------------------------------
    Field('CuantificacionCVSS', 'float', label=T('CVSS SCORE'), comment=T('None (0.0) | Low (0.1 - 3.9) | Medium (4.0 - 6.9) | High (7.0 - 8.9) | Critical (9.0 - 10.0)')),
    Field('VectorCVSS', 'string', label=T('CVSS VECTOR STRING')),
    Field('CuantificacionCVSSE', 'float', label=T('CVSS SCORE (RESIDUAL)'), comment=T('None (0.0) | Low (0.1 - 3.9) | Medium (4.0 - 6.9) | High (7.0 - 8.9) | Critical (9.0 - 10.0)')),
    Field('VectorCVSSE', 'string', label=T('CVSS VECTOR STRING (RESIDUAL)')),   
    Field('CalculoImpacto', 'string', label=T('IMPACT CALCULATION') ),
    Field('CalculoProbabilidad', 'string', label=T('PROBABILITY CALCULATION') ),
    Field('TipoTratamientoRiesgoId', 'reference TipoTratamientoRiesgo', label=T('RISK FACTOR TREATMENT'), notnull=True),
    Field('EvidenciaRiesgo', 'upload', label=T('RISK EVIDENCE'), uploadfolder=os.path.join(request.folder,'uploads')),
    Field('RiesgoMaterializadoCheck', 'boolean', label=T('MATERIALIZED RISK')),
    Field('CatalogoControlId', 'reference CatalogoControl', label=T('CONTROL'), notnull=True),
    Field('ObjetivoControl', 'text', label=T('CONTROL OBJECTIVE')),
    Field('Referencia', 'text', label=T('REFERENCE')),
    Field('ActividadControl', 'text', label=T('CONTROL ACTIVITY'), comment=T('What?, How?, For what?, When?')),
    Field('TipoControlId', 'reference TipoControl', label=T('CONTROL TYPE'), notnull=True),
    Field('ClasificacionControlId', 'reference ClasificacionControl', label=T('CONTROL CLASIFICATION'), notnull=True),
    Field('KeyControl','boolean', label=T('KEY CONTROL'), default=False),
    Field('ResponsableControl', 'string', label=T('CONTROL RESPONSIBLE')),
    Field('StatusImplementacionControl', 'string', label=T('CONTROL IMPLEMENTATION STATUS')),
    Field('EvidenciaControl', 'upload', label=T('CONTROL EVIDENCE')),
    Field('FechaImplementacionControl', 'date', label=T('CONTROL IMPLEMENTATION ESTIMATED DATE'), default=request.now, requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('ComentariosResponsableControl', 'text', label=T('COMMENTS')),
    Field('AnalistaRiesgo', 'string', label=T('RISK ANALYST')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('LogResponsableControl', 'string', label=T('CONTROL RESPONSIBLE (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    Field('AprobacionResponsableControl', 'boolean', label=T('CONTROL RESPONSIBLE (APPROVAL)'), default='F'),
    #format=lambda r: '%s %s %s %s %s' % ( r.id , '|' , str(r.FactorRiesgo), '|', str(r.ActividadControl) )
    format=lambda r: '%s %s %s %s %s %s %s' % ( r.id , '|', r.ProcesoId.Nombre, '|', r.ActivoTiId.Nombre, '|', str(r.FactorRiesgo) )
    )
db.TratamientoRiesgo.StatusImplementacionControl.requires= IS_IN_SET(['Implementado (Implemented)', 'No Implementado (Not Implemented)', 'En Progreso (In Progress)', 'N/A'])
#db.TratamientoRiesgo.ProcesoId.represent = lambda s,r: s.Nombre

db.define_table('TratamientoRiesgoAnalisisRiesgo',
    Field('AnalisisRiesgoId', 'reference AnalisisRiesgo', label=T('RISK'), notnull=True),
    Field('TratamientoRiesgoId', 'reference TratamientoRiesgo', label=T('RISK FACTOR'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    )
'''
db.define_table('RegulacionPolitica',
    Field('DetallePoliticaId', 'reference DetallePolitica', label=T('POLICY'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    )
db.RegulacionPolitica.DetallePoliticaId.requires = IS_IN_DB(db( db.DetallePolitica.AprobacionJefeRiesgo=='T' ), db.DetallePolitica.id, '%(Nombre)s')
'''

db.define_table('ActivoTiProceso',
    Field('ActivoTiId', 'reference ActivoTi', label=T('CONTAINER'), notnull=True),
    Field('ProcesoId', 'reference Proceso', label=T('PROCESS'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s %s %s' % (r.id, '|', r.ActivoTiId.Nombre, '|', r.ActivoTiId.TipoCapaSistemaId.Nombre, '|', r.ProcesoId.Nombre)
    )

db.define_table('GrupoMetricaCvss',
    Field('Nombre', 'string', label=T('METRIC GROUP NAME')),
    Field('Descripcion', 'text', label=T('METRIC GROUP DESCRIPTION')),
    format = lambda r: '%s' % (r.Nombre)
    )

db.define_table('ElementoMetricaCvss',
    Field('GrupoMetricaId', 'reference GrupoMetricaCvss', label=T('METRIC GROUP'), notnull=True),
    Field('Nombre', 'string', label=T('METRIC NAME')),
    Field('Descripcion', 'text', label=T('METRIC DESCRIPTION')),
    format = lambda r: '%s %s %s' % (r.GrupoMetricaId.Nombre, ' | ', r.Nombre)
    )

db.define_table('ValorMetricaCvss',
    Field('ElementoMetricaId', 'reference ElementoMetricaCvss', label=T('METRIC GROUP NAME'), notnull=True),
    Field('Nombre', 'string', label=T('Metric Group Name')),
    Field('Valor', 'integer', label=T('METRIC VALUE')),
    Field('Descripcion', 'text', label=T('METRIC VALUE DESCRPTION')),
    format = lambda r: '%s' % (r.Nombre)
    )

db.define_table('AlcanceRevision',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('Fecha', 'date', label=T('DATE'), requires = IS_DATE(format=('%d/%m/%Y'))) ,
    #Field('Fecha', 'date', label=T('DATE'), format=('%d-%m-%Y')) ,
    Field('LogAnalistaAuditoria', 'string', label=T('AUDIT ANALYST (LOG)')),
    Field('LogJefeAuditoria', 'string', label=T('AUDIT MANAGER (LOG)')),
    Field('AprobacionAnalistaAuditoria', 'boolean', label=T('AUDIT ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeAuditoria', 'boolean', label=T('AUDIT MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s ' % (r.Nombre)
    )


db.define_table('TipoRevision',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaAuditoria', 'string', label=T('AUDIT ANALYST (LOG)')),
    Field('LogJefeAuditoria', 'string', label=T('AUDIT MANAGER (LOG)')),
    Field('AprobacionAnalistaAuditoria', 'boolean', label=T('AUDIT ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeAuditoria', 'boolean', label=T('AUDIT MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s ' % (r.Nombre)
    )

db.define_table('ValorMetricaSeguridadTi',
    Field('TratamientoRiesgoId', 'reference TratamientoRiesgo', label=T('RISK FACTOR'), notnull=True),
    Field('ValorMetricaId', 'reference ValorMetrica', label=T('CVSS METRIC'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('Archivo', 'upload', label=T('FILE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('LogResponsableControl', 'string', label=T('CONTROL RESPONSIBLE (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    Field('AprobacionResponsableControl', 'boolean', label=T('CONTROL RESPONSIBLE (APPROVAL)'), default='F'),
    )

db.define_table('Documentacion',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('Archivo', 'upload', label=T('FILE')),
    #Field('Visible', 'boolean', label=T('VISIBLE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    )
db.Documentacion.Nombre.requires = IS_NOT_IN_DB(db, db.Documentacion.Nombre)

db.define_table('TipoIncidenteSeguridad',
    Field('Nombre', 'string', label=T('NAME')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s' % (r.Nombre)
    )
db.TipoIncidenteSeguridad.Nombre.requires=IS_NOT_IN_DB(db, db.TipoIncidenteSeguridad.Nombre)

db.define_table('IncidenteSeguridad',
    Field('Nombre', 'text', label=T('NAME')),
    Field('TipoIncidenteSeguridadId', 'reference TipoIncidenteSeguridad', label=T('INCIDENT SECURITY TYPE'), notnull=True),
    Field('ActivoTiId', 'reference ActivoTi', label=T('IT ASSET'), notnull=True),
    #Field('RegionId', 'reference Region', label=T('REGION')),
    #Field('ActivoTiRegionId', 'reference ActivoTiRegion', label=T('IT ASSET'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('Respuesta', 'text', label=T('INCIDENT RESPONSE')),
    Field('Fecha', 'date', label=T('DATE'), default=request.now, requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('Evidencia', 'upload', label=T('EVIDENCE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    )

db.define_table('BenchObjetivoControl',
    Field('BenchVersionId','reference BenchVersion', label=T('CONTROL VERSION'), notnull=True),
    Field('Numero', 'string', label=T('CONTROL OBJECTIVE ID')),
    Field('Nombre', 'string', label=T('CONTROL OBJECTIVE')),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    #Field('NivelMadurezId', 'reference NivelMadurez', label=T('MATURITY LEVEL')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s' % (r.BenchVersionId.Version, '|', r.Numero, '|', r.Nombre)
    )
#db.BenchObjetivoControl.Nombre.requires = IS_NOT_IN_DB(db(db.BenchObjetivoControl.BenchVersionId==request.vars.BenchVersionId), db.BenchObjetivoControl.Nombre)
db.BenchObjetivoControl.Numero.requires = IS_NOT_IN_DB(db(db.BenchObjetivoControl.BenchVersionId==request.vars.BenchVersionId), db.BenchObjetivoControl.Numero)

db.define_table('BenchControl',
    Field('BenchObjetivoControlId', 'reference BenchObjetivoControl', label=T('CONTROL OBJECTIVE'), notnull=True),
    Field('Numero', 'string', label=T('CONTROL ACTIVITY ID')),
    Field('Nombre', 'text', label=T('CONTROL ACTIVITY')),
    Field('Descripcion','text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s %s %s %s %s %s %s' % (r.id, '|', r.BenchObjetivoControlId.BenchVersionId.Version, '|', r.BenchObjetivoControlId.Numero, '|', r.BenchObjetivoControlId.Nombre, '|', r.Numero, '|',  r.Nombre)
    )
#db.BenchControl.Nombre.requires = IS_NOT_IN_DB(db(db.BenchControl.BenchObjetivoControlId==request.vars.BenchObjetivoControlId), db.BenchControl.Nombre)
db.BenchControl.Numero.requires = IS_NOT_IN_DB(db(db.BenchControl.BenchObjetivoControlId==request.vars.BenchObjetivoControlId), db.BenchControl.Numero)

db.define_table('CatalogoControlBenchControl',
    Field('CatalogoControlId','reference CatalogoControl', label=T('CONTROL CATALOGUE'), notnull=True),
    Field('BenchControlId','reference BenchControl', label=T('BENCHMARK'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    #format=lambda r: '%s %s %s' % (r.id, '|', r.Nombre)
    )
#db.ObjetivoControl.Nombre.requires=IS_NOT_IN_DB(db, db.ObjetivoControl.Nombre)

db.define_table('EvaluacionControl',
    #Field('CatalogoControlId', 'reference CatalogoControl', label=T('CONTROL'), notnull=True),
    Field('TipoRevisionId', 'reference TipoRevision', notnull=True, label=T('TEST TYPE'),  comment=T('Control Design evaluates control effectiveness - Audit evaluates control compliance')),

    Field('DetallePoliticaId', 'reference DetallePolitica', label=T('POLICY')),
    Field('BenchControlId', 'reference BenchControl', label=T('BENCHMARK')),
    Field('TratamientoRiesgoId', 'reference TratamientoRiesgo', label=T('CONTROL ACTIVITY')),

    Field('ProcesoId', 'reference Proceso', label=T('PROCESS'), notnull=True),
    Field('ActivoTiId', 'reference ActivoTi', label=T('SYSTEM'), notnull=True),

    Field('CumplimientoControl', 'boolean', label=T('PASS/FAIL')),
    Field('NivelMadurezId', 'reference NivelMadurez', label=T('CONTROL MATURITY LEVEL'), comment=T('0-Incomplete:not implemented or fails, no evidence. 1-Performed:achieves its process purpose, 2-Managed:planned, monitores and adjusted, 3-Established:defined process, capable of achieving its process, 4-Predictable:operates within defined limits, 5-Optimizing:continuously improved')),
    Field('FechaRevision', 'date', label=T('REVISION DATE'), default=request.now, requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('Hallazgo','text', label=T('FINDING')),
    Field('Recomendacion', 'text', label=T('RECOMMENDATION')),

    Field('CuantificacionCVSS', 'float', label=T('CVSS SCORE'), comment=T('None (0.0) | Low (0.1 - 3.9) | Medium (4.0 - 6.9) | High (7.0 - 8.9) | Critical (9.0 - 10.0)')),
    Field('VectorCVSS', 'string', label=T('CVSS VECTOR STRING')),

    Field('LogAnalistaAuditoria', 'string', label=T('AUDIT ANALYST (LOG)')),
    Field('LogJefeAuditoria', 'string', label=T('AUDIT MANAGER (LOG)')),
    #Field('LogResponsableControl', 'string', label=T('CONTROL RESPONSIBLE (LOG)')),
    Field('AprobacionAnalistaAuditoria', 'boolean', label=T('AUDIT ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeAuditoria', 'boolean', label=T('AUDIT MANAGER (APPROVAL)'), default='F'),
    #Field('AprobacionResponsableControl', 'boolean', label=T('CONTROL RESPONSIBLE (APPROVAL)'), default='F'),
    format=lambda r: '%s %s %s %s %s %s %s' % (r.id, '|', r.ProcesoId.Nombre, '|', r.ActivoTiId.Nombre, '|', r.Hallazgo)
    )

db.define_table('ControlCvss',
    Field('EvaluacionControlId', 'reference EvaluacionControl', label=T('CONTROL TEST'), notnull=True),
    Field('ValorMetricaId', 'reference ValorMetrica', label=T('CVSS METRIC'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('Archivo', 'upload', label=T('FILE')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    )

db.define_table('DetallePoliticaBenchControl',
    Field('DetallePoliticaId','reference DetallePolitica', label=T('POLICY'), notnull=True),
    Field('BenchControlId','reference BenchControl', label=T('BENCHMARK'), notnull=True),
    Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    #format=lambda r: '%s %s %s' % (r.id, '|', r.Nombre)
    )
#db.ObjetivoControl.Nombre.requires=IS_NOT_IN_DB(db, db.ObjetivoControl.Nombre)

db.define_table('EmailConfig',
    #Field('emailAcctId', 'string', label='Email ID Account: '),
    #Field('emailAcctPassw', 'string', label='Email ID Passwd: '),
    #Field('serverName', 'string', label='Server Name: '),
    #Field('serverIp', 'string', label='Server IP: '),
    #Field('serverPort', 'integer', label='Server Port: '),
    Field('server_c', 'string', label=T('SERVER') ),
    Field('port_c', 'integer', label=T('PORT') ),
    Field('sender_c', 'string', label=T('SENDER EMAIL') ),
    Field('login_c', 'string', label=T('LOGIN') ),
    Field('password_c', 'password', label=T('PASSWD') ),
    Field('tls_c', 'boolean', label=T('TLS STARTTLS (25, 587)'), comment=('The connection starts as plaintext SMTP'), default=False),
    Field('tls_2', 'boolean', label=T('SMTP-over-SSL (465)'), comment=('The connection starts with a SSL connection'), default=False ),
    Field('openRelay', 'boolean', label=T('OPEN RELAY'), comment=('SMTP email server that allows third-party relay of email messages'), default=True),
    #Field('testResult', 'string', label=T('TEST RESULT') ),
    #format='%(server_c)s %(sender_c)s %(login_c)s',
    format = lambda r: '%s %s %s %s %s %s %s' % (r.id, '|', r.server_c, '|', r.sender_c, '|', r.login_c)
)

db.define_table('TestSeguridad',
    Field('BenchControlId', 'reference BenchControl', label=T('BENCHMARK'), notnull=True),
    Field('ActivoTiId','reference ActivoTi', label=T('SYSTEM'), notnull=True),
    Field('ProcesoId', 'reference Proceso', label=T('PROCESS'), notnull=True),
    #Field('StatusControl', 'boolean', label=T('CONTROL IMPLEMENTED'), default=True),
    Field('NivelMadurezId', 'reference NivelMadurez', label=T('MATURITY LEVEL'), ),
    Field('Comentarios','text', label=T('FINDING')),
    #Field('Evidencia','upload', label=T('EVIDENCE')),
    Field('Fecha','date', label=T('DATE'), default=request.now, requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('PlanAccion','text', label=T('ACTION PLAN')),
    #Field('ProyectoId','reference Proyecto', label=T('PROJECT'), notnull=True),
    #Field('Cumplimiento', 'boolean', label=T('PASS/FAIL')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format = lambda r: '%s' % (r.Comentarios)
    )
#db.PruebaSeguridad.BenchControlId.requires=IS_NOT_IN_DB(db( (db.PruebaSeguridad.ActivoTiId==request.vars.ActivoTiId) & (db.PruebaSeguridad.ProcesoId==request.vars.ProcesoId) ), db.PruebaSeguridad.BenchControlId)

db.define_table('EvidenciaTestSeguridad',
    Field('TestSeguridadId', 'reference TestSeguridad', label=T('GAP ANALYSIS ID')),
    Field('Evidencia', 'upload', label=T('EVIDENCE')),
    )

db.define_table('PruebaWeb',
    Field('ActivoTiId','reference ActivoTi', label=T('SYSTEM'), notnull=True),
    Field('Dominio','string', label=T('DOMAIN')),
    Field('URL','string', label=T('URL')),
    Field('Hallazgo','text', label=T('FINDING')),
    #Field('Evidencia','upload', label=T('EVIDENCE')),
    Field('Fecha','date', label=T('DATE'), default=request.now, requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('PlanAccion','text', label=T('ACTION PLAN')),
    Field('LogAnalistaRiesgo', 'string', label=T('RISK ANALYST (LOG)')),
    Field('LogJefeRiesgo', 'string', label=T('RISK MANAGER (LOG)')),
    Field('AprobacionAnalistaRiesgo', 'boolean', label=T('RISK ANALYST (APPROVAL)'), default='F'),
    Field('AprobacionJefeRiesgo', 'boolean', label=T('RISK MANAGER (APPROVAL)'), default='F'),
    format = lambda r: '%s %s %s' % (r.id, '|', r.Hallazgo)
    )

db.define_table('EvidenciaPruebaWeb',
    Field('PruebaWebId', 'reference PruebaWeb', label=T('WEB TEST ID')),
    Field('Evidencia', 'upload', label=T('EVIDENCE')),
    )

db.define_table('EvaluacionEvidencia',
    Field('EvaluacionControlId', 'reference EvaluacionControl', label=T('CONTROL TEST')),
    Field('Evidencia', 'upload', label=T('EVIDENCE')),
    Field('Fecha', 'date', label=T('DATE'), requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('Comentarios', 'text', label=T('COMMENTS')),
    Field('Tipo', 'string', label=T('EVIDENCE TYPE'), ),
    )
db.EvaluacionEvidencia.Tipo.requires=IS_IN_SET(['Finding (Hallazgo)','Control'])

db.define_table('FactorEvidencia',
    Field('TratamientoRiesgoId', 'reference TratamientoRiesgo', label=T('RISK FACTOR')),
    Field('Evidencia', 'upload', label=T('EVIDENCE')),
    Field('Fecha', 'date', label=T('DATE')),
    Field('Comentarios', 'text', label=T('COMMENTS')),
    Field('Tipo', 'string', label=T('EVIDENCE TYPE')),
    )
db.EvaluacionEvidencia.Tipo.requires=IS_IN_SET(['Finding (Hallazgo)','Control'])
