#-----------------------------------------------------
#Copyright (C) Rodolfo Lopez rodolfo.lopez@grcbit.com
#-----------------------------------------------------
from datetime import date, datetime, timedelta
import os
import base64
import time
import math
from decimal import Decimal as D
#------------------------------------------------------------------------
demo = False            #True/False->To enable/disable access control
demo_data = False    #True/False->To upload initial data 
#------------------------------------------------------------------------

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if request.args(0) == 'login' and ("@" in str(request.post_vars.username)):
        redirect(URL('default','index'))
    return dict(form=auth())

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

#------------------------
#Index - Risk dashboard
#------------------------
@auth.requires_login()
def index():
    return TableroRiesgo()

@auth.requires_login()
def ReporteMapaCalor():
    return TableroRiesgo()

@auth.requires_login()
def ReporteRiesgo():
    return TableroRiesgo()

@auth.requires_login()
def ReporteFactorRiesgo():
    return TableroRiesgo()

@auth.requires_login()
def ReporteControlTest():
    return TableroRiesgo()

#----------------
#Menu Inventario
#----------------
@auth.requires_login()
def TipoObjetivo():
    db.TipoObjetivo.id.readable = False
    db.TipoObjetivo.AprobacionJefeRiesgo.writable = False
    db.TipoObjetivo.AprobacionAnalistaRiesgo.writable = False
    db.TipoObjetivo.LogJefeRiesgo.writable = False
    db.TipoObjetivo.LogAnalistaRiesgo.writable = False
    Tabla = 'TipoObjetivo'
    fields = (db.TipoObjetivo.Nombre, db.TipoObjetivo.Descripcion, db.TipoObjetivo.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TipoObjetivo, links=links, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TipoObjetivo, links=links, fields=fields, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query=db.TipoObjetivo.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def ClasificacionRiesgo():
    db.ClasificacionRiesgo.id.readable=False
    db.ClasificacionRiesgo.AprobacionJefeRiesgo.writable=False
    db.ClasificacionRiesgo.AprobacionAnalistaRiesgo.writable=False
    db.ClasificacionRiesgo.LogJefeRiesgo.writable=False
    db.ClasificacionRiesgo.LogAnalistaRiesgo.writable=False
    Tabla = 'ClasificacionRiesgo'
    fields = (db.ClasificacionRiesgo.Nombre, db.ClasificacionRiesgo.Descripcion, db.ClasificacionRiesgo.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.ClasificacionRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.ClasificacionRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.ClasificacionRiesgo.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def TipoTratamientoRiesgo():
    db.TipoTratamientoRiesgo.id.readable = False
    db.TipoTratamientoRiesgo.AprobacionJefeRiesgo.writable=False
    db.TipoTratamientoRiesgo.AprobacionAnalistaRiesgo.writable=False
    db.TipoTratamientoRiesgo.LogJefeRiesgo.writable=False
    db.TipoTratamientoRiesgo.LogAnalistaRiesgo.writable=False
    #db.TipoTratamientoRiesgo.AnalistaRiesgo.writable=False
    Tabla = 'TipoTratamientoRiesgo'
    fields = (db.TipoTratamientoRiesgo.Nombre, db.TipoTratamientoRiesgo.Descripcion, db.TipoTratamientoRiesgo.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TipoTratamientoRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TipoTratamientoRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.TipoTratamientoRiesgo.AprobacionJefeRiesgo == 'T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True,create=False, editable=False, deletable=False,user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def GrupoFactorRiesgo():
    db.TipoVulnerabilidad.id.readable = False
    db.TipoVulnerabilidad.LogJefeRiesgo.writable = False
    db.TipoVulnerabilidad.LogAnalistaRiesgo.writable = False
    db.TipoVulnerabilidad.AprobacionJefeRiesgo.writable = False
    db.TipoVulnerabilidad.AprobacionAnalistaRiesgo.writable = False
    Tabla = 'TipoVulnerabilidad'
    fields = (db.TipoVulnerabilidad.id, db.TipoVulnerabilidad.Nombre, db.TipoVulnerabilidad.Descripcion, db.TipoVulnerabilidad.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form = SQLFORM.grid(db.TipoVulnerabilidad, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form = SQLFORM.grid(db.TipoVulnerabilidad, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.TipoVulnerabilidad.AprobacionJefeRiesgo == 'T'
        return dict(form = SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def ClasificacionControl():
    db.ClasificacionControl.id.readable=False
    db.ClasificacionControl.AprobacionJefeRiesgo.writable=False
    db.ClasificacionControl.AprobacionAnalistaRiesgo.writable=False
    db.ClasificacionControl.LogJefeRiesgo.writable=False
    db.ClasificacionControl.LogAnalistaRiesgo.writable=False
    Tabla = 'ClasificacionControl'
    fields = (db.ClasificacionControl.Nombre, db.ClasificacionControl.Descripcion, db.ClasificacionControl.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.ClasificacionControl, fields=fields, links=links, deletable=True, searchable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.ClasificacionControl, fields=fields, links=links, deletable=False, searchable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.ClasificacionControl.AprobacionJefeRiesgo == 'T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, deletable=False, create=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def TipoControl():
    db.TipoControl.id.readable = False
    db.TipoControl.AprobacionJefeRiesgo.writable=False
    db.TipoControl.AprobacionAnalistaRiesgo.writable=False
    db.TipoControl.LogJefeRiesgo.writable=False
    db.TipoControl.LogAnalistaRiesgo.writable=False
    Tabla = 'TipoControl'
    fields = (db.TipoControl.Nombre, db.TipoControl.Descripcion, db.TipoControl.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TipoControl, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TipoControl, fields=fields, links=links, searchable=True, deletable=False, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.TipoControl.AprobacionJefeRiesgo == 'T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True,deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def GrupoControl():
    db.CatalogoControl.id.readable = False
    db.CatalogoControl.AprobacionJefeRiesgo.writable=False
    db.CatalogoControl.AprobacionAnalistaRiesgo.writable=False
    db.CatalogoControl.LogJefeRiesgo.writable=False
    db.CatalogoControl.LogAnalistaRiesgo.writable=False
    Tabla = 'CatalogoControl'
    fields = (db.CatalogoControl.id, db.CatalogoControl.Nombre, db.CatalogoControl.Descripcion, db.CatalogoControl.Baseline, db.CatalogoControl.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.CatalogoControl, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.CatalogoControl, fields=fields, links=links, searchable=True, deletable=False, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.CatalogoControl.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True,deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def NivelMadurez():
    db.NivelMadurez.id.readable = False
    db.NivelMadurez.AprobacionJefeRiesgo.writable=False
    db.NivelMadurez.AprobacionAnalistaRiesgo.writable=False
    db.NivelMadurez.LogJefeRiesgo.writable=False
    db.NivelMadurez.LogAnalistaRiesgo.writable=False
    Tabla = 'NivelMadurez'
    fields = (db.NivelMadurez.Nombre, db.NivelMadurez.Descripcion, db.NivelMadurez.Valor, db.NivelMadurez.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.NivelMadurez, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True,  user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.NivelMadurez, fields=fields, links=links, searchable=True, deletable=False, create=True, editable=True,  user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.NivelMadurez.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

'''
@auth.requires_login()
def Direccion():
    db.Direccion.AprobacionJefeRiesgo.writable=False
    db.Direccion.AprobacionAnalistaRiesgo.writable=False
    db.Direccion.LogJefeRiesgo.writable=False
    db.Direccion.LogAnalistaRiesgo.writable=False
    Tabla = 'Direccion'
    fields = (db.Direccion.id, db.Direccion.Nombre, db.Direccion.RegionId, db.Direccion.Responsable, db.Direccion.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.Direccion, fields=fields, links=links, searchable=True, create=True, deletable=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.Direccion, fields=fields, links=links, searchable=True, create=True, deletable=False, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.Direccion.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))
'''

#----------------
#Menu Contexto
#----------------
@auth.requires_login()
def CriterioImpacto():
    db.CriterioImpacto.id.readable = False
    db.CriterioImpacto.LogJefeRiesgo.writable = False
    db.CriterioImpacto.AprobacionJefeRiesgo.writable = False
    db.CriterioImpacto.Valor.writable = False
    db.CriterioImpacto.Nombre.writable = False
    #db.CriterioImpacto.
    Tabla = 'CriterioImpacto'
    fields = (db.CriterioImpacto.Nombre, db.CriterioImpacto.Valor, db.CriterioImpacto.Descripcion, db.CriterioImpacto.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
 
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.CriterioImpacto, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.CriterioImpacto.AprobacionJefeRiesgo == 'T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def CriterioProbabilidad():
    db.CriterioProbabilidad.LogJefeRiesgo.writable = False
    db.CriterioProbabilidad.AprobacionJefeRiesgo.writable = False
    db.CriterioProbabilidad.Valor.writable = False
    db.CriterioProbabilidad.Nombre.writable = False
    db.CriterioProbabilidad.id.readable = False
    Tabla = 'CriterioProbabilidad'
    fields = (db.CriterioProbabilidad.Nombre, db.CriterioProbabilidad.Valor, db.CriterioProbabilidad.Descripcion, db.CriterioProbabilidad.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.CriterioProbabilidad, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.CriterioProbabilidad.AprobacionJefeRiesgo == 'T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def CriterioRiesgo():
    db.CriterioRiesgo.LogJefeRiesgo.writable = False
    db.CriterioRiesgo.AprobacionJefeRiesgo.writable = False
    db.CriterioRiesgo.CriterioImpactoId.writable = False
    db.CriterioRiesgo.RiesgoValor.writable = False
    db.CriterioRiesgo.CriterioProbabilidadId.writable = False
    db.CriterioRiesgo.Nombre.writable = False
    db.CriterioRiesgo.id.readable = False
    #db.CriterioRiesgo.LogJefeRiesgo.readable = False
    #db.CriterioRiesgo.AprobacionJefeRiesgo.readable = False
    Tabla = 'CriterioRiesgo'
    fields = (db.CriterioRiesgo.CriterioImpactoId, db.CriterioRiesgo.CriterioProbabilidadId, db.CriterioRiesgo.Nombre, db.CriterioRiesgo.RiesgoValor, db.CriterioRiesgo.Descripcion, db.CriterioRiesgo.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.CriterioRiesgo, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.CriterioRiesgo.AprobacionJefeRiesgo == 'T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def Organizacion():
    db.Organizacion.LogJefeRiesgo.writable = False
    db.Organizacion.AprobacionJefeRiesgo.writable = False
    db.Organizacion.LogAnalistaRiesgo.writable = False
    db.Organizacion.AprobacionAnalistaRiesgo.writable = False
    Tabla = 'Organizacion'
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    fields = (db.Organizacion.id, db.Organizacion.Nombre, db.Organizacion.Descripcion, db.Organizacion.AprobacionJefeRiesgo)

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.Organizacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.Organizacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.Organizacion.AprobacionJefeRiesgo == 'T'
        return dict(form=SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500, fields=fields))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def ObjetivoOrganizacion():
    db.ObjetivoOrganizacion.LogJefeRiesgo.writable = False
    db.ObjetivoOrganizacion.AprobacionJefeRiesgo.writable = False
    db.ObjetivoOrganizacion.LogAnalistaRiesgo.writable = False
    db.ObjetivoOrganizacion.AprobacionAnalistaRiesgo.writable = False
    Tabla = 'ObjetivoOrganizacion'
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    fields = (db.ObjetivoOrganizacion.id, db.ObjetivoOrganizacion.Nombre, db.ObjetivoOrganizacion.Descripcion, db.ObjetivoOrganizacion.TipoObjetivoId, db.ObjetivoOrganizacion.AprobacionJefeRiesgo)
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.ObjetivoOrganizacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.ObjetivoOrganizacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.ObjetivoOrganizacion.AprobacionJefeRiesgo == 'T'
        return dict(form=SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500, fields=fields))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def RolResponsabilidad():
    db.RolResponsabilidad.LogJefeRiesgo.writable = False
    db.RolResponsabilidad.AprobacionJefeRiesgo.writable = False
    db.RolResponsabilidad.LogAnalistaRiesgo.writable = False
    db.RolResponsabilidad.AprobacionAnalistaRiesgo.writable = False
    Tabla = 'RolResponsabilidad'
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    fields = (db.RolResponsabilidad.id, db.RolResponsabilidad.Rol, db.RolResponsabilidad.Descripcion, db.RolResponsabilidad.AprobacionJefeRiesgo)
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.RolResponsabilidad, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.RolResponsabilidad, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = (db.RolResponsabilidad.AprobacionJefeRiesgo=='T')
        return dict(form=SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500, fields=fields))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def CatalogoPolitica():
    db.CatalogoPolitica.id.readable=False
    db.CatalogoPolitica.AprobacionJefeRiesgo.writable=False
    db.CatalogoPolitica.AprobacionAnalistaRiesgo.writable=False
    db.CatalogoPolitica.LogJefeRiesgo.writable=False
    db.CatalogoPolitica.LogAnalistaRiesgo.writable=False
    Tabla = 'CatalogoPolitica'
    fields = (db.CatalogoPolitica.id, db.CatalogoPolitica.Nombre, db.CatalogoPolitica.Version, db.CatalogoPolitica.FechaCreacion, db.CatalogoPolitica.Descripcion, db.CatalogoPolitica.Archivo, db.CatalogoPolitica.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form = SQLFORM.grid(db.CatalogoPolitica, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form = SQLFORM.grid(db.CatalogoPolitica, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query=(db.CatalogoPolitica.AprobacionJefeRiesgo=='T')
        return dict(form = SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
       redirect(URL('default','index'))

@auth.requires_login()
def DetallePolitica():
    db.DetallePolitica.id.readable=False
    db.DetallePolitica.AprobacionJefeRiesgo.writable=False
    db.DetallePolitica.AprobacionAnalistaRiesgo.writable=False
    db.DetallePolitica.LogJefeRiesgo.writable=False
    db.DetallePolitica.LogAnalistaRiesgo.writable=False
    Tabla = 'DetallePolitica'
    fields = (db.DetallePolitica.id, db.DetallePolitica.CatalogoPoliticaId, db.DetallePolitica.Codigo, db.DetallePolitica.Nombre, db.DetallePolitica.Archivo, db.DetallePolitica.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form = SQLFORM.grid(db.DetallePolitica, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500, orderby=db.DetallePolitica.Codigo ))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form = SQLFORM.grid(db.DetallePolitica, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500, orderby=db.DetallePolitica.Codigo ))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query=(db.DetallePolitica.AprobacionJefeRiesgo=='T')
        return dict(form = SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500, orderby=db.DetallePolitica.Codigo))
    else:
        redirect(URL('default','index'))

#--------------------
# Risks & Controls
#--------------------
@auth.requires_login()
def AnalisisRiesgo():
    db.AnalisisRiesgo.AnalistaRiesgo.default = auth.user.username
    #if versionGratuita==1:
    #    numRiesgos=db().select(db.AnalisisRiesgo.id, limitby=(0,10), orderby=db.AnalisisRiesgo.id).last().id
    #    db(db.AnalisisRiesgo.id>numRiesgos).delete()
    #    db(db.TratamientoRiesgo.AnalisisRiesgoId>numRiesgos).delete()
    db.AnalisisRiesgo.LogAnalistaRiesgo.writable=False
    db.AnalisisRiesgo.LogJefeRiesgo.writable=False
    db.AnalisisRiesgo.LogDuenoRiesgo.writable=False
    db.AnalisisRiesgo.AprobacionAnalistaRiesgo.writable=False
    db.AnalisisRiesgo.AprobacionJefeRiesgo.writable=False
    db.AnalisisRiesgo.AprobacionDuenoRiesgo.writable=False
    db.AnalisisRiesgo.AnalistaRiesgo.writable=False
    Tabla = 'AnalisisRiesgo'
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    fields=(db.AnalisisRiesgo.id, db.AnalisisRiesgo.Riesgo, db.AnalisisRiesgo.NivelRiesgo, db.AnalisisRiesgo.RiesgoMaterializado, db.AnalisisRiesgo.ImpactoJustificacion, db.AnalisisRiesgo.AprobacionJefeRiesgo)

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AnalisisRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AnalisisRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskOwner'):
        db.AnalisisRiesgo.Riesgo.writable = False
        db.AnalisisRiesgo.FechaRevision.writable = False
        db.AnalisisRiesgo.EvidenciaRiesgo.writable = False
        db.AnalisisRiesgo.RiesgoMaterializado.writable = False
        db.AnalisisRiesgo.NivelRiesgo.writable = False
        #db.AnalisisRiesgo.ImpactoJustificacion.writable = False
        db.AnalisisRiesgo.DuenoRiesgo.writable = False
        #db.AnalisisRiesgo.AnalisisRiesgo.writable = False
        db.AnalisisRiesgo.LogAnalistaRiesgo.writable = False
        db.AnalisisRiesgo.LogJefeRiesgo.writable = False
        db.AnalisisRiesgo.LogDuenoRiesgo.writable = False
        db.AnalisisRiesgo.AprobacionAnalistaRiesgo.writable = False
        db.AnalisisRiesgo.AprobacionJefeRiesgo.writable = False
        db.AnalisisRiesgo.AprobacionDuenoRiesgo.writable = False
        #ActualizaAprobacion(Tabla)
        riesgoId=[]
        #for a in db(db.AnalisisRiesgo.AprobacionJefeRiesgo=='T').select(db.AnalisisRiesgo.id, db.AnalisisRiesgo.DuenoRiesgo, cacheable=True):
        for a in db(db.AnalisisRiesgo.AprobacionJefeRiesgo=='T').select(db.AnalisisRiesgo.id, db.AnalisisRiesgo.DuenoRiesgo):
            try:
                for b in str(str(a.DuenoRiesgo).replace(' ','')).split(','):
                    if b==auth.user.username:
                        riesgoId.append(int(a.id))
            except:
                pass
        query = db.AnalisisRiesgo.id.belongs(riesgoId)
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = (db.AnalisisRiesgo.AprobacionJefeRiesgo=='T')
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def TratamientoRiesgo():
    db.TratamientoRiesgo.CalculoImpacto.readable = False
    db.TratamientoRiesgo.CalculoProbabilidad.readable = False
    db.TratamientoRiesgo.AnalistaRiesgo.default = auth.user.username
    db.TratamientoRiesgo.AnalistaRiesgo.writable=False
    db.TratamientoRiesgo.LogAnalistaRiesgo.writable = False
    db.TratamientoRiesgo.LogJefeRiesgo.writable = False
    db.TratamientoRiesgo.LogResponsableControl.writable = False
    db.TratamientoRiesgo.AprobacionAnalistaRiesgo.writable = False
    db.TratamientoRiesgo.AprobacionJefeRiesgo.writable = False
    db.TratamientoRiesgo.AprobacionResponsableControl.writable = False
    db.TratamientoRiesgo.CalculoImpacto.writable = False
    db.TratamientoRiesgo.CalculoProbabilidad.writable = False
    db.TratamientoRiesgo.CuantificacionCVSS.writable = False
    db.TratamientoRiesgo.VectorCVSS.writable = False
    db.TratamientoRiesgo.CuantificacionCVSSE.writable = False
    db.TratamientoRiesgo.VectorCVSSE.writable = False
    #if riesgosTI==False:
    #db.TratamientoRiesgo.CuantificacionCVSS.readable = False
    #db.TratamientoRiesgo.VectorCVSS.readable = False
    db.TratamientoRiesgo.CuantificacionCVSSE.readable = False
    db.TratamientoRiesgo.VectorCVSSE.readable = False

    Tabla="TratamientoRiesgo"

    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssEvaluation", args=[row.id, Tabla, "2", base64.b64encode(request.vars.get('keywords'))], vars=dict(metrica="base") ))   ]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])),  lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssEvaluation", args=[row.id, Tabla, "2"], vars=dict(metrica="base") )) ]
        
    fields=(db.TratamientoRiesgo.id, db.TratamientoRiesgo.FactorRiesgo, db.TratamientoRiesgo.ProcesoId, db.TratamientoRiesgo.ActivoTiId, db.TratamientoRiesgo.CriterioImpactoId, db.TratamientoRiesgo.CriterioProbabilidadId, db.TratamientoRiesgo.AprobacionJefeRiesgo)

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TratamientoRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TratamientoRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='controlResp'):
        #ActualizaAprobacion(Tabla)
        db.TratamientoRiesgo.FechaRevision.writable = False
        db.TratamientoRiesgo.ProcesoId.writable = False
        db.TratamientoRiesgo.ActivoTiId.writable = False
        db.TratamientoRiesgo.FactorRiesgo.writable = False
        db.TratamientoRiesgo.TipoVulnerabilidadId.writable = False
        db.TratamientoRiesgo.RiesgoFraude.writable = False
        db.TratamientoRiesgo.EscenarioAmenaza.writable = False
        db.TratamientoRiesgo.CriterioImpactoId.writable = False
        db.TratamientoRiesgo.CriterioProbabilidadId.writable = False
        db.TratamientoRiesgo.CuantificacionCVSS.writable = False
        db.TratamientoRiesgo.VectorCVSS.writable = False
        db.TratamientoRiesgo.CuantificacionCVSSE.writable = False
        db.TratamientoRiesgo.VectorCVSSE.writable = False
        db.TratamientoRiesgo.CalculoImpacto.writable = False
        db.TratamientoRiesgo.CalculoProbabilidad.writable = False
        db.TratamientoRiesgo.TipoTratamientoRiesgoId.writable = False
        db.TratamientoRiesgo.EvidenciaRiesgo.writable = False
        db.TratamientoRiesgo.RiesgoMaterializadoCheck.writable = False
        db.TratamientoRiesgo.CatalogoControlId.writable = False
        db.TratamientoRiesgo.ObjetivoControl.writable = False
        db.TratamientoRiesgo.Referencia.writable = False
        db.TratamientoRiesgo.ActividadControl.writable = False
        db.TratamientoRiesgo.TipoControlId.writable = False
        db.TratamientoRiesgo.ClasificacionControlId.writable = False
        db.TratamientoRiesgo.KeyControl.writable = False
        db.TratamientoRiesgo.ResponsableControl.writable = False
        #db.TratamientoRiesgo.StatusImplementacionControl.writable = False
        #db.TratamientoRiesgo.EvidenciaControl.writable = False
        #db.TratamientoRiesgo.FechaImplementacionControl.writable = False
        #db.TratamientoRiesgo..writable = False
        #db.TratamientoRiesgo.ComentariosResponsableControl.writable = False
        db.TratamientoRiesgo.AnalistaRiesgo.writable = False
        db.TratamientoRiesgo.LogAnalistaRiesgo.writable = False
        db.TratamientoRiesgo.LogJefeRiesgo.writable = False
        db.TratamientoRiesgo.LogResponsableControl.writable = False
        db.TratamientoRiesgo.AprobacionAnalistaRiesgo.writable = False
        db.TratamientoRiesgo.AprobacionJefeRiesgo.writable = False
        db.TratamientoRiesgo.AprobacionResponsableControl.writable = False

        controlId=[]
        for a in db(db.TratamientoRiesgo.AprobacionJefeRiesgo=='T').select(db.TratamientoRiesgo.id, db.TratamientoRiesgo.ResponsableControl):
            try:
                for b in str(str(a.ResponsableControl).replace(' ','')).split(','):
                    if b==auth.user.username:
                        controlId.append(int(a.id))
            except:
                pass
        query = db.TratamientoRiesgo.id.belongs(controlId)
        return dict(form=SQLFORM.grid(query=query, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskOwner'):
        #ActualizaAprobacion(Tabla)
        db.TratamientoRiesgo.FechaRevision.writable = False
        db.TratamientoRiesgo.ProcesoId.writable = False
        db.TratamientoRiesgo.ActivoTiId.writable = False
        db.TratamientoRiesgo.FactorRiesgo.writable = False
        db.TratamientoRiesgo.TipoVulnerabilidadId.writable = False
        db.TratamientoRiesgo.RiesgoFraude.writable = False
        db.TratamientoRiesgo.EscenarioAmenaza.writable = False
        db.TratamientoRiesgo.CriterioImpactoId.writable = False
        db.TratamientoRiesgo.CriterioProbabilidadId.writable = False
        db.TratamientoRiesgo.CuantificacionCVSS.writable = False
        db.TratamientoRiesgo.VectorCVSS.writable = False
        db.TratamientoRiesgo.CuantificacionCVSSE.writable = False
        db.TratamientoRiesgo.VectorCVSSE.writable = False
        db.TratamientoRiesgo.CalculoImpacto.writable = False
        db.TratamientoRiesgo.CalculoProbabilidad.writable = False
        db.TratamientoRiesgo.TipoTratamientoRiesgoId.writable = False
        db.TratamientoRiesgo.EvidenciaRiesgo.writable = False
        db.TratamientoRiesgo.RiesgoMaterializadoCheck.writable = False
        db.TratamientoRiesgo.CatalogoControlId.writable = False
        db.TratamientoRiesgo.ObjetivoControl.writable = False
        db.TratamientoRiesgo.Referencia.writable = False
        db.TratamientoRiesgo.ActividadControl.writable = False
        db.TratamientoRiesgo.TipoControlId.writable = False
        db.TratamientoRiesgo.ClasificacionControlId.writable = False
        db.TratamientoRiesgo.KeyControl.writable = False
        db.TratamientoRiesgo.ResponsableControl.writable = False
        #db.TratamientoRiesgo.StatusImplementacionControl.writable = False
        #db.TratamientoRiesgo.EvidenciaControl.writable = False
        #db.TratamientoRiesgo.FechaImplementacionControl.writable = False
        #db.TratamientoRiesgo..writable = False
        #db.TratamientoRiesgo.ComentariosResponsableControl.writable = False
        db.TratamientoRiesgo.AnalistaRiesgo.writable = False
        db.TratamientoRiesgo.LogAnalistaRiesgo.writable = False
        db.TratamientoRiesgo.LogJefeRiesgo.writable = False
        db.TratamientoRiesgo.LogResponsableControl.writable = False
        db.TratamientoRiesgo.AprobacionAnalistaRiesgo.writable = False
        db.TratamientoRiesgo.AprobacionJefeRiesgo.writable = False
        db.TratamientoRiesgo.AprobacionResponsableControl.writable = False

        controlId=[]
        for a in db((db.TratamientoRiesgo.AprobacionJefeRiesgo=='T') & (db.TratamientoRiesgoAnalisisRiesgo.TratamientoRiesgoId==db.TratamientoRiesgo.id) & (db.TratamientoRiesgoAnalisisRiesgo.AnalisisRiesgoId == db.AnalisisRiesgo.id)).select(db.TratamientoRiesgo.id, db.AnalisisRiesgo.DuenoRiesgo):
            try:
                for b in str(str(a.AnalisisRiesgo.DuenoRiesgo).replace(' ','')).split(','):
                    if b==auth.user.username:
                        controlId.append(int(a.TratamientoRiesgo.id))
            except:
                pass
        query = db.TratamientoRiesgo.id.belongs(controlId)
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = (db.TratamientoRiesgo.AprobacionJefeRiesgo=='T')
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def AnalisisRiesgoClasificacionRiesgo():
    #db.AnalisisRiesgoClasificacionRiesgo.id.readable=False
    db.AnalisisRiesgoClasificacionRiesgo.AprobacionJefeRiesgo.writable=False
    db.AnalisisRiesgoClasificacionRiesgo.AprobacionAnalistaRiesgo.writable=False
    db.AnalisisRiesgoClasificacionRiesgo.LogJefeRiesgo.writable=False
    db.AnalisisRiesgoClasificacionRiesgo.LogAnalistaRiesgo.writable=False
    Tabla = 'AnalisisRiesgoClasificacionRiesgo'

    fields = (db.AnalisisRiesgoClasificacionRiesgo.id, db.AnalisisRiesgoClasificacionRiesgo.AnalisisRiesgoId, db.AnalisisRiesgoClasificacionRiesgo.ClasificacionRiesgoId, db.AnalisisRiesgoClasificacionRiesgo.Descripcion, db.AnalisisRiesgoClasificacionRiesgo.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AnalisisRiesgoClasificacionRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AnalisisRiesgoClasificacionRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))

    elif auth.has_membership(role='riskOwner'):
        db.AnalisisRiesgoClasificacionRiesgo.AnalisisRiesgoId.writable=False
        controlId=[]
        for a in db((db.AnalisisRiesgoClasificacionRiesgo.AprobacionJefeRiesgo=='T') & (db.AnalisisRiesgoClasificacionRiesgo.AnalisisRiesgoId==db.AnalisisRiesgo.id)).select(db.AnalisisRiesgoClasificacionRiesgo.id, db.AnalisisRiesgo.DuenoRiesgo):
            try:
                for b in str(str(a.AnalisisRiesgo.DuenoRiesgo).replace(' ','')).split(','):
                    if b==auth.user.username:
                        controlId.append(int(a.AnalisisRiesgoClasificacionRiesgo.id))
            except:
                pass
        query = db.AnalisisRiesgoClasificacionRiesgo.id.belongs(controlId)
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))

    elif  auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.AnalisisRiesgoClasificacionRiesgo.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def AnalisisRiesgoObjetivoOrganizacion():
    #db.AnalisisRiesgoClasificacionRiesgo.id.readable=False
    db.AnalisisRiesgoObjetivoOrganizacion.AprobacionJefeRiesgo.writable=False
    db.AnalisisRiesgoObjetivoOrganizacion.AprobacionAnalistaRiesgo.writable=False
    db.AnalisisRiesgoObjetivoOrganizacion.LogJefeRiesgo.writable=False
    db.AnalisisRiesgoObjetivoOrganizacion.LogAnalistaRiesgo.writable=False
    Tabla = 'AnalisisRiesgoObjetivoOrganizacion'
    fields = (db.AnalisisRiesgoObjetivoOrganizacion.id, db.AnalisisRiesgoObjetivoOrganizacion.AnalisisRiesgoId, db.AnalisisRiesgoObjetivoOrganizacion.ObjetivoOrganizacionId, db.AnalisisRiesgoObjetivoOrganizacion.Descripcion, db.AnalisisRiesgoObjetivoOrganizacion.AprobacionJefeRiesgo)

    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AnalisisRiesgoObjetivoOrganizacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AnalisisRiesgoObjetivoOrganizacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))

    elif auth.has_membership(role='riskOwner'):
        db.AnalisisRiesgoObjetivoOrganizacion.AnalisisRiesgoId.writable=False
        controlId=[]
        for a in db((db.AnalisisRiesgoObjetivoOrganizacion.AprobacionJefeRiesgo=='T') & (db.AnalisisRiesgoObjetivoOrganizacion.AnalisisRiesgoId==db.AnalisisRiesgo.id)).select(db.AnalisisRiesgoObjetivoOrganizacion.id, db.AnalisisRiesgo.DuenoRiesgo):
            try:
                for b in str(str(a.AnalisisRiesgo.DuenoRiesgo).replace(' ','')).split(','):
                    if b==auth.user.username:
                        controlId.append(int(a.AnalisisRiesgoObjetivoOrganizacion.id))
            except:
                pass
        query = db.AnalisisRiesgoObjetivoOrganizacion.id.belongs(controlId)
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))

    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'): 
        query = db.AnalisisRiesgoObjetivoOrganizacion.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def TratamientoRiesgoAnalisisRiesgo():
    #db.AnalisisRiesgoClasificacionRiesgo.id.readable=False
    db.TratamientoRiesgoAnalisisRiesgo.AprobacionJefeRiesgo.writable=False
    db.TratamientoRiesgoAnalisisRiesgo.AprobacionAnalistaRiesgo.writable=False
    db.TratamientoRiesgoAnalisisRiesgo.LogJefeRiesgo.writable=False
    db.TratamientoRiesgoAnalisisRiesgo.LogAnalistaRiesgo.writable=False
    Tabla = 'TratamientoRiesgoAnalisisRiesgo'
    fields = (db.TratamientoRiesgoAnalisisRiesgo.id, db.TratamientoRiesgoAnalisisRiesgo.AnalisisRiesgoId, db.TratamientoRiesgoAnalisisRiesgo.TratamientoRiesgoId, db.TratamientoRiesgoAnalisisRiesgo.Descripcion, db.TratamientoRiesgoAnalisisRiesgo.AprobacionJefeRiesgo)

    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TratamientoRiesgoAnalisisRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TratamientoRiesgoAnalisisRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))

    elif auth.has_membership('controlResp'):
        db.TratamientoRiesgoAnalisisRiesgo.TratamientoRiesgoId.writable=False
        controlId=[]
        for a in db( (db.TratamientoRiesgoAnalisisRiesgo.AprobacionJefeRiesgo=='T') & (db.TratamientoRiesgoAnalisisRiesgo.TratamientoRiesgoId==db.TratamientoRiesgo.id) ).select(db.TratamientoRiesgoAnalisisRiesgo.id, db.TratamientoRiesgo.ResponsableControl):
            try:
                for b in str(str(a.ResponsableControl).replace(' ','')).split(','):
                    if b==auth.user.username:
                        controlId.append(int(a.id))
            except:
                pass
        query = db.TratamientoRiesgoAnalisisRiesgo.id.belongs(controlId)
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))

    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest') or auth.has_membership(role='processOwner') or auth.has_membership(role='informationOwner') or auth.has_membership(role='itAdmin') or auth.has_membership(role='riskOwner'):
        query = db.TratamientoRiesgoAnalisisRiesgo.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

#---------
#Activo
#---------
@auth.requires_login()
def EvaluacionControl():
    #db.SeguridadTi.id.readable = False
    db.EvaluacionControl.LogAnalistaAuditoria.writable = False
    db.EvaluacionControl.LogJefeAuditoria.writable = False
    #db.EvaluacionControl.LogResponsableControl.writable = False
    db.EvaluacionControl.AprobacionAnalistaAuditoria.writable = False
    db.EvaluacionControl.AprobacionJefeAuditoria.writable = False
    #db.EvaluacionControl.AprobacionResponsableControl.writable = False
    Tabla = 'EvaluacionControl'
     
    fields = (db.EvaluacionControl.id, db.EvaluacionControl.TipoRevisionId, db.EvaluacionControl.DetallePoliticaId, db.EvaluacionControl.BenchControlId, db.EvaluacionControl.TratamientoRiesgoId, db.EvaluacionControl.ActivoTiId, db.EvaluacionControl.ProcesoId, db.EvaluacionControl.AprobacionJefeAuditoria)
    if request.vars.get('keywords'):
        #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('File'),_class='button btn btn-info',_href=URL("default","EvaluacionEvidencia", vars=dict(EvaluacionControlId=row.id), args=[ base64.b64encode(request.vars.get('keywords'))])) ]
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssEvaluation1", args=[row.id, Tabla, "2", base64.b64encode(request.vars.get('keywords'))], vars=dict(metrica="base") )) ]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssEvaluation1", args=[row.id, Tabla, "2"], vars=dict(metrica="base") )) ]

    if auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.EvaluacionControl, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    #elif auth.has_membership(role='controlResp'):
    #    ActualizaAprobacion(Tabla)
    #    controlId=[]
    #    for a in db(db.EvaluacionControl.AprobacionJefeAuditoria=='T').select(db.EvaluacionControl.id, db.EvaluacionControl.ResponsableControl):
    #        try:
    #            for b in str(str(a.ResponsableControl).replace(' ','')).split(','):
    #                if b==auth.user.username:
    #                    controlId.append(int(a.id))
    #        except:
    #            pass
    #    query = db.EvaluacionControl.id.belongs(controlId)
    #    db.EvaluacionControl.TratamientoRiesgoId.writable=False
    #    db.EvaluacionControl.DetallePoliticaId.writable=False
    #    db.EvaluacionControl.CumplimientoControl.writable=False
    #    db.EvaluacionControl.EfectividadControl.writable=False
    #    db.EvaluacionControl.NivelMadurezId.writable=False
    #    db.EvaluacionControl.FechaRevision.writable=False
    #    db.EvaluacionControl.TipoRevisionId.writable=False
    #    db.EvaluacionControl.AlcanceRevisionId.writable=False
    #    db.EvaluacionControl.EscenarioRiesgo.writable=False
    #    db.EvaluacionControl.Recomendacion.writable=False
    #    db.EvaluacionControl.EvidenciaCumplimiento.writable=False
    #    db.EvaluacionControl.ResponsableControl.writable=False
    #    #db.EvaluacionControl.ComentariosResponsableControl.writable=False
    #    #db.EvaluacionControl.EvidenciaControl.writable=False
    #    #db.EvaluacionControl.FechaImplementacionControl.writable=False
    #    form=SQLFORM.grid(query=query, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.EvaluacionControl, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def TipoRevision():
    db.TipoRevision.id.readable = False
    db.TipoRevision.LogJefeAuditoria.writable = False
    db.TipoRevision.LogAnalistaAuditoria.writable = False
    db.TipoRevision.AprobacionJefeAuditoria.writable = False
    db.TipoRevision.AprobacionAnalistaAuditoria.writable = False
    #db.TipoRevision.Nombre.writable = False
    Tabla = 'TipoRevision'
    fields = (db.TipoRevision.Nombre, db.TipoRevision.Descripcion, db.TipoRevision.AprobacionJefeAuditoria)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.TipoRevision, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.TipoRevision, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

#------------------
#Proceso
#------------------

@auth.requires_login()
def ActivoInformacion():
    db.ActivoInformacion.LogAnalistaRiesgo.writable = False
    db.ActivoInformacion.LogJefeRiesgo.writable = False
    db.ActivoInformacion.LogDuenoInformacion.writable = False
    db.ActivoInformacion.AprobacionAnalistaRiesgo.writable = False
    db.ActivoInformacion.AprobacionJefeRiesgo.writable = False
    db.ActivoInformacion.AprobacionDuenoInformacion.writable = False
    Tabla = "ActivoInformacion"
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    #fields = (db.ActivoInformacion.id, db.ActivoInformacion.Nombre, db.ActivoInformacion.ClasificacionInformacionId, db.ActivoInformacion.RegulacionDatoId, db.ActivoInformacion.DuenoInformacion, db.ActivoInformacion.AprobacionJefeRiesgo)
    fields = (db.ActivoInformacion.id, db.ActivoInformacion.Nombre, db.ActivoInformacion.ClasificacionInformacionId, db.ActivoInformacion.DuenoInformacion, db.ActivoInformacion.AprobacionJefeRiesgo)
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoInformacion, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500, links=links)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoInformacion, fields=fields, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500, links=links)
    #elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp'):
        ActualizaAprobacion(Tabla)
        query = (db.ActivoInformacion.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='informationOwner'):
        ActivosInformacion=[]
        for a in db().select(db.ActivoInformacion.id, db.ActivoInformacion.DuenoInformacion, cacheable=True):
            try:
                for b in str(str(a.DuenoInformacion).replace(' ','')).split(','):
                    if b==auth.user.username:
                        ActivosInformacion.append(int(a.id))
            except:
                pass
        query = db.ActivoInformacion.id.belongs(ActivosInformacion)
        form = SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500, links=links)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

