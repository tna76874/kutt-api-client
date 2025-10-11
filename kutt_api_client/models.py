#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kutt models
"""
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID

# --- Core Data Models ---

class Link(BaseModel):
    id: UUID
    address: str
    banned: bool = False
    created_at: datetime
    updated_at: datetime
    target: HttpUrl
    link: HttpUrl
    description: Optional[str] = None
    password: bool = False
    visit_count: Optional[int] = 0


class Domain(BaseModel):
    id: UUID
    address: str
    homepage: Optional[str] = None
    banned: bool = False
    created_at: datetime
    updated_at: datetime


class User(BaseModel):
    apikey: str
    email: str
    domains: List[Domain]


# --- Stats Models ---

class StatsItemStatsBrowser(BaseModel):
    name: str
    value: int


class StatsItemStats(BaseModel):
    browser: Optional[List[StatsItemStatsBrowser]] = None
    os: Optional[List[StatsItemStatsBrowser]] = None
    country: Optional[List[StatsItemStatsBrowser]] = None
    referrer: Optional[List[StatsItemStatsBrowser]] = None


class StatsItem(BaseModel):
    stats: Optional[StatsItemStats] = None
    views: Optional[List[int]] = None


class Stats(BaseModel):
    id: UUID
    address: str
    target: HttpUrl
    link: HttpUrl
    banned: bool = False
    password: bool = False
    created_at: datetime
    updated_at: datetime
    visit_count: int
    updatedAt: Optional[str] = None
    lastDay: Optional[StatsItem] = None
    lastWeek: Optional[StatsItem] = None
    lastMonth: Optional[StatsItem] = None
    lastYear: Optional[StatsItem] = None


# --- Request Models ---

class GetLinksRequest(BaseModel):
    limit: int = 100
    skip: int = 0
    all_links: bool = Field(True, alias="all")

    def dump_kutt(self) -> dict:
        data = self.model_dump(exclude_none=True, by_alias=True)

        # bool → string für API-Kompatibilität
        data["all"] = "true" if self.all_links else "false"
        return data

class CreateLinkRequest(BaseModel):
    target: str
    description: Optional[str] = None
    expire_in: Optional[str] = Field(None, description="e.g. '2 minutes', '3 days'")
    password: Optional[str] = None
    customurl: Optional[str] = None
    reuse: bool = False
    domain: Optional[str] = None

    def dump_kutt(self) -> dict:
        """
        Gibt ein dict für den API-Request an Kutt.it zurück.
        - Wandelt den booleschen 'reuse'-Wert in 'true'/'false' Strings um.
        - Sanitized 'customurl' (äöüß → ae/oe/ue/ss usw.).
        """
        data = self.model_dump(exclude_none=True)

        # bool → string für API-Kompatibilität
        data["reuse"] = "true" if self.reuse else "false"

        # Falls customurl vorhanden: sanitize deutsche Sonderzeichen
        if "customurl" in data and data["customurl"]:
            data["customurl"] = self._sanitize_customurl(data["customurl"])

        return data

    @staticmethod
    def _sanitize_customurl(value: str) -> str:
        """Ersetzt deutsche Umlaute und ß durch ASCII-kompatible Schreibweise."""
        replacements = {
            "ä": "ae", "ö": "oe", "ü": "ue",
            "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
            "ß": "ss"
        }
        for src, dest in replacements.items():
            value = value.replace(src, dest)
        return value


class UpdateLinkRequest(BaseModel):
    id: UUID
    target: str
    address: str
    description: Optional[str] = None
    expire_in: Optional[str] = None

    def dump_kutt(self) -> dict:
        """
        Gibt ein dict für den API-Request an Kutt.it zurück.
        - Wandelt den booleschen 'reuse'-Wert in 'true'/'false' Strings um.
        - Sanitized 'customurl' (äöüß → ae/oe/ue/ss usw.).
        """
        data = self.model_dump(exclude_none=True)

        data.pop('id')
        
        return data

class CreateDomainRequest(BaseModel):
    address: str
    homepage: Optional[str] = None


# --- Response Wrapper Models ---

class DeleteResponse(BaseModel):
    message: str


class LinkListResponse(BaseModel):
    limit: int = 10
    skip: int = 0
    total: int = 0
    data: List[Link]

