# -*- coding: utf-8 -*-
"""
ownership.py — worksharing ownership / editability helpers.
Part of the icz BIM tool suite.
Author: icz

Shared by every tool that writes to elements in a workshared model, so each tool
skips elements checked out by other users and reports the owner identically.
Revit 2024+ safe (uses the CheckoutStatus enum, never the magic int 2).
IronPython 2.7 safe. Signature is (el, doc) to match the call sites these were
extracted from.
"""
from Autodesk.Revit.DB import WorksharingUtils, CheckoutStatus


def can_edit(el, doc):
    """True if `el` can be edited right now: the model isn't workshared, or `el`
    isn't owned / checked out by another user."""
    if not doc.IsWorkshared:
        return True
    try:
        return WorksharingUtils.GetCheckoutStatus(doc, el.Id) != CheckoutStatus.OwnedByOtherUser
    except:
        return True


def get_owner(el, doc):
    """Username that currently owns `el`, or 'Unknown' (also 'Unknown' when the
    model isn't workshared, the element has no owner, or the lookup fails)."""
    try:
        info = WorksharingUtils.GetWorksharingTooltipInfo(doc, el.Id)
        return info.Owner if info and info.Owner else "Unknown"
    except:
        return "Unknown"