#--------
#Proceso
#--------

@auth.requires_login()
def TipoVulnerabilidadAnalisisRiesgo():
    #db.AnalisisRiesgoClasificacionRiesgo.id.readable=False
    db.TipoVulnerabilidadAnalisisRiesgo.AprobacionJefeRiesgo.writable=False
    db.TipoVulnerabilidadAnalisisRiesgo.AprobacionAnalistaRiesgo.writable=False
    db.TipoVulnerabilidadAnalisisRiesgo.LogJefeRiesgo.writable=False
    db.TipoVulnerabilidadAnalisisRiesgo.LogAnalistaRiesgo.writable=False
    Tabla = 'TipoVulnerabilidadAnalisisRiesgo'
    fields = (db.TipoVulnerabilidadAnalisisRiesgo.id, db.TipoVulnerabilidadAnalisisRiesgo.AnalisisRiesgoId, db.TipoVulnerabilidadAnalisisRiesgo.TipoVulnerabilidadId, db.TipoVulnerabilidadAnalisisRiesgo.Descripcion, db.TipoVulnerabilidadAnalisisRiesgo.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TipoVulnerabilidadAnalisisRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TipoVulnerabilidadAnalisisRiesgo, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.TipoVulnerabilidadAnalisisRiesgo.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

'''
@auth.requires_login()
def GrupoControl():
    #db.CatalogoControl.id.readable = False
    db.GrupoControl.AprobacionJefeRiesgo.writable=False
    db.GrupoControl.AprobacionAnalistaRiesgo.writable=False
    db.GrupoControl.LogJefeRiesgo.writable=False
    db.GrupoControl.LogAnalistaRiesgo.writable=False
    Tabla = 'GrupoControl'
    #fields = (db.CatalogoControl.id, db.CatalogoControl.Nombre, db.CatalogoControl.Descripcion, db.CatalogoControl.ControlClave, db.CatalogoControl.AprobacionJefeRiesgo)
    fields = (db.GrupoControl.id, db.GrupoControl.Nombre, db.GrupoControl.Descripcion, db.GrupoControl.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.GrupoControl, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.GrupoControl, fields=fields, links=links, searchable=True, deletable=False, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        return dict(form=SQLFORM.grid(db.GrupoControl, fields=fields, searchable=True,deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))
@auth.requires_login()
def AlcanceControl():
    db.AlcanceControl.AprobacionJefeRiesgo.writable=False
    db.AlcanceControl.AprobacionAnalistaRiesgo.writable=False
    db.AlcanceControl.LogJefeRiesgo.writable=False
    db.AlcanceControl.LogAnalistaRiesgo.writable=False
    Tabla = 'AlcanceControl'
    fields = (db.AlcanceControl.id, db.AlcanceControl.Nombre, db.AlcanceControl.Descripcion, db.AlcanceControl.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AlcanceControl, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AlcanceControl, fields=fields, links=links, searchable=True, deletable=False, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        return dict(form=SQLFORM.grid(db.AlcanceControl, fields=fields, searchable=True,deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))
@auth.requires_login()
def BenchMark():
    #db.CatalogoControl.id.readable = False
    db.BenchMark.AprobacionJefeRiesgo.writable=False
    db.BenchMark.AprobacionAnalistaRiesgo.writable=False
    db.BenchMark.LogJefeRiesgo.writable=False
    db.BenchMark.LogAnalistaRiesgo.writable=False
    Tabla = 'BenchMark'
    fields = (db.BenchMark.id, db.BenchMark.Nombre, db.BenchMark.Descripcion, db.BenchMark.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.BenchMark, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.BenchMark, fields=fields, links=links, searchable=True, deletable=False, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        return dict(form=SQLFORM.grid(db.BenchMark, fields=fields, searchable=True,deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))
@auth.requires_login()
def ObjetivoControl():
    #db.CatalogoControl.id.readable = False
    db.BenchMarkLista.AprobacionJefeRiesgo.writable=False
    db.BenchMarkLista.AprobacionAnalistaRiesgo.writable=False
    db.BenchMarkLista.LogJefeRiesgo.writable=False
    db.BenchMarkLista.LogAnalistaRiesgo.writable=False
    Tabla = 'BenchMarkLista'
    fields = (db.BenchMarkLista.id, db.BenchMarkLista.BenchMarkId, db.BenchMarkLista.Codigo, db.BenchMarkLista.Nombre, db.BenchMarkLista.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.BenchMarkLista, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.BenchMarkLista, fields=fields, links=links, searchable=True, deletable=False, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        return dict(form=SQLFORM.grid(db.BenchMarkLista, fields=fields, searchable=True,deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))
'''        
@auth.requires_login()
def CatalogoControlBenchControl():
    #db.CatalogoControl.id.readable = False
    db.CatalogoControlBenchControl.AprobacionJefeRiesgo.writable=False
    db.CatalogoControlBenchControl.AprobacionAnalistaRiesgo.writable=False
    db.CatalogoControlBenchControl.LogJefeRiesgo.writable=False
    db.CatalogoControlBenchControl.LogAnalistaRiesgo.writable=False
    Tabla = 'CatalogoControlBenchControl'
    fields = (db.CatalogoControlBenchControl.id, db.CatalogoControlBenchControl.CatalogoControlId, db.CatalogoControlBenchControl.BenchControlId, db.CatalogoControlBenchControl.Descripcion, db.CatalogoControlBenchControl.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.CatalogoControlBenchControl, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.CatalogoControlBenchControl, fields=fields, links=links, searchable=True, deletable=False, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        return dict(form=SQLFORM.grid(db.CatalogoControlBenchControl, fields=fields, searchable=True,deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def DetallePoliticaBenchControl():
    #db.CatalogoControl.id.readable = False
    db.DetallePoliticaBenchControl.AprobacionJefeRiesgo.writable=False
    db.DetallePoliticaBenchControl.AprobacionAnalistaRiesgo.writable=False
    db.DetallePoliticaBenchControl.LogJefeRiesgo.writable=False
    db.DetallePoliticaBenchControl.LogAnalistaRiesgo.writable=False
    Tabla = 'DetallePoliticaBenchControl'
    fields = (db.DetallePoliticaBenchControl.id, db.DetallePoliticaBenchControl.DetallePoliticaId, db.DetallePoliticaBenchControl.BenchControlId, db.DetallePoliticaBenchControl.Descripcion, db.DetallePoliticaBenchControl.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.DetallePoliticaBenchControl, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.DetallePoliticaBenchControl, fields=fields, links=links, searchable=True, deletable=False, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        return dict(form=SQLFORM.grid(db.DetallePoliticaBenchControl, fields=fields, searchable=True,deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def ClasificacionInformacion():
    db.ClasificacionInformacion.id.readable=False
    db.ClasificacionInformacion.AprobacionJefeRiesgo.writable=False
    db.ClasificacionInformacion.AprobacionAnalistaRiesgo.writable=False
    db.ClasificacionInformacion.LogJefeRiesgo.writable=False
    db.ClasificacionInformacion.LogAnalistaRiesgo.writable=False
    Tabla = 'ClasificacionInformacion'
    fields = (db.ClasificacionInformacion.Nombre, db.ClasificacionInformacion.Descripcion, db.ClasificacionInformacion.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.ClasificacionInformacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.ClasificacionInformacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=15, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query=db.ClasificacionInformacion.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=500))
    else:
        redirect(URL('default','index'))
'''
@auth.requires_login()
def CicloNegocio():
    #if versionGratuita==1:
    #    db.CicloNegocio.Nombre.writable = False
    db.CicloNegocio.id.readable = False
    db.CicloNegocio.AprobacionJefeRiesgo.writable=False
    db.CicloNegocio.AprobacionAnalistaRiesgo.writable=False
    db.CicloNegocio.LogJefeRiesgo.writable=False
    db.CicloNegocio.LogAnalistaRiesgo.writable=False
    Tabla = 'CicloNegocio'
    #fields = (db.CicloNegocio.Nombre, db.CicloNegocio.Descripcion, db.CicloNegocio.AprobacionAnalistaRiesgo, db.CicloNegocio.AprobacionJefeRiesgo)
    fields = (db.CicloNegocio.Nombre, db.CicloNegocio.Descripcion, db.CicloNegocio.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.CicloNegocio, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.CicloNegocio, fields=fields, links=links, searchable=True, deletable=False, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        return dict(form = SQLFORM.grid(db.CicloNegocio, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))
'''
@auth.requires_login()
def TipoProceso():
    #if versionGratuita==1:
    #    db.TipoProceso.Nombre.writable = False
    db.TipoProceso.id.readable = False
    db.TipoProceso.AprobacionJefeRiesgo.writable=False
    db.TipoProceso.AprobacionAnalistaRiesgo.writable=False
    db.TipoProceso.LogJefeRiesgo.writable=False
    db.TipoProceso.LogAnalistaRiesgo.writable=False
    Tabla = 'TipoProceso'
    #fields = (db.TipoProceso.Nombre, db.TipoProceso.Descripcion, db.TipoProceso.AprobacionAnalistaRiesgo, db.TipoProceso.AprobacionJefeRiesgo)
    fields = (db.TipoProceso.Nombre, db.TipoProceso.Descripcion, db.TipoProceso.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TipoProceso, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TipoProceso, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        return dict(form=SQLFORM.grid(db.TipoProceso, fields=fields, searchable=True, create=False, deletable=False, editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def Proceso():
    #db.Proceso.id.readable = False
    db.Proceso.AprobacionJefeRiesgo.writable=False
    db.Proceso.AprobacionAnalistaRiesgo.writable=False
    db.Proceso.LogJefeRiesgo.writable=False
    db.Proceso.LogAnalistaRiesgo.writable=False
    Tabla = 'Proceso'
    #fields = (db.Proceso.Nombre, db.Proceso.Descripcion, db.Proceso.Dueno, db.Proceso.TipoProcesoId, db.Proceso.RegionId, db.Proceso.AprobacionAnalistaRiesgo, db.Proceso.AprobacionJefeRiesgo)
    #fields = (db.Proceso.id, db.Proceso.Nombre, db.Proceso.CicloNegocioId, db.Proceso.MacroProcesoId, db.Proceso.TipoProcesoId, db.Proceso.Descripcion, db.Proceso.AprobacionJefeRiesgo)
    fields = (db.Proceso.id, db.Proceso.Nombre, db.Proceso.TipoProcesoId, db.Proceso.Descripcion, db.Proceso.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('Copy'),_class='button btn btn-warning',_href=URL("default","CopiarRegistro", args=[row.id, Tabla]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])) ]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.Proceso, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.Proceso, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = (db.Proceso.AprobacionJefeRiesgo=='T')
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def MacroProceso():
    #db.MacroProceso.id.readable = False
    db.MacroProceso.AprobacionJefeRiesgo.writable=False
    db.MacroProceso.AprobacionAnalistaRiesgo.writable=False
    db.MacroProceso.LogJefeRiesgo.writable=False
    db.MacroProceso.LogAnalistaRiesgo.writable=False
    Tabla = 'MacroProceso'
    fields = (db.MacroProceso.id, db.MacroProceso.Nombre, db.MacroProceso.Descripcion, db.MacroProceso.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('Copy'),_class='button btn btn-warning',_href=URL("default","CopiarRegistro", args=[row.id, Tabla]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('Copy'),_class='button btn btn-warning',_href=URL("default","CopiarRegistro", args=[row.id, Tabla]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('Copy'),_class='button btn btn-warning',_href=URL("default","CopiarRegistro", args=[row.id, Tabla]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.MacroProceso, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.MacroProceso, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = (db.MacroProceso.AprobacionJefeRiesgo=='T')
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def TipoDato():
    db.TipoDato.id.readable = False
    db.TipoDato.LogJefeRiesgo.writable = False
    db.TipoDato.LogAnalistaRiesgo.writable = False
    db.TipoDato.AprobacionJefeRiesgo.writable = False
    db.TipoDato.AprobacionAnalistaRiesgo.writable = False
    Tabla = 'TipoDato'
    fields = (db.TipoDato.Nombre, db.TipoDato.Descripcion, db.TipoDato.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
 
    #if auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.TipoDato, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.TipoDato, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    #elif auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='guest'):
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        form = SQLFORM.grid(db.TipoDato, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

#-------------------
# Ambiente Control
#-------------------
@auth.requires_login()
def AreaImpacto():
    db.AreaImpacto.id.readable = False
    db.AreaImpacto.LogAnalistaRiesgo.writable = False
    db.AreaImpacto.AprobacionAnalistaRiesgo.writable = False
    db.AreaImpacto.LogJefeRiesgo.writable = False
    db.AreaImpacto.AprobacionJefeRiesgo.writable = False
    #db.AreaImpacto.Valor.writable = False
    #db.AreaImpacto.Nombre.writable = False
    Tabla = 'AreaImpacto'
    #fields = (db.AreaImpacto.Nombre, db.AreaImpacto.CriterioImpactoId, db.AreaImpacto.Descripcion, db.AreaImpacto.AprobacionJefeRiesgo)
    fields = (db.AreaImpacto.Nombre, db.AreaImpacto.Descripcion, db.AreaImpacto.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
 
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AreaImpacto, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AreaImpacto, fields=fields, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.AreaImpacto.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def AreaProbabilidad():
    db.AreaProbabilidad.id.readable = False
    db.AreaProbabilidad.LogAnalistaRiesgo.writable = False
    db.AreaProbabilidad.AprobacionAnalistaRiesgo.writable = False
    db.AreaProbabilidad.LogJefeRiesgo.writable = False
    db.AreaProbabilidad.AprobacionJefeRiesgo.writable = False
    #db.AreaImpacto.Valor.writable = False
    #db.AreaImpacto.Nombre.writable = False
    Tabla = 'AreaProbabilidad'
    fields = (db.AreaProbabilidad.Nombre, db.AreaProbabilidad.Descripcion, db.AreaProbabilidad.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
 
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AreaProbabilidad, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AreaProbabilidad, fields=fields, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.AreaProbabilidad.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def AreaImpactoCriterioImpacto():
    db.AreaImpactoCriterioImpacto.LogAnalistaRiesgo.writable = False
    db.AreaImpactoCriterioImpacto.AprobacionAnalistaRiesgo.writable = False
    db.AreaImpactoCriterioImpacto.LogJefeRiesgo.writable = False
    db.AreaImpactoCriterioImpacto.AprobacionJefeRiesgo.writable = False
    Tabla = 'AreaImpactoCriterioImpacto'

    fields = (db.AreaImpactoCriterioImpacto.id, db.AreaImpactoCriterioImpacto.AreaImpactoId, db.AreaImpactoCriterioImpacto.CriterioImpactoId, db.AreaImpactoCriterioImpacto.Descripcion, db.AreaImpactoCriterioImpacto.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
 
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AreaImpactoCriterioImpacto, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AreaImpactoCriterioImpacto, fields=fields, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.AreaImpactoCriterioImpacto.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def AreaProbabilidadCriterioProbabilidad():
    db.AreaProbabilidadCriterioProbabilidad.LogAnalistaRiesgo.writable = False
    db.AreaProbabilidadCriterioProbabilidad.AprobacionAnalistaRiesgo.writable = False
    db.AreaProbabilidadCriterioProbabilidad.LogJefeRiesgo.writable = False
    db.AreaProbabilidadCriterioProbabilidad.AprobacionJefeRiesgo.writable = False
    Tabla = 'AreaProbabilidadCriterioProbabilidad'

    fields = (db.AreaProbabilidadCriterioProbabilidad.id, db.AreaProbabilidadCriterioProbabilidad.AreaProbabilidadId, db.AreaProbabilidadCriterioProbabilidad.CriterioProbabilidadId, db.AreaProbabilidadCriterioProbabilidad.Descripcion, db.AreaProbabilidadCriterioProbabilidad.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
 
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AreaProbabilidadCriterioProbabilidad, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AreaProbabilidadCriterioProbabilidad, fields=fields, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.AreaProbabilidadCriterioProbabilidad.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def TratamientoRiesgoAreaImpacto():
    #db.TratamientoRiesgoAreaImpacto.id.readable = False
    db.TratamientoRiesgoAreaImpacto.LogAnalistaRiesgo.writable = False
    db.TratamientoRiesgoAreaImpacto.AprobacionAnalistaRiesgo.writable = False
    db.TratamientoRiesgoAreaImpacto.LogJefeRiesgo.writable = False
    db.TratamientoRiesgoAreaImpacto.AprobacionJefeRiesgo.writable = False
    Tabla = 'TratamientoRiesgoAreaImpacto'
    fields = (db.TratamientoRiesgoAreaImpacto.id, db.TratamientoRiesgoAreaImpacto.TratamientoRiesgoId, db.TratamientoRiesgoAreaImpacto.AreaImpactoCriterioImpactoId, db.TratamientoRiesgoAreaImpacto.Descripcion, db.TratamientoRiesgoAreaImpacto.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
 
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TratamientoRiesgoAreaImpacto, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TratamientoRiesgoAreaImpacto, fields=fields, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.TratamientoRiesgoAreaImpacto.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def TratamientoRiesgoAreaProbabilidad():
    db.TratamientoRiesgoAreaProbabilidad.id.readable = False
    db.TratamientoRiesgoAreaProbabilidad.LogJefeRiesgo.writable = False
    db.TratamientoRiesgoAreaProbabilidad.AprobacionJefeRiesgo.writable = False
    Tabla = 'TratamientoRiesgoAreaProbabilidad'
    fields = (db.TratamientoRiesgoAreaProbabilidad.TratamientoRiesgoId, db.TratamientoRiesgoAreaProbabilidad.AreaProbabilidadCriterioProbabilidadId, db.TratamientoRiesgoAreaProbabilidad.Descripcion, db.TratamientoRiesgoAreaProbabilidad.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
 
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TratamientoRiesgoAreaProbabilidad, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.TratamientoRiesgoAreaProbabilidad, fields=fields, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500, links=links))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.TratamientoRiesgoAreaProbabilidad.AprobacionJefeRiesgo=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))


@auth.requires_login()
def AmbienteControl():
    db.AmbienteControl.id.readable = False
    db.AmbienteControl.LogJefeRiesgo.writable = False
    db.AmbienteControl.LogAnalistaRiesgo.writable = False
    db.AmbienteControl.AprobacionJefeRiesgo.writable = False
    db.AmbienteControl.AprobacionAnalistaRiesgo.writable = False
    Tabla="AmbienteControl"
    fields = (db.AmbienteControl.Nombre, db.AmbienteControl.DireccionId, db.AmbienteControl.Descripcion, db.AmbienteControl.NivelMadurezId, db.AmbienteControl.Evidencia, db.AmbienteControl.AprobacionJefeRiesgo)
    #LinkJefeRiesgo = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    #Links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    #LinkAnalistaRiesgo = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AmbienteControl, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=3, maxtextlength=250, links=Links, fields=fields))
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.AmbienteControl, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=3, maxtextlength=250, links=Links, fields=fields))
    elif auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        return dict(form=SQLFORM.grid(db.AmbienteControl, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=3, maxtextlength=250, fields=fields))
    else:
        redirect(URL('default','index'))

#-----------
#Politicas
#-----------
@auth.requires_login()
def RegulacionDato():
    db.RegulacionDato.id.readable = False
    db.RegulacionDato.AprobacionJefeRiesgo.writable=False
    db.RegulacionDato.AprobacionAnalistaRiesgo.writable=False
    db.RegulacionDato.LogJefeRiesgo.writable=False
    db.RegulacionDato.LogAnalistaRiesgo.writable=False
    Tabla = 'RegulacionDato'
    fields = (db.RegulacionDato.Nombre, db.RegulacionDato.Version, db.RegulacionDato.Descripcion, db.RegulacionDato.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.RegulacionDato, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.RegulacionDato, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        query=(db.RegulacionDato.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def ActivoInformacionRegulacion():
    db.ActivoInformacionRegulacion.id.readable = False
    db.ActivoInformacionRegulacion.AprobacionJefeRiesgo.writable=False
    db.ActivoInformacionRegulacion.AprobacionAnalistaRiesgo.writable=False
    db.ActivoInformacionRegulacion.LogJefeRiesgo.writable=False
    db.ActivoInformacionRegulacion.LogAnalistaRiesgo.writable=False
    Tabla = 'ActivoInformacionRegulacion'
    fields = (db.ActivoInformacionRegulacion.ActivoInformacionId, db.ActivoInformacionRegulacion.RegulacionDatoId, db.ActivoInformacionRegulacion.Descripcion, db.ActivoInformacionRegulacion.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoInformacionRegulacion, fields=fields, searchable=True, links=links, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoInformacionRegulacion, fields=fields, searchable=True, links=links, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        query=(db.ActivoInformacionRegulacion.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def RegulacionPolitica():
    db.RegulacionPolitica.id.readable = False
    db.RegulacionPolitica.AprobacionJefeRiesgo.writable=False
    db.RegulacionPolitica.AprobacionAnalistaRiesgo.writable=False
    db.RegulacionPolitica.LogJefeRiesgo.writable=False
    db.RegulacionPolitica.LogAnalistaRiesgo.writable=False
    Tabla = 'RegulacionPolitica'
    fields = (db.RegulacionPolitica.RegulacionId, db.RegulacionPolitica.DetallePoliticaId, db.RegulacionPolitica.Descripcion, db.RegulacionPolitica.AprobacionAnalistaRiesgo, db.RegulacionPolitica.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.RegulacionPolitica, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=2500)
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        query=(db.RegulacionPolitica.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def PoliticaVigente():
    Politica = db(db.RegionPolitica.AprobacionJefeRiesgo=='T').select(db.RegionPolitica.ALL)
    return dict(Politica=Politica)

@auth.requires_login()
def ProcesoTipoProceso():
    db.ProcesoTipoProceso.id.readable = False
    db.ProcesoTipoProceso.AprobacionJefeRiesgo.writable=False
    db.ProcesoTipoProceso.AprobacionAnalistaRiesgo.writable=False
    db.ProcesoTipoProceso.LogJefeRiesgo.writable=False
    db.ProcesoTipoProceso.LogAnalistaRiesgo.writable=False
    Tabla = 'ProcesoTipoProceso'
    fields = (db.ProcesoTipoProceso.ProcesoId, db.ProcesoTipoProceso.TipoProcesoId, db.ProcesoTipoProceso.Descripcion, db.ProcesoTipoProceso.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ProcesoTipoProceso, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=2500)
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        query=(db.ProcesoTipoProceso.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def ProcesoMacroProceso():
    db.ProcesoMacroProceso.id.readable = False
    db.ProcesoMacroProceso.AprobacionJefeRiesgo.writable=False
    db.ProcesoMacroProceso.AprobacionAnalistaRiesgo.writable=False
    db.ProcesoMacroProceso.LogJefeRiesgo.writable=False
    db.ProcesoMacroProceso.LogAnalistaRiesgo.writable=False
    Tabla = 'ProcesoMacroProceso'
    fields = (db.ProcesoMacroProceso.ProcesoId, db.ProcesoMacroProceso.MacroProcesoId, db.ProcesoMacroProceso.Descripcion, db.ProcesoMacroProceso.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ProcesoMacroProceso, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=2500)
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        query=(db.ProcesoMacroProceso.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)
'''
@auth.requires_login()
def ProcesoCicloNegocio():
    db.ProcesoCicloNegocio.id.readable = False
    db.ProcesoCicloNegocio.AprobacionJefeRiesgo.writable=False
    db.ProcesoCicloNegocio.AprobacionAnalistaRiesgo.writable=False
    db.ProcesoCicloNegocio.LogJefeRiesgo.writable=False
    db.ProcesoCicloNegocio.LogAnalistaRiesgo.writable=False
    Tabla = 'ProcesoCicloNegocio'
    fields = (db.ProcesoCicloNegocio.ProcesoId, db.ProcesoCicloNegocio.CicloNegocioId, db.ProcesoCicloNegocio.Descripcion, db.ProcesoCicloNegocio.AprobacionJefeRiesgo)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ProcesoCicloNegocio, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=2500)
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        query=(db.ProcesoCicloNegocio.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)
'''
'''
@auth.requires_login()
def ProcesoRegion():
    #db.ProcesoRegion.id.readable = False
    db.ProcesoRegion.AprobacionJefeRiesgo.writable=False
    db.ProcesoRegion.AprobacionAnalistaRiesgo.writable=False
    db.ProcesoRegion.LogJefeRiesgo.writable=False
    db.ProcesoRegion.LogAnalistaRiesgo.writable=False
    Tabla = 'ProcesoRegion'
    fields = (db.ProcesoRegion.id, db.ProcesoRegion.ProcesoId, db.ProcesoRegion.RegionId, db.ProcesoRegion.Descripcion, db.ProcesoRegion.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ProcesoRegion, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ProcesoRegion, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        query=(db.ProcesoRegion.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)
'''
@auth.requires_login()
def ProcesoActivoInformacion():
    db.ProcesoActivoInformacion.AprobacionJefeRiesgo.writable=False
    db.ProcesoActivoInformacion.AprobacionAnalistaRiesgo.writable=False
    db.ProcesoActivoInformacion.LogJefeRiesgo.writable=False
    db.ProcesoActivoInformacion.LogAnalistaRiesgo.writable=False
    Tabla = 'ProcesoActivoInformacion'
    fields = (db.ProcesoActivoInformacion.id, db.ProcesoActivoInformacion.ProcesoId, db.ProcesoActivoInformacion.ActivoInformacionId, db.ProcesoActivoInformacion.Descripcion, db.ProcesoActivoInformacion.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ProcesoActivoInformacion, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ProcesoActivoInformacion, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        query=(db.ProcesoActivoInformacion.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def ActivoTiRegion():
    #db.RegionPolitica.id.readable = False
    db.ActivoTiRegion.AprobacionJefeRiesgo.writable=False
    db.ActivoTiRegion.AprobacionAnalistaRiesgo.writable=False
    db.ActivoTiRegion.LogJefeRiesgo.writable=False
    db.ActivoTiRegion.LogAnalistaRiesgo.writable=False
    Tabla = 'ActivoTiRegion'
    fields = (db.ActivoTiRegion.id, db.ActivoTiRegion.ActivoTiId, db.ActivoTiRegion.RegionId, db.ActivoTiRegion.Descripcion, db.ActivoTiRegion.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoTiRegion, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=2500)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoTiRegion, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=False, user_signature=True, paginate=15, maxtextlength=2500)
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        query=(db.RegionPolitica.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def ProcesoPolitica():
    db.ProcesoPolitica.id.readable = False
    db.ProcesoPolitica.AprobacionJefeRiesgo.writable=False
    db.ProcesoPolitica.AprobacionAnalistaRiesgo.writable=False
    db.ProcesoPolitica.LogJefeRiesgo.writable=False
    db.ProcesoPolitica.LogAnalistaRiesgo.writable=False
    Tabla = 'ProcesoPolitica'
    fields = (db.ProcesoPolitica.ProcesoId, db.ProcesoPolitica.RegionPoliticaId, db.ProcesoPolitica.Descripcion, db.ProcesoPolitica.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ProcesoPolitica, searchable=True, fields=fields, links=links, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='guest') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst'):
        query=(db.ProcesoPolitica.AprobacionJefeRiesgo=='T')
        form = SQLFORM.grid(query=query, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

#-------------
#Seguridad TI
#-------------
'''
@auth.requires_login()
def GrupoMetrica():
    #db.GrupoMetrica.id.readable = False
    db.GrupoMetrica.LogJefeRiesgo.writable = False
    db.GrupoMetrica.LogAnalistaRiesgo.writable = False
    db.GrupoMetrica.AprobacionJefeRiesgo.writable = False
    db.GrupoMetrica.AprobacionAnalistaRiesgo.writable = False
    db.GrupoMetrica.Nombre.writable = False
    Tabla = 'GrupoMetrica'
    fields = (db.GrupoMetrica.id, db.GrupoMetrica.Nombre, db.GrupoMetrica.Descripcion, db.GrupoMetrica.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.GrupoMetrica, links=links, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.GrupoMetrica, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def Metrica():
    #db.Metrica.id.readable = False
    db.Metrica.LogJefeRiesgo.writable = False
    db.Metrica.LogAnalistaRiesgo.writable = False
    db.Metrica.AprobacionJefeRiesgo.writable = False
    db.Metrica.AprobacionAnalistaRiesgo.writable = False
    db.Metrica.Nombre.writable = False
    db.Metrica.Codigo.writable = False
    db.Metrica.GrupoMetricaId.writable = False

    Tabla = 'Metrica'
    fields = (db.Metrica.id, db.Metrica.GrupoMetricaId, db.Metrica.Nombre, db.Metrica.Descripcion, db.Metrica.Codigo, db.Metrica.AprobacionJefeRiesgo)
    #fields = (db.TipoVulnerabilidad.Nombre, db.TipoVulnerabilidad.Descripcion, db.TipoVulnerabilidad.AprobacionAnalistaAuditoria, db.TipoVulnerabilidad.AprobacionJefeAuditoria)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='riksAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.Metrica, links=links, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.Metrica, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def ValorMetrica():
    #db.ValorMetrica.id.readable = False
    db.ValorMetrica.LogJefeRiesgo.writable = False
    db.ValorMetrica.LogAnalistaRiesgo.writable = False
    db.ValorMetrica.AprobacionJefeRiesgo.writable = False
    db.ValorMetrica.AprobacionAnalistaRiesgo.writable = False
    db.ValorMetrica.MetricaId.writable = False
    db.ValorMetrica.Nombre.writable = False
    db.ValorMetrica.ValorMetrica.writable = False
    db.ValorMetrica.ValorNumerico.writable = False
    Tabla = 'ValorMetrica'
    fields = (db.ValorMetrica.id, db.ValorMetrica.MetricaId, db.ValorMetrica.Nombre, db.ValorMetrica.Descripcion, db.ValorMetrica.ValorMetrica, db.ValorMetrica.ValorNumerico, db.ValorMetrica.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ValorMetrica, links=links, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.ValorMetrica, searchable=True, fields=fields, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)
'''
@auth.requires_login()
def AlcanceRevision():
    db.AlcanceRevision.id.readable = False
    db.AlcanceRevision.LogJefeAuditoria.writable = False
    db.AlcanceRevision.LogAnalistaAuditoria.writable = False
    db.AlcanceRevision.AprobacionJefeAuditoria.writable = False
    db.AlcanceRevision.AprobacionAnalistaAuditoria.writable = False
    Tabla = 'AlcanceRevision'
    fields = (db.AlcanceRevision.Nombre, db.AlcanceRevision.Descripcion, db.AlcanceRevision.Fecha, db.AlcanceRevision.AprobacionJefeAuditoria)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    #if auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.AlcanceRevision, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.AlcanceRevision, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.AlcanceRevision, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def TipoCapaSistema():
    db.TipoCapaSistema.id.readable = False
    db.TipoCapaSistema.LogJefeRiesgo.writable = False
    db.TipoCapaSistema.LogAnalistaRiesgo.writable = False
    db.TipoCapaSistema.AprobacionJefeRiesgo.writable = False
    db.TipoCapaSistema.AprobacionAnalistaRiesgo.writable = False
    Tabla = 'TipoCapaSistema'
    fields = (db.TipoCapaSistema.Nombre, db.TipoCapaSistema.Descripcion, db.TipoCapaSistema.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.TipoCapaSistema, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.TipoCapaSistema, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.TipoCapaSistema, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def Plataforma():
    db.Plataforma.id.readable=False
    db.Plataforma.LogJefeAuditoria.writable = False
    db.Plataforma.LogAnalistaAuditoria.writable = False
    db.Plataforma.AprobacionJefeAuditoria.writable = False
    db.Plataforma.AprobacionAnalistaAuditoria.writable = False
    Tabla = 'Plataforma'
    fields = (db.Plataforma.Nombre, db.Plataforma.Descripcion, db.Plataforma.Archivo, db.Plataforma.Administrador, db.Plataforma.AprobacionAnalistaAuditoria, db.Plataforma.AprobacionJefeAuditoria)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.Plataforma, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.Plataforma, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    else:
        redirect(URL('default', 'index'))
    return dict(form=form)

'''
@auth.requires_login()
def CapaSistema():
    db.CapaSistema.id.readable=False
    if auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
        form = SQLFORM.grid(db.CapaSistema, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.CapaSistema, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    else:
        redirect(URL('default', 'index'))
    return dict(form=form)
'''

@auth.requires_login()
def ActivoTi():
    #db.ActivoTi.id.readable = False
    db.ActivoTi.LogAnalistaRiesgo.writable = False
    db.ActivoTi.LogJefeRiesgo.writable = False
    db.ActivoTi.AprobacionAnalistaRiesgo.writable = False
    db.ActivoTi.AprobacionJefeRiesgo.writable = False
    Tabla = 'ActivoTi'
    #fields = (db.ActivoTi.id, db.ActivoTi.Nombre, db.ActivoTi.TipoCapaSistemaId, db.ActivoTi.IpInterna, db.ActivoTi.IpPublica, db.ActivoTi.Fecha, db.ActivoTi.CvssConfidentiality, db.ActivoTi.CvssIntegrity, db.ActivoTi.CvssAvailability, db.ActivoTi.CvssJustificacion, db.ActivoTi.AprobacionJefeRiesgo)
    #fields = (db.ActivoTi.id, db.ActivoTi.Nombre, db.ActivoTi.TipoCapaSistemaId, db.ActivoTi.Fecha, db.ActivoTi.CvssConfidentiality, db.ActivoTi.CvssIntegrity, db.ActivoTi.CvssAvailability, db.ActivoTi.CvssJustificacion, db.ActivoTi.AprobacionJefeRiesgo)
    #fields = (db.ActivoTi.id, db.ActivoTi.Nombre, db.ActivoTi.TipoCapaSistemaId, db.ActivoTi.Fecha, db.ActivoTi.CvssConfidentiality, db.ActivoTi.CvssIntegrity, db.ActivoTi.CvssAvailability, db.ActivoTi.AprobacionJefeRiesgo)
    fields = (db.ActivoTi.id, db.ActivoTi.Nombre, db.ActivoTi.TipoCapaSistemaId, db.ActivoTi.Fecha, db.ActivoTi.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssImpacto", args=[row.id, row.CvssConfidentiality, row.CvssIntegrity, row.CvssAvailability,  base64.b64encode(str(row.CvssJustificacion))]))]
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))])) ]
    else:
        #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssEvaluation", args=[row.id ]))]
        #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssImpacto", args=[row.id, row.CvssConfidentiality, row.CvssIntegrity, row.CvssAvailability,  base64.b64encode(str(row.CvssJustificacion) )] ))]
        #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssImpacto", args=[row.id, row.CvssConfidentiality, row.CvssIntegrity, row.CvssAvailability ] ))]
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoTi, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=200)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoTi, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=200)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.ActivoTi, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=200)
    elif auth.has_membership(role='ItAdministrator'):
        ActivoTi=[]
        for a in db(db.ActivoTi.AprobacionJefeRiesgo=='T').select(db.ActivoTi.id, db.ActivoTi.AdministradorInterno):
            try:
                for b in str(str(a.AdministradorInterno).replace(' ','')).split(','):
                    if b==auth.user.username:
                        ActivoTi.append(int(a.id))
            except:
                pass
        query = db.ActivoTi.id.belongs(ActivoTi)

        #query = (db.ActivoTi.AdministradoInterno.contains(auth.user.username, all=True))
        form = SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=15, maxtextlength=200)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def TipoCumplimiento():
    #Max 5 regitros
    TotalTipoCumplimiento=db().select(db.TipoCumplimiento.id, limitby=(0,5), orderby=db.TipoCumplimiento.id).last().id
    db(db.TipoCumplimiento.id>TotalTipoCumplimiento).delete()
    #--------------------------------------------------------------------------------
    db.TipoCumplimiento.id.readable=False
    db.TipoCumplimiento.LogAnalistaAuditoria.writable = False
    db.TipoCumplimiento.LogJefeAuditoria.writable = False
    db.TipoCumplimiento.AprobacionAnalistaAuditoria.writable = False
    db.TipoCumplimiento.AprobacionJefeAuditoria.writable = False
    Tabla = 'TipoCumplimiento'
    #fields = (db.TipoCumplimiento.Nombre, db.TipoCumplimiento.Descripcion, db.TipoCumplimiento.Color, db.TipoCumplimiento.AprobacionAnalistaAuditoria, db.TipoCumplimiento.AprobacionJefeAuditoria)
    fields = (db.TipoCumplimiento.Nombre, db.TipoCumplimiento.Descripcion, db.TipoCumplimiento.AprobacionJefeAuditoria)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.TipoCumplimiento, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.TipoCumplimiento, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    else:
        redirect(URL('default', 'index'))
    return dict(form=form)

@auth.requires_login()
def SeguridadTi():
    #db.SeguridadTi.id.readable = False
    db.SeguridadTi.LogAnalistaAuditoria.writable = False
    db.SeguridadTi.LogJefeAuditoria.writable = False
    db.SeguridadTi.LogResponsableControl.writable = False
    db.SeguridadTi.AprobacionAnalistaAuditoria.writable = False
    db.SeguridadTi.AprobacionJefeAuditoria.writable = False
    db.SeguridadTi.AprobacionResponsableControl.writable = False
    Tabla = 'SeguridadTi'
    #fields = (db.SeguridadTi.id, db.SeguridadTi.ActivoTiId, db.SeguridadTi.DetallePoliticaId, db.SeguridadTi.EscenarioRiesgo, db.SeguridadTi.Recomendacion, db.SeguridadTi.EfectividadControl, db.SeguridadTi.AprobacionResponsableControl, db.SeguridadTi.AprobacionAnalistaAuditoria, db.SeguridadTi.AprobacionJefeAuditoria)
    #fields = (db.SeguridadTi.id, db.SeguridadTi.ActivoTiId, db.SeguridadTi.DetallePoliticaId, db.SeguridadTi.EscenarioRiesgo, db.SeguridadTi.Recomendacion, db.SeguridadTi.AprobacionAnalistaAuditoria, db.SeguridadTi.AprobacionJefeAuditoria)
    fields = (db.SeguridadTi.id, db.SeguridadTi.ActivoTiId, db.SeguridadTi.DetallePoliticaId, db.SeguridadTi.EscenarioRiesgo, db.SeguridadTi.EvidenciaCumplimiento, db.SeguridadTi.Recomendacion, db.SeguridadTi.Cumplimiento, db.SeguridadTi.EfectividadControl, db.SeguridadTi.AprobacionJefeAuditoria)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssEvaluation", args=[row.id, Tabla, "2"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssEvaluation", args=[row.id, Tabla, "2"]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('CVSS'),_class='button btn btn-info',_href=URL("default","CvssEvaluation", args=[row.id, Tabla, "2"]))]
        
    if auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.SeguridadTi, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=5, maxtextlength=250)
    elif auth.has_membership(role='controlResp'):
        ActualizaAprobacion(Tabla)
        controlId=[]
        for a in db(db.SeguridadTi.AprobacionJefeAuditoria=='T').select(db.SeguridadTi.id, db.SeguridadTi.ResponsableControl):
            try:
                for b in str(str(a.ResponsableControl).replace(' ','')).split(','):
                    if b==auth.user.username:
                        controlId.append(int(a.id))
            except:
                pass
        #query = (db.SeguridadTi.id==0)
        #for i in controlId:
        #    query = (db.SeguridadTi.id==i) | query
        query = db.SeguridadTi.id.belongs(controlId)
        #query = (query) & ( (db.AnalisisRiesgo.AprobacionResponsableControl=='F') & (db.AnalisisRiesgo.AprobacionJefeRiesgo=='F') )
        db.SeguridadTi.ActivoTiId.writable=False
        db.SeguridadTi.DetallePoliticaId.writable=False
        db.SeguridadTi.ServicioActivoTi.writable=False
        db.SeguridadTi.EscenarioRiesgo.writable=False
        db.SeguridadTi.TipoVulnerabilidadId.writable=False
        db.SeguridadTi.AnalisisRiesgoId.writable=False
        db.SeguridadTi.TipoCumplimientoId.writable=False
        db.SeguridadTi.EvidenciaCumplimiento.writable=False
        db.SeguridadTi.Recomendacion.writable=False
        db.SeguridadTi.FechaRevision.writable=False
        db.SeguridadTi.ResponsableControl.writable=False
    #db.SeguridadTi.TipoTratamientoRiesgoId.writable=False
        db.SeguridadTi.EfectividadControl.writable=False
        db.SeguridadTi.NivelMadurezId.writable=False
        #db.SeguridadTi.Visible.writable=False
        form=SQLFORM.grid(query=query, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=5, maxtextlength=250)
    elif auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.SeguridadTi, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=5, maxtextlength=250)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def ActivoTiPlataforma():
    db.ActivoTiPlataforma.id.readable = False
    db.ActivoTiPlataforma.AprobacionJefeRiesgo.writable=False
    db.ActivoTiPlataforma.AprobacionAnalistaRiesgo.writable=False
    db.ActivoTiPlataforma.LogJefeRiesgo.writable=False
    db.ActivoTiPlataforma.LogAnalistaRiesgo.writable=False
    Tabla = 'ActivoTiPlataforma'
    fields = (db.ActivoTiPlataforma.ActivoTiId, db.ActivoTiPlataforma.PlataformaId, db.ActivoTiPlataforma.Descripcion, db.ActivoTiPlataforma.AprobacionAnalistaRiesgo, db.ActivoTiPlataforma.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoTiPlataforma, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.ActivoTiPlataforma, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def ActivoTiProceso():
    #db.ActivoTiProceso.id.readable = False
    db.ActivoTiProceso.AprobacionJefeRiesgo.writable=False
    db.ActivoTiProceso.AprobacionAnalistaRiesgo.writable=False
    db.ActivoTiProceso.LogJefeRiesgo.writable=False
    db.ActivoTiProceso.LogAnalistaRiesgo.writable=False
    Tabla = 'ActivoTiProceso'
    fields = (db.ActivoTiProceso.id, db.ActivoTiProceso.ActivoTiId, db.ActivoTiProceso.ProcesoId, db.ActivoTiProceso.Descripcion, db.ActivoTiProceso.AprobacionJefeRiesgo)
    #links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoTiProceso, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoTiProceso, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.ActivoTiProceso, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def ActivoTiActivoInformacion():
    #db.ActivoTiActivoInformacion.id.readable = False
    db.ActivoTiActivoInformacion.AprobacionJefeRiesgo.writable=False
    db.ActivoTiActivoInformacion.AprobacionAnalistaRiesgo.writable=False
    db.ActivoTiActivoInformacion.LogJefeRiesgo.writable=False
    db.ActivoTiActivoInformacion.LogAnalistaRiesgo.writable=False
    Tabla = 'ActivoTiActivoInformacion'
    fields = (db.ActivoTiActivoInformacion.id, db.ActivoTiActivoInformacion.ActivoTiId, db.ActivoTiActivoInformacion.ActivoInformacionId, db.ActivoTiActivoInformacion.Descripcion, db.ActivoTiActivoInformacion.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    if auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoTiActivoInformacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ActivoTiActivoInformacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.ActivoTiActivoInformacion, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

#---------------------------------------------------------------------------
#Se definen las metricas base, temporal y ambiental
#Las metricas ese cargan automaticamente cuando se crea una nueva instancia
#---------------------------------------------------------------------------
@auth.requires_login()
def GrupoMetrica():
    #db.GrupoMetrica.id.readable = False
    db.GrupoMetrica.LogJefeRiesgo.writable = False
    db.GrupoMetrica.LogAnalistaRiesgo.writable = False
    db.GrupoMetrica.AprobacionJefeRiesgo.writable = False
    db.GrupoMetrica.AprobacionAnalistaRiesgo.writable = False
    db.GrupoMetrica.Nombre.writable = False
    Tabla = 'GrupoMetrica'
    fields = (db.GrupoMetrica.id, db.GrupoMetrica.Nombre, db.GrupoMetrica.Descripcion, db.GrupoMetrica.AprobacionJefeRiesgo)
    #----------------------------------------------------------
    #Se usa if para obtener los queries/parametros de busqueda
    #y despues de ejecutar el proceso el usuario visualice los
    #mismos registros
    #----------------------------------------------------------
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        #-------------------------------------------------------
        #Se llama a la funcion ActualizaAprobacion para que 
        #se solicite nuevamente autorizacion en caso de edicion
        #-------------------------------------------------------
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.GrupoMetrica, links=links, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.GrupoMetrica, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

#------------------------------------------------------
#Catalogo para definir el detalle de las metricas CVSS
#------------------------------------------------------
@auth.requires_login()
def Metrica():
    #db.Metrica.id.readable = False
    db.Metrica.LogJefeRiesgo.writable = False
    db.Metrica.LogAnalistaRiesgo.writable = False
    db.Metrica.AprobacionJefeRiesgo.writable = False
    db.Metrica.AprobacionAnalistaRiesgo.writable = False
    db.Metrica.Nombre.writable = False
    db.Metrica.Codigo.writable = False
    db.Metrica.GrupoMetricaId.writable = False
    Tabla = 'Metrica'
    fields = (db.Metrica.id, db.Metrica.GrupoMetricaId, db.Metrica.Nombre, db.Metrica.Descripcion, db.Metrica.Codigo, db.Metrica.AprobacionJefeRiesgo)
    #----------------------------------------------------------
    #Se usa if para obtener los queries/parametros de busqueda
    #y despues de ejecutar el proceso el usuario visualice los
    #mismos registros
    #----------------------------------------------------------
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='riksAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        #-------------------------------------------------------
        #Se llama a la funcion ActualizaAprobacion para que 
        #se solicite nuevamente autorizacion en caso de edicion
        #-------------------------------------------------------
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.Metrica, links=links, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.Metrica, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

#------------------------------------------------------------------
#Catalogo para asignar valores numericos de las metricas definidas
#------------------------------------------------------------------
@auth.requires_login()
def ValorMetrica():
    #db.ValorMetrica.id.readable = False
    db.ValorMetrica.LogJefeRiesgo.writable = False
    db.ValorMetrica.LogAnalistaRiesgo.writable = False
    db.ValorMetrica.AprobacionJefeRiesgo.writable = False
    db.ValorMetrica.AprobacionAnalistaRiesgo.writable = False
    db.ValorMetrica.MetricaId.writable = False
    db.ValorMetrica.Nombre.writable = False
    db.ValorMetrica.ValorMetrica.writable = False
    db.ValorMetrica.ValorNumerico.writable = False
    Tabla = 'ValorMetrica'
    fields = (db.ValorMetrica.id, db.ValorMetrica.MetricaId, db.ValorMetrica.Nombre, db.ValorMetrica.Descripcion, db.ValorMetrica.ValorMetrica, db.ValorMetrica.ValorNumerico, db.ValorMetrica.AprobacionJefeRiesgo)
    #----------------------------------------------------------
    #Se usa if para obtener los queries/parametros de busqueda
    #y despues de ejecutar el proceso el usuario visualice los
    #mismos registros
    #----------------------------------------------------------
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        #-------------------------------------------------------
        #Se llama a la funcion ActualizaAprobacion para que 
        #se solicite nuevamente autorizacion en caso de edicion
        #-------------------------------------------------------
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ValorMetrica, links=links, fields=fields, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.ValorMetrica, searchable=True, fields=fields, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

#-----------------------------------------------------------------
#Se evaluan los factores de riesgo de acuerdo a las metricas CVSS
#-----------------------------------------------------------------
@auth.requires_login()
def ValorMetricaSeguridadTi():
    db.ValorMetricaSeguridadTi.LogAnalistaRiesgo.writable = False
    db.ValorMetricaSeguridadTi.LogJefeRiesgo.writable = False
    db.ValorMetricaSeguridadTi.LogResponsableControl.writable = False
    db.ValorMetricaSeguridadTi.AprobacionAnalistaRiesgo.writable = False
    db.ValorMetricaSeguridadTi.AprobacionJefeRiesgo.writable = False
    db.ValorMetricaSeguridadTi.AprobacionResponsableControl.writable = False
    Tabla = 'ValorMetricaSeguridadTi'
    fields = (db.ValorMetricaSeguridadTi.id, db.ValorMetricaSeguridadTi.TratamientoRiesgoId, db.ValorMetricaSeguridadTi.ValorMetricaId, db.ValorMetricaSeguridadTi.Descripcion, db.ValorMetricaSeguridadTi.AprobacionJefeRiesgo)
    #----------------------------------------------------------
    #Se usa if para obtener los queries/parametros de busqueda
    #y despues de ejecutar el proceso el usuario visualice los
    #mismos registros
    #----------------------------------------------------------
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        #-------------------------------------------------------
        #Se llama a la funcion ActualizaAprobacion para que 
        #se solicite nuevamente autorizacion en caso de edicion
        #-------------------------------------------------------
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ValorMetricaSeguridadTi, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.ValorMetrizaSeguridadTi, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

@auth.requires_login()
def ControlCvss():
    db.ControlCvss.LogAnalistaRiesgo.writable = False
    db.ControlCvss.LogJefeRiesgo.writable = False
    db.ControlCvss.AprobacionAnalistaRiesgo.writable = False
    db.ControlCvss.AprobacionJefeRiesgo.writable = False
    Tabla = 'ControlCvss'
    fields = (db.ControlCvss.id, db.ControlCvss.EvaluacionControlId, db.ControlCvss.ValorMetricaId, db.ControlCvss.Descripcion, db.ControlCvss.AprobacionJefeRiesgo)
    #----------------------------------------------------------
    #Se usa if para obtener los queries/parametros de busqueda
    #y despues de ejecutar el proceso el usuario visualice los
    #mismos registros
    #----------------------------------------------------------
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'):
        #-------------------------------------------------------
        #Se llama a la funcion ActualizaAprobacion para que 
        #se solicite nuevamente autorizacion en caso de edicion
        #-------------------------------------------------------
        ActualizaAprobacion(Tabla)
        form = SQLFORM.grid(db.ControlCvss, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='guest'):
        form = SQLFORM.grid(db.ControlCvss, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
    else:
        redirect(URL('default','index'))
    return dict(form=form)

#------------------------------------------------------------------------------------
#Esta funcion se utiliza para medir el impacto en base al sistema o activo de TI 
#Actualiza todos los registros de ValorMetricaSeguridadTi en base al sistema evaluado
#------------------------------------------------------------------------------------
@auth.requires_login()
#@auth.requires(auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin'))
def CvssImpacto():
    TratamientoRiesgoId = db(db.TratamientoRiesgo.ActivoTiId==request.args(0)).select(db.TratamientoRiesgo.id)
    for i in TratamientoRiesgoId:
        db.ValorMetricaSeguridadTi.update_or_insert(( (db.ValorMetricaSeguridadTi.TratamientoRiesgoId==i) & ((db.ValorMetricaSeguridadTi.ValorMetricaId==14 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==15 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==16 ))), TratamientoRiesgoId=i, ValorMetricaId=request.args(1), Descripcion=base64.b64decode(request.args(4)) )
    for i in TratamientoRiesgoId:
        db.ValorMetricaSeguridadTi.update_or_insert(( (db.ValorMetricaSeguridadTi.TratamientoRiesgoId==i) & ((db.ValorMetricaSeguridadTi.ValorMetricaId==17 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==18 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==19 ))), TratamientoRiesgoId=i, ValorMetricaId=request.args(2), Descripcion=base64.b64decode(request.args(4)) )
    for i in TratamientoRiesgoId:
        db.ValorMetricaSeguridadTi.update_or_insert(( (db.ValorMetricaSeguridadTi.TratamientoRiesgoId==i) & ((db.ValorMetricaSeguridadTi.ValorMetricaId==20 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==21 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==22 ))), TratamientoRiesgoId=i, ValorMetricaId=request.args(3), Descripcion=base64.b64decode(request.args(4)) )
    redirect(URL('default','ActivoTi'))

#--------------------------------------------------------
#Son las formulas CVSS 3.1 de acuerdo a la documentacion
#--------------------------------------------------------
'''
@auth.requires_login()
@auth.requires( auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin') )
def CvssEvaluation():
    if request.args(3):
        parametros = base64.b64decode(request.args(3))
    else:
        pass
    #----------------------------------------------------------------------------------------------
    #Se definen los valores minimos, en caso que no se evalue en el modulo ValorMetricaSeguridadTi
    #Por lo que si se evalua con estos valores, el resultado es 0, solo se evaluan metricas Base
    #----------------------------------------------------------------------------------------------

    #------------------------
    #Variables Iniciales Base
    #------------------------
    cvssBaseAV=0.2 #Physical
    cvssBaseAVString="P"
    cvssBaseAC=0.44 #High
    cvssBaseACString="H"
    cvssBasePR=0.27 #High
    cvssBasePRString="H"
    cvssBaseUI=0.62 #Required
    cvssBaseUIString="R"
    cvssBaseS =6.42 #Unhanged
    cvssBaseSString="U"
    cvssBaseC =0 #None
    cvssBaseCString="N"
    cvssBaseI =0 #None
    cvssBaseIString="N"
    cvssBaseA =0 #None
    cvssBaseAString="N"
    changed=0
    #------------------------------
    #Variables Iniciales Temporales
    #------------------------------
    cvssTempE  = 1 #Not Defined
    cvssTempEString  = "X"
    cvssTempRL = 1 #Not Defined
    cvssTempRLString = "X"
    cvssTempRC = 1 #Not Defined
    cvssTempRCString = "X"
    #--------------------------------
    #Variables Iniciales Ambientales
    #--------------------------------
    cvssEnvCR  = 1 #Not Defined
    cvssEnvCRString  = "X"
    cvssEnvIR  = 1 #Not Defined
    cvssEnvIRString  = "X"
    cvssEnvAR  = 1 #Not Defined
    cvssEnvARString  = "X"
    cvssEnvMAV = 1 #Physical
    cvssEnvMAVString = "P"
    cvssEnvMAC = 1 #High
    cvssEnvMACString = "H"
    cvssEnvMPR = 1 #High
    cvssEnvMPRString = "H"
    cvssEnvMUI = 1 #Required
    cvssEnvMUIString = "R"
    cvssEnvMS  = 1 #Unchanged
    cvssEnvMSString = "U"
    cvssEnvMC  = 0 #None
    cvssEnvMCString  = "N"
    cvssEnvMI  = 0 #None
    cvssEnvMIString  = "N"
    cvssEnvMA  = 0 #None
    cvssEnvMAString  = "N"
    changedE=0
    #---------------------------------------------
    #request.args(0) es el ID del factor de riesgo
    #---------------------------------------------
    cvss = db(db.ValorMetricaSeguridadTi.TratamientoRiesgoId==request.args(0)).select(db.ValorMetricaSeguridadTi.ALL)
    for s in cvss:
        #-----------------------------------------------------------------------
        #El grupo metrica 5 corresponde a "Base Metric Group | S | Scope (S)"
        #Los valores que se pueden tomar son 12 Changed(C), 13 Unchanged(U)
        #-----------------------------------------------------------------------
        if s.ValorMetricaId.MetricaId == 5:
            #--------------
            #12 Changed (C)
            #--------------
            if s.ValorMetricaId == 12:
                changed = 1
            #----------------
            #13 Unchanged (U)
            #----------------
            elif s.ValorMetricaId == 13:
                changed = 0
        #------------------------------------------------------------------------------------------
        #El grupo metrica 19 corresponde a "Environmental Metric Group | MS | Modified Scope (MS)"
        #Los valores son 64 Not Defined (X), 65 Modified Changed (C), 66 Modified Unchanged (U)	
        #------------------------------------------------------------------------------------------
        if s.ValorMetricaId.MetricaId == 19:
            #--------------
            #65 Changed (C)
            #--------------
            if s.ValorMetricaId == 65:
                changedE = 1
            #----------------
            #66 Unchanged (U)
            #----------------
            elif s.ValorMetricaId == 66:
                changedE = 0
        #for i in cvss:
        #------------------------------------------------
        #1 | Base Metric Group | AV | Attack Vector (AV)
        #------------------------------------------------
        if s.ValorMetricaId.MetricaId == 1:
            cvssBaseAV = s.ValorMetricaId.ValorNumerico
            cvssBaseAVString = s.ValorMetricaId.ValorMetrica
        #---------------------------------------------------
        #2 | Base Metric Group | AC | Attack Complexity (AC)
        #---------------------------------------------------
        if s.ValorMetricaId.MetricaId == 2:
            cvssBaseAC = s.ValorMetricaId.ValorNumerico
            cvssBaseACString = s.ValorMetricaId.ValorMetrica
        #-----------------------------------------------------
        #3 | Base Metric Group | PR | Privileges Required (PR)
        #-----------------------------------------------------
        if s.ValorMetricaId.MetricaId == 3 and changed == 0:
            cvssBasePR = s.ValorMetricaId.ValorNumerico
            cvssBasePRString = s.ValorMetricaId.ValorMetrica
        elif s.ValorMetricaId.MetricaId==3 and changed==1 and s.ValorMetricaId==7: #Changed (C) & PR High (H)
            cvssBasePR=0.5
            cvssBasePRString = s.ValorMetricaId.ValorMetrica
        elif s.ValorMetricaId.MetricaId==3 and changed==1 and s.ValorMetricaId==8: #Changed (C) & PR Low (L)
            cvssBasePR=0.68
            cvssBasePRString = s.ValorMetricaId.ValorMetrica
        #--------------------------------------------------
        #4 | Base Metric Group | UI | User Interaction (UI)
        #--------------------------------------------------
        if s.ValorMetricaId.MetricaId == 4:
            cvssBaseUI = s.ValorMetricaId.ValorNumerico
            cvssBaseUIString = s.ValorMetricaId.ValorMetrica
        #--------------------------------------
        #5 | Base Metric Group | S | Scope (S)
        #--------------------------------------
        if s.ValorMetricaId.MetricaId == 5:
            cvssBaseS = s.ValorMetricaId.ValorNumerico
            cvssBaseSString = s.ValorMetricaId.ValorMetrica
        #-------------------------------------------
        #6 | Base Metric Group | C | Confidentiality
        #-------------------------------------------
        if s.ValorMetricaId.MetricaId == 6:
            cvssBaseC = s.ValorMetricaId.ValorNumerico
            cvssBaseCString = s.ValorMetricaId.ValorMetrica
        #-----------------------------------------
        #7 | Base Metric Group | I | Integrity (I)
        #-----------------------------------------
        if s.ValorMetricaId.MetricaId == 7:
            cvssBaseI = s.ValorMetricaId.ValorNumerico
            cvssBaseIString = s.ValorMetricaId.ValorMetrica
        #--------------------------------------------
        #8 | Base Metric Group | A | Availability (A)
        #--------------------------------------------
        if s.ValorMetricaId.MetricaId == 8:
            cvssBaseA = s.ValorMetricaId.ValorNumerico
            cvssBaseAString = s.ValorMetricaId.ValorMetrica
        #--------------------
        #Metricas temporales
        #--------------------
        if s.ValorMetricaId.MetricaId == 9:
            cvssTempE = s.ValorMetricaId.ValorNumerico
            cvssTempEString = s.ValorMetricaId.ValorMetrica
        if s.ValorMetricaId.MetricaId == 10:
            cvssTempRL = s.ValorMetricaId.ValorNumerico
            cvssTempRLString = s.ValorMetricaId.ValorMetrica
        if s.ValorMetricaId.MetricaId == 11:
            cvssTempRC = s.ValorMetricaId.ValorNumerico
            cvssTempRCString = s.ValorMetricaId.ValorMetrica
        #---------------------
        #Metricas ambientales
        #---------------------
        if s.ValorMetricaId.MetricaId == 12:
            cvssEnvCR = s.ValorMetricaId.ValorNumerico
            cvssEnvCRString = s.ValorMetricaId.ValorMetrica
        if s.ValorMetricaId.MetricaId == 13:
            cvssEnvIR = s.ValorMetricaId.ValorNumerico
            cvssEnvIRString = s.ValorMetricaId.ValorMetrica
        if s.ValorMetricaId.MetricaId == 14:
            cvssEnvAR = s.ValorMetricaId.ValorNumerico
            cvssEnvARString = s.ValorMetricaId.ValorMetrica
        if s.ValorMetricaId.MetricaId == 15:
            cvssEnvMAV = s.ValorMetricaId.ValorNumerico
            cvssEnvMAVString = s.ValorMetricaId.ValorMetrica
        if s.ValorMetricaId.MetricaId == 16:
            cvssEnvMAC = s.ValorMetricaId.ValorNumerico
            cvssEnvMACString = s.ValorMetricaId.ValorMetrica
        #---------------------
        #Si no cambio el scope
        #---------------------
        if s.ValorMetricaId.MetricaId == 17 and changedE == 0:
            cvssEnvMPR = s.ValorMetricaId.ValorNumerico
            cvssEnvMPRString = s.ValorMetricaId.ValorMetrica
        #----------------------------------------------
        #Si cambio se asigna de acuerdo a su criticidad
        #----------------------------------------------
        elif s.ValorMetricaId.MetricaId == 17 and changedE == 1 and s.ValorMetricaId == 58: #Changed (C) & PR High (H)
            cvssEnvMPR=0.5
            cvssEnvMPRString = s.ValorMetricaId.ValorMetrica
        elif s.ValorMetricaId.MetricaId == 17 and changedE == 1 and s.ValorMetricaId == 59: #Changed (C) & PR Low (L)
            cvssEnvMPR=0.68
            cvssEnvMPRString = s.ValorMetricaId.ValorMetrica
        #-------------------------------
        #Modified User Interaction (MUI)
        #-------------------------------
        if s.ValorMetricaId.MetricaId == 18:
            cvssEnvMUI = s.ValorMetricaId.ValorNumerico
            cvssEnvMUIString = s.ValorMetricaId.ValorMetrica
        #-------------------
        #Modified Scope (MS)
        #-------------------
        if s.ValorMetricaId.MetricaId == 19:
            cvssEnvMS = s.ValorMetricaId.ValorNumerico
            cvssEnvMSString = s.ValorMetricaId.ValorMetrica
        #-------------------------------
        #Modified Confidentiality (MC)
        #-------------------------------
        if s.ValorMetricaId.MetricaId == 20:
            cvssEnvMC = s.ValorMetricaId.ValorNumerico
            cvssEnvMCString = s.ValorMetricaId.ValorMetrica
        #-----------------------
        #Modified Integrity (MI)
        #-----------------------
        if s.ValorMetricaId.MetricaId == 21:
            cvssEnvMI = s.ValorMetricaId.ValorNumerico
            cvssEnvMIString = s.ValorMetricaId.ValorMetrica
        #---------------------------
        #Modified Availability (MA)
        #---------------------------
        if s.ValorMetricaId.MetricaId == 22:
            cvssEnvMA = s.ValorMetricaId.ValorNumerico
            cvssEnvMAString = s.ValorMetricaId.ValorMetrica

    #---------------------
    #Calculo metrica BASE
    #---------------------
    ISS = 1-( (1-cvssBaseC) * (1-cvssBaseI) * (1-cvssBaseA) )
    Impact = ( ((7.52) * (ISS - 0.029)) - ( (3.25) * (math.pow((ISS - 0.02), 15))) )
    for i in cvss:
        if i.ValorMetricaId==13: #Unchanged (U)
            Impact = (6.42) * (ISS)
        elif i.ValorMetricaId==12:
            Impact = ( ((7.52) * (ISS - 0.029)) - ( (3.25) * (math.pow((ISS - 0.02), 15))) )
    Exploitability = (8.22) * (cvssBaseAV) * (cvssBaseAC) * (cvssBasePR) * (cvssBaseUI)
    BaseScore = roundup( min( 1.08*(Impact + Exploitability)  , 10) )
    if Impact <=0:
        BaseScore=0
    for i in cvss:
        if i.ValorMetricaId==13: #Unchanged (U)
            BaseScore = roundup( min( Impact + Exploitability  , 10) )
        elif i.ValorMetricaId==12:
            BaseScore = roundup( min( (1.08) * (Impact + Exploitability)  , 10) )
    #-----------------------------------------------------
    #Calculo metrica TEMPORAL (En proceso de desarrollo)
    #-----------------------------------------------------
    if BaseScore<=0:
        TempScore = 0
    else:
        TempScore = roundup(BaseScore * D(cvssTempE) * D(cvssTempRL) * D(cvssTempRC) )
    #----------------------------------------------------
    #Calculo metrica AMBIENTAL (En proceso de desarrollo)
    #----------------------------------------------------
    ISCM = min(1-((1-cvssEnvCR * cvssEnvMC) * (1-cvssEnvIR * cvssEnvMI) * (1-cvssEnvAR * cvssEnvMA)), 0.915 ) 
    ImpactM = 0
    if changedE==1:
        ImpactM = ( (7.52) * (ISCM - 0.029) -  3.25 * (math.pow( ISCM * 0.9731 - 0.02, 13)) )
    elif changedE==0:
        ImpactM = (6.42) * (ISCM)

    ExploitabilityM = (8.22) * (cvssEnvMAV) * (cvssEnvMAC) * (cvssEnvMPR) * (cvssEnvMUI)
    BaseScoreM = roundup(roundup( min( 1.08*(ImpactM + ExploitabilityM)  , 10) ) * D(cvssTempE) * D(cvssTempRL) * D(cvssTempRC))
    if ImpactM <= 0:
        BaseScoreM = 0
    for i in cvss:
        if i.ValorMetricaId==66: #Unchanged (U)
            BaseScoreM = roundup(roundup( min( ImpactM + ExploitabilityM  , 10) ) * D(cvssTempE) * D(cvssTempRL) * D(cvssTempRC))
        elif i.ValorMetricaId==65:
            BaseScoreM = roundup(roundup( min( 1.08*(ImpactM + ExploitabilityM)  , 10) ) * D(cvssTempE) * D(cvssTempRL) * D(cvssTempRC))
    #-----------------------
    #Definicion de vectores
    #-----------------------
    VectorString = "CVSS:3.1/AV:"+str(cvssBaseAVString)+"/AC:"+str(cvssBaseACString)+"/PR:"+str(cvssBasePRString)+"/UI:"+str(cvssBaseUIString)+"/S:"+str(cvssBaseSString)+"/C:"+str(cvssBaseCString)+"/I:"+str(cvssBaseIString)+"/A:"+str(cvssBaseAString)
    VectorStringE = "CVSS:3.1/AV:"+str(cvssBaseAVString)+"/AC:"+str(cvssBaseACString)+"/PR:"+str(cvssBasePRString)+"/UI:"+str(cvssBaseUIString)+"/S:"+str(cvssBaseSString)+"/C:"+str(cvssBaseCString)+"/I:"+str(cvssBaseIString)+"/A:"+str(cvssBaseAString)+"/E:"+str(cvssTempEString)+"/RL:"+str(cvssTempRLString)+"/RC:"+str(cvssTempRCString)+"/CR:"+str(cvssEnvCRString)+"/IR:"+str(cvssEnvIRString)+"/AR:"+str(cvssEnvARString)+"/MAV:"+str(cvssEnvMAVString)+"/MAC:"+str(cvssEnvMACString)+"/MPR:"+str(cvssEnvMPRString)+"/MUI:"+str(cvssEnvMUIString)+"/MS:"+str(cvssEnvMSString)+"/MC:"+str(cvssEnvMCString)+"/MI:"+str(cvssEnvMIString)+"/MA:"+str(cvssEnvMAString)

    #--------------------------------------------
    #Condicion para solo considerar metricas base
    #--------------------------------------------
    if request.vars.metrica =='base':
        db.TratamientoRiesgo.update_or_insert(db.TratamientoRiesgo.id == request.args(0), CuantificacionCVSS = BaseScore, VectorCVSS = VectorString)
        if request.args(3):
            redirect(URL('default', 'TratamientoRiesgo', vars=dict(keywords = parametros)))
        else:
            redirect(URL('default', 'TratamientoRiesgo'))
    #--------------------------------------------------
    #Condicion para solo considerar metricas temporales
    #--------------------------------------------------
    elif request.vars.metrica == 'temp':
        db.TratamientoRiesgo.update_or_insert(db.TratamientoRiesgo.id == request.args(0) , CuantificacionCVSS = BaseScore, VectorCVSS = VectorString, CuantificacionCVSSE = BaseScoreM, VectorCVSSE = VectorStringE)
        if request.args(3):
            redirect(URL('default', 'EvaluacionControl', vars=dict(keywords = parametros)))
        else:
            redirect(URL('default', 'EvaluacionControl'))
    else:
        pass

def roundup(num):
    return D(math.ceil(num * 10) / 10).quantize(D("0.1"))
'''

#--------------------------------
@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BenchVersion():
    #db.BenchVersion.id.readable=False
    db.BenchVersion.AprobacionJefeRiesgo.writable=False
    db.BenchVersion.AprobacionAnalistaRiesgo.writable=False
    db.BenchVersion.LogJefeRiesgo.writable=False
    db.BenchVersion.LogAnalistaRiesgo.writable=False
    Tabla = 'BenchVersion'
    
    fields = (db.BenchVersion.id, db.BenchVersion.Version, db.BenchVersion.Descripcion, db.BenchVersion.AprobacionJefeRiesgo)

    if request.vars.get('keywords'):
        links = [ lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1",  base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0",  base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('View Details'),_class='button btn btn-warning',_href=URL("default","Benchmark", args=[row.id]))]
    else:
        links = [ lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('View Details'),_class='button btn btn-warning',_href=URL("default","Benchmark", args=[row.id]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        #links = [lambda row: A(T('View Details'),_class='button btn btn-success',_href=URL("default","Benchmark", args=[row.id]))]
        form=SQLFORM.grid(db.BenchVersion, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500)
    else:
        ActualizaAprobacion(Tabla)
        form=SQLFORM.grid(db.BenchVersion, fields=fields, searchable=True, deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500)
    return dict(form=form)

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BenchObjetivoControl():
    db.BenchObjetivoControl.AprobacionJefeRiesgo.writable=False
    db.BenchObjetivoControl.AprobacionAnalistaRiesgo.writable=False
    db.BenchObjetivoControl.LogJefeRiesgo.writable=False
    db.BenchObjetivoControl.LogAnalistaRiesgo.writable=False
    db.BenchObjetivoControl.id.readable=False
    Tabla = 'BenchObjetivoControl'
    
    fields = (db.BenchObjetivoControl.id, db.BenchObjetivoControl.BenchVersionId, db.BenchObjetivoControl.Numero, db.BenchObjetivoControl.Nombre, db.BenchObjetivoControl.Descripcion, db.BenchObjetivoControl.AprobacionJefeRiesgo)

    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))] ))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"])), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form=SQLFORM.grid(db.BenchObjetivoControl, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500)
    else:
        ActualizaAprobacion(Tabla)
        form=SQLFORM.grid(db.BenchObjetivoControl, fields=fields, searchable=True, deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500)
    return dict(form=form)

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BenchControl():
    db.BenchControl.AprobacionJefeRiesgo.writable=False
    db.BenchControl.AprobacionAnalistaRiesgo.writable=False
    db.BenchControl.LogJefeRiesgo.writable=False
    db.BenchControl.LogAnalistaRiesgo.writable=False
    db.BenchControl.id.readable = False
    Tabla = 'BenchControl'
    
    fields = (db.BenchControl.id, db.BenchControl.BenchObjetivoControlId, db.BenchControl.Numero, db.BenchControl.Nombre, db.BenchControl.Descripcion, db.BenchControl.AprobacionJefeRiesgo)

    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form=SQLFORM.grid(db.BenchControl, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500)
    else:
        ActualizaAprobacion(Tabla)
        form=SQLFORM.grid(db.BenchControl, fields=fields, searchable=True, deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500)
    return dict(form=form)

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def PruebaSeguridad():
    db.TestSeguridad.AprobacionJefeRiesgo.writable=False
    db.TestSeguridad.AprobacionAnalistaRiesgo.writable=False
    db.TestSeguridad.LogJefeRiesgo.writable=False
    db.TestSeguridad.LogAnalistaRiesgo.writable=False
    Tabla = 'TestSeguridad'
    fields = (db.TestSeguridad.id, db.TestSeguridad.ActivoTiId, db.TestSeguridad.ProcesoId, db.TestSeguridad.BenchControlId, db.TestSeguridad.NivelMadurezId, db.TestSeguridad.Comentarios, db.TestSeguridad.AprobacionJefeRiesgo)

    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))])),  lambda row: A(T('File'),_class='button btn btn-info',_href=URL("default","EvidenciaTestSeguridad", vars=dict(TestSeguridadId=row.id)))  ]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('File'),_class='button btn btn-info',_href=URL("default","EvidenciaTestSeguridad", vars=dict(TestSeguridadId=row.id)))  ]

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form=SQLFORM.grid(db.TestSeguridad, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='controlResp'):
        ActualizaAprobacion(Tabla)
        db.TestSeguridad.BenchControlId.writable = False
        db.TestSeguridad.ActivoTiId.writable = False
        db.TestSeguridad.ProcesoId.writable = False
        db.TestSeguridad.Comentarios.writable = False
        db.TestSeguridad.Evidencia.writable = False
        db.TestSeguridad.Fecha.writable = False
        db.TestSeguridad.Cumplimiento.writable = False
        form=SQLFORM.grid(db.TestSeguridad, fields=fields, links=links, searchable=True, deletable=False, create=False, editable=True, user_signature=True, paginate=10, maxtextlength=500)
    else:
        #ActualizaAprobacion(Tabla)
        form=SQLFORM.grid(db.TestSeguridad, fields=fields, searchable=True, deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500)
    return dict(form=form)

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def EvidenciaTestSeguridad():
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        query = db.EvidenciaTestSeguridad.TestSeguridadId==request.vars.TestSeguridadId
        form = SQLFORM.grid(query=query, searchable=True, deletable=True, create=True, editable=True, paginate=10, maxtextlength=500, user_signature=True)
    elif auth.has_membership(role='controlResp'):
        query = db.EvidenciaTestSeguridad.TestSeguridadId==request.vars.TestSeguridadId
        form = SQLFORM.grid(query=query, searchable=True, deletable=False, create=False, editable=False, paginate=10, maxtextlength=500, user_signature=True)
    else:
        redirect(URL('default','PruebaSeguridad'))
    return dict(form=form)

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def PruebaWeb():
    db.PruebaWeb.id.readable=False
    db.PruebaWeb.AprobacionJefeRiesgo.writable=False
    db.PruebaWeb.AprobacionAnalistaRiesgo.writable=False
    db.PruebaWeb.LogJefeRiesgo.writable=False
    db.PruebaWeb.LogAnalistaRiesgo.writable=False
    Tabla = 'PruebaWeb'
    fields = (db.PruebaWeb.ActivoTiId, db.PruebaWeb.Hallazgo, db.PruebaWeb.PlanAccion, db.PruebaWeb.AprobacionJefeRiesgo)

    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))])), lambda row: A(T('File'),_class='button btn btn-info',_href=URL("default","EvidenciaPruebaWeb", vars=dict(PruebaWebId=row.id))) ]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"])), lambda row: A(T('File'),_class='button btn btn-info',_href=URL("default","EvidenciaPruebaWeb", vars=dict(PruebaWebId=row.id))) ] 

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        ActualizaAprobacion(Tabla)
        form=SQLFORM.grid(db.PruebaWeb, fields=fields, links=links, searchable=True, deletable=True, create=True, editable=True, user_signature=True, paginate=10, maxtextlength=500)
    elif auth.has_membership(role='controlResp'):
        ActualizaAprobacion(Tabla)
        db.PruebaWeb.ActivoTiId.writable = False
        db.PruebaWeb.Hallazgo.writable = False
        db.PruebaWeb.Evidencia.writable = False
        db.PruebaWeb.Fecha.writable = False
        form=SQLFORM.grid(db.PruebaWeb, fields=fields, links=links, searchable=True, deletable=False, create=False, editable=True, user_signature=True, paginate=10, maxtextlength=500)
    else:
        form=SQLFORM.grid(db.PruebaWeb, fields=fields, searchable=True, deletable=False, create=False, editable=False, user_signature=True, paginate=10, maxtextlength=500)
    return dict(form=form)

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def EvaluacionEvidencia():
    if request.vars.EvaluacionControlId:
        query = db.EvaluacionEvidencia.EvaluacionControlId==request.vars.EvaluacionControlId
    else:
        query = db.EvaluacionEvidencia.id>0

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        #query = db.EvaluacionEvidencia.EvaluacionControlId==request.vars.EvaluacionControlId
        form = SQLFORM.grid(query=query, searchable=True, deletable=True, create=True, editable=True, paginate=10, maxtextlength=500, user_signature=True)
    elif auth.has_membership(role='controlResp'):
        #query = db.EvidenciaPruebaWeb.PruebaWebId==request.vars.PruebaWebId
        #query = db.EvaluacionEvidencia.EvaluacionControlId==request.vars.EvaluacionControlId
        form = SQLFORM.grid(query=query, searchable=True, deletable=False, create=False, editable=False, paginate=10, maxtextlength=500, user_signature=True)
    else:
        redirect(URL('default','EvaluacionControl'))
    return dict(form=form)

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def ContenedorDocs():
    if request.vars.ActivoTiId:
        query = db.ContenedorDocs.ActivoTiId==request.vars.ActivoTiId
    else:
        query = db.ContenedorDocs.id>0

    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        form = SQLFORM.grid(query=query, searchable=True, deletable=True, create=True, editable=True, paginate=10, maxtextlength=500, user_signature=True)
    elif auth.has_membership(role='controlResp'):
        form = SQLFORM.grid(query=query, searchable=True, deletable=False, create=False, editable=False, paginate=10, maxtextlength=500, user_signature=True)
    else:
        redirect(URL('default','ActivoTi'))
    return dict(form=form)

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def FactorEvidencia():
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        query = db.FactorEvidencia.TratamientoRiesgoId==request.vars.TratamientoRiesgoId
        form = SQLFORM.grid(query=query, searchable=True, deletable=True, create=True, editable=True, paginate=10, maxtextlength=500, user_signature=True)
    elif auth.has_membership(role='controlResp'):
        query = db.FactorEvidencia.TratamientoRiesgoId==request.vars.TratamientoRiesgoId
        form = SQLFORM.grid(query=query, searchable=True, deletable=False, create=False, editable=False, paginate=10, maxtextlength=500, user_signature=True)
    else:
        redirect(URL('default','TratamientoRiesgo'))
    return dict(form=form)

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def Benchmark():
    BenchObjetivoControl = db( (db.BenchObjetivoControl.BenchVersionId==request.args(0)) & (db.BenchObjetivoControl.AprobacionJefeRiesgo=='T') ).select(db.BenchObjetivoControl.ALL)
    BenchEvaluacion = db( (db.BenchEvaluacion.BenchControlId==db.BenchControl.id) & (db.BenchEvaluacion.AprobacionJefeRiesgo=='T') & (db.BenchEvaluacion.StatusControl=='T') & (db.BenchEvaluacion.NivelMadurezId==db.NivelMadurez.id) & (db.BenchControl.BenchObjetivoControlId==db.BenchObjetivoControl.id) & (db.BenchControl.AprobacionJefeRiesgo=='T') & (db.BenchObjetivoControl.BenchVersionId==db.BenchVersion.id) & (db.BenchObjetivoControl.AprobacionJefeRiesgo=='T') & (db.BenchVersion.id==request.args(0)) & (db.BenchVersion.AprobacionJefeRiesgo=='T') ).select(db.BenchEvaluacion.ALL)
    
    NivelMadurez = db().select(db.NivelMadurez.ALL, orderby=db.NivelMadurez.Valor)
    BenchVersion = db(db.BenchVersion.id==request.args(0)).select(db.BenchVersion.Version).first().Version

    BenchNivelMadurez = []
    #lista = []
    #for i in BenchEvaluacion:
    for i in BenchObjetivoControl:
        lista = []
        lista.append(i.id)
        lista.append(0)
        lista.append(0)
        lista.append(0)
        lista.append(i.Nombre)
        #lista.append('')
        BenchNivelMadurez.append(lista)
    for i in BenchNivelMadurez:
        for a in BenchEvaluacion:
            if i[0]==a.BenchControlId.BenchObjetivoControlId:
                i[1]=i[1]+int(a.NivelMadurezId.Valor)
                i[2]=i[2]+1
    for i in BenchNivelMadurez:
        try:
            i[3]=int(i[1]) / int(i[2])
        except:
            i[3]=0

    return dict(BenchObjetivoControl=BenchObjetivoControl, BenchEvaluacion=BenchEvaluacion, NivelMadurez=NivelMadurez, BenchVersion=BenchVersion, BenchNivelMadurez=BenchNivelMadurez)
