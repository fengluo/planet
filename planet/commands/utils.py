# -*- coding: utf-8 -*-

import os
import re
import click
from planet.extensions import db
from planet.permissions import Need
from planet.account.models import create_user, Permission, Role


_email_regex = r"[^@]+@[^@]+\.[^@]+"


class FlaskCLIError(click.ClickException):
    """An exception that signals a usage error including color support.
    This aborts any further handling.

    :param styles: The style kwargs which should be forwarded to click.secho.
    """

    def __init__(self, message, **styles):
        click.ClickException.__init__(self, message)
        self.styles = styles

    def show(self, file=None):
        if file is None:
            file = click._compat.get_text_stderr()
        click.secho("[-] Error: %s" % self.format_message(), file=file,
                    **self.styles)


class EmailType(click.ParamType):
    """The choice type allows a value to be checked against a fixed set of
    supported values.  All of these values have to be strings.
    See :ref:`choice-opts` for an example.
    """
    name = "email"

    def convert(self, value, param, ctx):
        # Exact match
        if re.match(_email_regex, value):
            return value
        else:
            self.fail(("invalid email: %s" % value), param, ctx)

    def __repr__(self):
        return "email"


def create_permissions():
    admin = Role.query.filter_by(slug='admin').first()
    if not admin:
        admin = Role(name='Admin', slug='admin')
    for need in Need._needs:
        permission = Permission.query.filter(
            Permission.object_type == need.method,
            Permission.action_type == need.value).first()
        if not permission:
            permission = Permission(
                object_type=need.method,
                action_type=need.value)
            db.session.add(permission)
        admin.permissions.append(permission)
    db.session.add(admin)
    db.session.commit()
