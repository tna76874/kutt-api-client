#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Modules
"""
import requests
from .models import (
    Link,
    Stats,
    CreateLinkRequest,
    UpdateLinkRequest,
    DeleteResponse,
    LinkListResponse,
)


class KuttAPI:
    def __init__(self, api_key: str, base_url: str = "https://kutt.it/api/v2"):
        self.base_url = base_url
        self.headers = {
            "X-API-KEY": api_key
            # "Content-Type": "application/json"
        }

    def create_link(self, payload: CreateLinkRequest) -> Link:
        response = requests.post(
            f"{self.base_url}/links", headers=self.headers, json=payload.dump_kutt()
        )
        response.raise_for_status()
        return Link(**response.json())

    def update_link(self, link_id: str, payload: UpdateLinkRequest) -> Link:
        response = requests.patch(
            f"{self.base_url}/links/{link_id}", headers=self.headers, json=payload.model_dump_json(exclude_none=True)
        )
        response.raise_for_status()
        return Link(**response.json())

    def get_links(self, limit: int = 100, skip: int = 0, all_links: bool = True) -> LinkListResponse:
        params = {"limit": limit, "skip": skip, "all": all_links}
        response = requests.get(f"{self.base_url}/links", headers=self.headers, params=params)
        response.raise_for_status()
        return LinkListResponse(**response.json())

    def delete_link(self, link_id: str) -> DeleteResponse:
        response = requests.delete(f"{self.base_url}/links/{link_id}", headers=self.headers)
        response.raise_for_status()
        return DeleteResponse(**response.json())

    def get_link_stats(self, link_id: str) -> Stats:
        response = requests.get(f"{self.base_url}/links/{link_id}/stats", headers=self.headers)
        response.raise_for_status()
        return Stats(**response.json())