# links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "

'''
#----------------
#Otras funciones
#----------------
@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='admin') )
def AsignarCriterio():
    ValorImpacto = db( (db.TratamientoRiesgoAreaImpacto.TratamientoRiesgoId==request.args(0)) & (db.TratamientoRiesgoAreaImpacto.AreaImpactoCriterioImpactoId==db.AreaImpactoCriterioImpacto.id) & (db.TratamientoRiesgoAreaImpacto.AprobacionJefeRiesgo=='T') ).select(db.AreaImpactoCriterioImpacto.CriterioImpactoId)
    ValorProbabilidad = db( (db.TratamientoRiesgoAreaProbabilidad.TratamientoRiesgoId==request.args(0)) & (db.TratamientoRiesgoAreaProbabilidad.AreaProbabilidadCriterioProbabilidadId==db.AreaProbabilidadCriterioProbabilidad.id) &  (db.TratamientoRiesgoAreaProbabilidad.AprobacionJefeRiesgo=='T') ).select(db.AreaProbabilidadCriterioProbabilidad.CriterioProbabilidadId)

    suma = 0
    contador = 0
    for i in ValorImpacto:
        suma = suma + i.CriterioImpactoId
        contador = contador + 1
    try:
        Valor = float(suma) / float(contador)
    except:
        Valor = 0
    db(db.TratamientoRiesgo.id==request.args(0)).update(CalculoImpacto=Valor)

    suma = 0
    contador = 0
    for i in ValorProbabilidad:
        suma = suma + i.CriterioProbabilidadId
        contador = contador + 1
    try:
        Valor = float(suma) / float(contador)
    except:
        Valor = 0
    db(db.TratamientoRiesgo.id==request.args(0)).update(CalculoProbabilidad=Valor)

    redirect(URL('default', 'TratamientoRiesgo'))
    #redirect(URL('default', 'TratamientoRiesgo', vars=dict(Valor=Valor, idTratamientoRiesgo=request.args(0))))
    #return dict(ValorImpacto=float(Valor))
'''
'''
@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='iformationOwner') or auth.has_membership(role='admin') or auth.has_membership(role='guest') or auth.has_membership(role='controlResp'))
def CopiarRegistro():
    if request.args(1) == "TratamientoRiesgo":
        registro = db(db.TratamientoRiesgo.id==request.args(0)).select(db.TratamientoRiesgo.ALL)
        for i in registro:
            #db.TratamientoRiesgo.insert(AnalisisRiesgoId=i.AnalisisRiesgoId, FechaRevision=i.FechaRevision, ProcesoRegionId=i.ProcesoRegionId, ActivoTiId=i.ActivoTiId, ActivoTiRegionId=i.ActivoTiRegionId, ActivoInformacionId=i.ActivoInformacionId, FactorRiesgo=i.FactorRiesgo, RiesgoFraude=i.RiesgoFraude, EscenarioAmenaza=i.EscenarioAmenaza, TipoVulnerabilidadId=i.TipoVulnerabilidadId, CriterioImpactoId=i.CriterioImpactoId, CriterioProbabilidadId=i.CriterioProbabilidadId, TipoTratamientoRiesgoId=i.TipoTratamientoRiesgoId, EvidenciaRiesgo=i.EvidenciaRiesgo, RiesgoMaterializadoCheck=i.RiesgoMaterializadoCheck, CatalogoControlId=i.CatalogoControlId, TipoControlId=i.TipoControlId, ClasificacionControlId=i.ClasificacionControlId, NivelMadurezId=i.NivelMadurezId, KeyControl=i.KeyControl, ObjetivoControl=i.ObjetivoControl, ActividadControl=i.ActividadControl, DetallePoliticaId=i.DetallePoliticaId, ResponsableControl=i.ResponsableControl, ComentariosResponsableControl=i.ComentariosResponsableControl, EvidenciaControl=i.EvidenciaControl, FechaImplementacionControl=i.FechaImplementacionControl, AnalistaRiesgo=i.AnalistaRiesgo)
            db.TratamientoRiesgo.insert(FechaRevision=i.FechaRevision, ProcesoRegionId=i.ProcesoRegionId, ActivoTiRegionId=i.ActivoTiRegionId, ActivoInformacionId=i.ActivoInformacionId, FactorRiesgo=i.FactorRiesgo, RiesgoFraude=i.RiesgoFraude, EscenarioAmenaza=i.EscenarioAmenaza, TipoVulnerabilidadId=i.TipoVulnerabilidadId, CriterioImpactoId=i.CriterioImpactoId, CriterioProbabilidadId=i.CriterioProbabilidadId, TipoTratamientoRiesgoId=i.TipoTratamientoRiesgoId, EvidenciaRiesgo=i.EvidenciaRiesgo, RiesgoMaterializadoCheck=i.RiesgoMaterializadoCheck, CatalogoControlId=i.CatalogoControlId, TipoControlId=i.TipoControlId, ClasificacionControlId=i.ClasificacionControlId, NivelMadurezId=i.NivelMadurezId, KeyControl=i.KeyControl, ObjetivoControl=i.ObjetivoControl, ActividadControl=i.ActividadControl, DetallePoliticaId=i.DetallePoliticaId, ResponsableControl=i.ResponsableControl, ComentariosResponsableControl=i.ComentariosResponsableControl, EvidenciaControl=i.EvidenciaControl, FechaImplementacionControl=i.FechaImplementacionControl, AnalistaRiesgo=i.AnalistaRiesgo)
        redirect(URL('TratamientoRiesgo'))
    if request.args(1) == "AnalisisRiesgo":
        registro = db(db.AnalisisRiesgo.id==request.args(0)).select(db.AnalisisRiesgo.ALL)
        for i in registro:
            db.AnalisisRiesgo.insert(Riesgo=i.Riesgo, TipoTratamientoRiesgoId=i.TipoTratamientoRiesgoId, ClasificacionRiesgoId=i.ClasificacionRiesgoId, ObjetivoOrganizacionId=i.ObjetivoOrganizacionId, FechaRevision=i.FechaRevision, EvidenciaRiesgo=i.EvidenciaRiesgo, RiesgoMaterializado=i.RiesgoMaterializado, CriterioImpactoId=i.CriterioImpactoId, CriterioProbabilidadId=i.CriterioProbabilidadId, DuenoRiesgo=i.DuenoRiesgo, AnalistaRiesgo=i.AnalistaRiesgo)
        redirect(URL('AnalisisRiesgo'))
    if request.args(1) == "CatalogoPolitica":
        registro = db(db.CatalogoPolitica.id==request.args(0)).select(db.CatalogoPolitica.ALL)
        for i in registro:
            db.CatalogoPolitica.insert(Nombre=i.Nombre, Descripcion=i.Descripcion, Version=i.Version, Fecha=i.Fecha, Archivo=i.Archivo)
        redirect(URL('CatalogoPolitica'))
    if request.args(1) == "DetallePolitica":
        registro = db(db.DetallePolitica.id==request.args(0)).select(db.DetallePolitica.ALL)
        for i in registro:
            #db.DetallePolitica.insert(RegionPoliticaId=i.RegionPoliticaId, Codigo=i.Codigo, Nombre=i.Nombre, Comentarios=i.Comentarios, Archivo=i.Archivo)
            db.DetallePolitica.insert(RegionPoliticaId=i.RegionPoliticaId, Nombre=i.Nombre, Comentarios=i.Comentarios, Archivo=i.Archivo)
        redirect(URL('DetallePolitica'))
    if request.args(1) == "Proceso":
        registro = db(db.Proceso.id==request.args(0)).select(db.Proceso.ALL)
        for i in registro:
            db.Proceso.insert(Nombre=i.Nombre, Descripcion=i.Descripcion, Objetivo=i.Objetivo, Diagrama=i.Diagrama, Dueno=i.Dueno, TipoProcesoId=i.TipoProcesoId, CicloNegocioId=i.CicloNegocioId)
        redirect(URL('Proceso'))
    if request.args(1) == "EvaluacionControl":
        registro = db(db.EvaluacionControl.id==request.args(0)).select(db.EvaluacionControl.ALL)
        for i in registro:
            db.EvaluacionControl.insert(TratamientoRiesgoId=i.TratamientoRiesgoId, CumplimientoControl=i.CumplimientoControl, EfectividadControl=i.EfectividadControl, NivelMadurezId=i.NivelMadurezId, FechaRevision=i.FechaRevision, TipoRevisionId=i.TipoRevisionId, AlcanceRevisionId=i.AlcanceRevisionId, EscenarioRiesgo=i.EscenarioRiesgo, Recomendacion=i.Recomendacion, EvidenciaCumplimiento=i.EvidenciaCumplimiento, ResponsableControl=i.ResponsableControl, ComentariosResponsableControl=i.ComentariosResponsableControl, EvidenciaControl=i.EvidenciaControl, FechaImplementacionControl=i.FechaImplementacionControl)
        redirect(URL('EvaluacionControl'))
'''

