#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, abort

from planet.extensions import db
from planet.utils.permissions import auth
from planet.account import role_api
from planet.account.schemas import RoleSchema, PermissionSchema, GroupPermissionSchema
from planet.account.models import (get_role, get_all_roles, Permission)
from planet.account.permissions import (role_list_perm, role_show_perm,
                                        role_create_perm, role_update_perm,
                                        role_destory_perm)


@role_api.route('/roles', methods=['GET'])
@auth.require(401)
@role_list_perm.require(403)
def index():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    roles = get_all_roles(page, limit)
    return RoleSchema(exclude=('permissions', )).jsonify(roles)


@role_api.route('/roles/<role_id>', methods=['GET'])
@auth.require(401)
@role_show_perm.require(403)
def show(role_id):
    role_data = get_role(role_id)
    if not role_data:
        abort(404)
    return RoleSchema().jsonify(role_data)


@role_api.route('/roles', methods=['POST'])
@auth.require(401)
@role_create_perm.require(403)
def create():
    payload = request.get_json()
    role_schema = RoleSchema(only=('name', 'description', 'permissions'))
    role_data, errors = role_schema.load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    db.session.add(role_data)
    db.session.commit()
    return RoleSchema().jsonify(role_data)


@role_api.route('/roles/<role_id>', methods=['PUT'])
@auth.require(401)
@role_update_perm.require(403)
def update(role_id):
    role_data = get_role(role_id)
    if not role_data:
        abort(404)
    payload = request.get_json()
    role_data, errors = RoleSchema().load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    db.session.add(role_data)
    db.session.commit()
    return RoleSchema().jsonify(role_data)


@role_api.route('/roles/<role_id>', methods=['DELETE'])
@auth.require(401)
@role_destory_perm.require(403)
def destory(role_id):
    role_data = get_role(role_id)
    if not role_data:
        abort(404)
    db.session.delete(role_data)
    db.session.commit()

    return jsonify(code=10000, message='success')


@role_api.route('/permissions', methods=['GET'])
def permissions_index():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    format = request.args.get('format')
    if format == 'group':
        groups = Permission.query.group_by(Permission.object_type).all()
        group_permissions = []
        for group in groups:
            perms = Permission.query.filter(
                Permission.object_type == group.object_type).all()
            group_permissions.append({
                'name': group.name,
                'object_type': group.object_type,
                'permissions': perms
            })
        return GroupPermissionSchema().jsonify(group_permissions)
    permissions = Permission.query.order_by(
        Permission.created_at.desc()).paginate(page, limit)
    return PermissionSchema().jsonify(permissions)