@auth.requires_login()
def RegistroLog():
    signature = auth.user.username + ',' + request.client + ',' + str(request.now) + ',' + str(response.session_id)
    #try:
    if request.args(3):
        parametros = base64.b64decode(request.args(3))
    #except:
    else:
        #parametros = request.vars
        pass

    if request.args(1) == 'TipoObjetivo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoObjetivo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoObjetivo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoObjetivo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoObjetivo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TipoObjetivo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoObjetivo.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoObjetivo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoObjetivo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('TipoObjetivo', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TipoObjetivo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TipoObjetivo'))
    '''
    if request.args(1) == 'AreaImpacto':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.AreaImpacto.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AreaImpacto.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.AreaImpacto.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AreaImpacto.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.AreaImpacto.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AreaImpacto.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.AreaImpacto.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AreaImpacto.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('AreaImpacto', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AreaImpacto', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AreaImpacto'))

    if request.args(1) == 'AreaProbabilidad':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.AreaProbabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AreaProbabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.AreaProbabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AreaProbabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.AreaProbabilidad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AreaProbabilidad.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.AreaProbabilidad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AreaProbabilidad.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('AreaProbabilidad', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AreaProbabilidad', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AreaProbabilidad'))

    if request.args(1) == 'AreaImpactoCriterioImpacto':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.AreaImpactoCriterioImpacto.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AreaImpactoCriterioImpacto.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.AreaImpactoCriterioImpacto.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AreaImpactoCriterioImpacto.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.AreaImpactoCriterioImpacto.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AreaImpactoCriterioImpacto.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.AreaImpactoCriterioImpacto.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AreaImpactoCriterioImpacto.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('AreaImpactoCriterioImpacto', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AreaImpactoCriterioImpacto', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AreaImpactoCriterioImpacto'))

    if request.args(1) == 'AreaProbabilidadCriterioProbabilidad':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.AreaProbabilidadCriterioProbabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AreaProbabilidadCriterioProbabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.AreaProbabilidadCriterioProbabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AreaProbabilidadCriterioProbabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.AreaProbabilidadCriterioProbabilidad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AreaProbabilidadCriterioProbabilidad.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.AreaProbabilidadCriterioProbabilidad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AreaProbabilidadCriterioProbabilidad.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('AreaProbabilidadCriterioProbabilidad', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AreaProbabilidadCriterioProbabilidad', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AreaProbabilidadCriterioProbabilidad'))
    '''
    if request.args(1) == 'TratamientoRiesgoAreaImpacto':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TratamientoRiesgoAreaImpacto.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TratamientoRiesgoAreaImpacto.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TratamientoRiesgoAreaImpacto.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TratamientoRiesgoAreaImpacto.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TratamientoRiesgoAreaImpacto.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TratamientoRiesgoAreaImpacto.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TratamientoRiesgoAreaImpacto.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TratamientoRiesgoAreaImpacto.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('TratamientoRiesgoAreaImpacto', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TratamientoRiesgoAreaImpacto', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TratamientoRiesgoAreaImpacto'))

    if request.args(1) == 'TipoVulnerabilidadAnalisisRiesgo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoVulnerabilidadAnalisisRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoVulnerabilidadAnalisisRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoVulnerabilidadAnalisisRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoVulnerabilidadAnalisisRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TipoVulnerabilidadAnalisisRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoVulnerabilidadAnalisisRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoVulnerabilidadAnalisisRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoVulnerabilidadAnalisisRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('TratamientoRiesgoAnalisisRiesgo', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TipoVulnerabilidadAnalisisRiesgo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TipoVulnerabilidadAnalisisRiesgo'))

    if request.args(1) == 'TratamientoRiesgoAreaProbabilidad':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TratamientoRiesgoAreaProbabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TratamientoRiesgoAreaProbabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TratamientoRiesgoAreaProbabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TratamientoRiesgoAreaProbabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TratamientoRiesgoAreaProbabilidad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TratamientoRiesgoAreaProbabilidad.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TratamientoRiesgoAreaProbabilidad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TratamientoRiesgoAreaProbabilidad.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('TratamientoRiesgoAreaProbabilidad', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TratamientoRiesgoAreaProbabilidad', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TratamientoRiesgoAreaProbabilidad'))

    if request.args(1) == 'ClasificacionInformacion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ClasificacionInformacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ClasificacionInformacion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ClasificacionInformacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ClasificacionInformacion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ClasificacionInformacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ClasificacionInformacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ClasificacionInformacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ClasificacionInformacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ClasificacionInformacion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ClasificacionInformacion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ClasificacionInformacion'))

    if request.args(1) == 'TipoDato':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoDato.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoDato.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoDato.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoDato.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TipoDato.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoDato.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoDato.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoDato.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('TipoDato', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TipoDato', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TipoDato'))

    if request.args(1) == 'ClasificacionRiesgo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ClasificacionRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ClasificacionRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ClasificacionRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ClasificacionRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ClasificacionRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ClasificacionRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ClasificacionRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ClasificacionRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ClasificacionRiesgo', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ClasificacionRiesgo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ClasificacionRiesgo'))

    if request.args(1) == 'AnalisisRiesgoClasificacionRiesgo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.AnalisisRiesgoClasificacionRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AnalisisRiesgoClasificacionRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.AnalisisRiesgoClasificacionRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AnalisisRiesgoClasificacionRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.AnalisisRiesgoClasificacionRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AnalisisRiesgoClasificacionRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.AnalisisRiesgoClasificacionRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AnalisisRiesgoClasificacionRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('AnalisisRiesgoClasificacionRiesgo', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AnalisisRiesgoClasificacionRiesgo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AnalisisRiesgoClasificacionRiesgo'))

    if request.args(1) == 'TratamientoRiesgoAnalisisRiesgo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TratamientoRiesgoAnalisisRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TratamientoRiesgoAnalisisRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TratamientoRiesgoAnalisisRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TratamientoRiesgoAnalisisRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TratamientoRiesgoAnalisisRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TratamientoRiesgoAnalisisRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TratamientoRiesgoAnalisisRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TratamientoRiesgoAnalisisRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if request.args(3):
            redirect(URL('TratamientoRiesgoAnalisisRiesgo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TratamientoRiesgoAnalisisRiesgo'))

    if request.args(1) == 'AnalisisRiesgoObjetivoOrganizacion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.AnalisisRiesgoObjetivoOrganizacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AnalisisRiesgoObjetivoOrganizacion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.AnalisisRiesgoObjetivoOrganizacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AnalisisRiesgoObjetivoOrganizacion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.AnalisisRiesgoObjetivoOrganizacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AnalisisRiesgoObjetivoOrganizacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.AnalisisRiesgoObjetivoOrganizacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AnalisisRiesgoObjetivoOrganizacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('AnalisisRiesgoObjetivoOrganizacion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AnalisisRiesgoObjetivoOrganizacion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AnalisisRiesgoObjetivoOrganizacion'))

    if request.args(1) == 'TipoControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TipoControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('TipoControl', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TipoControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TipoControl'))

    if request.args(1) == 'GrupoControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.GrupoControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.GrupoControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.GrupoControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.GrupoControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.GrupoControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.GrupoControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.GrupoControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.GrupoControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('TipoControl', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('GrupoControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('GrupoControl'))

    if request.args(1) == 'ClasificacionControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ClasificacionControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ClasificacionControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ClasificacionControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ClasificacionControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ClasificacionControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ClasificacionControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ClasificacionControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ClasificacionControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if request.args(3):
            redirect(URL('ClasificacionControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ClasificacionControl'))
    #if request.args(3):
    #    redirect(URL(request.args(1), vars=dict(keywords=parametros)))
    #else:
    #    redirect(URL(request.arsg(1)))

    if request.args(1) == 'CatalogoControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.CatalogoControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CatalogoControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.CatalogoControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CatalogoControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.CatalogoControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.CatalogoControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.CatalogoControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.CatalogoControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('CatalogoControl', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('GrupoControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('GrupoControl'))
    
    if request.args(1) == 'ObjetivoControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ObjetivoControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ObjetivoControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ObjetivoControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ObjetivoControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ObjetivoControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ObjetivoControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ObjetivoControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ObjetivoControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ObjetivoControl', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ObjetivoControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ObjetivoControl'))

    if request.args(1) == 'CatalogoControlBenchControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.CatalogoControlBenchControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CatalogoControlBenchControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.CatalogoControlBenchControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CatalogoControlBenchControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.CatalogoControlBenchControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.CatalogoControlBenchControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.CatalogoControlBenchControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.CatalogoControlBenchControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('CatalogoControlObjetivoControl', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('CatalogoControlBenchControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('CatalogoControlBenchControl'))

    if request.args(1) == 'DetallePoliticaBenchControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.DetallePoliticaBenchControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.DetallePoliticaBenchControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.DetallePoliticaBenchControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.DetallePoliticaBenchControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.DetallePoliticaBenchControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.DetallePoliticaBenchControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.DetallePoliticaBenchControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.DetallePoliticaBenchControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('CatalogoControlObjetivoControl', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('DetallePoliticaBenchControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('DetallePoliticaBenchControl'))

    if request.args(1) == 'Region':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Region.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Region.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.Region.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Region.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.Region.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Region.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.Region.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Region.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('Region', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('Region', vars=dict(keywords=parametros)))
        else:
            redirect(URL('Region'))
   
    if request.args(1) == 'ProcesoRegion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ProcesoRegion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoRegion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoRegion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoRegion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ProcesoRegion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoRegion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoRegion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoRegion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ProcesoRegion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ProcesoRegion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ProcesoRegion'))
   
    if request.args(1) == 'RegionPolitica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.RegionPolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.RegionPolitica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.RegionPolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.RegionPolitica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.RegionPolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.RegionPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.RegionPolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.RegionPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('RegionPolitica', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('RegionPolitica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('RegionPolitica'))

    if request.args(1) == 'CicloNegocio':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.CicloNegocio.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CicloNegocio.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.CicloNegocio.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CicloNegocio.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.CicloNegocio.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.CicloNegocio.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.CicloNegocio.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.CicloNegocio.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('CicloNegocio', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('CicloNegocio', vars=dict(keywords=parametros)))
        else:
            redirect(URL('CicloNegocio'))

    if request.args(1) == 'TipoProceso':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoProceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoProceso.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoProceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoProceso.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TipoProceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoProceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoProceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoProceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('TipoProceso', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TipoProceso', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TipoProceso'))

    if request.args(1) == 'MacroProceso':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.MacroProceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.MacroProceso.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.MacroProceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.MacroProceso.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.MacroProceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.MacroProceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.MacroProceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.MacroProceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('MacroProceso', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('MacroProceso', vars=dict(keywords=parametros)))
        else:
            redirect(URL('MacroProceso'))

    if request.args(1) == 'ProcesoTipoProceso':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ProcesoTipoProceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoTipoProceso.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoTipoProceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoTipoProceso.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ProcesoTipoProceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoTipoProceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoTipoProceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoTipoProceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ProcesoTipoProceso', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ProcesoTipoProceso', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ProcesoTipoProceso'))

    if request.args(1) == 'ProcesoMacroProceso':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ProcesoMacroProceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoMacroProceso.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoMacroProceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoMacroProceso.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ProcesoMacroProceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoMacroProceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoMacroProceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoMacroProceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ProcesoMacroProceso', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ProcesoMacroProceso', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ProcesoMacroProceso'))

    if request.args(1) == 'ProcesoCicloNegocio':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ProcesoCicloNegocio.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoCicloNegocio.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoCicloNegocio.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoCicloNegocio.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ProcesoCicloNegocio.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoCicloNegocio.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoCicloNegocio.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoCicloNegocio.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ProcesoCicloNegocio', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ProcesoCicloNegocio', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ProcesoCicloNegocio'))

    if request.args(1) == 'Direccion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Direccion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Direccion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.Direccion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Direccion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.Direccion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Direccion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.Direccion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Direccion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('Direccion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('Direccion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('Direccion'))

    if request.args(1) == 'Documentacion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Documentacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Documentacion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.Documentacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Documentacion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.Documentacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Documentacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.Documentacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Documentacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('Documentacion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('Documentacion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('Documentacion'))

    if request.args(1) == 'Proceso':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Proceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Proceso.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.Proceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Proceso.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.Proceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Proceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.Proceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Proceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('Proceso', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('Proceso', vars=dict(keywords=parametros)))
        else:
            redirect(URL('Proceso'))

    if request.args(1) == 'ProcesoPolitica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ProcesoPolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoPolitica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoPolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoPolitica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ProcesoPolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoPolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ProcesoPolitica', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ProcesoPolitica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ProcesoPolitica'))

    if request.args(1) == 'NivelMadurez':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.NivelMadurez.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.NivelMadurez.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.NivelMadurez.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.NivelMadurez.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.NivelMadurez.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.NivelMadurez.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.NivelMadurez.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.NivelMadurez.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('NivelMadurez', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('NivelMadurez', vars=dict(keywords=parametros)))
        else:
            redirect(URL('NivelMadurez'))

    if request.args(1) == 'CriterioImpacto':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.CriterioImpacto.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CriterioImpacto.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.CriterioImpacto.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CriterioImpacto.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        #redirect(URL('CriterioImpacto', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('CriterioImpacto', vars=dict(keywords=parametros)))
        else:
            redirect(URL('CriterioImpacto'))

    if request.args(1) == 'CriterioProbabilidad':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.CriterioProbabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CriterioProbabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.CriterioProbabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CriterioProbabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        #redirect(URL('CriterioProbabilidad', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('CriterioProbabilidad', vars=dict(keywords=parametros)))
        else:
            redirect(URL('CriterioProbabilidad'))

    if request.args(1) == 'CriterioRiesgo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.CriterioRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CriterioRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.CriterioRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CriterioRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if request.args(3):
            redirect(URL('CriterioRiesgo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('CriterioRiesgo'))

    if request.args(1) == 'ObjetivoOrganizacion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ObjetivoOrganizacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ObjetivoOrganizacion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.ObjetivoOrganizacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ObjetivoOrganizacion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        #redirect(URL('ObjetivoOrganizacion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ObjetivoOrganizacion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ObjetivoOrganizacion'))

    if request.args(1) == 'Organizacion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Organizacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Organizacion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.Organizacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Organizacion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if request.args(3):
            redirect(URL('Organizacion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('Organizacion'))
    '''
    if request.args(1) == 'AmbienteControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.AmbienteControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AmbienteControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.AmbienteControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AmbienteControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.AmbienteControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AmbienteControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.AmbienteControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AmbienteControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('AmbienteControl', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AmbienteControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AmbienteControl'))
    '''
    if request.args(1) == 'ActivoInformacion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ActivoInformacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoInformacion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.ActivoInformacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoInformacion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ActivoInformacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoInformacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.ActivoInformacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoInformacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if (auth.has_membership(role='informationOwner')):
            if request.args(2)=='1':
                db(db.ActivoInformacion.id==request.args(0)).update(LogDuenoInformacion=signature)
                db(db.ActivoInformacion.id==request.args(0)).update(AprobacionDuenoInformacion='T')
            if request.args(2)=='0':
                db(db.ActivoInformacion.id==request.args(0)).update(LogDuenoInformacion=signature)
                db(db.ActivoInformacion.id==request.args(0)).update(AprobacionDuenoInformacion='F')
        #redirect(URL('ActivoInformacion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ActivoInformacion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ActivoInformacion'))

    if request.args(1) == 'RolResponsabilidad':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.RolResponsabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.RolResponsabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.RolResponsabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.RolResponsabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.RolResponsabilidad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.RolResponsabilidad.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.RolResponsabilidad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.RolResponsabilidad.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        '''
        if (auth.has_membership(role='informationOwner')):
            if request.args(2)=='1':
                db(db.RolResponsabilidad.id==request.args(0)).update(LogDuenoInformacion=signature)
                db(db.RolResponsabilidad.id==request.args(0)).update(AprobacionDuenoInformacion='T')
            if request.args(2)=='0':
                db(db.RolResponsabilidad.id==request.args(0)).update(LogDuenoInformacion=signature)
                db(db.RolResponsabilidad.id==request.args(0)).update(AprobacionDuenoInformacion='F')
        #redirect(URL('ActivoInformacion', vars=dict(keywords=parametros)))
        '''
        if request.args(3):
            redirect(URL('RolResponsabilidad', vars=dict(keywords=parametros)))
        else:
            redirect(URL('RolResponsabilidad'))

    if request.args(1) == 'AnalisisRiesgo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.AnalisisRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AnalisisRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.AnalisisRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AnalisisRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
                #db(db.AnalisisRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
                #db(db.AnalisisRiesgo.id==request.args(0)).update(AprobacionDuenoProceso='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.AnalisisRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AnalisisRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.AnalisisRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AnalisisRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if (auth.has_membership(role='processOwner')):
            if request.args(2)=='1':
                db(db.AnalisisRiesgo.id==request.args(0)).update(LogDuenoProceso=signature)
                db(db.AnalisisRiesgo.id==request.args(0)).update(AprobacionDuenoProceso='T')
            if request.args(2)=='0':
                db(db.AnalisisRiesgo.id==request.args(0)).update(LogDuenoProceso=signature)
                db(db.AnalisisRiesgo.id==request.args(0)).update(AprobacionDuenoProceso='F')
        #redirect(URL('AnalisisRiesgo', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AnalisisRiesgo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AnalisisRiesgo'))

    if request.args(1) == 'TratamientoRiesgo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TratamientoRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TratamientoRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.TratamientoRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TratamientoRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TratamientoRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TratamientoRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.TratamientoRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TratamientoRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if (auth.has_membership(role='controlResp')):
            if request.args(2)=='1':
                db(db.TratamientoRiesgo.id==request.args(0)).update(LogResponsableControl=signature)
                db(db.TratamientoRiesgo.id==request.args(0)).update(AprobacionResponsableControl='T')
            if request.args(2)=='0':
                db(db.TratamientoRiesgo.id==request.args(0)).update(LogResponsableControl=signature)
                db(db.TratamientoRiesgo.id==request.args(0)).update(AprobacionResponsableControl='F')
        #redirect(URL('TratamientoRiesgo'))
        #redirect(URL('TratamientoRiesgo', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TratamientoRiesgo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TratamientoRiesgo'))

    if request.args(1) == 'TipoTratamientoRiesgo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if (auth.has_membership(role='controlResp')):
            if request.args(2)=='1':
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(LogResponsableControl=signature)
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(AprobacionResponsableControl='T')
            if request.args(2)=='0':
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(LogResponsableControl=signature)
                db(db.TipoTratamientoRiesgo.id==request.args(0)).update(AprobacionResponsableControl='F')
        #redirect(URL('TipoTratamientoRiesgo', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TipoTratamientoRiesgo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TipoTratamientoRiesgo'))

    if request.args(1) == 'CatalogoPolitica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.CatalogoPolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.CatalogoPolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
                #db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
                #db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionResponsableControl='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.CatalogoPolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.CatalogoPolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('CatalogoPolitica', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('CatalogoPolitica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('CatalogoPolitica'))

    if request.args(1) == 'DetallePolitica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.DetallePolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.DetallePolitica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.DetallePolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.DetallePolitica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.DetallePolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.DetallePolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.DetallePolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.DetallePolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('DetallePolitica', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('DetallePolitica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('DetallePolitica'))

    if request.args(1) == 'RegulacionDato':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.RegulacionDato.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.RegulacionDato.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.RegulacionDato.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.RegulacionDato.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.RegulacionDato.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.RegulacionDato.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.RegulacionDato.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.RegulacionDato.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('RegulacionDato', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('RegulacionDato', vars=dict(keywords=parametros)))
        else:
            redirect(URL('RegulacionDato'))

    if request.args(1) == 'RegulacionPolitica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.RegulacionPolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.RegulacionPolitica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.RegulacionPolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.RegulacionPolitica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.RegulacionPolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.RegulacionPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.RegulacionPolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.RegulacionPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('RegulacionPolitica', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('RegulacionPolitica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('RegulacionPolitica'))

    if request.args(1) == 'GrupoMetrica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.GrupoMetrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.GrupoMetrica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.GrupoMetrica.id==request.args(0)).update(LogJefeRiesgi=signature)
                db(db.GrupoMetrica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.GrupoMetrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.GrupoMetrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.GrupoMetrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.GrupoMetrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('GrupoMetrica', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('GrupoMetrica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('GrupoMetrica'))

    if request.args(1) == 'Metrica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Metrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Metrica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.Metrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Metrica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.Metrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Metrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.Metrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Metrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('Metrica', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('Metrica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('Metrica'))

    if request.args(1) == 'AutoControlConfiguracion':
        if (auth.has_membership(role='auditManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db2(db2.AutoControlConfiguracion.id==request.args(0)).update(LogJefeAuditoria=signature)
                db2(db2.AutoControlConfiguracion.id==request.args(0)).update(AprobacionJefeAuditoria='T')
            elif request.args(2)=='0':
                db2(db2.AutoControlConfiguracion.id==request.args(0)).update(LogJefeAuditoria=signature)
                db2(db2.AutoControlConfiguracion.id==request.args(0)).update(AprobacionJefeAuditoria='F')
        elif (auth.has_membership(role='auditAnalyst')):
            if request.args(2)=='1':
                db2(db2.AutoControlConfiguracion.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db2(db2.AutoControlConfiguracion.id==request.args(0)).update(AprobacionAnalistaAuditoria='T')
            elif request.args(2)=='0':
                db2(db2.AutoControlConfiguracion.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db2(db2.AutoControlConfiguracion.id==request.args(0)).update(AprobacionAnalistaAuditoria='F')
        #redirect(URL('AutoControlConfiguracion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AutoControlConfiguracion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AutoControlConfiguracion'))

    if request.args(1) == 'AutoControlCuestionario':
        if (auth.has_membership(role='auditManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db2(db2.AutoControlCuestionario.id==request.args(0)).update(LogJefeAuditoria=signature)
                db2(db2.AutoControlCuestionario.id==request.args(0)).update(AprobacionJefeAuditoria='T')
            elif request.args(2)=='0':
                db2(db2.AutoControlCuestionario.id==request.args(0)).update(LogJefeAuditoria=signature)
                db2(db2.AutoControlCuestionario.id==request.args(0)).update(AprobacionJefeAuditoria='F')
        elif (auth.has_membership(role='auditAnalyst')):
            if request.args(2)=='1':
                db2(db2.AutoControlCuestionario.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db2(db2.AutoControlCuestionario.id==request.args(0)).update(AprobacionAnalistaAuditoria='T')
            elif request.args(2)=='0':
                db2(db2.AutoControlCuestionario.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db2(db2.AutoControlCuestionario.id==request.args(0)).update(AprobacionAnalistaAuditoria='F')
        #redirect(URL('AutoControlCuestionario', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AutoControlCuestionario', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AutoControlCuestionario'))

    if request.args(1) == 'ValorMetrica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ValorMetrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ValorMetrica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ValorMetrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ValorMetrica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ValorMetrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ValorMetrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ValorMetrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ValorMetrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ValorMetrica', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ValorMetrica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ValorMetrica'))

    if request.args(1) == 'TipoVulnerabilidad':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoVulnerabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoVulnerabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoVulnerabilidad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoVulnerabilidad.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TipoVulnerabilidad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoVulnerabilidad.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoVulnerabilidad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoVulnerabilidad.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if request.args(3):
            redirect(URL('GrupoFactorRiesgo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('GrupoFactorRiesgo'))

    if request.args(1) == 'TipoCapaSistema':
        if (auth.has_membership(role='auditManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoCapaSistema.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoCapaSistema.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoCapaSistema.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoCapaSistema.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='auditAnalyst')):
            if request.args(2)=='1':
                db(db.TipoCapaSistema.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoCapaSistema.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoCapaSistema.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoCapaSistema.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('TipoCapaSistema', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TipoCapaSistema', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TipoCapaSistema'))

    if request.args(1) == 'Plataforma':
        if (auth.has_membership(role='auditManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Plataforma.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.Plataforma.id==request.args(0)).update(AprobacionJefeAuditoria='T')
            elif request.args(2)=='0':
                db(db.Plataforma.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.Plataforma.id==request.args(0)).update(AprobacionJefeAuditoria='F')
        elif (auth.has_membership(role='auditAnalyst')):
            if request.args(2)=='1':
                db(db.Plataforma.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.Plataforma.id==request.args(0)).update(AprobacionAnalistaAuditoria='T')
            elif request.args(2)=='0':
                db(db.Plataforma.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.Plataforma.id==request.args(0)).update(AprobacionAnalistaAuditoria='F')
        #redirect(URL('Plataforma', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('Plataforma', vars=dict(keywords=parametros)))
        else:
            redirect(URL('Plataforma'))

    if request.args(1) == 'ActivoTi':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ActivoTi.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoTi.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoTi.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoTi.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ActivoTi.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoTi.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoTi.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoTi.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ActivoTi', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ActivoTi', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ActivoTi'))

    if request.args(1) == 'TipoCumplimiento':
        if (auth.has_membership(role='auditManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoCumplimiento.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.TipoCumplimiento.id==request.args(0)).update(AprobacionJefeAuditoria='T')
            elif request.args(2)=='0':
                db(db.TipoCumplimiento.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.TipoCumplimiento.id==request.args(0)).update(AprobacionJefeAuditoria='F')
        elif (auth.has_membership(role='auditAnalyst')):
            if request.args(2)=='1':
                db(db.TipoCumplimiento.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.TipoCumplimiento.id==request.args(0)).update(AprobacionAnalistaAuditoria='T')
            elif request.args(2)=='0':
                db(db.TipoCumplimiento.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.TipoCumplimiento.id==request.args(0)).update(AprobacionAnalistaAuditoria='F')
        #redirect(URL('TipoCumplimiento', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TipoCumplimiento', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TipoCumplimiento'))
    '''
    if request.args(1) == 'CatalogoPolitica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.CatalogoPolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.CatalogoPolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
                #db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
                #db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionResponsableControl='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.CatalogoPolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.CatalogoPolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.CatalogoPolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        redirect(URL('CatalogoPolitica'))

    if request.args(1) == 'DetallePolitica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.DetallePolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.DetallePolitica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            if request.args(2)=='0':
                db(db.DetallePolitica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.DetallePolitica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        if (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.DetallePolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.DetallePolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            if request.args(2)=='0':
                db(db.DetallePolitica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.DetallePolitica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        redirect(URL('DetallePolitica'))
    '''
    if request.args(1) == 'EvaluacionControl':
        if (auth.has_membership(role='auditManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.EvaluacionControl.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.EvaluacionControl.id==request.args(0)).update(AprobacionJefeAuditoria='T')
            if request.args(2)=='0':
                db(db.EvaluacionControl.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.EvaluacionControl.id==request.args(0)).update(AprobacionJefeAuditoria='F')
        if (auth.has_membership(role='auditAnalyst')):
            if request.args(2)=='1':
                db(db.EvaluacionControl.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.EvaluacionControl.id==request.args(0)).update(AprobacionAnalistaAuditoria='T')
            if request.args(2)=='0':
                db(db.EvaluacionControl.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.EvaluacionControl.id==request.args(0)).update(AprobacionAnalistaAuditoria='F')
        if (auth.has_membership(role='controlResp')):
            if request.args(2)=='1':
                db(db.EvaluacionControl.id==request.args(0)).update(LogResponsableControl=signature)
                db(db.EvaluacionControl.id==request.args(0)).update(AprobacionResponsableControl='T')
            if request.args(2)=='0':
                db(db.EvaluacionControl.id==request.args(0)).update(LogResponsableControl=signature)
                db(db.EvaluacionControl.id==request.args(0)).update(AprobacionResponsableControl='F')
        #redirect(URL('EvaluacionControl', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('EvaluacionControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('EvaluacionControl'))

    if request.args(1) == 'AlcanceRevision':
        if (auth.has_membership(role='auditManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.AlcanceRevision.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.AlcanceRevision.id==request.args(0)).update(AprobacionJefeAuditoria='T')
            if request.args(2)=='0':
                db(db.AlcanceRevision.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.AlcanceRevision.id==request.args(0)).update(AprobacionJefeAuditoria='F')
        if (auth.has_membership(role='auditAnalyst')):
            if request.args(2)=='1':
                db(db.AlcanceRevision.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.AlcanceRevision.id==request.args(0)).update(AprobacionAnalistaAuditoria='T')
            if request.args(2)=='0':
                db(db.AlcanceRevision.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.AlcanceRevision.id==request.args(0)).update(AprobacionAnalistaAuditoria='F')
        #redirect(URL('AlcanceRevision', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('AlcanceRevision', vars=dict(keywords=parametros)))
        else:
            redirect(URL('AlcanceRevision'))

    if request.args(1) == 'TipoRevision':
        if (auth.has_membership(role='auditManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoRevision.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.TipoRevision.id==request.args(0)).update(AprobacionJefeAuditoria='T')
            if request.args(2)=='0':
                db(db.TipoRevision.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.TipoRevision.id==request.args(0)).update(AprobacionJefeAuditoria='F')
        if (auth.has_membership(role='auditAnalyst')):
            if request.args(2)=='1':
                db(db.TipoRevision.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.TipoRevision.id==request.args(0)).update(AprobacionAnalistaAuditoria='T')
            if request.args(2)=='0':
                db(db.TipoRevision.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.TipoRevision.id==request.args(0)).update(AprobacionAnalistaAuditoria='F')
        #redirect(URL('TipoRevision', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TipoRevision', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TipoRevision'))

    if request.args(1) == 'TipoIncidenteSeguridad':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TipoIncidenteSeguridad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoIncidenteSeguridad.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoIncidenteSeguridad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TipoIncidenteSeguridad.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TipoIncidenteSeguridad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoIncidenteSeguridad.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TipoIncidenteSeguridad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TipoIncidenteSeguridad.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('TipoIncidenteSeguridad', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('TipoIncidenteSeguridad', vars=dict(keywords=parametros)))
        else:
            redirect(URL('TipoIncidenteSeguridad'))

    if request.args(1) == 'ActivoTiRegion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ActivoTiRegion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoTiRegion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoTiRegion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoTiRegion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ActivoTiRegion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoTiRegion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoTiRegion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoTiRegion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ActivoTiRegion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ActivoTiRegion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ActivoTiRegion'))

    if request.args(1) == 'ActivoTiActivoInformacion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ActivoTiActivoInformacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoTiActivoInformacion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoTiActivoInformacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoTiActivoInformacion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ActivoTiActivoInformacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoTiActivoInformacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoTiActivoInformacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoTiActivoInformacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ActivoTiRegion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ActivoTiActivoInformacion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ActivoTiActivoInformacion'))

    if request.args(1) == 'IncidenteSeguridad':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.IncidenteSeguridad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.IncidenteSeguridad.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.IncidenteSeguridad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.IncidenteSeguridad.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.IncidenteSeguridad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.IncidenteSeguridad.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.IncidenteSeguridad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.IncidenteSeguridad.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('IncidenteSeguridad', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('IncidenteSeguridad', vars=dict(keywords=parametros)))
        else:
            redirect(URL('IncidenteSeguridad'))

    if request.args(1) == 'ActivoTiPlataforma':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ActivoTiPlataforma.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoTiPlataforma.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoTiPlataforma.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoTiPlataforma.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ActivoTiPlataforma.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoTiPlataforma.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoTiPlataforma.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoTiPlataforma.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ActivoTiPlataforma', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ActivoTiPlataforma', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ActivoTiPlataforma'))

    if request.args(1) == 'ActivoTiProceso':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ActivoTiProceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoTiProceso.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoTiProceso.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoTiProceso.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ActivoTiProceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoTiProceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoTiProceso.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoTiProceso.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ActivoTiProceso', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ActivoTiProceso', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ActivoTiProceso'))

    if request.args(1) == 'ActivoInformacionRegulacion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ActivoInformacionRegulacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoInformacionRegulacion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoInformacionRegulacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ActivoInformacionRegulacion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ActivoInformacionRegulacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoInformacionRegulacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ActivoInformacionRegulacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ActivoInformacionRegulacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ActivoInformacionRegulacion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ActivoInformacionRegulacion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ActivoInformacionRegulacion'))

    if request.args(1) == 'ProcesoActivoInformacion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ProcesoActivoInformacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoActivoInformacion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoActivoInformacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ProcesoActivoInformacion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ProcesoActivoInformacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoActivoInformacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ProcesoActivoInformacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ProcesoActivoInformacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if request.args(3):
            redirect(URL('ProcesoActivoInformacion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ProcesoActivoInformacion'))
    '''
    if request.args(1) == 'IconoNodo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.IconoNodo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.IconoNodo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.IconoNodo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.IconoNodo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.IconoNodo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.IconoNodo.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.IconoNodo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.IconoNodo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('IconoNodo', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('IconoNodo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('IconoNodo'))

    if request.args(1) == 'Nodo':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Nodo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Nodo.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.Nodo.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Nodo.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.Nodo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Nodo.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.Nodo.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Nodo.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('Nodo', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('Nodo', vars=dict(keywords=parametros)))
        else:
            redirect(URL('Nodo'))

    if request.args(1) == 'Arista':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Arista.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Arista.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.Arista.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Arista.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.Arista.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Arista.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.Arista.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Arista.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('Arista', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('Arista', vars=dict(keywords=parametros)))
        else:
            redirect(URL('Arista'))

    if request.args(1) == 'ArquitecturaPregunta':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ArquitecturaPregunta.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ArquitecturaPregunta.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ArquitecturaPregunta.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ArquitecturaPregunta.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ArquitecturaPregunta.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ArquitecturaPregunta.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ArquitecturaPregunta.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ArquitecturaPregunta.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ArquitecturaPregunta', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ArquitecturaPregunta', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ArquitecturaPregunta'))

    if request.args(1) == 'ArquitecturaSistema':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ArquitecturaSistema.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ArquitecturaSistema.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ArquitecturaSistema.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ArquitecturaSistema.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ArquitecturaSistema.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ArquitecturaSistema.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ArquitecturaSistema.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ArquitecturaSistema.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('ArquitecturaSistema', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('ArquitecturaSistema', vars=dict(keywords=parametros)))
        else:
            redirect(URL('ArquitecturaSistema'))

    if request.args(1) == 'Auditoria':
        if (auth.has_membership(role='auditManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Auditoria.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.Auditoria.id==request.args(0)).update(AprobacionJefeAuditoria='T')
            if request.args(2)=='0':
                db(db.Auditoria.id==request.args(0)).update(LogJefeAuditoria=signature)
                db(db.Auditoria.id==request.args(0)).update(AprobacionJefeAuditoria='F')
        if (auth.has_membership(role='auditAnalyst')):
            if request.args(2)=='1':
                db(db.Auditoria.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.Auditoria.id==request.args(0)).update(AprobacionAnalistaAuditoria='T')
            if request.args(2)=='0':
                db(db.Auditoria.id==request.args(0)).update(LogAnalistaAuditoria=signature)
                db(db.Auditoria.id==request.args(0)).update(AprobacionAnalistaAuditoria='F')
        if (auth.has_membership(role='controlResp')):
            if request.args(2)=='1':
                db(db.Auditoria.id==request.args(0)).update(LogResponsableControl=signature)
                db(db.Auditoria.id==request.args(0)).update(AprobacionResponsableControl='T')
            if request.args(2)=='0':
                db(db.Auditoria.id==request.args(0)).update(LogResponsableControl=signature)
                db(db.Auditoria.id==request.args(0)).update(AprobacionResponsableControl='F')
        #redirect(URL('Auditoria', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('Auditoria', vars=dict(keywords=parametros)))
        else:
            redirect(URL('Auditoria'))
    '''
    if request.args(1) == 'BenchVersion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.BenchVersion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.BenchVersion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.BenchVersion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.BenchVersion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.BenchVersion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.BenchVersion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.BenchVersion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.BenchVersion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('tool', 'BenchVersion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('default', 'BenchVersion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'BenchVersion'))

    if request.args(1) == 'PruebaWeb':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.PruebaWeb.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.PruebaWeb.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.PruebaWeb.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.PruebaWeb.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.PruebaWeb.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.PruebaWeb.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.PruebaWeb.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.PruebaWeb.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('tool', 'BenchVersion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('default', 'PruebaWeb', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'PruebaWeb'))

    if request.args(1) == 'BenchObjetivoControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.BenchObjetivoControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.BenchObjetivoControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.BenchObjetivoControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.BenchObjetivoControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.BenchObjetivoControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.BenchObjetivoControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.BenchObjetivoControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.BenchObjetivoControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('tool', 'BenchObjetivoControl', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('default', 'BenchObjetivoControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'BenchObjetivoControl'))
        
    if request.args(1) == 'BenchControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.BenchControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.BenchControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.BenchControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.BenchControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.BenchControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.BenchControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.BenchControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.BenchControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('tool', 'BenchControl', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('default', 'BenchControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'BenchControl'))
        
    if request.args(1) == 'BenchEvaluacion':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.BenchEvaluacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.BenchEvaluacion.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.BenchEvaluacion.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.BenchEvaluacion.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.BenchEvaluacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.BenchEvaluacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.BenchEvaluacion.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.BenchEvaluacion.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('tool', 'BenchEvaluacion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('default', 'BenchEvaluacion', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'BenchEvaluacion'))

    if request.args(1) == 'TestSeguridad':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.TestSeguridad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TestSeguridad.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.TestSeguridad.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.TestSeguridad.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.TestSeguridad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TestSeguridad.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.TestSeguridad.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.TestSeguridad.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if request.args(3):
            redirect(URL('default', 'PruebaSeguridad', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'PruebaSeguridad'))

    if request.args(1) == 'AlcanceControl':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.AlcanceControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AlcanceControl.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.AlcanceControl.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.AlcanceControl.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.AlcanceControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AlcanceControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.AlcanceControl.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.AlcanceControl.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('tool', 'BenchEvaluacion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('default', 'AlcanceControl', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'AlcanceControl'))
    '''
    if request.args(1) == 'ValorMetricaSeguridadTi':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        #redirect(URL('tool', 'BenchEvaluacion', vars=dict(keywords=parametros)))
        if request.args(3):
            redirect(URL('default', 'ValorMetricaSeguridadTi', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'ValorMetricaSeguridadTi'))
    '''
    if request.args(1) == 'GrupoMetrica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.GrupoMetrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.GrupoMetrica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.GrupoMetrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.GrupoMetrica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.GrupoMetrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.GrupoMetrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.GrupoMetrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.GrupoMetrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if request.args(3):
            redirect(URL('default', 'GrupoMetrica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'GrupoMetrica'))
    if request.args(1) == 'Metrica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.Metrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Metrica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.Metrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.Metrica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.Metrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Metrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.Metrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.Metrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if request.args(3):
            redirect(URL('default', 'Metrica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'Metrica'))
    if request.args(1) == 'ValorMetrica':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ValorMetrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ValorMetrica.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ValorMetrica.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ValorMetrica.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ValorMetrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ValorMetrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ValorMetrica.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ValorMetrica.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if request.args(3):
            redirect(URL('default', 'ValorMetrica', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'ValorMetrica'))
    if request.args(1) == 'ValorMetricaSeguridadTi':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ValorMetricaSeguridadTi.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if request.args(3):
            redirect(URL('default', 'ValorMetricaSeguridadTi', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'ValorMetricaSeguridadTi'))

    if request.args(1) == 'ControlCvss':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.ControlCvss.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ControlCvss.id==request.args(0)).update(AprobacionJefeRiesgo='T')
            elif request.args(2)=='0':
                db(db.ControlCvss.id==request.args(0)).update(LogJefeRiesgo=signature)
                db(db.ControlCvss.id==request.args(0)).update(AprobacionJefeRiesgo='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.ControlCvss.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ControlCvss.id==request.args(0)).update(AprobacionAnalistaRiesgo='T')
            elif request.args(2)=='0':
                db(db.ControlCvss.id==request.args(0)).update(LogAnalistaRiesgo=signature)
                db(db.ControlCvss.id==request.args(0)).update(AprobacionAnalistaRiesgo='F')
        if request.args(3):
            redirect(URL('default', 'ControlCvss', vars=dict(keywords=parametros)))
        else:
            redirect(URL('default', 'ControlCvss'))

@auth.requires_login()
def ActualizaAprobacion(Tabla):
    if 'edit' in request.args:
        if Tabla=='TipoObjetivo':
            db(db.TipoObjetivo.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TipoObjetivo.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ClasificacionInformacion':
            db(db.ClasificacionInformacion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ClasificacionInformacion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='TipoDato':
            db(db.TipoDato.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TipoDato.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ClasificacionRiesgo':
            db(db.ClasificacionRiesgo.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ClasificacionRiesgo.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='AnalisisRiesgoObjetivoOrganizacion':
            db(db.AnalisisRiesgoObjetivoOrganizacion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.AnalisisRiesgoObjetivoOrganizacion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='AnalisisRiesgoClasificacionRiesgo':
            db(db.AnalisisRiesgoClasificacionRiesgo.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.AnalisisRiesgoClasificacionRiesgo.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='TratamientoRiesgoAnalisisRiesgo':
            db(db.TratamientoRiesgoAnalisisRiesgo.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TratamientoRiesgoAnalisisRiesgo.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='TipoTratamientoRiesgo':
            db(db.TipoTratamientoRiesgo.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TipoTratamientoRiesgo.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='TipoVulnerabilidadAnalisisRiesgo':
            db(db.TipoVulnerabilidadAnalisisRiesgo.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TipoVulnerabilidadAnalisisRiesgo.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='TipoControl':
            db(db.TipoControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TipoControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='GrupoControl':
            db(db.GrupoControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.GrupoControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='Region':
            db(db.Region.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.Region.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='RegionPolitica':
            db(db.RegionPolitica.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.RegionPolitica.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ClasificacionControl':
            db(db.ClasificacionControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ClasificacionControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='CatalogoControl':
            db(db.CatalogoControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.CatalogoControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ObjetivoControl':
            db(db.ObjetivoControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ObjetivoControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='CatalogoControlBenchControl':
            db(db.CatalogoControlObjetivoControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.CatalogoControlObjetivoControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='DetallePoliticaBenchControl':
            db(db.DetallePoliticaBenchControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.DetallePoliticaBenchControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='Region':
            db(db.Region.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.Region.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ProcesoRegion':
            db(db.ProcesoRegion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ProcesoRegion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='CicloNegocio':
            db(db.CicloNegocio.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.CicloNegocio.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='TipoProceso':
            db(db.TipoProceso.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TipoProceso.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='MacroProceso':
            db(db.MacroProceso.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.MacroProceso.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ProcesoCicloNegocio':
            db(db.ProcesoCicloNegocio.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ProcesoCicloNegocio.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ProcesoTipoProceso':
            db(db.ProcesoTipoProceso.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ProcesoTipoProceso.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ProcesoMacroProceso':
            db(db.ProcesoMacroProceso.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ProcesoMacroProceso.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ProcesoPolitica':
            db(db.ProcesoPolitica.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ProcesoPolitica.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='Direccion':
            db(db.Direccion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.Direccion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='Proceso':
            db(db.Proceso.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.Proceso.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='NivelMadurez':
            db(db.NivelMadurez.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.NivelMadurez.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='CriterioImpacto':
            db(db.CriterioImpacto.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='CriterioProbabilidad':
            db(db.CriterioProbabilidad.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='CriterioRiesgo':
            db(db.CriterioRiesgo.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='ObjetivoOrganizacion':
            db(db.ObjetivoOrganizacion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='Organizacion':
            db(db.Organizacion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='AmbienteControl':
            db(db.AmbienteControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.AmbienteControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ActivoInformacion':
            db(db.ActivoInformacion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ActivoInformacion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='RolResponsabilidad':
            db(db.RolResponsabilidad.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.RolResponsabilidad.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='AnalisisRiesgo':
            db(db.AnalisisRiesgo.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.AnalisisRiesgo.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.AnalisisRiesgo.id==request.args[len(request.args)-1]).update(AprobacionDuenoRiesgo='F')
        if Tabla=='TratamientoRiesgo':
            if (auth.has_membership(role='admin') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst')):
                db(db.TratamientoRiesgo.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
                db(db.TratamientoRiesgo.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
                db(db.TratamientoRiesgo.id==request.args[len(request.args)-1]).update(AprobacionResponsableControl='F')
            elif (auth.has_membership(role='controlResp')):
                db(db.TratamientoRiesgo.id==request.args[len(request.args)-1]).update(AprobacionResponsableControl='F')
        if Tabla=='CatalogoPolitica':
            db(db.CatalogoPolitica.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.CatalogoPolitica.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='DetallePolitica':
            db(db.DetallePolitica.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.DetallePolitica.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='RegulacionDato':
            db(db.RegulacionDato.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.RegulacionDato.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='RegulacionPolitica':
            db(db.RegulacionPolitica.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.RegulacionPolitica.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='Metrica':
            db(db.Metrica.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.Metrica.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='GrupoMetrica':
            db(db.GrupoMetrica.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.GrupoMetrica.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ValorMetrica':
            db(db.ValorMetrica.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ValorMetrica.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ControlCvss':
            db(db.ControlCvss.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ControlCvss.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='TipoVulnerabilidad':
            db(db.TipoVulnerabilidad.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TipoVulnerabilidad.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='TipoCapaSistema':
            db(db.TipoCapaSistema.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TipoCapaSistema.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='Plataforma':
            db(db.Plataforma.id==request.args[len(request.args)-1]).update(AprobacionJefeAuditoria='F')
            db(db.Plataforma.id==request.args[len(request.args)-1]).update(AprobacionAnalistaAuditoria='F')
        if Tabla=='ActivoTi':
            db(db.ActivoTi.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ActivoTi.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='TipoCumplimiento':
            db(db.TipoCumplimiento.id==request.args[len(request.args)-1]).update(AprobacionJefeAuditoria='F')
            db(db.TipoCumplimiento.id==request.args[len(request.args)-1]).update(AprobacionAnalistaAuditoria='F')
        if Tabla=='SeguridadTi':
            db(db.SeguridadTi.id==request.args[len(request.args)-1]).update(AprobacionJefeAuditoria='F')
            db(db.SeguridadTi.id==request.args[len(request.args)-1]).update(AprobacionAnalistaAuditoria='F')
            db(db.SeguridadTi.id==request.args[len(request.args)-1]).update(AprobacionResponsableControl='F')
        if Tabla=='TipoIncidenteSeguridad':
            db(db.TipoIncidenteSeguridad.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TipoIncidenteSeguridad.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='IncidenteSeguridad':
            db(db.IncidenteSeguridad.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.IncidenteSeguridad.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ActivoTiRegion':
            db(db.ActivoTiRegion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ActivoTiRegion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ActivoTiPlataforma':
            db(db.ActivoTiPlataforma.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ActivoTiPlataforma.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ActivoTiProceso':
            db(db.ActivoTiProceso.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ActivoTiProceso.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ActivoInformacionRegulacion':
            db(db.ActivoInformacionRegulacion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ActivoInformacionRegulacion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ProcesoActivoInformacion':
            db(db.ProcesoActivoInformacion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ProcesoActivoInformacion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='ActivoTiActivoInformacion':
            db(db.ActivoTiActivoInformacion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ActivoTiActivoInformacion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='AuditoriaControl':
            db(db.AuditoriaControl.id==request.args[len(request.args)-1]).update(AprobacionJefeAuditoria='F')
            db(db.AuditoriaControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaAuditoria='F')
            db(db.AuditoriaControl.id==request.args[len(request.args)-1]).update(AprobacionResponsableControl='F')
        if Tabla=='EvaluacionControl':
            db(db.EvaluacionControl.id==request.args[len(request.args)-1]).update(AprobacionJefeAuditoria='F')
            db(db.EvaluacionControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaAuditoria='F')
            #db(db.EvaluacionControl.id==request.args[len(request.args)-1]).update(AprobacionResponsableControl='F')
        if Tabla=='IngresoProceso':
            db(db.IngresoProceso.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.IngresoProceso.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='IngresoCiclo':
            db(db.IngresoCiclo.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.IngresoCiclo.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='AlcanceRevision':
            db(db.AlcanceRevision.id==request.args[len(request.args)-1]).update(AprobacionJefeAuditoria='F')
            db(db.AlcanceRevision.id==request.args[len(request.args)-1]).update(AprobacionAnalistaAuditoria='F')
        if Tabla=='TipoRevision':
            db(db.TipoRevision.id==request.args[len(request.args)-1]).update(AprobacionJefeAuditoria='F')
            db(db.TipoRevision.id==request.args[len(request.args)-1]).update(AprobacionAnalistaAuditoria='F')
        if Tabla=='Documentacion':
            db(db.Documentacion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.Documentacion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='AutoControlConfiguracion':
            db2(db2.AutoControlConfiguracion.id==request.args[len(request.args)-1]).update(AprobacionJefeAuditoria='F')
            db2(db2.AutoControlConfiguracion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaAuditoria='F')
        if Tabla=='AutoControlCuestionario':
            db2(db2.AutoControlCuestionario.id==request.args[len(request.args)-1]).update(AprobacionJefeAuditoria='F')
            db2(db2.AutoControlCuestionario.id==request.args[len(request.args)-1]).update(AprobacionAnalistaAuditoria='F')
        if Tabla=='AreaImpacto':
            db(db.AreaImpacto.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.AreaImpacto.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='AreaProbabilidad':
            db(db.AreaProbabilidad.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.AreaProbabilidad.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='AreaImpactoCriterioImpacto':
            db(db.AreaImpactoCriterioImpacto.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.AreaImpactoCriterioImpacto.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='AreaProbabilidadCriterioProbabilidad':
            db(db.AreaProbabilidadCriterioProbabilidad.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.AreaProbabilidadCriterioProbabilidad.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='TratamientoRiesgoAreaImpacto':
            db(db.TratamientoRiesgoAreaImpacto.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.TratamientoRiesgoAreaImpacto.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='TratamientoRiesgoAreaProbabilidad':
            db(db.TratamientoRiesgoAreaProbabilidad.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.TratamientoRiesgoAreaProbabilidad.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='BenchVersion':
            db(db.BenchVersion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.BenchVersion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='PruebaWeb':
            db(db.PruebaWeb.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.PruebaWeb.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='CatalogoControlBenchControl':
            db(db.CatalogoControlBenchControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.CatalogoControlBenchControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='AlcanceControl':
            db(db.AlcanceControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.AlcanceControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='ValorMetricaSeguridadTi':
            db(db.ValorMetricaSeguridadTi.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
            db(db.ValorMetricaSeguridadTi.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
        if Tabla=='BenchVersion':
            db(db.BenchVersion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.BenchVersion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='BenchObjetivoControl':
            db(db.BenchObjetivoControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.BenchObjetivoControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='BenchControl':
            db(db.BenchControl.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.BenchControl.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='BenchEvaluacion':
            db(db.BenchEvaluacion.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.BenchEvaluacion.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla=='TestSeguridad':
            db(db.TestSeguridad.id==request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.TestSeguridad.id==request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla == 'GrupoMetrica':
            db(db.GrupoMetrica.id == request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.GrupoMetrica.id == request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla == 'Metrica':
            db(db.Metrica.id == request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.Metrica.id == request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla == 'ValorMetrica':
            db(db.ValorMetrica.id == request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ValorMetrica.id == request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
        if Tabla == 'ValorMetricaSeguridadTi':
            db(db.ValorMetricaSeguridadTi.id == request.args[len(request.args)-1]).update(AprobacionJefeRiesgo='F')
            db(db.ValorMetricaSeguridadTi.id == request.args[len(request.args)-1]).update(AprobacionAnalistaRiesgo='F')
    else:
        pass

@auth.requires_login()
#if auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
@auth.requires( auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin') )
def CvssImpacto():
    TratamientoRiesgoId = db(db.TratamientoRiesgo.ActivoTiId==request.args(0)).select(db.TratamientoRiesgo.id)
    for i in TratamientoRiesgoId:
        db.ValorMetricaSeguridadTi.update_or_insert(( (db.ValorMetricaSeguridadTi.TratamientoRiesgoId==i) & ((db.ValorMetricaSeguridadTi.ValorMetricaId==14 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==15 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==16 ))), TratamientoRiesgoId=i, ValorMetricaId=request.args(1), Descripcion=base64.b64decode(request.args(4)) )
    for i in TratamientoRiesgoId:
        db.ValorMetricaSeguridadTi.update_or_insert(( (db.ValorMetricaSeguridadTi.TratamientoRiesgoId==i) & ((db.ValorMetricaSeguridadTi.ValorMetricaId==17 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==18 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==19 ))), TratamientoRiesgoId=i, ValorMetricaId=request.args(2), Descripcion=base64.b64decode(request.args(4)) )
    for i in TratamientoRiesgoId:
        db.ValorMetricaSeguridadTi.update_or_insert(( (db.ValorMetricaSeguridadTi.TratamientoRiesgoId==i) & ((db.ValorMetricaSeguridadTi.ValorMetricaId==20 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==21 ) | (db.ValorMetricaSeguridadTi.ValorMetricaId==22 ))), TratamientoRiesgoId=i, ValorMetricaId=request.args(3), Descripcion=base64.b64decode(request.args(4)) )
    redirect(URL('default','ActivoTi'))

@auth.requires_login()
#if auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
@auth.requires( auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin') )
def CvssEvaluation():
    if request.args(3):
        parametros = base64.b64decode(request.args(3))
    else:
        pass

    #ActualizaAprobacion(request.args(1))
    #db.auth_user.update_or_insert((db.auth_user.id==4),first_name="riskAnalyst", last_name="riskAnalyst", email="riskAnalyst@mail.com", username="riskAnalyst", password=db.auth_user.password.validate('Password01')[0])
    #return dict()
    #CvssEvaluation
    #db(db.SeguridadTi.AprobacionJefeAuditoria == 'T').select(db.SeguridadTi.id, db.SeguridadTi.ResponsableControl):
    #--------------------------------
    #Asignacion inicial de valores
    #--------------------------------
    #cvssBaseAV=0.85 #Network
    #cvssBaseAVString="N"
    #cvssBaseAC=0.77 #Low
    #cvssBaseACString="L"
    #cvssBasePR=0.85 #None
    #cvssBasePRString="N"
    #cvssBaseUI=0.85 #None
    #cvssBaseUIString="N"
    #cvssBaseS =7.52 #Changed
    #cvssBaseSString="C"
    #cvssBaseC =0.56 #High
    #cvssBaseCString="H"
    #cvssBaseI =0.56 #High
    #cvssBaseIString="H"
    #cvssBaseA =0.56 #High
    #cvssBaseAString="H"
    #changed=1
    cvssBaseAV=0.2 #Physical
    cvssBaseAVString="P"
    cvssBaseAC=0.44 #High
    cvssBaseACString="H"
    cvssBasePR=0.27 #High
    cvssBasePRString="H"
    cvssBaseUI=0.62 #Required
    cvssBaseUIString="R"
    cvssBaseS =6.42 #Unhanged
    cvssBaseSString="U"
    cvssBaseC =0 #None
    cvssBaseCString="N"
    cvssBaseI =0 #None
    cvssBaseIString="N"
    cvssBaseA =0 #None
    cvssBaseAString="N"
    changed=0
    #---------------------
    #Variables temporales
    #---------------------
    cvssTempE  = 1 
    cvssTempEString  = "X" 
    cvssTempRL = 1
    cvssTempRLString = "X"
    cvssTempRC = 1
    cvssTempRCString = "X"
    #---------------------
    #Variables Ambientales
    #---------------------
    cvssEnvCR  = 1.5
    cvssEnvIR  = 1.5
    cvssEnvAR  = 1.5
    cvssEnvMAV = 0.85
    cvssEnvMAC = 0.77
    cvssEnvMPR = 0.85
    cvssEnvMUI = 0.85
    cvssEnvMS  = 7.52
    cvssEnvMC  = 0.56
    cvssEnvMI  = 0.56
    cvssEnvMA  = 0.56
    #ISS = 1-[(1-cvssBaseC) (1-cvssBaseI) (1-cvssBaseA)]
    #Exploitability = (8.22) (cvssBaseAV) (cvssBaseAC) (cvssBasePR) (cvssBaseUI)
    #Impact = [((7.52) (ISS - 0.029)) - ( (3.25) ((ISS - 0.02)^15)) ]
    #BaseScore = round( min( 1.08(impact*Exploitability)  , 10) )

    cvss = db(db.ValorMetricaSeguridadTi.TratamientoRiesgoId==request.args(0)).select(db.ValorMetricaSeguridadTi.ALL)
    for s in cvss:
        #-----------------------------------------------------------------------
        #El grupo metrica 5 corresponde a 5 | Base Metric Group | S | Scope (S)
        #Changed(C) y Unchanged(U)
        #-----------------------------------------------------------------------
        #if s.ValorMetricaId.GrupoMetricaId==5:
        if s.ValorMetricaId.MetricaId==5:
            #----------------------------
            #Scope (S)    Changed (C)	  
            #----------------------------
            if s.ValorMetricaId==12:
                changed=1
            #----------------------------
            #Scope (S)    Unchanged (U)	  
            #----------------------------
            elif s.ValorMetricaId==13:
                changed=0

    for i in cvss:

        if i.ValorMetricaId.MetricaId==1:
        #if i.ValorMetricaId.Nombre=="Attack Vector (AV)":
            cvssBaseAV=i.ValorMetricaId.ValorNumerico
            cvssBaseAVString=i.ValorMetricaId.ValorMetrica
        #else:
        #    cvssBaseAV = 0.85
        if i.ValorMetricaId.MetricaId==2:
            cvssBaseAC=i.ValorMetricaId.ValorNumerico
            cvssBaseACString=i.ValorMetricaId.ValorMetrica

        if i.ValorMetricaId.MetricaId==3 and changed==0:
            cvssBasePR=i.ValorMetricaId.ValorNumerico
            cvssBasePRString=i.ValorMetricaId.ValorMetrica
        elif i.ValorMetricaId.MetricaId==3 and changed==1 and i.ValorMetricaId==7: #Changed (C) & PR High (H)
            cvssBasePR=0.5
            cvssBasePRString=i.ValorMetricaId.ValorMetrica
        elif i.ValorMetricaId.MetricaId==3 and changed==1 and i.ValorMetricaId==8: #Changed (C) & PR Low (L)
            cvssBasePR=0.68
            cvssBasePRString=i.ValorMetricaId.ValorMetrica

        if i.ValorMetricaId.MetricaId==4:
            cvssBaseUI=i.ValorMetricaId.ValorNumerico
            cvssBaseUIString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==5:
            cvssBaseS=i.ValorMetricaId.ValorNumerico
            cvssBaseSString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==6:
            cvssBaseC=i.ValorMetricaId.ValorNumerico
            cvssBaseCString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==7:
            cvssBaseI=i.ValorMetricaId.ValorNumerico
            cvssBaseIString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==8:
            cvssBaseA=i.ValorMetricaId.ValorNumerico
            cvssBaseAString=i.ValorMetricaId.ValorMetrica
        #--------------------
        #Metricas temporales
        #--------------------
        if i.ValorMetricaId.MetricaId==9:
            cvssTempE=i.ValorMetricaId.ValorNumerico
            cvssTempEString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==10:
            cvssTempRL=i.ValorMetricaId.ValorNumerico
            cvssTempRLString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==11:
            cvssTempRC=i.ValorMetricaId.ValorNumerico
            cvssTempRCString=i.ValorMetricaId.ValorMetrica

    ISS = 1-( (1-cvssBaseC) * (1-cvssBaseI) * (1-cvssBaseA) )
    #Impact = ( ((7.52) * (ISS - 0.029)) - ( (3.25) * ((ISS - 0.02)**15)) )
    Impact = ( ((7.52) * (ISS - 0.029)) - ( (3.25) * (math.pow((ISS - 0.02), 15))) )

        #if i.ValorMetricaId.GrupoMetricaId==5 and i.ValorMetricaId==13:
    for i in cvss:
        if i.ValorMetricaId==13: #Unchanged (U)	
            Impact = (6.42) * (ISS)
        elif i.ValorMetricaId==12:
            Impact = ( ((7.52) * (ISS - 0.029)) - ( (3.25) * (math.pow((ISS - 0.02), 15))) )

    #ISS = 1-[(1-cvssBaseC) (1-cvssBaseI) (1-cvssBaseA)]
    Exploitability = (8.22) * (cvssBaseAV) * (cvssBaseAC) * (cvssBasePR) * (cvssBaseUI)
    #Impact = [((7.52) (ISS - 0.029)) - ( (3.25) ((ISS - 0.02)^15)) ]
    BaseScore = roundup( min( 1.08*(Impact + Exploitability)  , 10) )

    if Impact <=0:
        BaseScore=0

    for i in cvss:
        if i.ValorMetricaId==13: #Unchanged (U)	
            BaseScore = roundup( min( Impact + Exploitability  , 10) )
        elif i.ValorMetricaId==12:
            BaseScore = roundup( min( (1.08) * (Impact + Exploitability)  , 10) )
    #-------------------------
    #Calculo metrica temporal
    #-------------------------
    TemScore = roundup(BaseScore * cvssTempE * cvssTempRL * cvssTempRC )
    
    VectorString = "CVSS:3.1/AV:"+str(cvssBaseAVString)+"/AC:"+str(cvssBaseACString)+"/PR:"+str(cvssBasePRString)+"/UI:"+str(cvssBaseUIString)+"/S:"+str(cvssBaseSString)+"/C:"+str(cvssBaseCString)+"/I:"+str(cvssBaseIString)+"/A:"+str(cvssBaseAString)
    #VectorString = "CVSS:3.1/AV:"+str(cvssBaseAVString)+"/AC:"+str(cvssBaseACString)+"/PR:"+str(cvssBasePRString)+"/UI:"+str(cvssBaseUIString)+"/S:"+str(cvssBaseSString)+"/C:"+str(cvssBaseCString)+"/I:"+str(cvssBaseIString)+"/A:"+str(cvssBaseAString)+"/E:"+str(cvssTempE)+"/RL:"+str(cvssTempRL)+"/RC:"+str(cvssTempRC)
    #db.TratamientoRiesgo.update_or_insert(db.TratamientoRiesgo.id==request.args(0) , CuantificacionCVSS=BaseScore, VectorCVSS=VectorString)
    db.TratamientoRiesgo.update_or_insert(db.TratamientoRiesgo.id==request.args(0) , CuantificacionCVSS=BaseScore, VectorCVSS=VectorString)

    if request.args(3):
        redirect(URL('TratamientoRiesgo', vars=dict(keywords=parametros)))
    else:
        redirect(URL('TratamientoRiesgo'))


@auth.requires_login()
#if auth.has_membership(role='auditAnalyst') or auth.has_membership(role='auditManager') or auth.has_membership(role='admin'):
@auth.requires( auth.has_membership(role='riskAnalyst') or auth.has_membership(role='riskManager') or auth.has_membership(role='admin') )
def CvssEvaluation1():
    if request.args(3):
        parametros = base64.b64decode(request.args(3))
    else:
        pass

    cvssBaseAV=0.2 #Physical
    cvssBaseAVString="P"
    cvssBaseAC=0.44 #High
    cvssBaseACString="H"
    cvssBasePR=0.27 #High
    cvssBasePRString="H"
    cvssBaseUI=0.62 #Required
    cvssBaseUIString="R"
    cvssBaseS =6.42 #Unhanged
    cvssBaseSString="U"
    cvssBaseC =0 #None
    cvssBaseCString="N"
    cvssBaseI =0 #None
    cvssBaseIString="N"
    cvssBaseA =0 #None
    cvssBaseAString="N"
    changed=0
    #---------------------
    #Variables temporales
    #---------------------
    cvssTempE  = 1 
    cvssTempEString  = "X" 
    cvssTempRL = 1
    cvssTempRLString = "X"
    cvssTempRC = 1
    cvssTempRCString = "X"
    #---------------------
    #Variables Ambientales
    #---------------------
    cvssEnvCR  = 1.5
    cvssEnvIR  = 1.5
    cvssEnvAR  = 1.5
    cvssEnvMAV = 0.85
    cvssEnvMAC = 0.77
    cvssEnvMPR = 0.85
    cvssEnvMUI = 0.85
    cvssEnvMS  = 7.52
    cvssEnvMC  = 0.56
    cvssEnvMI  = 0.56
    cvssEnvMA  = 0.56

    cvss = db(db.ControlCvss.EvaluacionControlId==request.args(0)).select(db.ControlCvss.ALL)
    for s in cvss:
        #-----------------------------------------------------------------------
        #El grupo metrica 5 corresponde a 5 | Base Metric Group | S | Scope (S)
        #Changed(C) y Unchanged(U)
        #-----------------------------------------------------------------------
        #if s.ValorMetricaId.GrupoMetricaId==5:
        if s.ValorMetricaId.MetricaId==5:
            #----------------------------
            #Scope (S)    Changed (C)	  
            #----------------------------
            if s.ValorMetricaId==12:
                changed=1
            #----------------------------
            #Scope (S)    Unchanged (U)	  
            #----------------------------
            elif s.ValorMetricaId==13:
                changed=0

    for i in cvss:

        if i.ValorMetricaId.MetricaId==1:
        #if i.ValorMetricaId.Nombre=="Attack Vector (AV)":
            cvssBaseAV=i.ValorMetricaId.ValorNumerico
            cvssBaseAVString=i.ValorMetricaId.ValorMetrica
        #else:
        #    cvssBaseAV = 0.85
        if i.ValorMetricaId.MetricaId==2:
            cvssBaseAC=i.ValorMetricaId.ValorNumerico
            cvssBaseACString=i.ValorMetricaId.ValorMetrica

        if i.ValorMetricaId.MetricaId==3 and changed==0:
            cvssBasePR=i.ValorMetricaId.ValorNumerico
            cvssBasePRString=i.ValorMetricaId.ValorMetrica
        elif i.ValorMetricaId.MetricaId==3 and changed==1 and i.ValorMetricaId==7: #Changed (C) & PR High (H)
            cvssBasePR=0.5
            cvssBasePRString=i.ValorMetricaId.ValorMetrica
        elif i.ValorMetricaId.MetricaId==3 and changed==1 and i.ValorMetricaId==8: #Changed (C) & PR Low (L)
            cvssBasePR=0.68
            cvssBasePRString=i.ValorMetricaId.ValorMetrica

        if i.ValorMetricaId.MetricaId==4:
            cvssBaseUI=i.ValorMetricaId.ValorNumerico
            cvssBaseUIString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==5:
            cvssBaseS=i.ValorMetricaId.ValorNumerico
            cvssBaseSString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==6:
            cvssBaseC=i.ValorMetricaId.ValorNumerico
            cvssBaseCString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==7:
            cvssBaseI=i.ValorMetricaId.ValorNumerico
            cvssBaseIString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==8:
            cvssBaseA=i.ValorMetricaId.ValorNumerico
            cvssBaseAString=i.ValorMetricaId.ValorMetrica
        #--------------------
        #Metricas temporales
        #--------------------
        if i.ValorMetricaId.MetricaId==9:
            cvssTempE=i.ValorMetricaId.ValorNumerico
            cvssTempEString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==10:
            cvssTempRL=i.ValorMetricaId.ValorNumerico
            cvssTempRLString=i.ValorMetricaId.ValorMetrica
        if i.ValorMetricaId.MetricaId==11:
            cvssTempRC=i.ValorMetricaId.ValorNumerico
            cvssTempRCString=i.ValorMetricaId.ValorMetrica

    ISS = 1-( (1-cvssBaseC) * (1-cvssBaseI) * (1-cvssBaseA) )
    #Impact = ( ((7.52) * (ISS - 0.029)) - ( (3.25) * ((ISS - 0.02)**15)) )
    Impact = ( ((7.52) * (ISS - 0.029)) - ( (3.25) * (math.pow((ISS - 0.02), 15))) )

        #if i.ValorMetricaId.GrupoMetricaId==5 and i.ValorMetricaId==13:
    for i in cvss:
        if i.ValorMetricaId==13: #Unchanged (U)	
            Impact = (6.42) * (ISS)
        elif i.ValorMetricaId==12:
            Impact = ( ((7.52) * (ISS - 0.029)) - ( (3.25) * (math.pow((ISS - 0.02), 15))) )

    #ISS = 1-[(1-cvssBaseC) (1-cvssBaseI) (1-cvssBaseA)]
    Exploitability = (8.22) * (cvssBaseAV) * (cvssBaseAC) * (cvssBasePR) * (cvssBaseUI)
    #Impact = [((7.52) (ISS - 0.029)) - ( (3.25) ((ISS - 0.02)^15)) ]
    BaseScore = roundup( min( 1.08*(Impact + Exploitability)  , 10) )

    if Impact <=0:
        BaseScore=0

    for i in cvss:
        if i.ValorMetricaId==13: #Unchanged (U)	
            BaseScore = roundup( min( Impact + Exploitability  , 10) )
        elif i.ValorMetricaId==12:
            BaseScore = roundup( min( (1.08) * (Impact + Exploitability)  , 10) )

    #-------------------------
    #Calculo metrica temporal
    #-------------------------
    TemScore = roundup(BaseScore * cvssTempE * cvssTempRL * cvssTempRC )
    
    VectorString = "CVSS:3.1/AV:"+str(cvssBaseAVString)+"/AC:"+str(cvssBaseACString)+"/PR:"+str(cvssBasePRString)+"/UI:"+str(cvssBaseUIString)+"/S:"+str(cvssBaseSString)+"/C:"+str(cvssBaseCString)+"/I:"+str(cvssBaseIString)+"/A:"+str(cvssBaseAString)
    #VectorString = "CVSS:3.1/AV:"+str(cvssBaseAVString)+"/AC:"+str(cvssBaseACString)+"/PR:"+str(cvssBasePRString)+"/UI:"+str(cvssBaseUIString)+"/S:"+str(cvssBaseSString)+"/C:"+str(cvssBaseCString)+"/I:"+str(cvssBaseIString)+"/A:"+str(cvssBaseAString)+"/E:"+str(cvssTempE)+"/RL:"+str(cvssTempRL)+"/RC:"+str(cvssTempRC)

    #db.TratamientoRiesgo.update_or_insert(db.TratamientoRiesgo.id==request.args(0) , CuantificacionCVSS=BaseScore, VectorCVSS=VectorString)
    db.EvaluacionControl.update_or_insert(db.EvaluacionControl.id==request.args(0) , CuantificacionCVSS=BaseScore, VectorCVSS=VectorString)

    if request.args(3):
        redirect(URL('EvaluacionControl', vars=dict(keywords=parametros)))
    else:
        redirect(URL('EvaluacionControl'))

        
def roundup(num):
    return D(math.ceil(num * 10) / 10).quantize(D("0.1"))

@auth.requires_login()
def EmailConfig():
    if auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='admin') :
        links = [lambda row: A('SMTP Test',_class='button btn btn-warning',_href=URL("default","testSMTP", args=[row.id, row.server_c, row.port_c, row.tls_2, row.openRelay, base64.b64encode(str(row.login_c)), base64.b64encode(str(row.password_c)), row.tls_c]))]
        form = SQLFORM.grid(db.EmailConfig, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
        return dict(form=form)
    else:
        redirect(URL('default','index'))

'''
@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='admin'))
def testSMTP():
    socket.setdefaulttimeout(30)
    host = request.args(1)
    port = request.args(2)
    user = base64.b64decode(request.args(5))
    pasw = base64.b64decode(request.args(6))
    testTime = time.strftime("%c")
    try:
        #----------------
        #Crear objeto 
        #----------------
        if request.args(3)=='True':
            server = smtplib.SMTP_SSL()
        elif request.args(3)=='False':
            server = smtplib.SMTP()
        #---------------------------------------------------
        #Si es openrelay se realiza conexion sin autenticar
        #---------------------------------------------------
        if request.args(4)=='True':
            smtpRes = server.connect(host, port)
            db.phishingConfig.update_or_insert((db.phishingConfig.id==request.args(0)), testResult=str(str(testTime) + "|" + str(smtpRes) ) )
        elif request.args(4)=='False':
            server.connect(host, port)
            if request.args(7)=='True':
                server.starttls()
            smtpRes = server.login(user, pasw)
            db.phishingConfig.update_or_insert((db.phishingConfig.id==request.args(0)), testResult=str(str(testTime) + "|" + str(smtpRes) )  )
        server.quit()
    except Exception, e:
            db.phishingConfig.update_or_insert((db.phishingConfig.id==request.args(0)), testResult=str(str(testTime) + "|" + str(e) ) )
    redirect(URL('default', 'EmailConfig'))
'''

@auth.requires_login()
def BarraIncidenteSistemaTI():
    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='iformationOwner') or auth.has_membership(role='admin') or auth.has_membership(role='guest') or auth.has_membership(role='controlResp'):
        return TableroIncidenteSeguridadTi()
    else:
        pass

@auth.requires_login()
def BarraTipoIncidenteSeguridadTI():
    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='iformationOwner') or auth.has_membership(role='admin') or auth.has_membership(role='guest') or auth.has_membership(role='controlResp'):
        return TableroIncidenteSeguridadTi()
    else:
        pass

@auth.requires_login()
def BarraRegionIncidenteSeguridadTI():
    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='iformationOwner') or auth.has_membership(role='admin') or auth.has_membership(role='guest') or auth.has_membership(role='controlResp'):
        return TableroIncidenteSeguridadTi()
    else:
        pass

@auth.requires_login()
def TableroIncidenteSeguridadTi():
    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='iformationOwner') or auth.has_membership(role='admin') or auth.has_membership(role='guest') or auth.has_membership(role='controlResp'):
        pass
    else:
        redirect(URL('default', 'index'))

    queryIncidenteSeguridad = (db.IncidenteSeguridad.TipoIncidenteSeguridadId==db.TipoIncidenteSeguridad.id) & (db.IncidenteSeguridad.ActivoTiRegionId==db.ActivoTiRegion.id) & (db.IncidenteSeguridad.AprobacionJefeRiesgo=='T')
    queryActivoTiRegion = (db.ActivoTiRegion.ActivoTiId==db.ActivoTi.id) & (db.ActivoTiRegion.RegionId==db.Region.id)

    Periodo = request.now.year
    Parametro = {}
    Parametro.update(dict(request.vars))

    if request.vars.Periodo:
        Parametro['Periodo'] = request.vars.Periodo
        queryIncidenteSeguridad = queryIncidenteSeguridad & (db.IncidenteSeguridad.Fecha.year()==request.vars.Periodo)
    if request.vars.ActivoTi:
        Parametro['ActivoTi'] = request.vars.ActivoTi
        queryIncidenteSeguridad = queryIncidenteSeguridad & (db.ActivoTiRegion.ActivoTiId==request.vars.ActivoTi) 
    if request.vars.TipoIncidenteSeguridad:
        Parametro['TipoIncidenteSeguridad'] = request.vars.TipoIncidenteSeguridad
        queryIncidenteSeguridad = queryIncidenteSeguridad & (db.IncidenteSeguridad.TipoIncidenteSeguridadId==request.vars.TipoIncidenteSeguridad) 
    if request.vars.Region:
        Parametro['Region'] = request.vars.Region
        queryIncidenteSeguridad = queryIncidenteSeguridad & (db.ActivoTiRegion.RegionId==request.vars.Region)
    if request.vars.Mes:
        Parametro['Mes'] = request.vars.Mes
        queryIncidenteSeguridad = queryIncidenteSeguridad & (db.IncidenteSeguridad.Fecha.month()==request.vars.Mes)

    CountActivoTi = db.ActivoTiRegion.id.count()
    CountTipoIncidenteSeguridad = db.TipoIncidenteSeguridad.id.count()
    CountRegion = db.ActivoTiRegion.id.count()
    CountIncidenteSeguridad = db.IncidenteSeguridad.id.count()
    TotalIncidenteSeguridad = db(queryIncidenteSeguridad).count()

    GrupoActivoTi = db(queryIncidenteSeguridad & queryActivoTiRegion).select(db.ActivoTiRegion.ALL, CountActivoTi, groupby=db.ActivoTiRegion.ActivoTiId | db.ActivoTiRegion.id)
    GrupoTipoIncidenteSeguridad = db(queryIncidenteSeguridad).select(db.IncidenteSeguridad.TipoIncidenteSeguridadId, CountTipoIncidenteSeguridad, groupby=db.IncidenteSeguridad.TipoIncidenteSeguridadId)
    GrupoIncidenteSeguridad = db(queryIncidenteSeguridad).select(db.IncidenteSeguridad.ALL, CountIncidenteSeguridad, groupby=db.IncidenteSeguridad.id) 
    GrupoRegion = db(queryIncidenteSeguridad & queryActivoTiRegion).select(db.ActivoTiRegion.RegionId, CountRegion, groupby=db.ActivoTiRegion.RegionId)

    ActivoTiRegion = db(queryIncidenteSeguridad & queryActivoTiRegion).select(db.ActivoTiRegion.ALL, distinct=True)
    TotalActivoTi = db(queryIncidenteSeguridad).count()
    Plataforma = db(queryIncidenteSeguridad).select(db.Plataforma.ALL, distinct=True)
    TipoIncidenteSeguridad = db(queryIncidenteSeguridad).select(db.TipoIncidenteSeguridad.ALL, distinct=True)

    TotalTipoIncidenteSeguridad = db(queryIncidenteSeguridad).count()
    Organizacion = db(db.Configuracion).select(db.Configuracion.Organizacion).first().Organizacion
    IncidenteSeguridad = db(queryIncidenteSeguridad).select(db.IncidenteSeguridad.ALL, distinct=True)

    return dict(Organizacion=Organizacion, CountTipoIncidenteSeguridad=CountTipoIncidenteSeguridad, GrupoTipoIncidenteSeguridad=GrupoTipoIncidenteSeguridad, ActivoTiRegion=ActivoTiRegion, Parametro=Parametro, Plataforma=Plataforma, TipoIncidenteSeguridad=TipoIncidenteSeguridad, GrupoActivoTi=GrupoActivoTi, GrupoRegion=GrupoRegion, IncidenteSeguridad=IncidenteSeguridad, GrupoIncidenteSeguridad=GrupoIncidenteSeguridad, TotalIncidenteSeguridad=TotalIncidenteSeguridad, TotalTipoIncidenteSeguridad=TotalTipoIncidenteSeguridad, TotalActivoTi=TotalActivoTi, CountActivoTi=CountActivoTi)

@auth.requires_login()
def TableroSeguridadTi():
    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='iformationOwner') or auth.has_membership(role='admin') or auth.has_membership(role='guest') or auth.has_membership(role='controlResp'):
        pass
    else:
        redirect(URL('default', 'index'))
    
    #Variables para manejar los filtros de busqueda
    FiltroPeriodo = 0
    FiltroActivoTi = 0
    #FiltroPlataforma = 0
    FiltroRegion = 0
    FiltroMes = 0
    FiltroCumplimiento = 0
    Periodo = request.now.year
    Parametro = {} #Variable tipo diccionario
    Parametro.update(dict(request.vars))

    #Query join desde la tabla de SeguridadTi
    #QuerySeguridadTi = (db.SeguridadTi.ActivoTiId==db.ActivoTi.id) & (db.SeguridadTi.DetallePoliticaId==db.DetallePolitica.id) & (db.SeguridadTi.TipoVulnerabilidadId==db.TipoVulnerabilidad.id) & (db.SeguridadTi.AnalisisRiesgoId==db.AnalisisRiesgo.id) & (db.SeguridadTi.TipoTratamientoRiesgoId==db.TipoTratamientoRiesgo.id) & (db.SeguridadTi.NivelMadurezId==db.NivelMadurez.id)
    QuerySeguridadTi = (db.SeguridadTi.ActivoTiId==db.ActivoTi.id) & (db.SeguridadTi.DetallePoliticaId==db.DetallePolitica.id) & (db.SeguridadTi.TipoVulnerabilidadId==db.TipoVulnerabilidad.id) & (db.SeguridadTi.NivelMadurezId==db.NivelMadurez.id)
    QueryActivoTi = (db.ActivoTi.TipoCapaSistemaId==db.TipoCapaSistema.id) & (db.ActivoTi.RegionId==db.Region.id)
    QueryPolitica = (db.DetallePolitica.CatalogoPoliticaId==db.CatalogoPolitica.id)
    QueryAnalisisRiesgo    =       (db.AnalisisRiesgo.ClasificacionRiesgoId==db.ClasificacionRiesgo.id) & (db.AnalisisRiesgo.ObjetivoOrganizacionId==db.ObjetivoOrganizacion.id) & (db.AnalisisRiesgo.CriterioProbabilidadId==db.CriterioProbabilidad.id) & (db.AnalisisRiesgo.CriterioImpactoId==db.CriterioImpacto.id) & (db.ObjetivoOrganizacion.TipoObjetivoId==db.TipoObjetivo.id)      
    QueryAprobacion = (db.SeguridadTi.AprobacionJefeAuditoria=='T') & (db.ActivoTi.AprobacionJefeRiesgo=='T') & (db.CatalogoPolitica.AprobacionJefeRiesgo=='T') & (db.DetallePolitica.AprobacionJefeRiesgo=='T') & (db.TipoVulnerabilidad.AprobacionJefeRiesgo=='T') & (db.AnalisisRiesgo.AprobacionJefeRiesgo=='T') & (db.TipoTratamientoRiesgo.AprobacionJefeRiesgo=='T') & (db.NivelMadurez.AprobacionJefeRiesgo=='T') & (db.TipoCapaSistema.AprobacionJefeAuditoria=='T') & (db.Region.AprobacionJefeRiesgo=='T') & (db.ClasificacionRiesgo.AprobacionJefeRiesgo=='T') & (db.ObjetivoOrganizacion.AprobacionJefeRiesgo=='T') & (db.CriterioProbabilidad.AprobacionJefeRiesgo=='T') & (db.CriterioImpacto.AprobacionJefeRiesgo=='T') & (db.TipoObjetivo.AprobacionJefeRiesgo=='T') 
    QuerySeguridadTi = (QuerySeguridadTi) & (QueryActivoTi) & (QueryPolitica) & (QueryAnalisisRiesgo) & (db.SeguridadTi.AprobacionJefeAuditoria=='T')

    if request.vars.Periodo:
        Parametro['Periodo'] = request.vars.Periodo
        QueryPeriodo = (db.SeguridadTi.FechaRevision.year()==request.vars.Periodo)
        FiltroPeriodo = 1
    if request.vars.ActivoTi:
        Parametro['ActivoTi'] = request.vars.ActivoTi
        QueryActivoTi = (db.ActivoTi.id==request.vars.ActivoTi) 
        FiltroActivoTi = 1
    if request.vars.Region:
        Parametro['Region'] = request.vars.Region
        QueryRegion = ((db.ActivoTi.RegionId==db.Region.id) & (db.ActivoTi.RegionId==request.vars.Region))
        FiltroRegion = 1
    if request.vars.Mes:
        Parametro['Mes'] = request.vars.Mes
        QueryMes=(db.SeguridadTi.FechaRevision.month()==request.vars.Mes)
        FiltroMes = 1

    if FiltroPeriodo == 1:
        QuerySeguridadTi = QuerySeguridadTi & QueryPeriodo
    if FiltroActivoTi == 1:
        QuerySeguridadTi = QuerySeguridadTi & QueryActivoTi
    if FiltroRegion == 1:
        QuerySeguridadTi = QuerySeguridadTi & QueryRegion
    if FiltroMes == 1:
        QuerySeguridadTi = QuerySeguridadTi & QueryMes

    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='admin') or auth.has_membership(role='guest'):
        QuerySeguridadTi = QuerySeguridadTi

    elif auth.has_membership(role='controlResp'):
        controlId=[]
        for a in db(db.SeguridadTi.AprobacionJefeAuditoria == 'T').select(db.SeguridadTi.id, db.SeguridadTi.ResponsableControl):
            try:
                for b in str(str(a.ResponsableControl).replace(' ','')).split(','):
                    if b==auth.user.username:
                        controlId.append(int(a.id))
            except:
                pass
        #query = (db.SeguridadTi.id==0)
        query = db.SeguridadTi.id.belongs(controlId)
        QuerySeguridadTi = (QuerySeguridadTi) & (query)

    CountSeguridadTi = db.SeguridadTi.id.count()
    CountActivoTi = db.ActivoTi.id.count()
    EfectividadControl = db((QuerySeguridadTi) & ( db.SeguridadTi.EfectividadControl=='T' ) ).count()
    TotalSeguridadTi = db(QuerySeguridadTi).count()
    
    GrupoTipoTratamientoRiesgo = db(QuerySeguridadTi).select(db.TipoTratamientoRiesgo.Nombre, db.TipoTratamientoRiesgo.Color, CountSeguridadTi)
    GrupoTipoCumplimiento= db(QuerySeguridadTi).select(db.SeguridadTi.Cumplimiento, db.ActivoTi.Nombre, CountSeguridadTi, groupby=db.SeguridadTi.Cumplimiento)
    #GrupoSeguridadTi = db(QuerySeguridadTi).select(db.SeguridadTi.Cumplimiento, db.ActivoTi.Nombre, CountSeguridadTi, groupby=db.ActivoTi.id)
    #GrupoActivoTi = db(QuerySeguridadTi).select(db.SeguridadTi.ActivoTiId, CountActivoTi, groupby=db.SeguridadTi.ActivoTiId)
    GrupoTipoVulnerabilidad = db(QuerySeguridadTi & (db.SeguridadTi.EfectividadControl=='F')).select(db.SeguridadTi.TipoVulnerabilidadId, CountSeguridadTi, groupby=db.SeguridadTi.TipoVulnerabilidadId)
    GrupoNivelMadurezControl = db(QuerySeguridadTi).select(db.SeguridadTi.NivelMadurezId,CountSeguridadTi, groupby=db.SeguridadTi.NivelMadurezId)

    #ActivoTi = db( (QuerySeguridadTi) & db.ActivoTi.id==db.SeguridadTi.ActivoTiId).select(db.ActivoTi.ALL, distinct=True) #Solo los que tienen prueba asociada
    ActivoTi = db(QuerySeguridadTi).select(db.ActivoTi.ALL, distinct=True) #Solo los que tienen prueba asociada
    TipoVulnerabilidad = db(QuerySeguridadTi & (db.SeguridadTi.EfectividadControl=='F')).select(db.TipoVulnerabilidad.ALL, distinct=True)
    #CatalogoPolitica = db(QuerySeguridadTi).select(db.CatalogoPolitica.ALL, distinct=True)
    AnalisisRiesgo = db(QuerySeguridadTi).select(db.AnalisisRiesgo.ALL, distinct=True)
    TratamientoRiesgo = db(QuerySeguridadTi).select(db.TratamientoRiesgo.ALL, distinct=True)
    
    Plataforma = db(QuerySeguridadTi).select(db.Plataforma.ALL, distinct=True)
    Region = db(QuerySeguridadTi).select(db.Region.ALL, distinct=True)
    SeguridadTi = db(QuerySeguridadTi).select(db.SeguridadTi.ALL, distinct=True)
    CatalogoPolitica = db(QuerySeguridadTi).select(db.CatalogoPolitica.ALL, distinct=True)
    
    #Query
    #TipoTratamientoRiesgo = db(db.TipoTratamientoRiesgo).select(db.TipoTratamientoRiesgo.ALL, distinct=True)
    TipoTratamientoRiesgo = db(QuerySeguridadTi).select(db.TipoTratamientoRiesgo.ALL, distinct=True)
    #TipoCumplimiento = db(db.TipoCumplimiento).select(db.TipoCumplimiento.ALL, distinct=True)
    #NivelMadurez = db(db.NivelMadurez).select(db.NivelMadurez.ALL, orderby=db.NivelMadurez.Valor, distinct=True)
    NivelMadurez = db(QuerySeguridadTi).select(db.NivelMadurez.ALL, orderby=db.NivelMadurez.Valor, distinct=True)
    #CatalogoPolitica = db(db.CatalogoPolitica).select(db.CatalogoPolitica.ALL, distinct=True)

    #cumplimiento por activo
    GrupoActivoTi = []
    for i in ActivoTi:
        ListaActivoTi = []
        Sistema = str(i.Nombre) + ' | ' + str(i.TipoCapaSistemaId.Nombre)
        ListaActivoTi.append(i.id)
        ListaActivoTi.append(Sistema)
        ListaActivoTi.append(0)
        ListaActivoTi.append(0)
        GrupoActivoTi.append(ListaActivoTi)
    for a in SeguridadTi:
        for b in GrupoActivoTi:
            if (a.ActivoTiId==b[0]) and (a.Cumplimiento==True):
                b[2]=b[2]+1
            elif (a.ActivoTiId==b[0]) and (a.Cumplimiento==False):
                b[3]=b[3]+1

    #cumplimiento por control
    GrupoAnalisisRiesgo = []
    for i in TratamientoRiesgo:
        ListaAnalisisRiesgo = []
        ListaAnalisisRiesgo.append(i.id)
        ListaAnalisisRiesgo.append(i.Control)
        ListaAnalisisRiesgo.append(0)
        ListaAnalisisRiesgo.append(0)
        GrupoAnalisisRiesgo.append(ListaAnalisisRiesgo)
    for a in SeguridadTi:
        for b in GrupoAnalisisRiesgo:
            if (a.TratamientoRiesgoId == b[0]) and (a.Cumplimiento=='T'):
                b[2]=b[2]+1
            elif (a.TratamientoRiesgoId == b[0]) and (a.Cumplimiento=='F'):
                b[3]=b[3]+1

    #cumplimiento por politica
    GrupoPolitica = []
    for i in CatalogoPolitica:
        ListaPolitica = []
        ListaPolitica.append(i.id)
        ListaPolitica.append(i.Nombre)
        ListaPolitica.append(0)
        ListaPolitica.append(0)
        GrupoPolitica.append(ListaPolitica)
    for a in SeguridadTi:
        for b in GrupoPolitica:
            if (a.DetallePoliticaId.CatalogoPoliticaId == b[0]) and (a.Cumplimiento==True):
                b[2]=b[2]+1
            elif (a.DetallePoliticaId.CatalogoPoliticaId == b[0]) and (a.Cumplimiento==False):
                b[3]=b[3]+1

    TotalActivoTi = 0
    TotalTipoVulnerabilidad = 0
    TotalCatalogoPolitica = 0
    for i in ActivoTi:
        TotalActivoTi = TotalActivoTi + 1
    for i in TipoVulnerabilidad:
        TotalTipoVulnerabilidad = TotalTipoVulnerabilidad + 1
    for i in CatalogoPolitica:
        TotalCatalogoPolitica = TotalCatalogoPolitica + 1
    Organizacion = db(db.Configuracion).select(db.Configuracion.Organizacion).first().Organizacion

    return dict(GrupoTipoTratamientoRiesgo=GrupoTipoTratamientoRiesgo, GrupoPolitica=GrupoPolitica, GrupoAnalisisRiesgo=GrupoAnalisisRiesgo, GrupoActivoTi=GrupoActivoTi, Parametro=Parametro, ActivoTi=ActivoTi, Plataforma=Plataforma, Region=Region, TipoCumplimiento=TipoCumplimiento, SeguridadTi=SeguridadTi, Periodo=Periodo, TotalSeguridadTi=TotalSeguridadTi, TotalActivoTi=TotalActivoTi, GrupoTipoCumplimiento=GrupoTipoCumplimiento, CountSeguridadTi=CountSeguridadTi, GrupoNivelMadurezControl=GrupoNivelMadurezControl, NivelMadurez=NivelMadurez, EfectividadControl=EfectividadControl, CatalogoPolitica=CatalogoPolitica, ListaPolitica=ListaPolitica, AnalisisRiesgo=AnalisisRiesgo, ListaAnalisisRiesgo=ListaAnalisisRiesgo, CountActivoTi=CountActivoTi, TotalTipoVulnerabilidad=TotalTipoVulnerabilidad, GrupoTipoVulnerabilidad=GrupoTipoVulnerabilidad, TipoVulnerabilidad=TipoVulnerabilidad, Organizacion=Organizacion, TotalCatalogoPolitica=TotalCatalogoPolitica)

@auth.requires_login()
def TableroAuditoria():
    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='iformationOwner') or auth.has_membership(role='admin') or auth.has_membership(role='guest') or auth.has_membership(role='controlResp'):
        pass
    else:
        redirect(URL('default', 'index'))
    
    #Variables para los filtros de busqueda
    FiltroPeriodo = 0
    FiltroProceso = 0
    #FiltroPlataforma = 0
    FiltroRegion = 0
    FiltroMes = 0
    FiltroCumplimiento = 0
    Periodo = request.now.year
    Parametro = {}
    Parametro.update(dict(request.vars))

    #Query join desde la tabla de auditoria
    QueryAuditoria = (db.Auditoria.ProcesoId==db.Proceso.id) & (db.Auditoria.DetallePoliticaId==db.DetallePolitica.id) & (db.Auditoria.AnalisisRiesgoId==db.AnalisisRiesgo.id) & (db.Auditoria.TipoControlId==db.TipoControl.id) & (db.Auditoria.ClasificacionControlId==db.ClasificacionControl.id) & (db.Auditoria.TipoTratamientoRiesgoId==db.TipoTratamientoRiesgo.id) & (db.Auditoria.NivelMadurezId==db.NivelMadurez.id)
    QueryProceso = (db.Proceso.CicloNegocioId==db.CicloNegocio.id) & (db.Proceso.TipoProcesoId==db.TipoProceso.id) & (db.Proceso.RegionId==db.Region.id)
    QueryPolitica = (db.DetallePolitica.CatalogoPoliticaId==db.CatalogoPolitica.id)
    QueryAnalisisRiesgo    =       (db.AnalisisRiesgo.ClasificacionRiesgoId==db.ClasificacionRiesgo.id) & (db.AnalisisRiesgo.ObjetivoOrganizacionId==db.ObjetivoOrganizacion.id) & (db.AnalisisRiesgo.CriterioProbabilidadId==db.CriterioProbabilidad.id) & (db.AnalisisRiesgo.CriterioImpactoId==db.CriterioImpacto.id) & (db.ObjetivoOrganizacion.TipoObjetivoId==db.TipoObjetivo.id)      
    #QueryAuditoria = (QueryAuditoria) & (QueryProceso) & (QueryPolitica) & (QueryAnalisisRiesgo) & (db.Auditoria.AprobacionJefeAuditoria=='T')  & (db.CatalogoPolitica.AprobacionJefeRiesgo=='T') & (db.DetallePolitica.AprobacionJefeRiesgo=='T')
    QueryAuditoria = (QueryAuditoria) & (QueryProceso) & (QueryPolitica) & (QueryAnalisisRiesgo) & (db.Auditoria.AprobacionJefeAuditoria=='T')

    if request.vars.Periodo:
        Parametro['Periodo'] = request.vars.Periodo
        QueryPeriodo = (db.Auditoria.FechaRevision.year()==request.vars.Periodo)
        FiltroPeriodo = 1
    if request.vars.Proceso:
        Parametro['Proceso'] = request.vars.Proceso
        QueryProceso = (db.Auditoria.ProcesoId==request.vars.Proceso) 
        FiltroProceso = 1
    if request.vars.Region:
        Parametro['Region'] = request.vars.Region
        QueryRegion = ((db.Auditoria.ProcesoId==db.Proceso.id) & (db.Proceso.RegionId==request.vars.Region))
        FiltroRegion = 1
    if request.vars.Mes:
        Parametro['Mes'] = request.vars.Mes
        QueryMes=(db.Auditoria.FechaRevision.month()==request.vars.Mes)
        FiltroMes = 1
    #if request.vars.TipoCumplimiento:
    #    Parametro['TipoCumplimiento'] = request.vars.TipoCumplimiento
    #    QueryCumplimiento = (db.Auditoria.TipoCumplimientoId==request.vars.TipoCumplimiento)
    #    FiltroCumplimiento = 1

    if FiltroPeriodo == 1:
        QueryAuditoria = QueryAuditoria & QueryPeriodo
    if FiltroProceso == 1:
        QueryAuditoria = QueryAuditoria & QueryProceso
    if FiltroRegion == 1:
        QueryAuditoria = QueryAuditoria & QueryRegion
    if FiltroMes == 1:
        QueryAuditoria = QueryAuditoria & QueryMes
    #if FiltroCumplimiento == 1:
    #    QueryAuditoria = QueryAuditoria & QueryCumplimiento

    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='admin') or auth.has_membership(role='guest'):
        QueryAuditoria = QueryAuditoria

    elif auth.has_membership(role='controlResp'):
        controlId=[]
        for a in db(db.Auditoria.AprobacionJefeAuditoria == 'T').select(db.Auditoria.id, db.Auditoria.ResponsableControl):
            try:
                for b in str(str(a.ResponsableControl).replace(' ','')).split(','):
                    if b==auth.user.username:
                        controlId.append(int(a.id))
            except:
                pass
        query = db.Auditoria.id.belongs(controlId)
        QueryAuditoria = (QueryAuditoria) & (query)

    CountAuditoria = db.Auditoria.id.count()
    CountProceso = db.Proceso.id.count()
    EfectividadControl = db((QueryAuditoria) & ( db.Auditoria.EfectividadControl=='T' ) ).count()
    TotalAuditoria = db(QueryAuditoria).count()
    #CountTipoCumplimiento = db.TipoCumplimiento.id.count()
    #CountEfectividadControl = db((QueryAuditoria) & (db.Auditoria.EfectividadControl=='T')).count()
    
    
    GrupoTipoTratamientoRiesgo = db(QueryAuditoria).select(db.TipoTratamientoRiesgo.Nombre, db.TipoTratamientoRiesgo.Color, CountAuditoria, groupby=db.Auditoria.TipoTratamientoRiesgoId)
    GrupoTipoCumplimiento= db(QueryAuditoria).select(db.Auditoria.Cumplimiento, db.Proceso.Nombre, CountAuditoria, groupby=db.Auditoria.Cumplimiento)
    #GrupoProceso = db(QueryAuditoria).select(db.Proceso.Nombre, CountAuditoria, groupby=db.Auditoria.ProcesoId)
    #GrupoAuditoria = db(QueryAuditoria).select(db.Auditoria.ALL, CountAuditoria, groupby=db.Auditoria.ProcesoId)
    GrupoNivelMadurezControl = db(QueryAuditoria).select(db.Auditoria.NivelMadurezId, CountAuditoria, groupby=db.Auditoria.NivelMadurezId)

    Proceso = db(QueryAuditoria).select(db.Proceso.ALL, distinct=True)
    AnalisisRiesgo = db(QueryAuditoria).select(db.AnalisisRiesgo.ALL, distinct=True)
    Region = db(QueryAuditoria).select(db.Region.ALL, distinct=True)
    Auditoria = db(QueryAuditoria).select(db.Auditoria.ALL, distinct=True)
    CatalogoPolitica = db(QueryAuditoria).select(db.CatalogoPolitica.ALL, distinct=True)
    
    TipoTratamientoRiesgo = db(QueryAuditoria).select(db.TipoTratamientoRiesgo.ALL, distinct=True)
    #TipoCumplimiento = db(QueryAuditoria).select(db.TipoCumplimiento.ALL, distinct=True)
    NivelMadurez = db(QueryAuditoria).select(db.NivelMadurez.ALL, orderby=db.NivelMadurez.Valor, distinct=True)

    #ListaProceso = []
    #ListaPolitica = []
    #ListaAnalisisRiesgo = []
    #TotalProceso = 0
    #TotalAuditoria = 0
    #TotalTipoVulnerabilidad = 0
    
    #Cumplimiento por proceso
    GrupoProceso = []
    for i in Proceso:
        ListaProceso = []
        ProcesoNombre = str(i.RegionId.Nombre) + ' | ' + str(i.Nombre)
        ListaProceso.append(i.id)
        ListaProceso.append(ProcesoNombre)
        ListaProceso.append(0)
        ListaProceso.append(0)
        GrupoProceso.append(ListaProceso)
    for a in Auditoria:
        for b in GrupoProceso:
            if (a.ProcesoId==b[0]) and (a.Cumplimiento==True):
                b[2]=b[2]+1
            elif (a.ProcesoId==b[0]) and (a.Cumplimiento==False):
                b[3]=b[3]+1

    #cumplimiento por riesgo
    GrupoAnalisisRiesgo = []
    for i in AnalisisRiesgo:
        ListaAnalisisRiesgo = []
        ListaAnalisisRiesgo.append(i.id)
        ListaAnalisisRiesgo.append(i.Riesgo)
        ListaAnalisisRiesgo.append(0)
        ListaAnalisisRiesgo.append(0)
        GrupoAnalisisRiesgo.append(ListaAnalisisRiesgo)
    for a in Auditoria:
        for b in GrupoAnalisisRiesgo:
            if (a.AnalisisRiesgoId == b[0]) and (a.Cumplimiento==True):
                b[2]=b[2]+1
            elif (a.AnalisisRiesgoId == b[0]) and (a.Cumplimiento==False):
                b[3]=b[3]+1

    #cumplimiento por politica
    GrupoPolitica = []
    for i in CatalogoPolitica:
        ListaPolitica = []
        ListaPolitica.append(i.id)
        ListaPolitica.append(i.Nombre)
        ListaPolitica.append(0)
        ListaPolitica.append(0)
        GrupoPolitica.append(ListaPolitica)
    for a in Auditoria:
        for b in GrupoPolitica:
            if (a.DetallePoliticaId.CatalogoPoliticaId == b[0]) and (a.Cumplimiento==True):
                b[2]=b[2]+1
            elif (a.DetallePoliticaId.CatalogoPoliticaId == b[0]) and (a.Cumplimiento==False):
                b[3]=b[3]+1

    TotalProceso = 0
    #TotalTipoVulnerabilidad = 0
    TotalCatalogoPolitica = 0
    #NivelMadurezMax = []
    for i in Proceso:
        TotalProceso = TotalProceso + 1
    for i in CatalogoPolitica:
        TotalCatalogoPolitica = TotalCatalogoPolitica + 1

    Organizacion = db(db.Configuracion).select(db.Configuracion.Organizacion).first().Organizacion

    return dict(EfectividadControl=EfectividadControl, TotalCatalogoPolitica=TotalCatalogoPolitica, GrupoPolitica=GrupoPolitica, GrupoAuditoria=GrupoProceso, Proceso=Proceso, Parametro=Parametro, Region=Region, Auditoria=Auditoria, Periodo=Periodo, TotalAuditoria=TotalAuditoria, ListaProceso=ListaProceso, GrupoProceso=GrupoProceso, TotalProceso=TotalProceso, CountAuditoria=CountAuditoria, GrupoTipoTratamientoRiesgo=GrupoTipoTratamientoRiesgo, GrupoNivelMadurezControl=GrupoNivelMadurezControl, NivelMadurez=NivelMadurez, CatalogoPolitica=CatalogoPolitica, ListaPolitica=ListaPolitica, AnalisisRiesgo=AnalisisRiesgo, ListaAnalisisRiesgo=ListaAnalisisRiesgo, CountProceso=CountProceso, Organizacion=Organizacion)

@auth.requires_login()
def TableroEvaluacionControl():
    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='iformationOwner') or auth.has_membership(role='admin') or auth.has_membership(role='guest') or auth.has_membership(role='controlResp'):
        pass	
    else:
        redirect(URL('default', 'index'))
    
    Parametro = {}
    Parametro.update(dict(request.vars))

    QueryAuditoria = (db.EvaluacionControl.TratamientoRiesgoId==db.TratamientoRiesgo.id) & (db.EvaluacionControl.CatalogoControlId==db.CatalogoControl.id) & (db.EvaluacionControl.DetallePoliticaId==db.DetallePolitica.id) & (db.EvaluacionControl.ProcesoId==db.Proceso.id) & (db.EvaluacionControl.ActivoTiId==db.ActivoTi.id) & (db.EvaluacionControl.NivelMadurezId==db.NivelMadurez.id) & (db.EvaluacionControl.TipoRevisionId==db.TipoRevision.id) & (db.EvaluacionControl.AprobacionJefeAuditoria=='T')

    queryTratamientoRiesgoAnalisisRiesgo = (db.TratamientoRiesgoAnalisisRiesgo.TratamientoRiesgoId==db.TratamientoRiesgo.id) & (db.TratamientoRiesgoAnalisisRiesgo.AnalisisRiesgoId==db.AnalisisRiesgo.id)

    if request.vars.Proceso:
        Parametro['Proceso'] = request.vars.Proceso
        QueryAuditoria = QueryAuditoria & (db.EvaluacionControl.ProcesoId==request.vars.Proceso) 
    if request.vars.ActivoTi:
        Parametro['ActivoTi'] = request.vars.ActivoTi
        QueryAuditoria = QueryAuditoria & (db.EvaluacionControl.ActivoTiId==request.vars.ActivoTi) 
    if request.vars.Politica:
        Parametro['Politica'] = request.vars.Politica
        QueryAuditoria = QueryAuditoria & (db.EvaluacionControl.DetallePoliticaId==db.DetallePolitica.id)
    if request.vars.Factor:
        Parametro['Factor'] = request.vars.Factor
        QueryAuditoria = QueryAuditoria & (db.EvaluacionControl.TratamientoRiesgoId==request.vars.Factor)
    if request.vars.Control:
        Parametro['Control'] = request.vars.Control
        QueryAuditoria = QueryAuditoria & (db.EvaluacionControl.CatalogoControlId==request.vars.Control)

    if auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='admin') or auth.has_membership(role='guest'):
        QueryAuditoria = QueryAuditoria

    elif auth.has_membership(role='controlResp'):
        controlId=[]
        for a in db(db.EvaluacionControl.AprobacionJefeAuditoria == 'T').select(db.EvaluacionControl.id, db.EvaluacionControl.ResponsableControl):
            try:
                for b in str(str(a.ResponsableControl).replace(' ','')).split(','):
                    if b==auth.user.username:
                        controlId.append(int(a.id))
            except:
                pass
        query = db.EvaluacionControl.id.belongs(controlId)
        QueryAuditoria = (QueryAuditoria) & (query)

    CountAuditoria = db.EvaluacionControl.id.count()
    CountProceso = db.Proceso.id.count()
    EfectividadControl = db((QueryAuditoria) & ( db.EvaluacionControl.EfectividadControl=='T' )).count()
    CumplimientoControl = db((QueryAuditoria) & ( db.EvaluacionControl.CumplimientoControl=='T' ) & (db.EvaluacionControl.TipoRevisionId==2) ).count()
    TotalAuditoria = db(QueryAuditoria).count()
    TotalAuditoriaCumplimiento = db(QueryAuditoria & (db.EvaluacionControl.TipoRevisionId==2)).count()
    
    #GrupoTipoCumplimiento= db(QueryAuditoria & (db.TratamientoRiesgo.ProcesoRegionId==db.ProcesoRegion.id) & (db.ProcesoRegion.ProcesoId==db.Proceso.id) ).select(db.EvaluacionControl.CumplimientoControl, db.Proceso.Nombre, CountAuditoria, groupby=db.EvaluacionControl.CumplimientoControl)
    #GrupoTipoCumplimiento= db(QueryAuditoria & (db.TratamientoRiesgo.ProcesoRegionId==db.ProcesoRegion.id) & (db.ProcesoRegion.ProcesoId==db.Proceso.id) ).select(db.EvaluacionControl.CumplimientoControl, db.Proceso.Nombre, CountAuditoria)
    GrupoNivelMadurezControl = db(QueryAuditoria).select(db.EvaluacionControl.NivelMadurezId, CountAuditoria, groupby=db.EvaluacionControl.NivelMadurezId)

    Proceso = db(QueryAuditoria & (db.TratamientoRiesgo.ProcesoId==db.Proceso.id) ).select(db.Proceso.ALL, distinct=True)
    ActivoTi = db(QueryAuditoria & (db.TratamientoRiesgo.ActivoTiId==db.ActivoTi.id) ).select(db.ActivoTi.ALL, distinct=True)
    #Region = db(QueryAuditoria & (db.TratamientoRiesgo.ProcesoId==db.Proceso.id) ).select(db.Region.ALL, distinct=True)
    #CatalogoPolitica = db(QueryAuditoria & (db.TratamientoRiesgo.DetallePoliticaId==db.DetallePolitica.id) & (db.DetallePolitica.RegionPoliticaId==db.RegionPolitica.id) & (db.RegionPolitica.CatalogoPoliticaId==db.CatalogoPolitica.id)).select(db.CatalogoPolitica.ALL, distinct=True)
    CatalogoPolitica = db(QueryAuditoria ).select(db.CatalogoPolitica.ALL, distinct=True)
    CatalogoControl = db(QueryAuditoria ).select(db.CatalogoControl.ALL, distinct=True)
    FactorRiesgo = db(QueryAuditoria ).select(db.TratamientoRiesgo.ALL, distinct=True)

    #AnalisisRiesgo = db(QueryAuditoria & (db.TratamientoRiesgo.AnalisisRiesgoId==db.AnalisisRiesgo.id) ).select(db.AnalisisRiesgo.ALL, distinct=True)
    AnalisisRiesgo = db(QueryAuditoria & queryTratamientoRiesgoAnalisisRiesgo ).select(db.AnalisisRiesgo.ALL, distinct=True)
    Auditoria = db(QueryAuditoria & (db.TratamientoRiesgo.CriterioImpactoId==db.CriterioRiesgo.CriterioImpactoId) & (db.TratamientoRiesgo.CriterioProbabilidadId==db.CriterioRiesgo.CriterioProbabilidadId) ).select(db.EvaluacionControl.ALL, db.CriterioRiesgo.ALL, distinct=True)
    
    TipoTratamientoRiesgo = db(QueryAuditoria).select(db.TipoTratamientoRiesgo.ALL, distinct=True)
    NivelMadurez = db(QueryAuditoria).select(db.NivelMadurez.ALL, orderby=db.NivelMadurez.Valor, distinct=True)

    GrupoProceso = []
    for i in Proceso:
        ListaProceso = []
        #ProcesoNombre = str(i.RegionId.Nombre) + ' | ' + str(i.Nombre)
        ProcesoNombre = str(i.Nombre)
        ListaProceso.append(i.id)
        ListaProceso.append(ProcesoNombre)
        ListaProceso.append(0) #cumplimiento
        ListaProceso.append(0) #cumplimiento
        ListaProceso.append(0) #diseno
        ListaProceso.append(0) #diseno
        GrupoProceso.append(ListaProceso)
    #----------------------------------------------------------------------------
    #La logica toma las 3 lineas de defensa DuenoProceso-RiesgosControl-Auditoria
    #----------------------------------------------------------------------------
    for a in Auditoria:
        for b in GrupoProceso:
            #if (a.EvaluacionControl.ProcesoRegionId.ProcesoId==b[0]) and (a.EvaluacionControl.CumplimientoControl==True) and (a.EvaluacionControl.TipoRevisionId==2):
            if (a.EvaluacionControl.ProcesoId==b[0]) and (a.EvaluacionControl.CumplimientoControl==True) and (a.EvaluacionControl.TipoRevisionId==3):
                b[2]=b[2]+1
            #elif (a.EvaluacionControl.ProcesoRegionId.ProcesoId==b[0]) and (a.EvaluacionControl.CumplimientoControl==False) and (a.EvaluacionControl.TipoRevisionId==2):
            elif (a.EvaluacionControl.ProcesoId==b[0]) and (a.EvaluacionControl.CumplimientoControl==False) and (a.EvaluacionControl.TipoRevisionId==3):
                b[3]=b[3]+1
            #if (a.EvaluacionControl.ProcesoRegionId.ProcesoId==b[0]) and (a.EvaluacionControl.EfectividadControl==True):
            if (a.EvaluacionControl.ProcesoId==b[0]) and (a.EvaluacionControl.EfectividadControl==True):
                b[4]=b[4]+1
            #elif (a.EvaluacionControl.ProcesoRegionId.ProcesoId==b[0]) and (a.EvaluacionControl.EfectividadControl==False):
            elif (a.EvaluacionControl.ProcesoId==b[0]) and (a.EvaluacionControl.EfectividadControl==False):
                b[5]=b[5]+1

    GrupoActivoTi = []
    for i in ActivoTi:
        ListaActivoTi = []
        #ProcesoNombre = str(i.RegionId.Nombre) + ' | ' + str(i.Nombre)
        ListaActivoTi.append(i.id)
        ListaActivoTi.append(i.Nombre)
        ListaActivoTi.append(0) #cumplimiento
        ListaActivoTi.append(0) #cumplimiento
        ListaActivoTi.append(0) #diseno
        ListaActivoTi.append(0) #diseno
        GrupoActivoTi.append(ListaActivoTi)
    for a in Auditoria:
        for b in GrupoActivoTi:
            #if (a.EvaluacionControl.ActivoTiRegionId.ActivoTiId==b[0]) and (a.EvaluacionControl.CumplimientoControl==True) and (a.EvaluacionControl.TipoRevisionId==2):
            if (a.EvaluacionControl.ActivoTiId==b[0]) and (a.EvaluacionControl.CumplimientoControl==True) and (a.EvaluacionControl.TipoRevisionId==3):
                b[2]=b[2]+1
            #elif (a.EvaluacionControl.ActivoTiRegionId.ActivoTiId==b[0]) and (a.EvaluacionControl.CumplimientoControl==False)and (a.EvaluacionControl.TipoRevisionId==2):
            elif (a.EvaluacionControl.ActivoTiId==b[0]) and (a.EvaluacionControl.CumplimientoControl==False)and (a.EvaluacionControl.TipoRevisionId==3):
                b[3]=b[3]+1
            #if (a.EvaluacionControl.ActivoTiRegionId.ActivoTiId==b[0]) and (a.EvaluacionControl.EfectividadControl==True):
            if (a.EvaluacionControl.ActivoTiId==b[0]) and (a.EvaluacionControl.EfectividadControl==True):
                b[4]=b[4]+1
            #elif (a.EvaluacionControl.ActivoTiRegionId.ActivoTiId==b[0]) and (a.EvaluacionControl.EfectividadControl==False):
            elif (a.EvaluacionControl.ActivoTiId==b[0]) and (a.EvaluacionControl.EfectividadControl==False):
                b[5]=b[5]+1
    '''
    #cumplimiento por riesgo
    GrupoAnalisisRiesgo = []
    for i in AnalisisRiesgo:
        ListaAnalisisRiesgo = []
        ListaAnalisisRiesgo.append(i.id)
        ListaAnalisisRiesgo.append(i.Riesgo)
        ListaAnalisisRiesgo.append(0)
        ListaAnalisisRiesgo.append(0)
        ListaAnalisisRiesgo.append(0)
        ListaAnalisisRiesgo.append(0)
        GrupoAnalisisRiesgo.append(ListaAnalisisRiesgo)
    for a in Auditoria:
        for b in GrupoAnalisisRiesgo:
            if (a.EvaluacionControl.TratamientoRiesgoId.AnalisisRiesgoId == b[0]) and (a.EvaluacionControl.CumplimientoControl==True) and (a.EvaluacionControl.TipoRevisionId==2):
                b[2]=b[2]+1
            elif (a.EvaluacionControl.TratamientoRiesgoId.AnalisisRiesgoId == b[0]) and (a.EvaluacionControl.CumplimientoControl==False) and (a.EvaluacionControl.TipoRevisionId==2):
                b[3]=b[3]+1
            if (a.EvaluacionControl.TratamientoRiesgoId.AnalisisRiesgoId == b[0]) and (a.EvaluacionControl.EfectividadControl==True):
                b[4]=b[4]+1
            elif (a.EvaluacionControl.TratamientoRiesgoId.AnalisisRiesgoId == b[0]) and (a.EvaluacionControl.EfectividadControl==False):
                b[5]=b[5]+1
    '''
    #cumplimiento por politica
    GrupoPolitica = []
    for i in CatalogoPolitica:
        ListaPolitica = []
        ListaPolitica.append(i.id)
        ListaPolitica.append(i.Nombre)
        ListaPolitica.append(0)
        ListaPolitica.append(0)
        ListaPolitica.append(0)
        ListaPolitica.append(0)
        GrupoPolitica.append(ListaPolitica)
    for a in Auditoria:
        for b in GrupoPolitica:
            #if (a.EvaluacionControl.DetallePoliticaId.RegionPoliticaId.CatalogoPoliticaId == b[0]) and (a.EvaluacionControl.CumplimientoControl==True) and (a.EvaluacionControl.TipoRevisionId==2):
            if (a.EvaluacionControl.DetallePoliticaId == b[0]) and (a.EvaluacionControl.CumplimientoControl==True) and (a.EvaluacionControl.TipoRevisionId==3):
                b[2]=b[2]+1
            #elif (a.EvaluacionControl.DetallePoliticaId.RegionPoliticaId.CatalogoPoliticaId == b[0]) and (a.EvaluacionControl.CumplimientoControl==False) and (a.EvaluacionControl.TipoRevisionId==2):
            elif (a.EvaluacionControl.DetallePoliticaId == b[0]) and (a.EvaluacionControl.CumplimientoControl==False) and (a.EvaluacionControl.TipoRevisionId==3):
                b[3]=b[3]+1
            #if (a.EvaluacionControl.DetallePoliticaId.RegionPoliticaId.CatalogoPoliticaId == b[0]) and (a.EvaluacionControl.EfectividadControl==True):
            if (a.EvaluacionControl.DetallePoliticaId == b[0]) and (a.EvaluacionControl.EfectividadControl==True):
                b[4]=b[4]+1
            #elif (a.EvaluacionControl.DetallePoliticaId.RegionPoliticaId.CatalogoPoliticaId== b[0]) and (a.EvaluacionControl.EfectividadControl==False):
            elif (a.EvaluacionControl.DetallePoliticaId== b[0]) and (a.EvaluacionControl.EfectividadControl==False):
                b[5]=b[5]+1

    TotalProceso = 0
    #TotalTipoVulnerabilidad = 0
    TotalCatalogoPolitica = 0
    #NivelMadurezMax = []
    for i in Proceso:
        TotalProceso = TotalProceso + 1
    for i in CatalogoPolitica:
        TotalCatalogoPolitica = TotalCatalogoPolitica + 1

    Organizacion = db(db.Configuracion).select(db.Configuracion.Organizacion).first().Organizacion

    return dict(EfectividadControl=EfectividadControl, TotalCatalogoPolitica=TotalCatalogoPolitica, GrupoPolitica=GrupoPolitica, GrupoProceso=GrupoProceso, Proceso=Proceso, Parametro=Parametro, Auditoria=Auditoria, TotalAuditoria=TotalAuditoria, TotalProceso=TotalProceso, CountAuditoria=CountAuditoria, GrupoNivelMadurezControl=GrupoNivelMadurezControl, NivelMadurez=NivelMadurez, CatalogoPolitica=CatalogoPolitica, AnalisisRiesgo=AnalisisRiesgo, CumplimientoControl=CumplimientoControl, Organizacion=Organizacion, ActivoTi=ActivoTi, GrupoActivoTi=GrupoActivoTi, TotalAuditoriaCumplimiento=TotalAuditoriaCumplimiento, CatalogoControl=CatalogoControl, FactorRiesgo=FactorRiesgo)

@auth.requires_login()
def Configuracion():
    db.Configuracion.id.readable = False
    #db.Configuracion.MatrizRiesgo.readable = False
    #db.Configuracion.MatrizRiesgo.writable = False
    #if versionGratuita==1:
    #    db.Configuracion.Organizacion.writable = False
    #    db.Configuracion.Lenguaje.writable = False
    #if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
    if auth.has_membership(role='admin'):
        return dict(form=SQLFORM.grid(db.Configuracion, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=15, maxtextlength=250))
    else:
        return dict(form=SQLFORM.grid(db.Configuracion, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250))

@auth.requires_login()
def Documentacion():
    #db.Documentacion.id.readable = False
    db.Documentacion.LogAnalistaRiesgo.writable=False
    db.Documentacion.LogJefeRiesgo.writable=False
    db.Documentacion.AprobacionAnalistaRiesgo.writable=False
    db.Documentacion.AprobacionJefeRiesgo.writable=False

    Tabla = "Documentacion"
    fields = (db.Documentacion.id, db.Documentacion.Nombre, db.Documentacion.Descripcion, db.Documentacion.Archivo, db.Documentacion.AprobacionJefeRiesgo)
    if request.vars.get('keywords'):
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1", base64.b64encode(request.vars.get('keywords'))] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0", base64.b64encode(request.vars.get('keywords'))]))]
    else:
        links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default","RegistroLog", args=[row.id, Tabla, "1"] )), lambda row: A(T('Unlock'),_class='button btn btn-primary',_href=URL("default","RegistroLog", args=[row.id, Tabla, "0"]))]
        
    query = (db.Documentacion.AprobacionJefeRiesgo=='T')
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst'):
        ActualizaAprobacion(Tabla)
        return dict(form=SQLFORM.grid(db.Documentacion, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    else:
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    #else:
    #    redirect(URL('default','index'))

#@auth.requires_login()
def Licencia():
    return dict(Licencia='')
#--------------
# IT Security
#--------------
####manejar los parametros GET y poner grafico nuevo

@auth.requires_login()
#@auth.requires(auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'))
#@auth.requires(auth.has_membership(role='adminItSecurity'))
def dataTypes():
    if auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'):
        pass
    else:
        redirect(URL('default', 'index'))
        
    db.dataTypes.id.readable=False
    if auth.has_membership(role='adminItSecurity'):
        form = SQLFORM.grid(db.dataTypes, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='auditorItSecurity'):
        form = SQLFORM.grid(db.dataTypes, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    return dict(form=form)

@auth.requires_login()
#@auth.requires(auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'))
#@auth.requires(auth.has_membership(role='adminItSecurity'))
def threatActors():
    if auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'):
        pass
    else:
        redirect(URL('default', 'index'))
        
    db.threatActors.id.readable = False
    if auth.has_membership(role='adminItSecurity'):
        form = SQLFORM.grid(db.threatActors, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='auditorItSecurity'):
        form = SQLFORM.grid(db.threatActors, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    return dict(form=form)

@auth.requires_login()
#@auth.requires(auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'))
#@auth.requires(auth.has_membership(role='adminItSecurity'))
def threatComplexity():
    if auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'):
        pass
    else:
        redirect(URL('default', 'index'))
        
    db.threatComplexity.id.readable = False
    if auth.has_membership(role='adminItSecurity'):
        form = SQLFORM.grid(db.threatComplexity, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='auditorItSecurity'):
        form = SQLFORM.grid(db.threatComplexity, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    return dict(form=form)

@auth.requires_login()
#@auth.requires(auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorTI') or auth.has_membership(role='auditorItSecurity'))
#@auth.requires(auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'))
#@auth.requires(auth.has_membership(role='adminItSecurity'))
def businessUnits():

    if auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'):
        pass
    else:
        redirect(URL('default', 'index'))
        
    db.businessUnits.id.readable = False
    if auth.has_membership(role='adminItSecurity'):
        form = SQLFORM.grid(db.businessUnits, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    #elif auth.has_membership(role='auditorTI'):
    #    form = SQLFORM.grid(db.businessUnits, searchable=True, create=True, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='auditorItSecurity'):
        form = SQLFORM.grid(db.businessUnits, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    return dict(form=form)

@auth.requires_login()
#@auth.requires(auth.has_membership(role='adminItSecurity'))
#@auth.requires(auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'))
def regions():
    if auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'):
        pass
    else:
        redirect(URL('default', 'index'))
        
    db.regions.id.readable=False
    if auth.has_membership(role='adminItSecurity'):
        form = SQLFORM.grid(db.regions, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    elif auth.has_membership(role='auditorItSecurity'):
        form = SQLFORM.grid(db.regions, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    return dict(form=form)

@auth.requires_login()
#@auth.requires(auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'))
def riskTypes():
    if auth.has_membership(role='adminItSecurity') or auth.has_membership(role='auditorItSecurity'):
        pass
    else:
        redirect(URL('default', 'index'))
        
    if auth.has_membership(role='adminItSecurity'):
        form = SQLFORM.grid(db.riskTypes, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)    
    elif auth.has_membership(role='auditorItSecurity'):
        form = SQLFORM.grid(db.riskTypes, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
    return dict(form=form)


#-----------------------
# Information Gathering
#-----------------------

@auth.requires_login()
#@auth.requires(auth.has_membership(role='adminItSecurity')or auth.has_membership(role='auditorItSecurity'))
#@auth.requires(auth.has_membership(role='adminItSecurity'))
def services():
    db.services.id.readable = False
    if auth.has_membership(role='adminItSecurity'):
        form = SQLFORM.grid(db.services, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=15, maxtextlength=250)
    #elif auth.has_membership(role='auditorItSecurity'):
    #    db.services.serviceDescription.readable=False
    #    db.services.serviceInfoGathering.readable=False
    #    db.services.serviceDocs.readable=False
    #    form = SQLFORM.grid(db.services, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=15, maxtextlength=250)
        return dict(form=form)
    else:
        redirect(URL('default','index'))

#--------------------------
# Vulnerability Assessment
#--------------------------
@auth.requires_login()
def TipoRiesgo():
    table = 'tipos_riesgo'
    if auth.has_membership(role='admin') or auth.has_membership(role='riskSupervisor'):
        return dict(form=SQLFORM.grid(db.tipo_riesgo, searchable=True, create=True, user_signature=True, editable=True, paginate=15, maxtextlength=300))
    elif auth.has_membership(role='riskManagement'):
        return dict(form=SQLFORM.grid(db.tipo_riesgo, searchable=True, create=False, deletable=False, user_signature=True, editable=False, paginate=15, maxtextlength=300))
    else:
        redirect(URL('default','index'))
        
@auth.requires_login()
#@auth.requires(auth.has_membership(role='guest') or auth.has_membership(role='manager') or auth.has_membership(role='admin') or auth.has_membership(role='riskManagement') or auth.has_membership(role='auditor'))
def plataforma_add():
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManagement'):
        return dict(form=SQLFORM.grid(db.plataforma, searchable=True, create=True, user_signature=True, editable=True, paginate=15, maxtextlength=300))
    else:
        redirect(URL('default','index'))
    #else:
    #    return dict(form=SQLFORM.grid(db.plataforma, searchable=True, create=False, user_signature=True, editable=False, paginate=15, maxtextlength=300))

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def MatrizRiesgo():
    return TableroRiesgo()

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def FactorRiesgo():
    '''
    #------------------------------------------------------------------------------
    #Pendiente recibir parametros HTTP para modificar los queries
    #------------------------------------------------------------------------------
    queryAnalisisRiesgo = (db.AnalisisRiesgo.AprobacionJefeRiesgo=='T')
    queryAnalisisRiesgoClasificacionRiesgo = (db.AnalisisRiesgoClasificacionRiesgo.AnalisisRiesgoId==db.AnalisisRiesgo.id) & (db.AnalisisRiesgoClasificacionRiesgo.ClasificacionRiesgoId==db.ClasificacionRiesgo.id) & (db.AnalisisRiesgoClasificacionRiesgo.AprobacionJefeRiesgo=='T')
    queryAnalisisRiesgoObjetivoOrganizacion = (db.AnalisisRiesgoObjetivoOrganizacion.AnalisisRiesgoId==db.AnalisisRiesgo.id) & (db.AnalisisRiesgoObjetivoOrganizacion.ObjetivoOrganizacionId==db.ObjetivoOrganizacion.id) & (db.AnalisisRiesgoObjetivoOrganizacion.AprobacionJefeRiesgo=='T')
    queryTratamientoRiesgoAnalisisRiesgo = (db.TratamientoRiesgoAnalisisRiesgo.TratamientoRiesgoId==db.TratamientoRiesgo.id) & (db.TratamientoRiesgoAnalisisRiesgo.AnalisisRiesgoId==db.AnalisisRiesgo.id) & (db.TratamientoRiesgoAnalisisRiesgo.AprobacionJefeRiesgo=='T')
    queryTotalAnalisisRiesgo = queryAnalisisRiesgo & queryAnalisisRiesgoClasificacionRiesgo & queryAnalisisRiesgoObjetivoOrganizacion & queryTratamientoRiesgoAnalisisRiesgo

    queryTratamientoRiesgo = (db.TratamientoRiesgo.ProcesoId==db.Proceso.id) & (db.TratamientoRiesgo.ActivoTiId==db.ActivoTi.id) & (db.TratamientoRiesgo.TipoVulnerabilidadId==db.TipoVulnerabilidad.id) & (db.TratamientoRiesgo.CriterioImpactoId==db.CriterioRiesgo.CriterioImpactoId) & (db.TratamientoRiesgo.CriterioProbabilidadId==db.CriterioRiesgo.CriterioProbabilidadId) & (db.TratamientoRiesgo.TipoTratamientoRiesgoId==db.TipoTratamientoRiesgo.id) & (db.TratamientoRiesgo.CatalogoControlId==db.CatalogoControl.id) & (db.TratamientoRiesgo.TipoControlId==db.TipoControl.id) & (db.TratamientoRiesgo.ClasificacionControlId==db.ClasificacionControl.id) & (db.TratamientoRiesgo.AprobacionJefeRiesgo=='T')
    queryActivoTi = (db.ActivoTi.TipoCapaSistemaId==db.TipoCapaSistema.id) & (db.ActivoTi.AprobacionJefeRiesgo=='T')
    queryProcesoRegion = (db.ProcesoRegion.ProcesoId==db.Proceso.id) & (db.ProcesoRegion.RegionId==db.Region.id) & (db.ProcesoRegion.AprobacionJefeRiesgo=='T')
    queryProcesoActivoInformacion = (db.ProcesoActivoInformacion.ProcesoId==db.Proceso.id) & (db.ProcesoActivoInformacion.ActivoInformacionId==db.ActivoInformacion.id) & (db.ProcesoActivoInformacion.AprobacionJefeRiesgo=='T')
    queryActivoTiRegion = (db.ActivoTiRegion.ActivoTiId==db.ActivoTi.id) & (db.ActivoTiRegion.RegionId==db.Region.id) & (db.ActivoTiRegion.AprobacionJefeRiesgo=='T')
    queryActivoTiProceso = (db.ActivoTiProceso.ActivoTiId==db.ActivoTi.id) & (db.ActivoTiProceso.ProcesoId==db.Proceso.id) & (db.ActivoTiProceso.AprobacionJefeRiesgo=='T')
    queryActivoTiActivoInformacion = (db.ActivoTiActivoInformacion.ActivoTiId==db.ActivoTi.id) & (db.ActivoTiActivoInformacion.ActivoInformacionId==db.ActivoInformacion.id) & (db.ActivoTiActivoInformacion.AprobacionJefeRiesgo=='T')
    queryTotalTratamientoRiesgo = queryTratamientoRiesgo & queryActivoTi & queryProcesoRegion & queryProcesoActivoInformacion & queryActivoTiRegion & queryActivoTiProceso & queryActivoTiActivoInformacion

    MatrizControl =   db( queryTratamientoRiesgo & queryTratamientoRiesgoAnalisisRiesgo & queryAnalisisRiesgo & queryAnalisisRiesgoObjetivoOrganizacion & queryAnalisisRiesgoClasificacionRiesgo).select(db.TratamientoRiesgo.ALL, db.AnalisisRiesgo.ALL, db.CriterioRiesgo.ALL, db.ClasificacionRiesgo.ALL, db.ObjetivoOrganizacion.ALL)
    #MatrizControlId = db( queryTratamientoRiesgo & queryTratamientoRiesgoAnalisisRiesgo & queryAnalisisRiesgoObjetivoOrganizacion & queryAnalisisRiesgoClasificacionRiesgo ).select(db.TratamientoRiesgo.id, distinct=True, groupby=db.TratamientoRiesgo.id)
    MatrizControlId = db( queryTratamientoRiesgo ).select(db.TratamientoRiesgo.id, distinct=True, groupby=db.TratamientoRiesgo.id)
    TotalMatrizControl = db( queryTratamientoRiesgo ).count()


    ArregloMatrizControl1 = []
    ArregloMatrizControl = []
    for i in MatrizControlId:
        ArregloMatrizControl1.append(i.id)
    for i in ArregloMatrizControl1:
        ArregloMatrizControl2 = []
        objetivo = ''
        clasificacion = ''
        riesgo = ''
        for x in MatrizControl:
            if i == x.TratamientoRiesgo.id:
                factorRiesgo = x.TratamientoRiesgo.FactorRiesgo
                #------------------------------------------------
                #Para armar un arreglo con las diferentes 
                #clasificaciones que se asignan al riesgo
                #------------------------------------------------
                if str(x.ClasificacionRiesgo.Nombre) in str(clasificacion):
                    clasificacion = clasificacion
                else:
                    clasificacion = clasificacion + ' | ' + str(x.ClasificacionRiesgo.Nombre)
                pass
                #------------------------------------------------
                #Para armar un arreglo con las diferentes 
                #obejtivos que son afectados por el riesgo 
                #------------------------------------------------
                if str(x.ObjetivoOrganizacion.Nombre) in str(objetivo):
                    objetivo = objetivo
                else:
                    objetivo = objetivo + ' | ' + str(x.ObjetivoOrganizacion.Nombre)
                pass
                idFactorRiesgo = x.TratamientoRiesgo.id
                factorRiesgoImpactoNivel = x.TratamientoRiesgo.CriterioImpactoId.Valor
                factorRiesgoImpactoNombre = x.TratamientoRiesgo.CriterioImpactoId.Nombre
                factorRiesgoProbabilidadNivel = x.TratamientoRiesgo.CriterioProbabilidadId.Valor
                factorRiesgoProbabilidadNombre = x.TratamientoRiesgo.CriterioProbabilidadId.Nombre
                tipoTratamientoRiesgo = x.TratamientoRiesgo.TipoTratamientoRiesgoId.Nombre
                #procesoRegion = str(x.TratamientoRiesgo.ProcesoRegionId.RegionId.Nombre) + ' | ' + str(x.TratamientoRiesgo.ProcesoRegionId.ProcesoId.CicloNegocioId.Nombre) + ' | ' + str(x.TratamientoRiesgo.ProcesoRegionId.ProcesoId.MacroProcesoId.Nombre) + ' | ' + str(x.TratamientoRiesgo.ProcesoRegionId.ProcesoId.TipoProcesoId.Nombre) + ' | ' + str(x.TratamientoRiesgo.ProcesoRegionId.ProcesoId.Nombre)
                procesoRegion = str(x.TratamientoRiesgo.ProcesoId.Nombre)
                #activoTI = str(x.TratamientoRiesgo.ActivoTiId.id) + ' | ' + str(x.TratamientoRiesgo.ActivoTiId.Nombre) + ' | ' + str(x.TratamientoRiesgo.ActivoTiId.TipoCapaSistemaId.Nombre)
                #activoTI = str(x.TratamientoRiesgo.ActivoTiRegionId.RegionId.Nombre) + ' | ' + str(x.TratamientoRiesgo.ActivoTiRegionId.ActivoTiId.Nombre) + ' | ' + str(x.TratamientoRiesgo.ActivoTiRegionId.ActivoTiId.TipoCapaSistemaId.Nombre)
                activoTI = str(x.TratamientoRiesgo.ActivoTiId.Nombre)
                riesgoFraude = x.TratamientoRiesgo.RiesgoFraude
                escenarioAmenaza = x.TratamientoRiesgo.EscenarioAmenaza
                riesgoMaterializadoCheck = x.TratamientoRiesgo.RiesgoMaterializadoCheck
                tipoVulnerabilidad = x.TratamientoRiesgo.TipoVulnerabilidadId.Nombre
                if x.TratamientoRiesgo.EvidenciaRiesgo:
                    evidenciaTratamientoRiesgo = URL('default/download', str(x.TratamientoRiesgo.EvidenciaRiesgo))
                else:
                    evidenciaTratamientoRiesgo = ''
                pass
                fechaRevision = x.TratamientoRiesgo.FechaRevision
                if str(x.AnalisisRiesgo.Riesgo) in str(riesgo):
                    riesgo = riesgo
                else:
                    riesgo = riesgo + ' | ' + str(x.AnalisisRiesgo.Riesgo)
                pass
                if x.AnalisisRiesgo.EvidenciaRiesgo:
                    evidenciaRiesgo = URL('default/download', str(x.AnalisisRiesgo.EvidenciaRiesgo))
                else:
                    evidenciaRiesgo = ''
                pass
                riesgoMaterializado = x.AnalisisRiesgo.RiesgoMaterializado
                duenoProceso = x.AnalisisRiesgo.DuenoProceso
                catalogoControl = x.TratamientoRiesgo.CatalogoControlId.Nombre
                tipoControl = x.TratamientoRiesgo.TipoControlId.Nombre
                clasificacionControl = x.TratamientoRiesgo.ClasificacionControlId.Nombre
                keyControl = x.TratamientoRiesgo.KeyControl
                objetivoControl = x.TratamientoRiesgo.ObjetivoControl
                actividadControl = x.TratamientoRiesgo.ActividadControl
                #nivelMadurez = x.TratamientoRiesgo.NivelMadurezId.Nombre
                nivelMadurez = ''
                comentariosRespCtrl = x.TratamientoRiesgo.ComentariosResponsableControl
                if x.TratamientoRiesgo.EvidenciaControl:
                    evidenciaControl = URL('default/download', str(x.TratamientoRiesgo.EvidenciaControl))
                else:
                    evidenciaControl = ''
                fechaImplementacionControl = x.TratamientoRiesgo.FechaImplementacionControl
                responsableCtrl = x.TratamientoRiesgo.ResponsableControl
                #politica = str(x.TratamientoRiesgo.DetallePoliticaId.RegionPoliticaId.RegionId.Nombre) + ' | ' + str(x.TratamientoRiesgo.DetallePoliticaId.RegionPoliticaId.CatalogoPoliticaId.id) + ' | ' + str(x.TratamientoRiesgo.DetallePoliticaId.RegionPoliticaId.CatalogoPoliticaId.Nombre) + ' | ' + str(x.TratamientoRiesgo.DetallePoliticaId.Codigo) + ' | ' + str(x.TratamientoRiesgo.DetallePoliticaId.Nombre)
                politica = ""
                analistaRiesgo = x.AnalisisRiesgo.AnalistaRiesgo
                cvssValor = x.TratamientoRiesgo.CuantificacionCVSS
                cvssVector = x.TratamientoRiesgo.VectorCVSS
                statusControl = x.TratamientoRiesgo.StatusImplementacionControl
                riesgoImpacto = x.AnalisisRiesgo.CriterioImpactoId.Nombre
        ArregloMatrizControl2.append(idFactorRiesgo)
        ArregloMatrizControl2.append(factorRiesgo)
        ArregloMatrizControl2.append(int(factorRiesgoImpactoNivel))
        ArregloMatrizControl2.append(factorRiesgoImpactoNombre)
        ArregloMatrizControl2.append(int(factorRiesgoProbabilidadNivel))
        ArregloMatrizControl2.append(factorRiesgoProbabilidadNombre)
        ArregloMatrizControl2.append(tipoTratamientoRiesgo)
        ArregloMatrizControl2.append(procesoRegion)
        ArregloMatrizControl2.append(activoTI)
        ArregloMatrizControl2.append(riesgoFraude)
        ArregloMatrizControl2.append(escenarioAmenaza)
        ArregloMatrizControl2.append(riesgoMaterializadoCheck)
        ArregloMatrizControl2.append(tipoVulnerabilidad)
        ArregloMatrizControl2.append(evidenciaTratamientoRiesgo)
        ArregloMatrizControl2.append(fechaRevision)
        ArregloMatrizControl2.append(riesgo)
        ArregloMatrizControl2.append(clasificacion)
        ArregloMatrizControl2.append(objetivo)
        ArregloMatrizControl2.append(evidenciaRiesgo)
        ArregloMatrizControl2.append(riesgoMaterializado)
        ArregloMatrizControl2.append(duenoProceso)
        ArregloMatrizControl2.append(catalogoControl)
        ArregloMatrizControl2.append(tipoControl)
        ArregloMatrizControl2.append(clasificacionControl)
        ArregloMatrizControl2.append(keyControl)
        ArregloMatrizControl2.append(objetivoControl)
        ArregloMatrizControl2.append(actividadControl)
        ArregloMatrizControl2.append(nivelMadurez)
        ArregloMatrizControl2.append(comentariosRespCtrl)
        ArregloMatrizControl2.append(evidenciaControl)
        ArregloMatrizControl2.append(fechaImplementacionControl)
        ArregloMatrizControl2.append(responsableCtrl)
        ArregloMatrizControl2.append(politica)
        ArregloMatrizControl2.append(analistaRiesgo)
        ArregloMatrizControl2.append(cvssValor)
        ArregloMatrizControl2.append(cvssVector)
        ArregloMatrizControl2.append(statusControl)
        ArregloMatrizControl2.append(riesgoImpacto)
        ArregloMatrizControl.append(ArregloMatrizControl2)
    #return TableroRiesgo()
    return dict(ArregloMatrizControl=ArregloMatrizControl, TotalMatrizControl=TotalMatrizControl)
    '''
    return TableroRiesgo()

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BarraControlProceso():
    return TableroRiesgo()
    #redirect(URL('default','TableroRiesgo'))

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BarraTipoVulnerabilidad():
    return TableroRiesgo()

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BarraCatalogoControl():
    return TableroRiesgo()

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BarraControlActivo():
    return TableroRiesgo()

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BarraControlRiesgo():
    return TableroRiesgo()

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BarraControlActivoTi():
    return TableroRiesgo()

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BarraClasificacionControl():
    return TableroRiesgo()

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest'))
def BarraNivelMadurez():
    return TableroRiesgo()

#@auth.requires_login()
#def indexSeguridadTi():
#    return TableroSeguridadTi()

@auth.requires_login()
def indexIncidenteSeguridadTi():
    return TableroIncidenteSeguridadTi()

#@auth.requires_login()
#def indexAuditoria():
#    return TableroAuditoria()

@auth.requires_login()
def indexEvaluacionControl():
    return TableroEvaluacionControl()

'''
@auth.requires_login()
def indexArquitecturaSistema():
    #response.flash = T("Hello World")
    #return dict(message=T('Welcome to web2py!'))
    if not request.vars.proceso:
        VarProceso=1
    elif request.vars.proceso:
        VarProceso=request.vars.proceso

    Nodo = db((db.Nodo.ProcesoId==VarProceso) & (db.Nodo.AprobacionJefeRiesgo=='T')).select(db.Nodo.ALL)
    #Arista = db( (db.Arista.NodoId1==db.Nodo.id) & (db.Arista.NodoId2==db.Nodo.id) & (db.Nodo.ProcesoId==request.vars.proceso) ).select(db.Arista.ALL)
    Arista = db( (db.Arista.NodoId1==db.Nodo.id)  & (db.Nodo.ProcesoId==VarProceso) & (db.Arista.AprobacionJefeRiesgo=='T') ).select(db.Arista.ALL)
    Proceso = db(db.Proceso).select(db.Proceso.ALL)
    NombreProceso = db(db.Proceso.id==VarProceso).select(db.Proceso.Nombre, db.Proceso.RegionId).first()
    return dict(Nodo=Nodo, Arista=Arista, Proceso=Proceso, NombreProceso=NombreProceso)
'''

@auth.requires_login()
def Usuario():
    #if auth.has_membership(role='admin') and demo==0:
    #if auth.has_membership(role='admin') and versionGratuita==0:
    if auth.has_membership(role='admin'):
        return dict(form=SQLFORM.grid(db.auth_user, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    else:
        #return dict(form=SQLFORM.grid(db.auth_user, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
        redirect(URL('default','index'))

@auth.requires_login()
def Email():
    #if auth.has_membership(role='admin') and demo==0:
    #if auth.has_membership(role='admin') and versionGratuita==0:
    if auth.has_membership(role='admin'):
        return dict(form=SQLFORM.grid(db.Email, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    else:
        #return dict(form=SQLFORM.grid(db.Email, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
        redirect(URL('default','index'))
@auth.requires_login()
def Grupo():
    #if auth.has_membership(role='admin') and demo==0:
    #if auth.has_membership(role='admin') and versionGratuita==0:
    if auth.has_membership(role='admin'):
        #if demo==1: 
        return dict(form=SQLFORM.grid(db.auth_membership, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
        #elif demo==0:
    else:
        #return dict(form=SQLFORM.grid(db.auth_membership, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
        redirect(URL('default','index'))

@auth.requires_login()
@auth.requires(auth.has_membership(role='riskManager') or auth.has_membership(role='auditManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='processOwner') or auth.has_membership(role='controlResp') or auth.has_membership(role='admin') or auth.has_membership(role='guest') or auth.has_membership('riskOwner') )
def TableroRiesgo():
    #---------------------------
    #Queries ANALISIS RIESGO
    #---------------------------
    queryAnalisisRiesgo = (db.AnalisisRiesgo.AprobacionJefeRiesgo=='T')
    queryAnalisisRiesgoClasificacionRiesgo = (db.AnalisisRiesgoClasificacionRiesgo.AnalisisRiesgoId==db.AnalisisRiesgo.id) & (db.AnalisisRiesgoClasificacionRiesgo.ClasificacionRiesgoId==db.ClasificacionRiesgo.id) & (db.AnalisisRiesgoClasificacionRiesgo.AprobacionJefeRiesgo=='T')
    queryAnalisisRiesgoObjetivoOrganizacion = (db.AnalisisRiesgoObjetivoOrganizacion.AnalisisRiesgoId==db.AnalisisRiesgo.id) & (db.AnalisisRiesgoObjetivoOrganizacion.ObjetivoOrganizacionId==db.ObjetivoOrganizacion.id) & (db.AnalisisRiesgoObjetivoOrganizacion.AprobacionJefeRiesgo=='T')
    queryTratamientoRiesgoAnalisisRiesgo = (db.TratamientoRiesgoAnalisisRiesgo.TratamientoRiesgoId==db.TratamientoRiesgo.id) & (db.TratamientoRiesgoAnalisisRiesgo.AnalisisRiesgoId==db.AnalisisRiesgo.id) & (db.TratamientoRiesgoAnalisisRiesgo.AprobacionJefeRiesgo=='T')
    queryTotalAnalisisRiesgo = queryAnalisisRiesgo & queryAnalisisRiesgoClasificacionRiesgo & queryAnalisisRiesgoObjetivoOrganizacion & queryTratamientoRiesgoAnalisisRiesgo
    #---------------------------
    #Queries FACTOR DE RIESGO 
    #---------------------------
    queryTratamientoRiesgo = (db.TratamientoRiesgo.ProcesoId==db.Proceso.id) & (db.TratamientoRiesgo.ActivoTiId==db.ActivoTi.id) & (db.TratamientoRiesgo.TipoVulnerabilidadId==db.TipoVulnerabilidad.id) & (db.TratamientoRiesgo.CriterioImpactoId==db.CriterioRiesgo.CriterioImpactoId) & (db.TratamientoRiesgo.CriterioProbabilidadId==db.CriterioRiesgo.CriterioProbabilidadId) & (db.TratamientoRiesgo.TipoTratamientoRiesgoId==db.TipoTratamientoRiesgo.id) & (db.TratamientoRiesgo.CatalogoControlId==db.CatalogoControl.id) & (db.TratamientoRiesgo.TipoControlId==db.TipoControl.id) & (db.TratamientoRiesgo.ClasificacionControlId==db.ClasificacionControl.id) & (db.TratamientoRiesgo.AprobacionJefeRiesgo=='T')
    queryProceso = (db.Proceso.TipoProcesoId == db.TipoProceso.id) & (db.Proceso.AprobacionJefeRiesgo == 'T')
    queryActivoTi = (db.ActivoTi.TipoCapaSistemaId==db.TipoCapaSistema.id) & (db.ActivoTi.AprobacionJefeRiesgo=='T')
    queryCatalogoControl = (db.CatalogoControl.Baseline==db.BenchVersion.id) & (db.CatalogoControl.AprobacionJefeRiesgo=='T')
    queryTotalTratamientoRiesgo = queryTratamientoRiesgo & queryProceso & queryActivoTi & queryCatalogoControl
    #----------------
    #Queries OTROS
    #----------------
    queryActivoInformacion = (db.ActivoInformacion.ClasificacionInformacionId == db.ClasificacionInformacion.id) & (db.ActivoInformacion.AprobacionJefeRiesgo == 'T')
    queryProcesoActivoInformacion = (db.ProcesoActivoInformacion.ProcesoId==db.Proceso.id) & (db.ProcesoActivoInformacion.ActivoInformacionId==db.ActivoInformacion.id) & (db.ProcesoActivoInformacion.AprobacionJefeRiesgo=='T')
    queryActivoTiActivoInformacion = (db.ActivoTiActivoInformacion.ActivoTiId==db.ActivoTi.id) & (db.ActivoTiActivoInformacion.ActivoInformacionId==db.ActivoInformacion.id) & (db.ActivoTiActivoInformacion.AprobacionJefeRiesgo=='T')
    queryActivoTiProceso = (db.ActivoTiProceso.ActivoTiId==db.ActivoTi.id) & (db.ActivoTiProceso.ProcesoId==db.Proceso.id) & (db.ActivoTiProceso.AprobacionJefeRiesgo=='T')
    queryActivoInformacionRegulacion = (db.ActivoInformacionRegulacion.ActivoInformacionId==db.ActivoInformacion.id) & (db.ActivoInformacionRegulacion.RegulacionDatoId == db.RegulacionDato.id) & (db.ActivoInformacionRegulacion.AprobacionJefeRiesgo=='T')
    queryTotalOtros = queryActivoInformacion & queryProcesoActivoInformacion & queryActivoTiActivoInformacion & queryActivoTiProceso & queryActivoInformacionRegulacion 
    #----------------------------
    #Queries EVALUACION CONTROL
    #----------------------------
    queryEvaluacionControl = (db.EvaluacionControl.TipoRevisionId==db.TipoRevision.id) & (db.EvaluacionControl.DetallePoliticaId==db.DetallePolitica.id) & (db.EvaluacionControl.BenchControlId==db.BenchControl.id) & (db.EvaluacionControl.TratamientoRiesgoId==db.TratamientoRiesgo.id) & (db.EvaluacionControl.ProcesoId==db.Proceso.id) & (db.EvaluacionControl.ActivoTiId==db.ActivoTi.id) & (db.EvaluacionControl.NivelMadurezId==db.NivelMadurez.id) & (db.EvaluacionControl.AprobacionJefeAuditoria=='T')
    queryDetallePolitica = (db.DetallePolitica.CatalogoPoliticaId == db.CatalogoPolitica.id) & (db.DetallePolitica.AprobacionJefeRiesgo=='T')
    queryBenchControl = (db.BenchControl.BenchObjetivoControlId==db.BenchObjetivoControl.id) & (db.BenchControl.AprobacionJefeRiesgo=='T')
    queryTotalEvaluacionControl = queryEvaluacionControl & queryDetallePolitica & queryBenchControl & queryTotalTratamientoRiesgo 
    #----------------------------
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        queryAnalisisRiesgo = queryTotalAnalisisRiesgo
        queryTratamientoRiesgo = queryTotalTratamientoRiesgo
    elif auth.has_membership(role='riskOwner'):
        riesgoId = []
        for a in db(db.AnalisisRiesgo.AprobacionJefeRiesgo=='T').select(db.AnalisisRiesgo.id, db.AnalisisRiesgo.DuenoRiesgo):
            try:
                for b in str(str(a.DuenoRiesgo).replace(' ','')).split(','):
                    if b==auth.user.username:
                        riesgoId.append(int(a.id))
            except:
                pass
        query = db.AnalisisRiesgo.id.belongs(riesgoId)
        #queryAnalisisRiesgo = (queryAnalisisRiesgo) & (query)
        queryAnalisisRiesgo = (queryTotalAnalisisRiesgo) & (query)
        controlId=[]
        for a in db((db.TratamientoRiesgo.AprobacionJefeRiesgo=='T') & (db.TratamientoRiesgoAnalisisRiesgo.TratamientoRiesgoId==db.TratamientoRiesgo.id) & (db.TratamientoRiesgoAnalisisRiesgo.AnalisisRiesgoId == db.AnalisisRiesgo.id)).select(db.TratamientoRiesgo.id, db.AnalisisRiesgo.DuenoRiesgo):
            try:
                for b in str(str(a.AnalisisRiesgo.DuenoRiesgo).replace(' ','')).split(','):
                    if b==auth.user.username:
                        controlId.append(int(a.TratamientoRiesgo.id))
            except:
                pass
        query = db.TratamientoRiesgo.id.belongs(controlId)
        queryTratamientoRiesgo = (queryTotalTratamientoRiesgo) & (query)
    else:
        queryAnalisisRiesgo = (db.AnalisisRiesgo.id == 0)
        queryTratamientoRiesgo = (db.TratamientoRiesgo.id == 0)
    #------------------------------
    #Queries menu PARAMETROS HTTP
    #------------------------------
    Parametro = {}
    Parametro.update(dict(request.vars))
    if request.vars.Riesgo:
        Parametro['Riesgo'] = request.vars.Riesgo
        queryAnalisisRiesgo = queryTotalAnalisisRiesgo & (db.AnalisisRiesgo.id==request.vars.Riesgo)
        queryTratamientoRiesgo = queryTotalTratamientoRiesgo & queryTotalAnalisisRiesgo & (db.AnalisisRiesgo.id==request.vars.Riesgo)
    if request.vars.Objetivo:
        Parametro['Objetivo'] = request.vars.Objetivo
        queryAnalisisRiesgo = queryTotalAnalisisRiesgo & (db.AnalisisRiesgoObjetivoOrganizacion.ObjetivoOrganizacionId==request.vars.Objetivo)
        queryTratamientoRiesgo = queryTotalTratamientoRiesgo & queryTotalAnalisisRiesgo & (db.AnalisisRiesgoObjetivoOrganizacion.ObjetivoOrganizacionId==request.vars.Objetivo)
    if request.vars.Tipo:
        Parametro['Tipo'] = request.vars.Tipo
        queryAnalisisRiesgo = queryTotalAnalisisRiesgo & (db.AnalisisRiesgoClasificacionRiesgo.ClasificacionRiesgoId==request.vars.Tipo)
        queryTratamientoRiesgo = queryTotalTratamientoRiesgo & queryTotalAnalisisRiesgo & (db.AnalisisRiesgoClasificacionRiesgo.ClasificacionRiesgoId==request.vars.Tipo)
    if request.vars.Factor:
        Parametro['Factor'] = request.vars.Factor
        queryAnalisisRiesgo= queryTotalAnalisisRiesgo & queryTotalTratamientoRiesgo & (db.TratamientoRiesgo.TipoVulnerabilidadId==request.vars.Factor)
        queryTratamientoRiesgo = queryTotalTratamientoRiesgo & (db.TratamientoRiesgo.TipoVulnerabilidadId==request.vars.Factor)
    if request.vars.Control:
        Parametro['Control'] = request.vars.Control
        queryAnalisisRiesgo = queryTotalAnalisisRiesgo & queryTotalTratamientoRiesgo & (db.TratamientoRiesgo.CatalogoControlId==request.vars.Control)
        queryTratamientoRiesgo = queryTotalTratamientoRiesgo & (db.TratamientoRiesgo.CatalogoControlId==request.vars.Control)
    #------------------------------
    #Grafico y matriz NIVEL RIESGO
    #------------------------------
    TotalRiesgo = db.AnalisisRiesgo.id.count()
    MatrizRiesgoClasificacion = db(queryTotalAnalisisRiesgo).select(db.AnalisisRiesgo.NivelRiesgo,  TotalRiesgo, groupby=db.AnalisisRiesgo.NivelRiesgo, distinct=True)
    MatrizRiesgoId = db(queryAnalisisRiesgo & queryAnalisisRiesgoClasificacionRiesgo & queryAnalisisRiesgoObjetivoOrganizacion).select(db.AnalisisRiesgo.id, distinct=True, groupby=db.AnalisisRiesgo.id )
    MatrizRiesgo  =  db(queryAnalisisRiesgo & queryAnalisisRiesgoClasificacionRiesgo & queryAnalisisRiesgoObjetivoOrganizacion).select(db.AnalisisRiesgo.ALL, db.CriterioRiesgo.Nombre, db.CriterioRiesgo.RiesgoValor, db.ObjetivoOrganizacion.Nombre, db.ClasificacionRiesgo.Nombre, distinct=True )
    ArregloMatrizRiesgo1 = []
    ArregloMatrizRiesgo = []
    riesgo = ''
    clasificacion = ''
    impacto = ''
    probabilidad = ''
    riesgoValor = ''
    riesgoNivel = ''
    consecuencia = ''
    objetivo = ''
    ArregloMatrizRiesgo1 = []
    ArregloMatrizRiesgo = []
    for i in MatrizRiesgoId:
        ArregloMatrizRiesgo1.append(i.id)
    for i in ArregloMatrizRiesgo1:
        ArregloMatrizRiesgo2 = []
        objetivo = ''
        clasificacion = ''
        validacion = False
        for x in MatrizRiesgo:
            if i == x.AnalisisRiesgo.id:
                validacion = True
                riesgo = x.AnalisisRiesgo.Riesgo
                if str(x.ClasificacionRiesgo.Nombre) in str(clasificacion):
                    clasificacion = clasificacion
                else:
                    clasificacion = clasificacion + ' | ' + str(x.ClasificacionRiesgo.Nombre)
                pass
                if str(x.ObjetivoOrganizacion.Nombre) in str(objetivo):
                    objetivo = objetivo
                else:
                    objetivo = objetivo + ' | ' + str(x.ObjetivoOrganizacion.Nombre)
                pass
                impacto = x.AnalisisRiesgo.NivelRiesgo
                #probabilidad = x.AnalisisRiesgo.NivelRiesgo
                #riesgoValor = int(x.CriterioRiesgo.RiesgoValor)
                #riesgoNivel = x.CriterioRiesgo.Nombre
                consecuencia = x.AnalisisRiesgo.RiesgoMaterializado
        if validacion == True:
            ArregloMatrizRiesgo2.append(riesgo)
            ArregloMatrizRiesgo2.append(clasificacion)
            ArregloMatrizRiesgo2.append(impacto)
            #ArregloMatrizRiesgo2.append(probabilidad)
            #ArregloMatrizRiesgo2.append(riesgoValor)
            #ArregloMatrizRiesgo2.append(riesgoNivel)
            ArregloMatrizRiesgo2.append(consecuencia)
            ArregloMatrizRiesgo2.append(objetivo)
            ArregloMatrizRiesgo.append(ArregloMatrizRiesgo2)
    #return dict(MatrizRiesgoControl=MatrizRiesgoControl)
    MatrizRiesgoControl = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.ALL)

    #-------------------------------
    #Grafico y matriz FACTOR RIESGO
    #-------------------------------
    MatrizControl =   db( queryTratamientoRiesgo & queryAnalisisRiesgo ).select(db.TratamientoRiesgo.ALL, db.AnalisisRiesgo.ALL, db.CriterioRiesgo.ALL, db.ClasificacionRiesgo.ALL, db.ObjetivoOrganizacion.ALL)
    MatrizControlId = db( queryTratamientoRiesgo & queryAnalisisRiesgo ).select(db.TratamientoRiesgo.id, distinct=True, groupby=db.TratamientoRiesgo.id)
    ArregloMatrizControl1 = []
    ArregloMatrizControl = []
    for i in MatrizControlId:
        ArregloMatrizControl1.append(i.id)
    for i in ArregloMatrizControl1:
        ArregloMatrizControl2 = []
        objetivo = ''
        clasificacion = ''
        riesgo = ''
        #El if es para agrupar los campos de clasificacion, objetivo, etc...
        for x in MatrizControl:
            if i == x.TratamientoRiesgo.id:
                factorRiesgo = x.TratamientoRiesgo.FactorRiesgo
                #------------------------------------------------
                #Para armar un arreglo con las diferentes 
                #clasificaciones que se asignan al riesgo
                #------------------------------------------------
                if str(x.ClasificacionRiesgo.Nombre) in str(clasificacion):
                    clasificacion = clasificacion
                else:
                    clasificacion = clasificacion + ' | ' + str(x.ClasificacionRiesgo.Nombre)
                pass
                #------------------------------------------------
                #Para armar un arreglo con las diferentes 
                #obejtivos que son afectados por el riesgo 
                #------------------------------------------------
                if str(x.ObjetivoOrganizacion.Nombre) in str(objetivo):
                    objetivo = objetivo
                else:
                    objetivo = objetivo + ' | ' + str(x.ObjetivoOrganizacion.Nombre)
                pass
                idFactorRiesgo = x.TratamientoRiesgo.id
                #idFactorRiesgo = ""
                factorRiesgoImpactoNivel = x.TratamientoRiesgo.CriterioImpactoId.Valor
                factorRiesgoImpactoNombre = x.TratamientoRiesgo.CriterioImpactoId.Nombre
                factorRiesgoProbabilidadNivel = x.TratamientoRiesgo.CriterioProbabilidadId.Valor
                factorRiesgoProbabilidadNombre = x.TratamientoRiesgo.CriterioProbabilidadId.Nombre
                factorRiesgoNivel = x.CriterioRiesgo.RiesgoValor
                factorRiesgoNombre = x.CriterioRiesgo.Nombre
                tipoTratamientoRiesgo = x.TratamientoRiesgo.TipoTratamientoRiesgoId.Nombre
                procesoRegion = str(x.TratamientoRiesgo.ProcesoId.Nombre)
                activoTI = str(x.TratamientoRiesgo.ActivoTiId.Nombre)
                riesgoFraude = x.TratamientoRiesgo.RiesgoFraude
                escenarioAmenaza = x.TratamientoRiesgo.EscenarioAmenaza
                riesgoMaterializadoCheck = x.TratamientoRiesgo.RiesgoMaterializadoCheck
                tipoVulnerabilidad = x.TratamientoRiesgo.TipoVulnerabilidadId.Nombre
                referencia = x.TratamientoRiesgo.Referencia
                if x.TratamientoRiesgo.EvidenciaRiesgo:
                    evidenciaTratamientoRiesgo = URL('default/download', str(x.TratamientoRiesgo.EvidenciaRiesgo))
                else:
                    evidenciaTratamientoRiesgo = ''
                pass
                fechaRevision = x.TratamientoRiesgo.FechaRevision
                if str(x.AnalisisRiesgo.Riesgo) in str(riesgo):
                    riesgo = riesgo
                else:
                    riesgo = riesgo + ' | ' + str(x.AnalisisRiesgo.Riesgo)
                pass
                if x.AnalisisRiesgo.EvidenciaRiesgo:
                    evidenciaRiesgo = URL('default/download', str(x.AnalisisRiesgo.EvidenciaRiesgo))
                else:
                    evidenciaRiesgo = ''
                pass
                riesgoMaterializado = x.AnalisisRiesgo.RiesgoMaterializado
                duenoProceso = x.AnalisisRiesgo.DuenoRiesgo
                catalogoControl = x.TratamientoRiesgo.CatalogoControlId.Nombre
                tipoControl = x.TratamientoRiesgo.TipoControlId.Nombre
                clasificacionControl = x.TratamientoRiesgo.ClasificacionControlId.Nombre
                keyControl = x.TratamientoRiesgo.KeyControl
                objetivoControl = x.TratamientoRiesgo.ObjetivoControl
                actividadControl = x.TratamientoRiesgo.ActividadControl
                #nivelMadurez = x.TratamientoRiesgo.NivelMadurezId.Nombre
                nivelMadurez = ''
                comentariosRespCtrl = x.TratamientoRiesgo.ComentariosResponsableControl
                if x.TratamientoRiesgo.EvidenciaControl:
                    evidenciaControl = URL('default/download', str(x.TratamientoRiesgo.EvidenciaControl))
                else:
                    evidenciaControl = ''
                fechaImplementacionControl = x.TratamientoRiesgo.FechaImplementacionControl
                responsableCtrl = x.TratamientoRiesgo.ResponsableControl
                politica = ""
                analistaRiesgo = x.AnalisisRiesgo.AnalistaRiesgo
                cvssValor = x.TratamientoRiesgo.CuantificacionCVSS
                cvssVector = x.TratamientoRiesgo.VectorCVSS
                statusControl = x.TratamientoRiesgo.StatusImplementacionControl
                riesgoImpacto = x.AnalisisRiesgo.NivelRiesgo
        ArregloMatrizControl2.append(idFactorRiesgo)
        ArregloMatrizControl2.append(factorRiesgo)
        ArregloMatrizControl2.append(int(factorRiesgoImpactoNivel))
        ArregloMatrizControl2.append(factorRiesgoImpactoNombre)
        ArregloMatrizControl2.append(int(factorRiesgoProbabilidadNivel))
        ArregloMatrizControl2.append(factorRiesgoProbabilidadNombre)
        ArregloMatrizControl2.append(tipoTratamientoRiesgo)
        ArregloMatrizControl2.append(procesoRegion)
        ArregloMatrizControl2.append(activoTI)
        ArregloMatrizControl2.append(riesgoFraude)
        ArregloMatrizControl2.append(escenarioAmenaza)
        ArregloMatrizControl2.append(riesgoMaterializadoCheck)
        ArregloMatrizControl2.append(tipoVulnerabilidad)
        ArregloMatrizControl2.append(evidenciaTratamientoRiesgo)
        ArregloMatrizControl2.append(fechaRevision)
        ArregloMatrizControl2.append(riesgo)
        ArregloMatrizControl2.append(clasificacion)
        ArregloMatrizControl2.append(objetivo)
        ArregloMatrizControl2.append(evidenciaRiesgo)
        ArregloMatrizControl2.append(riesgoMaterializado)
        ArregloMatrizControl2.append(duenoProceso)
        ArregloMatrizControl2.append(catalogoControl)
        ArregloMatrizControl2.append(tipoControl)
        ArregloMatrizControl2.append(clasificacionControl)
        ArregloMatrizControl2.append(keyControl)
        ArregloMatrizControl2.append(objetivoControl)
        ArregloMatrizControl2.append(actividadControl)
        ArregloMatrizControl2.append(nivelMadurez)
        ArregloMatrizControl2.append(comentariosRespCtrl)
        ArregloMatrizControl2.append(evidenciaControl)
        ArregloMatrizControl2.append(fechaImplementacionControl)
        ArregloMatrizControl2.append(responsableCtrl)
        ArregloMatrizControl2.append(politica)
        ArregloMatrizControl2.append(analistaRiesgo)
        ArregloMatrizControl2.append(cvssValor)
        ArregloMatrizControl2.append(cvssVector)
        ArregloMatrizControl2.append(statusControl)
        ArregloMatrizControl2.append(riesgoImpacto)
        ArregloMatrizControl2.append(factorRiesgoNivel)
        ArregloMatrizControl2.append(factorRiesgoNombre)
        ArregloMatrizControl2.append(referencia)
        ArregloMatrizControl.append(ArregloMatrizControl2)
    #-------------------------
    #Relaciones para el menu
    #-------------------------
    ClasificacionRiesgo = db(queryAnalisisRiesgo & queryAnalisisRiesgoClasificacionRiesgo).select(db.ClasificacionRiesgo.ALL, distinct=True, groupby=db.ClasificacionRiesgo.id)
    ObjetivoOrganizacion = db(queryAnalisisRiesgo & queryAnalisisRiesgoObjetivoOrganizacion).select(db.ObjetivoOrganizacion.ALL, distinct=True, groupby=db.ObjetivoOrganizacion.id)
    AnalisisRiesgo = db(queryAnalisisRiesgo).select(db.AnalisisRiesgo.ALL, distinct=True, groupby=db.AnalisisRiesgo.id)
    TipoFactorRiesgo = db(queryTratamientoRiesgo).select(db.TipoVulnerabilidad.ALL, distinct=True, groupby=db.TipoVulnerabilidad.id)
    CatalogoControl = db(queryTratamientoRiesgo).select(db.CatalogoControl.ALL, distinct=True, groupby=db.CatalogoControl.id)
    #CatalogoControl = db(db.CatalogoControl).select(db.CatalogoControl.id, distinct=True, groupby=db.CatalogoControl.id)
    NivelRiesgo = db(queryAnalisisRiesgo).select(db.CriterioRiesgo.RiesgoValor, db.CriterioRiesgo.Nombre, distinct=True, groupby=db.CriterioRiesgo.RiesgoValor | db.CriterioRiesgo.Nombre)    
    try:
        Organizacion = db(db.Configuracion).select(db.Configuracion.Organizacion).first().Organizacion
    except:
        Organizacion = "XXX"
   
    #--------------------
    #Matriz Prueba Web
    #--------------------
    ArregloEvidenciaControl = []
    MatrizEvaluacionControl = db((db.EvaluacionControl.DetallePoliticaId==db.DetallePolitica.id) & (db.EvaluacionControl.AprobacionJefeAuditoria=='T')).select(db.EvaluacionControl.ALL)
    EvaluacionEvidencia = db(db.EvaluacionEvidencia).select(db.EvaluacionControl.ALL)
    for i in MatrizEvaluacionControl:
        PruebaControl = []
        PruebaControl.append(i.TipoRevisionId.Nombre)
        try:
            PruebaControl.append(i.DetallePoliticaId.Nombre)
        except:
            PruebaControl.append('')
        pass
        try:
            PruebaControl.append(i.BenchControlId.Nombre)
        except:
            PruebaControl.append('')
        pass
        try:
            PruebaControl.append(i.TratamientoRiesgoId.FactorRiesgo)
        except:
            PruebaControl.append('')
        pass
        PruebaControl.append(i.ProcesoId.Nombre)
        PruebaControl.append(i.ActivoTiId.Nombre)
        PruebaControl.append(i.CumplimientoControl)
        PruebaControl.append(i.NivelMadurezId.Nombre)
        PruebaControl.append(i.FechaRevision)
        PruebaControl.append(i.Hallazgo)
        PruebaControl.append(i.Recomendacion)
        EvidenciaEvaluacion = []
        for x in EvaluacionEvidencia:
            if x.EvaluacionControlId == i.id:
                Archivo = URL('default/download', str(x.Evidencia))
                EvidenciaEvaluacion.append(Archivo)
        PruebaControl.append(EvidenciaEvaluacion)
        ArregloEvidenciaControl.append(PruebaControl)

    #Funciones para el grafico de barra horizontal para mostrar cumplimiento y nivel de madurez
    MatrizEvaluacionControl2 = db((db.EvaluacionControl.DetallePoliticaId==db.DetallePolitica.id) & (db.EvaluacionControl.BenchControlId==db.BenchControl.id) & (db.EvaluacionControl.TratamientoRiesgoId==db.TratamientoRiesgo.id) & (db.EvaluacionControl.AprobacionJefeAuditoria=='T')).select(db.EvaluacionControl.ALL)
    #Arreglo para obtener el nombre de los benchmark, control y politica
    CatalogoControl = []
    for i in MatrizEvaluacionControl2:
        CatalogoControl.append(i.DetallePoliticaId.CatalogoPoliticaId.Nombre)
        CatalogoControl.append(i.BenchControlId.BenchObjetivoControlId.BenchVersionId.Version)
        CatalogoControl.append(i.TratamientoRiesgoId.TipoVulnerabilidadId.Nombre)
    CatalogoControl = set(CatalogoControl)
    #MatrizEvaluacionControl2 = db((db.EvaluacionControl.DetallePoliticaId==db.DetallePolitica.id) & (db.EvaluacionControl.BenchControlId==db.BenchControl.id) & (db.EvaluacionControl.TratamientoRiesgoId==db.TratamientoRiesgo.id) & (db.EvaluacionControl.AprobacionJefeAuditoria=='T')).select(db.EvaluacionControl.ALL)

    #Funcion para el arreglo que es enviado para crear el grafico de Cumplimiento
    CatalogoEval = []
    for c in CatalogoControl:
        CatalogoEval1 = []
        pas = 0
        fail = 0
        CatalogoEval1.append(c)
        for m in MatrizEvaluacionControl2:
            if c == m.DetallePoliticaId.CatalogoPoliticaId.Nombre or c==m.BenchControlId.BenchObjetivoControlId.BenchVersionId.Version or c==m.TratamientoRiesgoId.TipoVulnerabilidadId.Nombre:
                if m.CumplimientoControl == False:
                    fail = fail + 1
                elif m.CumplimientoControl == True:
                    pas = pas + 1

        CatalogoEval1.append(pas)
        CatalogoEval1.append(fail)
        CatalogoEval.append(CatalogoEval1)

    #Funcion para el arreglo que es enviado para crear el grafico de nivel de madurez
    NivelMadurez = db(db.NivelMadurez.AprobacionJefeRiesgo=='T').select(db.NivelMadurez.ALL)
    matrizA = {}
    col = 1     #Es el nivel de madurez
    fila = 1    #politica, tipo control, version benchcontrol
    for n in NivelMadurez:
        #col = 1
        matrizA[0,col] = n.Nombre
        col = col + 1
    for c in CatalogoControl:
        #fila = 1
        matrizA[fila,0] = c
        fila = fila + 1
    #Para inicializar la matriz a 0
    for c in range(1,col):
        for f in range(1,fila):
            matrizA[f, c] = 0
    #col2 = 1
    #fila2 = 1
    #CatalogoEval2 = []
    for f in range(1,fila):
        #CatalogoEval1 = []
        #pas = 0
        #fail = 0
        #matrizA[0,f]
        #CatalogoEval1.append(c)
        for m in MatrizEvaluacionControl2:
            if matrizA[f,0] == m.DetallePoliticaId.CatalogoPoliticaId.Nombre or matrizA[f,0] == m.BenchControlId.BenchObjetivoControlId.BenchVersionId.Version or matrizA[f,0] == m.TratamientoRiesgoId.TipoVulnerabilidadId.Nombre:
            #if matrizA[f,0] == m.DetallePoliticaId.CatalogoPoliticaId.Nombre:
                for c in range(1,col):
                    if matrizA[0,c] == m.NivelMadurezId.Nombre:
                        matrizA[f,c] = matrizA[f,c] + 1
    for n in NivelMadurez:
        for c in range(1,col):
            if matrizA[0,c] == n.Nombre:
                #matrizA[0,c] = str(n.Nombre) + ' ' + str(n.Valor)
                matrizA[0,c] = str(n.Valor) + ' - ' + str(n.Nombre)

    #------------------------
    #Matriz Categoria Riesgo
    #------------------------
    ArregloRiesgoCategoria = []
    ArregloRiesgoCategoria1 = []
    ArregloRiesgoCategoria2 = []
    ArregloRiesgoCategoria3 = []
    MatrizRiesgoCategoria = db(queryAnalisisRiesgoClasificacionRiesgo & queryAnalisisRiesgo).select(db.AnalisisRiesgoClasificacionRiesgo.ALL)
    for i in MatrizRiesgoCategoria:
        ArregloRiesgoCategoria1.append(i.AnalisisRiesgoId.Riesgo)
    ArregloRiesgoCategoria1 = set(ArregloRiesgoCategoria1)
    for i in ArregloRiesgoCategoria1:
        ArregloRiesgoCategoria2 = []
        ArregloRiesgoCategoria3 = []
        categoria = ''
        for x in MatrizRiesgoCategoria:
            if i == x.AnalisisRiesgoId.Riesgo:
                categoria = categoria + ' | ' + str(x.ClasificacionRiesgoId.Nombre)
        ArregloRiesgoCategoria3.append(i)
        ArregloRiesgoCategoria3.append(categoria)
        ArregloRiesgoCategoria.append(ArregloRiesgoCategoria3)
    #--------------------------------
    #Grafico Pastel Categoria Riesgo
    #--------------------------------
    TotalRiesgoCategoria = db.AnalisisRiesgoClasificacionRiesgo.id.count()
    #MatrizRiesgoCategoria = db(queryAnalisisRiesgoClasificacionRiesgo & queryAnalisisRiesgo).select(db.AnalisisRiesgoClasificacionRiesgo.ALL, TotalRiesgoCategoria, groupby=db.AnalisisRiesgoClasificacionRiesgo.ClasificacionRiesgoId)
    MatrizRiesgoCategoria = db(queryAnalisisRiesgoClasificacionRiesgo & queryAnalisisRiesgo).select(db.AnalisisRiesgoClasificacionRiesgo.ClasificacionRiesgoId, TotalRiesgoCategoria, groupby=db.AnalisisRiesgoClasificacionRiesgo.ClasificacionRiesgoId)
    #----------------------
    #Grafico Mapa de Calor
    #----------------------
    ArregloMapa1 = {}
    FactorRiesgoMapa = db(queryTratamientoRiesgo).select(db.TratamientoRiesgo.CriterioImpactoId, db.TratamientoRiesgo.CriterioProbabilidadId)
    for a in range(1,6):
        for b in range(1,6):
            ArregloMapa1[a,b]=0
    for i in FactorRiesgoMapa:
        ArregloMapa1[i.CriterioImpactoId, i.CriterioProbabilidadId] = ArregloMapa1[i.CriterioImpactoId, i.CriterioProbabilidadId] + 1
    #----------------------------------------------
    #Graficos relacionados al tratamiento de riesgo
    #----------------------------------------------
    TotalFactorRiesgo = db.TratamientoRiesgo.id.count()
    #FactorRiesgoProceso = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.ALL, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.ProcesoId, distinct=True)
    FactorRiesgoProceso = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.ProcesoId, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.ProcesoId, distinct=True)
    #FactorRiesgoActivoTi = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.ALL, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.ActivoTiId, distinct=True)
    FactorRiesgoActivoTi = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.ActivoTiId, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.ActivoTiId, distinct=True)
    FactorRiesgoTipo = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.TipoVulnerabilidadId, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.TipoVulnerabilidadId, distinct=True)
    FactorRiesgoTratamiento = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.TipoTratamientoRiesgoId, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.TipoTratamientoRiesgoId, distinct=True)
    FactorRiesgoTipoControl = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.TipoControlId, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.TipoControlId, distinct=True)
    FactorRiesgoCataControl = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.CatalogoControlId, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.CatalogoControlId, distinct=True)
    FactorRiesgoClasControl = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.ClasificacionControlId, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.ClasificacionControlId, distinct=True)
    FactorRiesgoStatusControl = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.StatusImplementacionControl, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.StatusImplementacionControl, distinct=True)
    FactorRiesgoFraude = db(queryTotalTratamientoRiesgo).select(db.TratamientoRiesgo.RiesgoFraude, TotalFactorRiesgo, groupby=db.TratamientoRiesgo.RiesgoFraude, distinct=True)
    #-------------------------------
    #Grafico para nivel de riesgo
    #-------------------------------

    return dict(FactorRiesgoFraude=FactorRiesgoFraude, FactorRiesgoStatusControl=FactorRiesgoStatusControl, FactorRiesgoClasControl=FactorRiesgoClasControl, FactorRiesgoCataControl=FactorRiesgoCataControl, FactorRiesgoTipoControl=FactorRiesgoTipoControl, FactorRiesgoTratamiento=FactorRiesgoTratamiento, FactorRiesgoTipo=FactorRiesgoTipo, FactorRiesgoActivoTi=FactorRiesgoActivoTi, FactorRiesgoProceso=FactorRiesgoProceso, ArregloMapa1=ArregloMapa1, ArregloRiesgoCategoria=ArregloRiesgoCategoria, MatrizRiesgoCategoria=MatrizRiesgoCategoria, MatrizRiesgoControl=MatrizRiesgoControl, matrizA=matrizA, col=col, fila=fila, CatalogoEval=CatalogoEval, MatrizRiesgoClasificacion=MatrizRiesgoClasificacion, ArregloMatrizControl=ArregloMatrizControl, GrupoControl=GrupoControl, Parametro=Parametro,   AmbienteControl=AmbienteControl, NivelMadurez=NivelMadurez, ClasificacionRiesgo=ClasificacionRiesgo, TipoTratamientoRiesgo=TipoTratamientoRiesgo, Organizacion=Organizacion, SeguridadTi=SeguridadTi, TipoCumplimiento=TipoCumplimiento, ActivoTiProceso=ActivoTiProceso, ObjetivoOrganizacion=ObjetivoOrganizacion, AnalisisRiesgo=AnalisisRiesgo, TipoFactorRiesgo=TipoFactorRiesgo, CatalogoControl=CatalogoControl, NivelRiesgo=NivelRiesgo, ArregloMatrizRiesgo=ArregloMatrizRiesgo, ArregloEvidenciaControl = ArregloEvidenciaControl, MatrizControlId=ArregloMatrizControl1)
